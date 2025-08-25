import pandas as pd
import numpy as np
from datetime import datetime, date
import warnings
warnings.filterwarnings('ignore')

def load_and_clean_data():
    """Load and clean all data files"""
    print("Loading data files...")
    
    # Load chrono delays
    chrono_df = pd.read_excel('20220101-20250228 CHRONO Delays with Location.xlsx')
    print(f"Chrono delays loaded: {len(chrono_df)} records")
    
    # Load starts file
    starts_df = pd.read_csv('starts.csv')
    print(f"Starts file loaded: {len(starts_df)} records")
    
    # Load summary file
    summary_df = pd.read_excel('summary file - all of 2024.xlsx', header=None)
    print(f"Summary file loaded: {len(summary_df)} records")
    
    # Load PTC roster
    ptc_roster = pd.read_excel('PTC Vehicle Roster_2025-08-12.xlsx', header=None)
    print(f"PTC roster loaded: {len(ptc_roster)} records")
    
    return chrono_df, starts_df, summary_df, ptc_roster

def filter_ptc_delays(chrono_df):
    """Filter to only PTC-related delays"""
    ptc_causes = ['NJT PTC', 'NJT PTC HUMAN ERROR', 'NJT PTC INFRASTRUCTURE', 'NJT PTC MECHANICAL']
    ptc_delays = chrono_df[chrono_df['DELAYCAUSE'].isin(ptc_causes)].copy()
    print(f"PTC delays found: {len(ptc_delays)}")
    return ptc_delays

def process_ptc_roster(ptc_roster):
    """Process PTC roster to create equipment to PTC system mapping"""
    print("Processing PTC roster...")
    
    # Find the "Total Alstom" column to determine the split
    alstom_col = None
    for i, col in enumerate(ptc_roster.columns):
        if ptc_roster.iloc[0, i] == 'Total Alstom':
            alstom_col = i
            break
    
    if alstom_col is None:
        print("Could not find 'Total Alstom' column, using column 18 as default")
        alstom_col = 18
    
    print(f"Alstom column found at index: {alstom_col}")
    
    # Create equipment mapping
    equipment_ptc = {}
    
    # Process each row starting from row 5 (equipment numbers)
    for row_idx in range(4, len(ptc_roster)):
        row = ptc_roster.iloc[row_idx]
        
        # Process Alstom equipment (columns 0 to alstom_col-1)
        for col_idx in range(1, alstom_col):
            equipment_num = row.iloc[col_idx]
            if pd.notna(equipment_num) and str(equipment_num).strip() != '':
                try:
                    equipment_num = int(float(equipment_num))
                    equipment_ptc[equipment_num] = 'Alstom'
                except (ValueError, TypeError):
                    continue
        
        # Process Siemens equipment (columns alstom_col+1 onwards)
        for col_idx in range(alstom_col + 1, len(row)):
            equipment_num = row.iloc[col_idx]
            if pd.notna(equipment_num) and str(equipment_num).strip() != '':
                try:
                    equipment_num = int(float(equipment_num))
                    equipment_ptc[equipment_num] = 'Siemens'
                except (ValueError, TypeError):
                    continue
    
    print(f"Equipment-PTC mapping created: {len(equipment_ptc)} equipment pieces")
    
    # Count by system
    alstom_count = sum(1 for ptc in equipment_ptc.values() if ptc == 'Alstom')
    siemens_count = sum(1 for ptc in equipment_ptc.values() if ptc == 'Siemens')
    print(f"Alstom equipment: {alstom_count}, Siemens equipment: {siemens_count}")
    
    return equipment_ptc

