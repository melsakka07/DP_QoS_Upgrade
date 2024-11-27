import re
from typing import Dict, List
import csv
from datetime import datetime
import os

def parse_sub_data(content: str) -> Dict[str, Dict]:
    """Parse subscriber data from the content and return organized results"""
    results = {
        'sub_data': {},
        'optgprs_data': {}
    }
    
    # Split records by END marker
    records = content.split('---    END')
    
    for record in records:
        # Process SUB records
        sub_match = re.search(r'%%LST SUB:IMSI="([^"]+)"', record)
        if sub_match:
            imsi = sub_match.group(1)
            gprs_data = re.search(r'"GPRS Data"(.*?)(?="|\Z)', record, re.DOTALL)
            eps_data = re.search(r'"EPS Data"(.*?)(?="|\Z)', record, re.DOTALL)
            
            sub_info = {}
            
            if gprs_data:
                gprs_text = gprs_data.group(1)
                cntxid = re.search(r'CNTXID\s*=\s*(\d+)', gprs_text)
                apntplid = re.search(r'APNTPLID\s*=\s*(\d+)', gprs_text)
                sub_info['gprs_cntxid'] = cntxid.group(1) if cntxid else 'N/A'
                sub_info['gprs_apntplid'] = apntplid.group(1) if apntplid else 'N/A'
            
            if eps_data:
                eps_text = eps_data.group(1)
                cntxid = re.search(r'CNTXID\s*=\s*(\d+)', eps_text)
                apntplid = re.search(r'APNTPLID\s*=\s*(\d+)', eps_text)
                sub_info['eps_cntxid'] = cntxid.group(1) if cntxid else 'N/A'
                sub_info['eps_apntplid'] = apntplid.group(1) if apntplid else 'N/A'
            
            if sub_info:
                results['sub_data'][imsi] = sub_info
        
        # Process OPTGPRS records
        optgprs_match = re.search(r'%%LST OPTGPRS:IMSI="([^"]+)"', record)
        if optgprs_match:
            imsi = optgprs_match.group(1)
            optgprs_info = {}
            
            apntplid = re.search(r'APNTPLID\s*=\s*(\d+)', record)
            qostplid = re.search(r'QOSTPLID\s*=\s*(\d+)', record)
            eps_qostplid = re.search(r'EPS_QOSTPLID\s*=\s*(\d+)', record)
            apn_type = re.search(r'APN_TYPE\s*=\s*(\w+)', record)
            
            optgprs_info['apntplid'] = apntplid.group(1) if apntplid else 'N/A'
            optgprs_info['qostplid'] = qostplid.group(1) if qostplid else 'N/A'
            optgprs_info['eps_qostplid'] = eps_qostplid.group(1) if eps_qostplid else 'N/A'
            optgprs_info['apn_type'] = apn_type.group(1) if apn_type else 'N/A'
            
            results['optgprs_data'][imsi] = optgprs_info
    
    return results

def export_to_csv(results: Dict[str, Dict], output_prefix: str = 'subscriber_data'):
    """Export results to CSV files"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create output directory if it doesn't exist
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    # Export SUB data
    sub_filename = os.path.join(output_dir, f'{output_prefix}_sub_{timestamp}.csv')
    with open(sub_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['IMSI', 'GPRS_CNTXID', 'GPRS_APNTPLID', 'EPS_CNTXID', 'EPS_APNTPLID'])
        for imsi, data in results['sub_data'].items():
            writer.writerow([
                imsi,
                data.get('gprs_cntxid', 'N/A'),
                data.get('gprs_apntplid', 'N/A'),
                data.get('eps_cntxid', 'N/A'),
                data.get('eps_apntplid', 'N/A')
            ])
    
    # Export OPTGPRS data
    optgprs_filename = os.path.join(output_dir, f'{output_prefix}_optgprs_{timestamp}.csv')
    with open(optgprs_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['IMSI', 'APNTPLID', 'QOSTPLID', 'EPS_QOSTPLID', 'APN_TYPE'])
        for imsi, data in results['optgprs_data'].items():
            writer.writerow([
                imsi,
                data.get('apntplid', 'N/A'),
                data.get('qostplid', 'N/A'),
                data.get('eps_qostplid', 'N/A'),
                data.get('apn_type', 'N/A')
            ])
    
    return sub_filename, optgprs_filename

def main():
    try:
        # Read input file
        with open('sub-list.txt', 'r') as file:
            content = file.read()
        
        # Parse data
        results = parse_sub_data(content)
        
        # Export to CSV
        sub_file, optgprs_file = export_to_csv(results)
        
        print(f"Processing complete!")
        print(f"SUB data exported to: {sub_file}")
        print(f"OPTGPRS data exported to: {optgprs_file}")
        
        # Print summary
        print(f"\nSummary:")
        print(f"Total SUB records: {len(results['sub_data'])}")
        print(f"Total OPTGPRS records: {len(results['optgprs_data'])}")
        
    except FileNotFoundError:
        print("Error: sub-list.txt file not found!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 