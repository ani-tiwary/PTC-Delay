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
    summary_df = pd.read_excel('summary file - all of 2024.xlsx')
    print(f"Summary file loaded: {len(summary_df)} records")
    
    # Load PTC roster
    ptc_roster = pd.read_excel('PTC Vehicle Roster_2025-08-12.xlsx', header=None)
    print(f"PTC roster loaded: {len(ptc_roster)} records")
    
    return chrono_df, starts_df, summary_df, ptc_roster

def filter_ptc_delays(chrono_df):
    """Filter to only PTC-related delays"""
    ptc_causes = ['NJ PTC', 'NJ PTC HUMAN ERROR', 'NJ PTC INFRASTRUCTURE', 'NJT PTC MECHANICAL']
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
    return equipment_ptc

def extract_lead_equipment(summary_df):
    """Extract lead equipment (locomotive) from summary file"""
    print("Extracting lead equipment from summary file...")
    
    # Create mapping from consist to lead equipment
    consist_to_equipment = {}
    
    for _, row in summary_df.iterrows():
        try:
            consist = row.iloc[2]  # Column 2 is Consist
            equipment = row.iloc[4]  # Column 4 is Equipment (locomotive)
            
            if pd.notna(consist) and pd.notna(equipment):
                try:
                    consist = str(int(float(consist)))
                    equipment = int(float(equipment))
                    consist_to_equipment[consist] = equipment
                except (ValueError, TypeError):
                    continue
        except IndexError:
            continue
    
    print(f"Consist to equipment mapping created: {len(consist_to_equipment)} entries")
    return consist_to_equipment

def match_delays_to_equipment(ptc_delays, consist_to_equipment, equipment_ptc):
    """Match delays to equipment and PTC systems"""
    print("Matching delays to equipment...")
    
    results = []
    
    for _, delay in ptc_delays.iterrows():
        train_id = str(delay['TRAINID'])  # Convert to string for matching
        
        # Try to find equipment for this train
        lead_equipment = None
        ptc_system = None
        
        if train_id in consist_to_equipment:
            lead_equipment = consist_to_equipment[train_id]
            ptc_system = equipment_ptc.get(lead_equipment)
        
        results.append({
            'date': delay['Date'],
            'train_id': train_id,
            'delay_cause': delay['DELAYCAUSE'],
            'delay_minutes': delay['Delay (Minutes)'],
            'lead_equipment': lead_equipment,
            'ptc_system': ptc_system
        })
    
    return pd.DataFrame(results)

def analyze_results(results_df):
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
    
    # Question 2: How many pieces of fleet have Alstom PTC
    alstom_equipment = set()
    siemens_equipment = set()
    
    for _, row in results_df.iterrows():
        if row['ptc_system'] == 'Alstom' and pd.notna(row['lead_equipment']):
            alstom_equipment.add(row['lead_equipment'])
        elif row['ptc_system'] == 'Siemens' and pd.notna(row['lead_equipment']):
            siemens_equipment.add(row['lead_equipment'])
    
    print(f"\n2. Pieces of fleet with Alstom PTC: {len(alstom_equipment)}")
    print(f"   Equipment numbers: {sorted(alstom_equipment)}")
    
    # Question 3: Alstom PTC delays in 2024
    print(f"\n3. Alstom PTC delays in 2024: {len(alstom_delays)}")
    print(f"   Total delay time: {alstom_total_delay:.1f} minutes ({alstom_total_delay/60:.1f} hours)")
    
    # Question 4: How many pieces of fleet have Siemens PTC
    print(f"\n4. Pieces of fleet with Siemens PTC: {len(siemens_equipment)}")
    print(f"   Equipment numbers: {sorted(siemens_equipment)}")
    
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
        'alstom_equipment_count': len(alstom_equipment),
        'siemens_equipment_count': len(siemens_equipment),
        'alstom_delays_2024': len(alstom_delays),
        'siemens_delays_2024': len(siemens_delays),
        'expected_reduction': expected_reduction if 'expected_reduction' in locals() else None
    }

def main():
    """Main analysis function"""
    print("NJ TRANSIT PTC DELAY ANALYSIS")
    print("="*50)
    
    # Load data
    chrono_df, starts_df, summary_df, ptc_roster = load_and_clean_data()
    
    # Filter PTC delays
    ptc_delays = filter_ptc_delays(chrono_df)
    
    # Process PTC roster
    equipment_ptc = process_ptc_roster(ptc_roster)
    
    # Extract lead equipment
    consist_to_equipment = extract_lead_equipment(summary_df)
    
    # Match delays to equipment
    results_df = match_delays_to_equipment(ptc_delays, consist_to_equipment, equipment_ptc)
    
    # Analyze results
    analysis_results = analyze_results(results_df)
    
    # Save results
    results_df.to_csv('ptc_analysis_results.csv', index=False)
    print(f"\nDetailed results saved to 'ptc_analysis_results.csv'")
    
    return analysis_results

if __name__ == "__main__":
    main()
