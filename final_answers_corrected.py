import pandas as pd

print("="*80)
print("NJ TRANSIT PTC DELAY ANALYSIS - CORRECTED FINAL ANSWERS")
print("="*80)

# Load the analysis results
df = pd.read_csv('ptc_analysis_results_final.csv')
df['date'] = pd.to_datetime(df['date'])

# Filter to 2024 data
df_2024 = df[df['date'].dt.year == 2024].copy()
matched_2024 = df_2024[df_2024['ptc_system'].notna()].copy()

# Calculate statistics
alstom_delays = matched_2024[matched_2024['ptc_system'] == 'Alstom']
siemens_delays = matched_2024[matched_2024['ptc_system'] == 'Siemens']

alstom_total_delay = alstom_delays['delay_minutes'].sum()
siemens_total_delay = siemens_delays['delay_minutes'].sum()

alstom_count = len(alstom_delays)
siemens_count = len(siemens_delays)

alstom_avg_delay = alstom_total_delay / alstom_count if alstom_count > 0 else 0
siemens_avg_delay = siemens_total_delay / siemens_count if siemens_count > 0 else 0

expected_reduction = alstom_total_delay - (alstom_count * siemens_avg_delay)

print("\n" + "="*80)
print("ANSWERS TO ASSIGNMENT QUESTIONS")
print("="*80)

print(f"\n1. What is the expected reduction in PTC related delays if all equipment was switched to Siemens?")
print(f"   ANSWER: {expected_reduction:.1f} minutes ({expected_reduction/60:.1f} hours)")
print(f"   DETAILS: Alstom average delay: {alstom_avg_delay:.1f} min, Siemens average delay: {siemens_avg_delay:.1f} min")

print(f"\n2. How many pieces of the fleet have Alstom PTC?")
print(f"   ANSWER: 435 pieces of equipment")
print(f"   SOURCE: Direct count from PTC Vehicle Roster")

print(f"\n3. How many Alstom PTC delays were there in 2024?")
print(f"   ANSWER: {alstom_count} delays")
print(f"   TOTAL DELAY TIME: {alstom_total_delay:.1f} minutes ({alstom_total_delay/60:.1f} hours)")

print(f"\n4. How many pieces of the fleet have Siemens PTC?")
print(f"   ANSWER: 101 pieces of equipment")
print(f"   SOURCE: Direct count from PTC Vehicle Roster")

print(f"\n5. How many Siemens PTC delays were there in 2024?")
print(f"   ANSWER: {siemens_count} delays")
print(f"   TOTAL DELAY TIME: {siemens_total_delay:.1f} minutes ({siemens_total_delay/60:.1f} hours)")

print("\n" + "="*80)
print("IMPROVEMENTS MADE")
print("="*80)

print(f"\n• PTC Cause Filtering:")
print(f"  - CORRECTED: Changed from 'NJ PTC' to 'NJT PTC'")
print(f"  - Now includes: NJT PTC, NJT PTC HUMAN ERROR, NJT PTC INFRASTRUCTURE, NJT PTC MECHANICAL")

print(f"\n• Equipment Counts:")
print(f"  - CORRECTED: Equipment counts now come directly from PTC Vehicle Roster")
print(f"  - Alstom: 435 pieces (vs previous 75)")
print(f"  - Siemens: 101 pieces (vs previous 21)")

print(f"\n• Cross-Matching Logic:")
print(f"  - IMPLEMENTED: Proper integration of summary file and starts file")
print(f"  - ADDED: Day-of-week logic (MF, SA, SS) with holiday handling")
print(f"  - IMPROVED: Equipment matching using both data sources")

print(f"\n• Data Coverage:")
print(f"  - Total PTC delays analyzed: {len(df)}")
print(f"  - Delays with identified equipment: {len(df[df['ptc_system'].notna()])} ({len(df[df['ptc_system'].notna()])/len(df)*100:.1f}%)")
print(f"  - Delays without equipment match: {len(df[df['ptc_system'].isna()])}")

print(f"\n• Delay Cause Breakdown:")
cause_counts = df['delay_cause'].value_counts()
for cause, count in cause_counts.items():
    print(f"  {cause}: {count}")

print("\n" + "="*80)
print("KEY FINDINGS")
print("="*80)

print(f"\n• Performance Comparison:")
print(f"  - Alstom average delay: {alstom_avg_delay:.1f} minutes")
print(f"  - Siemens average delay: {siemens_avg_delay:.1f} minutes")
print(f"  - Difference: {alstom_avg_delay - siemens_avg_delay:.1f} minutes ({((alstom_avg_delay - siemens_avg_delay)/alstom_avg_delay)*100:.1f}% difference)")

print(f"\n• Fleet Distribution:")
print(f"  - Alstom equipment: 435 pieces (81.2%)")
print(f"  - Siemens equipment: 101 pieces (18.8%)")

print(f"\n• Delay Distribution:")
print(f"  - Alstom delays: {alstom_count} ({alstom_count/(alstom_count+siemens_count)*100:.1f}%)")
print(f"  - Siemens delays: {siemens_count} ({siemens_count/(alstom_count+siemens_count)*100:.1f}%)")

print("\n" + "="*80)
print("CONCLUSION")
print("="*80)
print("The corrected analysis shows that while Alstom equipment experiences more PTC-related delays than")
print("Siemens equipment, the average delay duration is very similar between the two systems. The expected")
print("reduction from switching all equipment to Siemens would be modest (2.1 hours annually), suggesting")
print("that other factors beyond PTC system type may be more significant contributors to delays.")
print("\nThe higher number of Alstom delays may be attributed to the larger Alstom fleet size rather than")
print("inherent system differences.")
