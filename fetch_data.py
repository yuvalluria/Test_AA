#!/usr/bin/env python3
"""
Script to fetch intelligence evaluation data from artificialanalysis.ai API
"""
import requests
import json
from typing import Dict, List, Any

API_KEY = "aa_OXmwOTJvjVHpPnJQsOgimbFMwsPoVgOT"
BASE_URL = "https://api.artificialanalysis.ai"

def fetch_models():
    """Fetch list of open source models"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/v1/models", headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching models: {e}")
        return None

def fetch_model_evaluations(model_id: str):
    """Fetch evaluations for a specific model"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/v1/models/{model_id}/evaluations", headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching evaluations for {model_id}: {e}")
        return None

def fetch_all_evaluations():
    """Fetch all evaluations"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        # Try different possible endpoints
        endpoints = [
            "/v1/evaluations",
            "/v1/benchmarks",
            "/v1/models/open-source",
            "/v1/benchmarks/results"
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
                if response.status_code == 200:
                    return response.json()
            except:
                continue
        
        # If direct endpoints don't work, try to get models first
        models = fetch_models()
        if models:
            all_data = {"models": models}
            return all_data
            
    except Exception as e:
        print(f"Error fetching evaluations: {e}")
        return None

def main():
    print("Fetching data from artificialanalysis.ai API...")
    
    # Try to fetch all evaluations
    data = fetch_all_evaluations()
    
    if data:
        print("\n=== API Response ===")
        print(json.dumps(data, indent=2))
        
        # Save to file
        with open("api_data.json", "w") as f:
            json.dump(data, f, indent=2)
        print("\nData saved to api_data.json")
    else:
        print("Failed to fetch data. Trying alternative approach...")
        
        # Try fetching models list
        models = fetch_models()
        if models:
            print("\n=== Models ===")
            print(json.dumps(models, indent=2))
            with open("models.json", "w") as f:
                json.dump(models, f, indent=2)

if __name__ == "__main__":
    main()




