import pandas as pd

print("="*80)
print("NJ TRANSIT PTC DELAY ANALYSIS - FINAL ANSWERS")
print("="*80)

# Load the analysis results
df = pd.read_csv('ptc_analysis_results.csv')
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

# Get unique equipment counts
alstom_equipment = set()
siemens_equipment = set()

for _, row in df.iterrows():
    if row['ptc_system'] == 'Alstom' and pd.notna(row['lead_equipment']):
        alstom_equipment.add(row['lead_equipment'])
    elif row['ptc_system'] == 'Siemens' and pd.notna(row['lead_equipment']):
        siemens_equipment.add(row['lead_equipment'])

print("\n" + "="*80)
print("ANSWERS TO ASSIGNMENT QUESTIONS")
print("="*80)

print(f"\n1. What is the expected reduction in PTC related delays if all equipment was switched to Siemens?")
print(f"   ANSWER: {expected_reduction:.1f} minutes ({expected_reduction/60:.1f} hours)")
print(f"   DETAILS: Alstom average delay: {alstom_avg_delay:.1f} min, Siemens average delay: {siemens_avg_delay:.1f} min")

print(f"\n2. How many pieces of the fleet have Alstom PTC?")
print(f"   ANSWER: {len(alstom_equipment)} pieces of equipment")
print(f"   EQUIPMENT NUMBERS: {sorted(alstom_equipment)}")

print(f"\n3. How many Alstom PTC delays were there in 2024?")
print(f"   ANSWER: {alstom_count} delays")
print(f"   TOTAL DELAY TIME: {alstom_total_delay:.1f} minutes ({alstom_total_delay/60:.1f} hours)")

print(f"\n4. How many pieces of the fleet have Siemens PTC?")
print(f"   ANSWER: {len(siemens_equipment)} pieces of equipment")
print(f"   EQUIPMENT NUMBERS: {sorted(siemens_equipment)}")

print(f"\n5. How many Siemens PTC delays were there in 2024?")
print(f"   ANSWER: {siemens_count} delays")
print(f"   TOTAL DELAY TIME: {siemens_total_delay:.1f} minutes ({siemens_total_delay/60:.1f} hours)")

print("\n" + "="*80)
print("ADDITIONAL INSIGHTS")
print("="*80)

print(f"\n• Data Coverage:")
print(f"  - Total PTC delays analyzed: {len(df)}")
print(f"  - Delays with identified equipment: {len(df[df['ptc_system'].notna()])} ({len(df[df['ptc_system'].notna()])/len(df)*100:.1f}%)")
print(f"  - Delays without equipment match: {len(df[df['ptc_system'].isna()])}")

print(f"\n• Fleet Distribution:")
print(f"  - Alstom equipment: {len(alstom_equipment)} pieces ({len(alstom_equipment)/(len(alstom_equipment)+len(siemens_equipment))*100:.1f}%)")
print(f"  - Siemens equipment: {len(siemens_equipment)} pieces ({len(siemens_equipment)/(len(alstom_equipment)+len(siemens_equipment))*100:.1f}%)")

print(f"\n• Performance Comparison:")
print(f"  - Alstom delays per equipment: {alstom_count/len(alstom_equipment):.1f}")
print(f"  - Siemens delays per equipment: {siemens_count/len(siemens_equipment):.1f}")
print(f"  - Alstom is {alstom_count/len(alstom_equipment)/(siemens_count/len(siemens_equipment)):.1f}x more likely to have delays per equipment")

print(f"\n• Delay Duration Analysis:")
print(f"  - Alstom average delay: {alstom_avg_delay:.1f} minutes")
print(f"  - Siemens average delay: {siemens_avg_delay:.1f} minutes")
print(f"  - Difference: {alstom_avg_delay - siemens_avg_delay:.1f} minutes ({((alstom_avg_delay - siemens_avg_delay)/alstom_avg_delay)*100:.1f}% difference)")

print("\n" + "="*80)
print("CONCLUSION")
print("="*80)
print("The analysis shows that while Alstom equipment experiences more PTC-related delays than Siemens equipment,")
print("the average delay duration is very similar between the two systems. The expected reduction from switching")
print("all equipment to Siemens would be modest (1.7 hours annually), suggesting that other factors beyond")
print("PTC system type may be more significant contributors to delays.")
print("\nThe higher number of Alstom delays may be attributed to the larger Alstom fleet size rather than")
print("inherent system differences.")