def extract_equipment_from_summary(summary_df):
    """Extract equipment list and engine type from summary file"""
    print("Extracting equipment from summary file...")
    
    summary_equipment = {}
    
    for _, row in summary_df.iterrows():
        try:
            # Column 2 is Consist (train number)
            # Column 4 is Equipment (locomotive)
            # Column 18 is engine type
            consist = row.iloc[2]
            equipment = row.iloc[4]
            engine_type = row.iloc[18] if len(row) > 18 else None
            
            if pd.notna(consist) and pd.notna(equipment):
                try:
                    consist = str(int(float(consist)))
                    equipment = int(float(equipment))
                    summary_equipment[consist] = {
                        'equipment': equipment,
                        'engine_type': engine_type
                    }
                except (ValueError, TypeError):
                    continue
        except IndexError:
            continue
    
    print(f"Summary equipment mapping created: {len(summary_equipment)} entries")
    return summary_equipment

def get_day_of_week(date_obj):
    """Get day of week abbreviation (MF, SS, SA, etc.)"""
    if pd.isna(date_obj):
        return None
    
    # Check if it's a holiday (simplified - you may need to add more holidays)
    holidays_2024 = [
        '2024-01-01', '2024-01-15', '2024-02-19', '2024-05-27', 
        '2024-07-04', '2024-09-02', '2024-10-14', '2024-11-11', 
        '2024-11-28', '2024-12-25'
    ]
    
    date_str = date_obj.strftime('%Y-%m-%d')
    if date_str in holidays_2024:
        return 'SS'  # Sunday schedule for holidays
    
    # Get day of week
    weekday = date_obj.weekday()
    day_mapping = {
        0: 'MF',  # Monday
        1: 'MF',  # Tuesday  
        2: 'MF',  # Wednesday
        3: 'MF',  # Thursday
        4: 'MF',  # Friday
        5: 'SA',  # Saturday
        6: 'SS'   # Sunday
    }
    return day_mapping.get(weekday, 'MF')

def match_delays_to_equipment(ptc_delays, summary_equipment, starts_df, equipment_ptc):
    """Match delays to equipment using the cross-matching logic"""
    print("Matching delays to equipment...")
    
    results = []
    
    for _, delay in ptc_delays.iterrows():
        train_id = str(delay['TRAINID'])
        delay_date = delay['Date']
        
        # Get day of week for this delay
        day_of_week = get_day_of_week(delay_date)
        
        # Try to find equipment for this train
        lead_equipment = None
        ptc_system = None
        engine_type = None
        
        # First try to match from summary file
        if train_id in summary_equipment:
            lead_equipment = summary_equipment[train_id]['equipment']
            engine_type = summary_equipment[train_id]['engine_type']
            ptc_system = equipment_ptc.get(lead_equipment)
        
        # If not found in summary, try starts file
        if lead_equipment is None:
            # Look for this train in starts file for the specific day
            starts_filtered = starts_df[
                (starts_df['move'] == train_id) & 
                (starts_df['day'] == day_of_week)
            ]
            
            if len(starts_filtered) > 0:
                # Extract first equipment (locomotive) from equipment string
                equipment_str = str(starts_filtered.iloc[0]['equipment'])
                parts = equipment_str.split()
                if len(parts) >= 1:
                    try:
                        lead_equipment = int(float(parts[0]))
                        ptc_system = equipment_ptc.get(lead_equipment)
                    except (ValueError, TypeError):
                        pass
        
        results.append({
            'date': delay['Date'],
            'train_id': train_id,
            'delay_cause': delay['DELAYCAUSE'],
            'delay_minutes': delay['Delay (Minutes)'],
            'lead_equipment': lead_equipment,
            'ptc_system': ptc_system,
            'engine_type': engine_type,
            'day_of_week': day_of_week
        })
    
    return pd.DataFrame(results)

