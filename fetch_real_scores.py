#!/usr/bin/env python3
"""
Fetch real benchmark scores for all models from artificialanalysis.ai API
"""
import requests
import json
import time
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

API_KEY = "aa_OXmwOTJvjVHpPnJQsOgimbFMwsPoVgOT"
BASE_URL = "https://api.artificialanalysis.ai"

# Benchmark IDs mapping
BENCHMARK_IDS = {
    "mmlu": "mmlu",
    "aalcr": "aalcr",
    "scicode": "scicode",
    "tau2-bench": "tau2-bench",
    "telecom": "telecom",
    "hellaswag": "hellaswag",
    "arc": "arc",
    "truthfulqa": "truthfulqa",
    "gsm8k": "gsm8k",
    "winogrande": "winogrande",
}

def fetch_model_benchmarks(model_id: str, model_name: str) -> Optional[Dict]:
    """Fetch benchmark scores for a specific model"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "X-API-Key": API_KEY,
        "api-key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Try multiple endpoint patterns
    endpoints = [
        f"{BASE_URL}/v1/models/{model_id}/benchmarks",
        f"{BASE_URL}/v1/models/{model_id}/scores",
        f"{BASE_URL}/v1/models/{model_id}/evaluations",
        f"{BASE_URL}/v1/benchmarks/{model_id}",
        f"{BASE_URL}/models/{model_id}/benchmarks",
        f"{BASE_URL}/v1/evaluations?model={model_id}",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # Process the response to extract scores
                scores = extract_scores_from_response(data)
                if scores:
                    return scores
        except Exception as e:
            continue
    
    return None

def extract_scores_from_response(data: any) -> Optional[Dict]:
    """Extract benchmark scores from API response"""
    scores = {}
    
    if isinstance(data, dict):
        # Try different response structures
        if 'scores' in data:
            scores_data = data['scores']
        elif 'benchmarks' in data:
            scores_data = data['benchmarks']
        elif 'evaluations' in data:
            scores_data = data['evaluations']
        elif 'results' in data:
            scores_data = data['results']
        else:
            scores_data = data
        
        if isinstance(scores_data, dict):
            for benchmark_id in BENCHMARK_IDS.values():
                # Try different key formats
                for key in [benchmark_id, benchmark_id.replace("-", "_"), benchmark_id.upper()]:
                    if key in scores_data:
                        value = scores_data[key]
                        if isinstance(value, (int, float)):
                            # Convert to 0-1 range if needed
                            score = value / 100.0 if value > 1 else value
                            scores[benchmark_id] = score
                        elif isinstance(value, dict) and 'score' in value:
                            score = value['score']
                            score = score / 100.0 if score > 1 else score
                            scores[benchmark_id] = score
        elif isinstance(scores_data, list):
            # List of benchmark results
            for item in scores_data:
                if isinstance(item, dict):
                    benchmark_id = item.get('benchmark_id') or item.get('benchmark') or item.get('name', '').lower()
                    score = item.get('score') or item.get('value')
                    if benchmark_id and score is not None:
                        benchmark_id = benchmark_id.lower().replace(" ", "-").replace("_", "-")
                        if benchmark_id in BENCHMARK_IDS.values():
                            score = score / 100.0 if score > 1 else score
                            scores[benchmark_id] = score
    
    return scores if scores else None

def fetch_all_benchmarks_batch() -> Optional[Dict]:
    """Try to fetch all benchmarks at once"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "X-API-Key": API_KEY,
        "api-key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    endpoints = [
        f"{BASE_URL}/v1/benchmarks/all",
        f"{BASE_URL}/v1/evaluations/all",
        f"{BASE_URL}/v1/models/all/benchmarks",
        f"{BASE_URL}/v1/benchmarks/results",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, headers=headers, timeout=30)
            if response.status_code == 200:
                return response.json()
        except:
            continue
    
    return None

def update_model_scores(models: List[Dict], max_workers: int = 10) -> List[Dict]:
    """Update scores for all models using parallel requests"""
    print(f"Fetching benchmark scores for {len(models)} models...")
    print("This may take a while...\n")
    
    # First, try to get all benchmarks at once
    print("Attempting to fetch all benchmarks at once...")
    all_benchmarks = fetch_all_benchmarks_batch()
    
    if all_benchmarks:
        print("✓ Successfully fetched all benchmarks!")
        # Process the batch response
        return process_batch_response(models, all_benchmarks)
    
    print("Batch fetch failed. Fetching individual model scores...")
    
    updated_models = []
    successful = 0
    failed = 0
    
    # Use thread pool for parallel requests
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_model = {
            executor.submit(fetch_model_benchmarks, model["id"], model["name"]): model
            for model in models
        }
        
        for future in as_completed(future_to_model):
            model = future_to_model[future]
            try:
                scores = future.result()
                if scores:
                    model["scores"] = scores
                    successful += 1
                    if successful % 10 == 0:
                        print(f"  ✓ Fetched scores for {successful} models...")
                else:
                    failed += 1
            except Exception as e:
                failed += 1
            
            updated_models.append(model)
            time.sleep(0.1)  # Rate limiting
    
    print(f"\n✓ Successfully fetched scores for {successful} models")
    print(f"⚠ Could not fetch scores for {failed} models (will use generated scores)")
    
    return updated_models

def process_batch_response(models: List[Dict], batch_data: Dict) -> List[Dict]:
    """Process batch response and match to models"""
    # This will need to be adjusted based on actual API response structure
    model_scores_map = {}
    
    if isinstance(batch_data, dict):
        if 'models' in batch_data:
            for model_data in batch_data['models']:
                model_id = model_data.get('id') or model_data.get('model_id')
                scores = extract_scores_from_response(model_data)
                if model_id and scores:
                    model_scores_map[model_id] = scores
        elif 'results' in batch_data:
            for result in batch_data['results']:
                model_id = result.get('model_id') or result.get('model')
                scores = extract_scores_from_response(result)
                if model_id and scores:
                    model_scores_map[model_id] = scores
    
    # Update models with fetched scores
    for model in models:
        model_id = model["id"]
        if model_id in model_scores_map:
            model["scores"] = model_scores_map[model_id]
    
    return models

def main():
    # Load existing data
    print("Loading existing models data...")
    with open("evaluations_data.json", "r") as f:
        data = json.load(f)
    
    models = data.get("models", [])
    benchmarks = data.get("benchmarks", [])
    
    print(f"Found {len(models)} models and {len(benchmarks)} benchmarks\n")
    
    # Update scores
    updated_models = update_model_scores(models, max_workers=5)
    
    # Save updated data
    data["models"] = updated_models
    
    with open("evaluations_data.json", "w") as f:
        json.dump(data, f, indent=2)
    
    # Count models with scores
    models_with_scores = sum(1 for m in updated_models if m.get("scores"))
    print(f"\n✓ Updated evaluations_data.json")
    print(f"✓ {models_with_scores} models have benchmark scores")
    print(f"✓ {len(updated_models) - models_with_scores} models need scores (using generated)")
    
    # Show sample
    print("\n=== Sample Models with Scores ===")
    for model in updated_models[:5]:
        if model.get("scores"):
            print(f"\n{model['name']}:")
            for benchmark, score in list(model["scores"].items())[:3]:
                print(f"  {benchmark}: {score:.2%}")

if __name__ == "__main__":
    main()




