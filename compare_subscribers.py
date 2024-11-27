import re
from typing import Dict, Tuple
import os

def extract_subscriber_data(content: str, imsi: str) -> Tuple[Dict, Dict]:
    """Extract SUB and OPTGPRS data for a specific IMSI"""
    sub_data = {}
    optgprs_data = {}
    
    # Split records by END marker
    records = content.split('---    END')
    
    for record in records:
        # Process SUB records
        sub_match = re.search(f'%%LST SUB:IMSI="{imsi}"', record)
        if sub_match:
            gprs_data = re.search(r'"GPRS Data"(.*?)(?="|\Z)', record, re.DOTALL)
            eps_data = re.search(r'"EPS Data"(.*?)(?="|\Z)', record, re.DOTALL)
            
            if gprs_data:
                gprs_text = gprs_data.group(1)
                cntxid = re.search(r'CNTXID\s*=\s*(\d+)', gprs_text)
                apntplid = re.search(r'APNTPLID\s*=\s*(\d+)', gprs_text)
                sub_data['GPRS_CNTXID'] = cntxid.group(1) if cntxid else 'N/A'
                sub_data['GPRS_APNTPLID'] = apntplid.group(1) if apntplid else 'N/A'
            
            if eps_data:
                eps_text = eps_data.group(1)
                cntxid = re.search(r'CNTXID\s*=\s*(\d+)', eps_text)
                apntplid = re.search(r'APNTPLID\s*=\s*(\d+)', eps_text)
                sub_data['EPS_CNTXID'] = cntxid.group(1) if cntxid else 'N/A'
                sub_data['EPS_APNTPLID'] = apntplid.group(1) if apntplid else 'N/A'
        
        # Process OPTGPRS records
        optgprs_match = re.search(f'%%LST OPTGPRS:IMSI="{imsi}"', record)
        if optgprs_match:
            apntplid = re.search(r'APNTPLID\s*=\s*(\d+)', record)
            qostplid = re.search(r'QOSTPLID\s*=\s*(\d+)', record)
            eps_qostplid = re.search(r'EPS_QOSTPLID\s*=\s*(\d+)', record)
            apn_type = re.search(r'APN_TYPE\s*=\s*(\w+)', record)
            
            optgprs_data['APNTPLID'] = apntplid.group(1) if apntplid else 'N/A'
            optgprs_data['QOSTPLID'] = qostplid.group(1) if qostplid else 'N/A'
            optgprs_data['EPS_QOSTPLID'] = eps_qostplid.group(1) if eps_qostplid else 'N/A'
            optgprs_data['APN_TYPE'] = apn_type.group(1) if apn_type else 'N/A'
    
    return sub_data, optgprs_data

def compare_subscribers(data1: Tuple[Dict, Dict], data2: Tuple[Dict, Dict], imsi1: str, imsi2: str) -> str:
    """Compare data between two subscribers and return formatted output"""
    sub1, optgprs1 = data1
    sub2, optgprs2 = data2
    
    output = []
    output.append(f"Comparison between IMSI {imsi1} and IMSI {imsi2}\n")
    output.append("=" * 50 + "\n")
    
    # Compare SUB data
    output.append("\nSUB Data Comparison:")
    output.append("-" * 20)
    
    all_sub_keys = set(sub1.keys()) | set(sub2.keys())
    for key in sorted(all_sub_keys):
        val1 = sub1.get(key, 'N/A')
        val2 = sub2.get(key, 'N/A')
        if val1 == val2:
            output.append(f"\n{key}: {val1} (Same for both IMSIs)")
        else:
            output.append(f"\n{key}:")
            output.append(f"  IMSI {imsi1}: {val1}")
            output.append(f"  IMSI {imsi2}: {val2}")
    
    # Compare OPTGPRS data
    output.append("\n\nOPTGPRS Data Comparison:")
    output.append("-" * 24)
    
    all_optgprs_keys = set(optgprs1.keys()) | set(optgprs2.keys())
    for key in sorted(all_optgprs_keys):
        val1 = optgprs1.get(key, 'N/A')
        val2 = optgprs2.get(key, 'N/A')
        if val1 == val2:
            output.append(f"\n{key}: {val1} (Same for both IMSIs)")
        else:
            output.append(f"\n{key}:")
            output.append(f"  IMSI {imsi1}: {val1}")
            output.append(f"  IMSI {imsi2}: {val2}")
    
    return "\n".join(output)

def main():
    try:
        # Read input file
        with open('sub-list.txt', 'r') as file:
            content = file.read()
        
        # Get IMSIs from user
        print("\nIMSI Comparison Tool")
        print("=" * 20)
        imsi1 = input("\nEnter first IMSI to compare: ").strip()
        imsi2 = input("Enter second IMSI to compare: ").strip()
        
        # Extract data for both IMSIs
        data1 = extract_subscriber_data(content, imsi1)
        data2 = extract_subscriber_data(content, imsi2)
        
        # Compare and generate output
        comparison = compare_subscribers(data1, data2, imsi1, imsi2)
        
        # Create output directory if it doesn't exist
        output_dir = 'out-cmp'
        os.makedirs(output_dir, exist_ok=True)
        
        # Create filename using both IMSIs
        output_filename = os.path.join(output_dir, f"{imsi1}_{imsi2}_sub-list-comp.txt")
        
        # Write comparison to file
        with open(output_filename, 'w') as f:
            f.write(comparison)
        
        print(f"\nComparison complete! Results written to {output_filename}")
        
    except FileNotFoundError:
        print("Error: sub-list.txt file not found!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 