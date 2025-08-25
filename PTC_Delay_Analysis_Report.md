# NJ TRANSIT PTC DELAY ANALYSIS REPORT

## Executive Summary

This analysis examines PTC (Positive Train Control) related delays in NJ Transit operations, specifically comparing delays between Alstom and Siemens PTC systems. The analysis covers delay records from 2022-2025 and provides insights into equipment distribution and delay patterns.

## Key Findings

### 1. Expected Reduction in PTC Delays if All Equipment Switched to Siemens
**Answer: 101.4 minutes (1.7 hours) reduction**

- **Alstom average delay**: 13.1 minutes per incident
- **Siemens average delay**: 12.4 minutes per incident
- **Analysis**: While Siemens shows slightly better performance (0.7 minutes less per incident), the difference is relatively small, suggesting both systems perform similarly in terms of delay duration.

### 2. Fleet Distribution by PTC System

#### Alstom PTC Equipment
**Answer: 75 pieces of equipment**

**Equipment Numbers:**
- 1314, 1319, 1343, 1355, 1360, 1367, 1393, 1424, 1450, 1470, 1478, 1483, 1518
- 4201, 4218, 4601, 4603, 4604, 4608, 4610, 4615, 4616, 4620, 4626, 4627
- 6005, 6007, 6010, 6012, 6018, 6020, 6021, 6028, 6031, 6038, 6042, 6047, 6050, 6051, 6052, 6055, 6056, 6064, 6065, 6075, 6077, 6081
- 6700, 6701, 6703, 6704, 6706, 6708, 6710, 6712, 6713, 6714
- 7000, 7001, 7009, 7015, 7016, 7017, 7022, 7025, 7026, 7038, 7042, 7046, 7047, 7048, 7053, 7058, 7059, 7060

#### Siemens PTC Equipment
**Answer: 21 pieces of equipment**

**Equipment Numbers:**
- 4502, 4505, 4511, 4514, 4530, 4533, 4535, 4543
- 4631, 4633, 4635, 4636, 4637, 4638, 4646, 4648, 4652, 4655, 4657, 4660, 4664

### 3. 2024 Delay Statistics

#### Alstom PTC Delays in 2024
**Answer: 146 delays**

- **Total delay time**: 1,911 minutes (31.9 hours)
- **Average delay per incident**: 13.1 minutes
- **Percentage of total PTC delays**: 67.3% (146 out of 217 matched delays)

#### Siemens PTC Delays in 2024
**Answer: 71 delays**

- **Total delay time**: 880 minutes (14.7 hours)
- **Average delay per incident**: 12.4 minutes
- **Percentage of total PTC delays**: 32.7% (71 out of 217 matched delays)

## Detailed Analysis

### Data Coverage
- **Total PTC delays analyzed**: 5,140
- **Delays with identified equipment**: 724 (14.1%)
- **Delays without equipment match**: 4,416 (85.9%)

### Delay Cause Breakdown
All analyzed delays were categorized as "NJT PTC MECHANICAL", indicating mechanical issues with the PTC system itself.

### Equipment Matching Success Rate
The analysis successfully matched 14.1% of PTC delays to specific equipment. The lower match rate is due to:
1. Limited consist data availability in the summary file
2. Some train IDs not appearing in the summary file
3. Potential data quality issues in the source files

## Recommendations

### 1. System Performance
- Both Alstom and Siemens PTC systems show similar performance in terms of delay duration
- The small difference (0.7 minutes) suggests system choice may not be the primary factor in PTC-related delays

### 2. Fleet Management
- Alstom equipment represents 78% of the identified fleet (75 out of 96 pieces)
- Siemens equipment represents 22% of the identified fleet (21 out of 96 pieces)
- Consider the higher frequency of Alstom delays (146 vs 71) when planning maintenance and upgrades

### 3. Data Quality Improvements
- Improve data linkage between delay records and equipment assignments
- Consider implementing more robust tracking systems to increase the match rate
- Standardize train identification across all systems

## Methodology

### Data Sources
1. **Chrono Delays File**: Contains 62,086 delay records with PTC-specific filtering
2. **Summary File**: Contains equipment assignments and consist information
3. **PTC Vehicle Roster**: Maps equipment numbers to PTC system types
4. **Starts File**: Additional equipment scheduling information

### Analysis Process
1. **Filtered PTC delays** using specific delay causes: NJ PTC, NJ PTC HUMAN ERROR, NJ PTC INFRASTRUCTURE, NJT PTC MECHANICAL
2. **Extracted lead equipment** (locomotives) from summary file
3. **Mapped equipment to PTC systems** using the vehicle roster
4. **Matched delays to equipment** using train ID to consist mapping
5. **Analyzed 2024 data** for specific statistics

### Limitations
- Limited equipment matching success rate (14.1%)
- Analysis focuses on mechanical PTC delays only
- Equipment assignments may vary over time
- Some equipment may have been reassigned or retired

## Conclusion

The analysis reveals that while Alstom equipment experiences more PTC-related delays than Siemens equipment, the average delay duration is similar between the two systems. The expected reduction from switching all equipment to Siemens would be modest (1.7 hours annually), suggesting that other factors beyond PTC system type may be more significant contributors to delays.

The higher number of Alstom delays (146 vs 71) may be attributed to the larger Alstom fleet size (75 vs 21 pieces of equipment) rather than inherent system differences.
