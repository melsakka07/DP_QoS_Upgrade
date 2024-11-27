# Subscriber Data Parser and Comparison Tools

This toolkit provides two utilities for working with HLR/HSS subscriber data:
1. A parser that extracts data to CSV files
2. A comparison tool that analyzes differences between two subscribers

## Parser Usage (parse_subscriber_data.py)

1. Place your `sub-list.txt` file in the same directory as the script
2. Run the script:   ```
   python parse_subscriber_data.py   ```
3. The script will create an `output` directory (if it doesn't exist) and generate two CSV files inside it:
   - output/subscriber_data_sub_[timestamp].csv - Contains SUB record data
   - output/subscriber_data_optgprs_[timestamp].csv - Contains OPTGPRS record data

### Parser Output Format

#### SUB Data CSV
- IMSI
- GPRS_CNTXID
- GPRS_APNTPLID
- EPS_CNTXID
- EPS_APNTPLID

#### OPTGPRS Data CSV
- IMSI
- APNTPLID
- QOSTPLID
- EPS_QOSTPLID
- APN_TYPE

## Comparison Tool Usage (compare_subscribers.py)

1. Place your `sub-list.txt` file in the same directory as the script
2. Run the script:   ```
   python compare_subscribers.py   ```
3. Enter the two IMSIs you want to compare when prompted
4. The script will create an `out-cmp` directory (if it doesn't exist) and generate a comparison file:
   - out-cmp/[IMSI1]_[IMSI2]_sub-list-comp.txt

### Comparison Output Format
The comparison file shows:
- SUB Data differences and similarities
  - GPRS_CNTXID
  - GPRS_APNTPLID
  - EPS_CNTXID
  - EPS_APNTPLID
- OPTGPRS Data differences and similarities
  - APNTPLID
  - QOSTPLID
  - EPS_QOSTPLID
  - APN_TYPE

## Requirements
- Python 3.6+