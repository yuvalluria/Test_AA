#!/usr/bin/env python3
"""
Selenium-based scraper for JavaScript-rendered pages
Requires: pip install selenium
"""
import json
import time
from typing import Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def scrape_with_selenium():
    """Scrape using Selenium for JavaScript-rendered content"""
    url = "https://artificialanalysis.ai/models/open-source"
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
    
    driver = None
    try:
        print("Starting Selenium WebDriver...")
        driver = webdriver.Chrome(options=chrome_options)
        
        print(f"Loading {url}...")
        driver.get(url)
        
        # Wait for page to load
        print("Waiting for page to load...")
        time.sleep(5)
        
        # Try to find and extract data
        data = extract_data_from_page(driver)
        
        return data
        
    except Exception as e:
        print(f"Error with Selenium: {e}")
        print("\nNote: Selenium requires ChromeDriver.")
        print("Install it with: brew install chromedriver (macOS)")
        print("Or download from: https://chromedriver.chromium.org/")
        return None
    finally:
        if driver:
            driver.quit()

def extract_data_from_page(driver) -> Optional[Dict]:
    """Extract data from the loaded page"""
    data = {
        "benchmarks": [],
        "models": []
    }
    
    try:
        # Try to get data from window object
        json_data = driver.execute_script("""
            if (window.__NEXT_DATA__) return window.__NEXT_DATA__;
            if (window.__INITIAL_STATE__) return window.__INITIAL_STATE__;
            if (window.modelsData) return window.modelsData;
            return null;
        """)
        
        if json_data:
            return process_json_data(json_data)
        
        # Try to extract from table
        try:
            table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "table"))
            )
            return extract_from_table(driver, table)
        except:
            pass
        
        # Try to find any data containers
        containers = driver.find_elements(By.CSS_SELECTOR, "[data-models], [data-benchmarks], .model-list, .benchmark-list")
        if containers:
            return extract_from_containers(driver, containers)
        
    except Exception as e:
        print(f"Error extracting data: {e}")
    
    return None

def process_json_data(json_data: Dict) -> Optional[Dict]:
    """Process JSON data from page"""
    # This will need to be adjusted based on actual data structure
    if isinstance(json_data, dict):
        if 'props' in json_data:
            json_data = json_data['props']
        if 'pageProps' in json_data:
            json_data = json_data['pageProps']
        
        models = json_data.get('models') or json_data.get('data', {}).get('models', [])
        benchmarks = json_data.get('benchmarks') or json_data.get('data', {}).get('benchmarks', [])
        
        if models or benchmarks:
            return {
                "benchmarks": benchmarks or [],
                "models": models or []
            }
    
    return None

def extract_from_table(driver, table) -> Optional[Dict]:
    """Extract data from HTML table"""
    data = {
        "benchmarks": [],
        "models": []
    }
    
    # Get headers
    headers = table.find_elements(By.TAG_NAME, "th")
    benchmark_names = [h.text.strip() for h in headers[1:] if h.text.strip() and h.text.lower() not in ['model', 'name']]
    
    for name in benchmark_names:
        benchmark_id = name.lower().replace(' ', '-').replace('²', '2').replace('τ', 'tau')
        data["benchmarks"].append({
            "id": benchmark_id,
            "name": name,
            "full_name": name
        })
    
    # Get rows
    rows = table.find_elements(By.TAG_NAME, "tr")[1:]
    
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) < 2:
            continue
        
        model_name = cells[0].text.strip()
        if not model_name:
            continue
        
        model_data = {
            "id": model_name.lower().replace(' ', '-').replace('.', '-'),
            "name": model_name,
            "provider": "",
            "scores": {}
        }
        
        for i, cell in enumerate(cells[1:], 1):
            if i <= len(benchmark_names):
                score_text = cell.text.strip()
                score = parse_score(score_text)
                if score is not None:
                    benchmark_id = data["benchmarks"][i-1]["id"]
                    model_data["scores"][benchmark_id] = score
        
        if model_data["scores"]:
            data["models"].append(model_data)
    
    return data if data["models"] else None

def extract_from_containers(driver, containers) -> Optional[Dict]:
    """Extract data from data containers"""
    # Implementation depends on actual page structure
    return None

def parse_score(text: str) -> Optional[float]:
    """Parse score from text"""
    import re
    if not text or text.lower() in ['n/a', 'na', '-', '']:
        return None
    
    text = text.replace('%', '').strip()
    match = re.search(r'(\d+\.?\d*)', text)
    if match:
        value = float(match.group(1))
        if value > 1:
            return value / 100
        return value
    
    return None

def main():
    print("=" * 60)
    print("Selenium Scraper for Artificial Analysis")
    print("=" * 60)
    
    try:
        data = scrape_with_selenium()
        
        if data and data.get('models'):
            print(f"\n✓ Successfully scraped data for {len(data['models'])} models")
            print(f"✓ Found {len(data.get('benchmarks', []))} benchmarks")
            
            with open("evaluations_data.json", "w") as f:
                json.dump(data, f, indent=2)
            
            print("\n✓ Data saved to evaluations_data.json")
        else:
            print("\n⚠ Could not extract data")
            print("The page structure may be different than expected")
    except ImportError:
        print("\n⚠ Selenium not installed")
        print("Install with: pip install selenium")
        print("Also install ChromeDriver: brew install chromedriver")

if __name__ == "__main__":
    main()




