#!/usr/bin/env python3
"""
Web scraper to extract intelligence evaluation data from artificialanalysis.ai
"""
import requests
from bs4 import BeautifulSoup
import json
import re
from typing import Dict, List, Optional
import time

def scrape_evaluations_page():
    """Scrape the open-source models page"""
    url = "https://artificialanalysis.ai/models/open-source"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    try:
        print(f"Fetching {url}...")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for JSON data in script tags
        data = extract_json_data(soup)
        
        if data:
            return data
        
        # Try to extract from HTML structure
        return extract_from_html(soup)
        
    except Exception as e:
        print(f"Error scraping page: {e}")
        return None

def extract_json_data(soup: BeautifulSoup) -> Optional[Dict]:
    """Extract JSON data from script tags"""
    scripts = soup.find_all('script')
    
    for script in scripts:
        if not script.string:
            continue
        
        content = script.string
        
        # Look for common patterns
        patterns = [
            r'window\.__INITIAL_STATE__\s*=\s*({.+?});',
            r'window\.__NEXT_DATA__\s*=\s*({.+?});',
            r'const\s+data\s*=\s*({.+?});',
            r'var\s+modelsData\s*=\s*({.+?});',
            r'"models":\s*\[({.+?})\]',
            r'"benchmarks":\s*\[({.+?})\]',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            for match in matches:
                try:
                    json_data = json.loads(match)
                    if isinstance(json_data, dict) and ('models' in json_data or 'benchmarks' in json_data):
                        return json_data
                except:
                    pass
        
        # Try to find any JSON object
        try:
            json_match = re.search(r'\{[^{}]*"models"[^{}]*\}', content, re.DOTALL)
            if json_match:
                json_data = json.loads(json_match.group())
                if isinstance(json_data, dict):
                    return json_data
        except:
            pass
    
    return None

def extract_from_html(soup: BeautifulSoup) -> Optional[Dict]:
    """Extract data from HTML table structure"""
    data = {
        "benchmarks": [],
        "models": []
    }
    
    # Find table
    table = soup.find('table')
    if not table:
        # Try to find any data structure
        tables = soup.find_all(['table', 'div'], class_=re.compile(r'table|model|benchmark', re.I))
        if tables:
            table = tables[0]
    
    if table:
        # Extract headers (benchmarks)
        headers = table.find_all(['th', 'thead'])
        benchmark_names = []
        
        for header in headers:
            if header.name == 'th':
                text = header.get_text(strip=True)
                if text and text.lower() not in ['model', 'name', 'provider']:
                    benchmark_names.append(text)
            elif header.name == 'thead':
                ths = header.find_all('th')
                for th in ths:
                    text = th.get_text(strip=True)
                    if text and text.lower() not in ['model', 'name', 'provider']:
                        benchmark_names.append(text)
        
        # Create benchmark list
        for i, name in enumerate(benchmark_names):
            benchmark_id = name.lower().replace(' ', '-').replace('²', '2').replace('τ', 'tau')
            data["benchmarks"].append({
                "id": benchmark_id,
                "name": name,
                "full_name": name
            })
        
        # Extract model rows
        rows = table.find_all('tr')[1:]  # Skip header row
        
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) < 2:
                continue
            
            model_name = cells[0].get_text(strip=True)
            if not model_name or model_name.lower() in ['model', 'name']:
                continue
            
            model_data = {
                "id": model_name.lower().replace(' ', '-').replace('.', '-'),
                "name": model_name,
                "provider": "",
                "scores": {}
            }
            
            # Extract scores
            for i, cell in enumerate(cells[1:], 1):
                if i <= len(benchmark_names):
                    score_text = cell.get_text(strip=True)
                    score = parse_score(score_text)
                    if score is not None:
                        benchmark_id = data["benchmarks"][i-1]["id"]
                        model_data["scores"][benchmark_id] = score
            
            if model_data["scores"]:
                data["models"].append(model_data)
    
    return data if data["models"] else None

def parse_score(text: str) -> Optional[float]:
    """Parse score from text"""
    if not text or text.lower() in ['n/a', 'na', '-', '']:
        return None
    
    # Remove percentage sign and convert
    text = text.replace('%', '').strip()
    
    # Try to extract number
    match = re.search(r'(\d+\.?\d*)', text)
    if match:
        value = float(match.group(1))
        # If it's > 1, assume it's a percentage and convert to decimal
        if value > 1:
            return value / 100
        return value
    
    return None

def main():
    print("=" * 60)
    print("Web Scraper for Artificial Analysis Intelligence Evaluations")
    print("=" * 60)
    
    data = scrape_evaluations_page()
    
    if data and data.get('models'):
        print(f"\n✓ Successfully scraped data for {len(data['models'])} models")
        print(f"✓ Found {len(data.get('benchmarks', []))} benchmarks")
        
        # Save to file
        with open("evaluations_data.json", "w") as f:
            json.dump(data, f, indent=2)
        
        print("\n✓ Data saved to evaluations_data.json")
        
        # Print summary
        print("\n=== Sample Models ===")
        for model in data['models'][:3]:
            print(f"  - {model['name']}: {len(model.get('scores', {}))} scores")
            for benchmark, score in list(model.get('scores', {}).items())[:3]:
                print(f"    {benchmark}: {score}")
    else:
        print("\n⚠ Could not scrape data from website")
        print("The page structure may have changed or requires JavaScript rendering")
        print("You may need to use a headless browser like Selenium or Playwright")

if __name__ == "__main__":
    main()




