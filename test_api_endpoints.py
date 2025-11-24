#!/usr/bin/env python3
"""
Test different API endpoint patterns to find the correct one
"""
import requests
import json

API_KEY = "aa_OXmwOTJvjVHpPnJQsOgimbFMwsPoVgOT"
BASE_URL = "https://api.artificialanalysis.ai"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "X-API-Key": API_KEY,
    "api-key": API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Test various endpoint patterns
endpoints_to_test = [
    # Models endpoints
    f"{BASE_URL}/v1/models",
    f"{BASE_URL}/models",
    f"{BASE_URL}/v1/llm/models",
    f"{BASE_URL}/llm/models",
    
    # Benchmarks endpoints
    f"{BASE_URL}/v1/benchmarks",
    f"{BASE_URL}/benchmarks",
    f"{BASE_URL}/v1/llm/benchmarks",
    f"{BASE_URL}/llm/benchmarks",
    
    # Evaluations endpoints
    f"{BASE_URL}/v1/evaluations",
    f"{BASE_URL}/evaluations",
    f"{BASE_URL}/v1/llm/evaluations",
    f"{BASE_URL}/llm/evaluations",
    
    # Intelligence endpoints
    f"{BASE_URL}/v1/intelligence",
    f"{BASE_URL}/intelligence",
    
    # Combined endpoints
    f"{BASE_URL}/v1/models/benchmarks",
    f"{BASE_URL}/v1/benchmarks/models",
]

print("Testing API endpoints...\n")

for endpoint in endpoints_to_test:
    try:
        response = requests.get(endpoint, headers=headers, timeout=10)
        print(f"{endpoint}: {response.status_code}")
        if response.status_code == 200:
            print(f"  ✓ SUCCESS!")
            try:
                data = response.json()
                print(f"  Response type: {type(data)}")
                if isinstance(data, dict):
                    print(f"  Keys: {list(data.keys())[:10]}")
                elif isinstance(data, list):
                    print(f"  List length: {len(data)}")
                print(f"  Sample: {str(data)[:200]}")
            except:
                print(f"  Response: {response.text[:200]}")
            print()
    except Exception as e:
        print(f"{endpoint}: Error - {e}\n")




