import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the results
df = pd.read_csv('ptc_analysis_results.csv')

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Filter to only matched results
matched_df = df[df['ptc_system'].notna()].copy()

# Create visualizations
plt.style.use('default')
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('NJ TRANSIT PTC DELAY ANALYSIS - 2024', fontsize=16, fontweight='bold')

# 1. Delay count by PTC system
ptc_counts = matched_df[matched_df['date'].dt.year == 2024]['ptc_system'].value_counts()
axes[0, 0].pie(ptc_counts.values, labels=ptc_counts.index, autopct='%1.1f%%', startangle=90)
axes[0, 0].set_title('PTC Delays by System (2024)')

# 2. Average delay duration by PTC system
avg_delays = matched_df[matched_df['date'].dt.year == 2024].groupby('ptc_system')['delay_minutes'].mean()
axes[0, 1].bar(avg_delays.index, avg_delays.values, color=['#ff7f0e', '#1f77b4'])
axes[0, 1].set_title('Average Delay Duration by PTC System (2024)')
axes[0, 1].set_ylabel('Minutes')
for i, v in enumerate(avg_delays.values):
    axes[0, 1].text(i, v + 0.1, f'{v:.1f}', ha='center', va='bottom')

# 3. Total delay time by PTC system
total_delays = matched_df[matched_df['date'].dt.year == 2024].groupby('ptc_system')['delay_minutes'].sum()
axes[1, 0].bar(total_delays.index, total_delays.values, color=['#ff7f0e', '#1f77b4'])
axes[1, 0].set_title('Total Delay Time by PTC System (2024)')
axes[1, 0].set_ylabel('Minutes')
for i, v in enumerate(total_delays.values):
    axes[1, 0].text(i, v + 20, f'{v:.0f}', ha='center', va='bottom')

# 4. Monthly delay trends
matched_df['month'] = matched_df['date'].dt.to_period('M')
monthly_delays = matched_df[matched_df['date'].dt.year == 2024].groupby(['month', 'ptc_system']).size().unstack(fill_value=0)
monthly_delays.plot(kind='line', marker='o', ax=axes[1, 1])
axes[1, 1].set_title('Monthly PTC Delays by System (2024)')
axes[1, 1].set_ylabel('Number of Delays')
axes[1, 1].legend(title='PTC System')
axes[1, 1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('ptc_delay_analysis_charts.png', dpi=300, bbox_inches='tight')
print("Charts saved as 'ptc_delay_analysis_charts.png'")

# Create summary statistics table
print("\n" + "="*60)
print("SUMMARY STATISTICS TABLE")
print("="*60)

summary_stats = pd.DataFrame({
    'Metric': [
        'Total Delays (2024)',
        'Total Delay Time (minutes)',
        'Total Delay Time (hours)',
        'Average Delay Duration (minutes)',
        'Equipment Count',
        'Delays per Equipment'
    ],
    'Alstom': [
        len(matched_df[(matched_df['date'].dt.year == 2024) & (matched_df['ptc_system'] == 'Alstom')]),
        matched_df[(matched_df['date'].dt.year == 2024) & (matched_df['ptc_system'] == 'Alstom')]['delay_minutes'].sum(),
        matched_df[(matched_df['date'].dt.year == 2024) & (matched_df['ptc_system'] == 'Alstom')]['delay_minutes'].sum() / 60,
        matched_df[(matched_df['date'].dt.year == 2024) & (matched_df['ptc_system'] == 'Alstom')]['delay_minutes'].mean(),
        75,  # From analysis
        len(matched_df[(matched_df['date'].dt.year == 2024) & (matched_df['ptc_system'] == 'Alstom')]) / 75
    ],
    'Siemens': [
        len(matched_df[(matched_df['date'].dt.year == 2024) & (matched_df['ptc_system'] == 'Siemens')]),
        matched_df[(matched_df['date'].dt.year == 2024) & (matched_df['ptc_system'] == 'Siemens')]['delay_minutes'].sum(),
        matched_df[(matched_df['date'].dt.year == 2024) & (matched_df['ptc_system'] == 'Siemens')]['delay_minutes'].sum() / 60,
        matched_df[(matched_df['date'].dt.year == 2024) & (matched_df['ptc_system'] == 'Siemens')]['delay_minutes'].mean(),
        21,  # From analysis
        len(matched_df[(matched_df['date'].dt.year == 2024) & (matched_df['ptc_system'] == 'Siemens')]) / 21
    ]
})

print(summary_stats.to_string(index=False, float_format='%.1f'))
