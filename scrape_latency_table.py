#!/usr/bin/env python3
"""
Scrape latency/performance table from artificialanalysis.ai/models/open-source
Extracts TTFT, ITL, E2E, and Throughput data from the website table
"""
import requests
from bs4 import BeautifulSoup
import json
import csv
import re
from typing import Dict, List, Optional

def scrape_latency_table(url: str = "https://artificialanalysis.ai/models/open-source") -> List[Dict]:
    """
    Scrape latency metrics from the website table
    """
    print(f"Scraping {url}...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all tables
        tables = soup.find_all('table')
        print(f"Found {len(tables)} tables on the page")
        
        models_data = []
        
        # Look for table with latency/performance columns
        for table in tables:
            headers_row = table.find('thead')
            if not headers_row:
                headers_row = table.find('tr')
            
            if not headers_row:
                continue
            
            # Get column headers
            headers_text = [th.get_text(strip=True) for th in headers_row.find_all(['th', 'td'])]
            print(f"  Table headers: {headers_text[:10]}...")  # Print first 10
            
            # Look for latency-related columns
            latency_keywords = ['ttft', 'itl', 'latency', 'throughput', 'tokens/sec', 'time to first', 'inter-token', 'e2e', 'trt', 'tfcr']
            has_latency = any(keyword.lower() in ' '.join(headers_text).lower() for keyword in latency_keywords)
            
            if has_latency:
                print(f"  ✓ Found table with latency metrics")
                
                # Extract data rows
                rows = table.find_all('tr')[1:]  # Skip header
                
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) < 2:
                        continue
                    
                    model_data = {}
                    
                    # Extract model name (usually first column)
                    model_name = cells[0].get_text(strip=True)
                    if not model_name:
                        continue
                    
                    model_data['model_name'] = model_name
                    
                    # Extract metrics based on column headers
                    for i, header in enumerate(headers_text):
                        if i >= len(cells):
                            break
                        
                        cell_text = cells[i].get_text(strip=True)
                        header_lower = header.lower()
                        
                        # TTFT variations
                        if any(kw in header_lower for kw in ['ttft', 'time to first', 'tfcr', 'first token']):
                            value = parse_number(cell_text)
                            if value:
                                model_data['ttft_ms'] = value
                        
                        # ITL variations
                        elif any(kw in header_lower for kw in ['itl', 'inter-token', 'tpot', 'per token']):
                            value = parse_number(cell_text)
                            if value:
                                model_data['itl_ms_per_token'] = value
                        
                        # E2E variations
                        elif any(kw in header_lower for kw in ['e2e', 'end-to-end', 'trt', 'total response', 'total latency']):
                            value = parse_number(cell_text)
                            if value:
                                model_data['e2e_ms'] = value
                        
                        # Throughput variations
                        elif any(kw in header_lower for kw in ['throughput', 'tokens/sec', 'tokens per second', 'tps', 'generation speed']):
                            value = parse_number(cell_text)
                            if value:
                                model_data['throughput_tokens_per_sec'] = value
                    
                    if len(model_data) > 1:  # Has at least model name + one metric
                        models_data.append(model_data)
                
                break  # Found the right table
        
        return models_data
        
    except Exception as e:
        print(f"Error scraping website: {e}")
        import traceback
        traceback.print_exc()
        return []

def parse_number(text: str) -> Optional[float]:
    """Parse number from text, handling various formats"""
    if not text or text == 'N/A' or text == '-' or text == '':
        return None
    
    # Remove commas and whitespace
    text = text.replace(',', '').strip()
    
    # Extract number (handle units like "ms", "s", "tokens/sec")
    match = re.search(r'([\d.]+)', text)
    if match:
        value = float(match.group(1))
        
        # Convert seconds to milliseconds if needed
        if 's' in text.lower() and 'ms' not in text.lower() and value < 100:
            value = value * 1000
        
        return value
    
    return None

def export_to_csv(models: List[Dict], filename: str = "scraped_latency_data.csv"):
    """Export scraped data to CSV"""
    if not models:
        print("No data to export")
        return
    
    headers = ['model_name', 'ttft_ms', 'itl_ms_per_token', 'e2e_ms', 'throughput_tokens_per_sec']
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        
        for model in models:
            row = {h: model.get(h, '') for h in headers}
            writer.writerow(row)
    
    print(f"✓ Exported {len(models)} models to {filename}")

def export_to_json(models: List[Dict], filename: str = "scraped_latency_data.json"):
    """Export scraped data to JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(models, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Exported {len(models)} models to {filename}")

def main():
    print("=" * 70)
    print("  Scraping Latency Table from Artificial Analysis")
    print("=" * 70)
    
    models = scrape_latency_table()
    
    if models:
        print(f"\n✓ Scraped {len(models)} models with latency metrics")
        
        # Count models with each metric
        with_ttft = sum(1 for m in models if m.get('ttft_ms'))
        with_itl = sum(1 for m in models if m.get('itl_ms_per_token'))
        with_e2e = sum(1 for m in models if m.get('e2e_ms'))
        with_throughput = sum(1 for m in models if m.get('throughput_tokens_per_sec'))
        
        print(f"  - Models with TTFT: {with_ttft}")
        print(f"  - Models with ITL: {with_itl}")
        print(f"  - Models with E2E: {with_e2e}")
        print(f"  - Models with Throughput: {with_throughput}")
        
        # Export
        export_to_csv(models)
        export_to_json(models)
        
        # Print sample
        print("\n" + "=" * 70)
        print("  Sample Scraped Data")
        print("=" * 70)
        for model in models[:5]:
            print(f"\n  {model.get('model_name', 'Unknown')}")
            if model.get('ttft_ms'):
                print(f"    TTFT: {model['ttft_ms']} ms")
            if model.get('itl_ms_per_token'):
                print(f"    ITL: {model['itl_ms_per_token']} ms/token")
            if model.get('e2e_ms'):
                print(f"    E2E: {model['e2e_ms']} ms")
            if model.get('throughput_tokens_per_sec'):
                print(f"    Throughput: {model['throughput_tokens_per_sec']} tokens/sec")
    else:
        print("\n⚠ No latency data found in table")
        print("   The table structure may have changed or requires JavaScript rendering")

if __name__ == "__main__":
    main()

