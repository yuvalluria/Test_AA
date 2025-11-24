#!/usr/bin/env python3
"""
Script to scrape intelligence evaluation data from artificialanalysis.ai
"""
import requests
from bs4 import BeautifulSoup
import json
import re
from typing import Dict, List, Any

API_KEY = "aa_OXmwOTJvjVHpPnJQsOgimbFMwsPoVgOT"

def fetch_with_api():
    """Try to fetch data using the API key"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "X-API-Key": API_KEY,
        "api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    # Try various possible API endpoints
    endpoints = [
        "https://api.artificialanalysis.ai/v1/benchmarks",
        "https://api.artificialanalysis.ai/benchmarks",
        "https://api.artificialanalysis.ai/v1/models",
        "https://api.artificialanalysis.ai/models",
        "https://api.artificialanalysis.ai/v1/evaluations",
        "https://api.artificialanalysis.ai/evaluations",
    ]
    
    for endpoint in endpoints:
        try:
            print(f"Trying: {endpoint}")
            response = requests.get(endpoint, headers=headers, timeout=10)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code != 404:
                print(f"Response: {response.text[:200]}")
        except Exception as e:
            print(f"Error with {endpoint}: {e}")
            continue
    
    return None

def scrape_website():
    """Scrape the website directly"""
    url = "https://artificialanalysis.ai/models/open-source"
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try to extract data from the page
        # This will need to be adjusted based on actual page structure
        data = {
            "models": [],
            "benchmarks": []
        }
        
        # Look for script tags with JSON data
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string:
                # Try to find JSON data
                if 'models' in script.string.lower() or 'benchmarks' in script.string.lower():
                    try:
                        # Try to extract JSON
                        json_match = re.search(r'\{.*\}', script.string, re.DOTALL)
                        if json_match:
                            json_data = json.loads(json_match.group())
                            if isinstance(json_data, dict):
                                data.update(json_data)
                    except:
                        pass
        
        return data if data.get("models") or data.get("benchmarks") else None
        
    except Exception as e:
        print(f"Error scraping website: {e}")
        return None

def main():
    print("Attempting to fetch data...")
    
    # Try API first
    print("\n=== Trying API ===")
    api_data = fetch_with_api()
    
    if api_data:
        print("\n=== API Data Retrieved ===")
        print(json.dumps(api_data, indent=2)[:1000])
        with open("api_data.json", "w") as f:
            json.dump(api_data, f, indent=2)
        return
    
    # Try scraping
    print("\n=== Trying Web Scraping ===")
    scraped_data = scrape_website()
    
    if scraped_data:
        print("\n=== Scraped Data Retrieved ===")
        print(json.dumps(scraped_data, indent=2)[:1000])
        with open("scraped_data.json", "w") as f:
            json.dump(scraped_data, f, indent=2)
    else:
        print("\n=== Creating Sample Structure ===")
        # Create a sample structure based on what the user described
        sample_data = create_sample_structure()
        with open("sample_data.json", "w") as f:
            json.dump(sample_data, f, indent=2)
        print("Created sample_data.json with expected structure")

def create_sample_structure():
    """Create a sample data structure based on user requirements"""
    return {
        "benchmarks": [
            {"id": "mmlu", "name": "MMLU", "description": "Massive Multitask Language Understanding"},
            {"id": "aalcr", "name": "AALCR", "description": "AALCR Benchmark"},
            {"id": "scicode", "name": "SciCode", "description": "Scientific Code Understanding"},
            {"id": "tau2-bench", "name": "τ²-Bench", "description": "Tau Squared Benchmark"},
            {"id": "telecom", "name": "Telecom", "description": "Telecom Benchmark"}
        ],
        "models": [
            {
                "id": "deepseek-v3.2",
                "name": "DeepSeek V3.2",
                "scores": {
                    "mmlu": 0.85,
                    "aalcr": 0.69,
                    "scicode": 0.42
                }
            }
        ]
    }

if __name__ == "__main__":
    main()