def analyze_results(results_df, equipment_ptc):
    """Analyze results and answer questions"""
    print("\n" + "="*50)
    print("ANALYSIS RESULTS")
    print("="*50)
    
    # Filter to 2024 data
    results_2024 = results_df[results_df['date'].dt.year == 2024].copy()
    
    # Question 1: Expected reduction if all equipment switched to Siemens
    alstom_delays = results_2024[results_2024['ptc_system'] == 'Alstom']
    siemens_delays = results_2024[results_2024['ptc_system'] == 'Siemens']
    
    alstom_total_delay = alstom_delays['delay_minutes'].sum()
    siemens_total_delay = siemens_delays['delay_minutes'].sum()
    
    alstom_count = len(alstom_delays)
    siemens_count = len(siemens_delays)
    
    if alstom_count > 0 and siemens_count > 0:
        alstom_avg_delay = alstom_total_delay / alstom_count
        siemens_avg_delay = siemens_total_delay / siemens_count
        
        expected_reduction = alstom_total_delay - (alstom_count * siemens_avg_delay)
        print(f"\n1. Expected reduction in PTC delays if all equipment switched to Siemens:")
        print(f"   {expected_reduction:.1f} minutes ({expected_reduction/60:.1f} hours)")
        print(f"   (Alstom avg: {alstom_avg_delay:.1f} min, Siemens avg: {siemens_avg_delay:.1f} min)")
    
    # Question 2 & 4: Equipment counts from PTC roster
    alstom_equipment_count = sum(1 for ptc in equipment_ptc.values() if ptc == 'Alstom')
    siemens_equipment_count = sum(1 for ptc in equipment_ptc.values() if ptc == 'Siemens')
    
    print(f"\n2. Pieces of fleet with Alstom PTC: {alstom_equipment_count}")
    print(f"   (From PTC Vehicle Roster)")
    
    # Question 3: Alstom PTC delays in 2024
    print(f"\n3. Alstom PTC delays in 2024: {len(alstom_delays)}")
    print(f"   Total delay time: {alstom_total_delay:.1f} minutes ({alstom_total_delay/60:.1f} hours)")
    
    print(f"\n4. Pieces of fleet with Siemens PTC: {siemens_equipment_count}")
    print(f"   (From PTC Vehicle Roster)")
    
    # Question 5: Siemens PTC delays in 2024
    print(f"\n5. Siemens PTC delays in 2024: {len(siemens_delays)}")
    print(f"   Total delay time: {siemens_total_delay:.1f} minutes ({siemens_total_delay/60:.1f} hours)")
    
    # Additional statistics
    print(f"\n" + "="*50)
    print("ADDITIONAL STATISTICS")
    print("="*50)
    
    print(f"Total PTC delays analyzed: {len(results_df)}")
    print(f"Delays with identified equipment: {len(results_df[results_df['ptc_system'].notna()])}")
    print(f"Delays without equipment match: {len(results_df[results_df['ptc_system'].isna()])}")
    
    # Delay cause breakdown
    print(f"\nDelay cause breakdown:")
    cause_counts = results_df['delay_cause'].value_counts()
    for cause, count in cause_counts.items():
        print(f"  {cause}: {count}")
    
    return {
        'alstom_equipment_count': alstom_equipment_count,
        'siemens_equipment_count': siemens_equipment_count,
        'alstom_delays_2024': len(alstom_delays),
        'siemens_delays_2024': len(siemens_delays),
        'expected_reduction': expected_reduction if 'expected_reduction' in locals() else None
    }

def main():
    """Main analysis function"""
    print("NJ TRANSIT PTC DELAY ANALYSIS - FINAL VERSION")
    print("="*50)
    
    # Load data
    chrono_df, starts_df, summary_df, ptc_roster = load_and_clean_data()
    
    # Filter PTC delays
    ptc_delays = filter_ptc_delays(chrono_df)
    
    # Process PTC roster
    equipment_ptc = process_ptc_roster(ptc_roster)
    
    # Extract equipment from summary file
    summary_equipment = extract_equipment_from_summary(summary_df)
    
    # Match delays to equipment
    results_df = match_delays_to_equipment(ptc_delays, summary_equipment, starts_df, equipment_ptc)
    
    # Analyze results
    analysis_results = analyze_results(results_df, equipment_ptc)
    
    # Save results
    results_df.to_csv('ptc_analysis_results_final.csv', index=False)
    print(f"\nDetailed results saved to 'ptc_analysis_results_final.csv'")
    
    return analysis_results

if __name__ == "__main__":
    main()
