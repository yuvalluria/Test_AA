#!/usr/bin/env python3
"""
Fetch all models and their benchmark scores from artificialanalysis.ai API
and export to CSV format
"""
import requests
import json
import csv
import time
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

API_KEY = "aa_OXmwOTJvjVHpPnJQsOgimbFMwsPoVgOT"
BASE_URL = "https://api.artificialanalysis.ai"

# All 10 benchmarks
BENCHMARKS = [
    {"id": "mmlu", "name": "MMLU"},
    {"id": "aalcr", "name": "AALCR"},
    {"id": "scicode", "name": "SciCode"},
    {"id": "tau2-bench", "name": "τ²-Bench"},
    {"id": "telecom", "name": "Telecom"},
    {"id": "hellaswag", "name": "HellaSwag"},
    {"id": "arc", "name": "ARC"},
    {"id": "truthfulqa", "name": "TruthfulQA"},
    {"id": "gsm8k", "name": "GSM8K"},
    {"id": "winogrande", "name": "Winogrande"},
]

def get_headers():
    """Get API headers"""
    return {
        "Authorization": f"Bearer {API_KEY}",
        "X-API-Key": API_KEY,
        "api-key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

def fetch_all_models() -> Optional[List[Dict]]:
    """Fetch all open-source models"""
    headers = get_headers()
    
    endpoints = [
        f"{BASE_URL}/v1/models",
        f"{BASE_URL}/v1/models/open-source",
        f"{BASE_URL}/models",
        f"{BASE_URL}/open-source/models",
    ]
    
    for endpoint in endpoints:
        try:
            print(f"Trying endpoint: {endpoint}")
            response = requests.get(endpoint, headers=headers, timeout=30)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Handle different response formats
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    if 'models' in data:
                        return data['models']
                    elif 'data' in data:
                        return data['data']
                    elif 'results' in data:
                        return data['results']
        except Exception as e:
            print(f"Error with {endpoint}: {e}")
            continue
    
    return None

def fetch_model_evaluations(model_id: str) -> Optional[Dict]:
    """Fetch evaluations/benchmarks for a specific model"""
    headers = get_headers()
    
    endpoints = [
        f"{BASE_URL}/v1/models/{model_id}/evaluations",
        f"{BASE_URL}/v1/models/{model_id}/benchmarks",
        f"{BASE_URL}/v1/models/{model_id}/scores",
        f"{BASE_URL}/v1/evaluations?model_id={model_id}",
        f"{BASE_URL}/v1/benchmarks?model_id={model_id}",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
        except:
            continue
    
    return None

def extract_benchmark_scores(evaluation_data: any) -> Dict[str, float]:
    """Extract benchmark scores from evaluation data"""
    scores = {}
    
    if not evaluation_data:
        return scores
    
    # Handle different response structures
    if isinstance(evaluation_data, dict):
        # Try to find scores in various locations
        data_sources = [
            evaluation_data.get('scores', {}),
            evaluation_data.get('benchmarks', {}),
            evaluation_data.get('evaluations', {}),
            evaluation_data.get('results', {}),
            evaluation_data,
        ]
        
        for data_source in data_sources:
            if isinstance(data_source, dict):
                for benchmark in BENCHMARKS:
                    benchmark_id = benchmark["id"]
                    # Try different key formats
                    for key in [benchmark_id, benchmark_id.replace("-", "_"), benchmark_id.upper(), benchmark["name"].lower()]:
                        if key in data_source:
                            value = data_source[key]
                            if isinstance(value, (int, float)):
                                # Normalize to 0-1 range
                                score = value / 100.0 if value > 1 else value
                                scores[benchmark_id] = score
                                break
                            elif isinstance(value, dict):
                                score = value.get('score') or value.get('value')
                                if score is not None:
                                    score = score / 100.0 if score > 1 else score
                                    scores[benchmark_id] = score
                                    break
        
        # Also check for list of evaluations
        if 'evaluations' in evaluation_data and isinstance(evaluation_data['evaluations'], list):
            for eval_item in evaluation_data['evaluations']:
                if isinstance(eval_item, dict):
                    benchmark_id = eval_item.get('benchmark_id') or eval_item.get('benchmark', {}).get('id', '').lower()
                    score = eval_item.get('score') or eval_item.get('value')
                    if benchmark_id and score is not None:
                        benchmark_id = benchmark_id.replace(" ", "-").replace("_", "-")
                        if benchmark_id in [b["id"] for b in BENCHMARKS]:
                            score = score / 100.0 if score > 1 else score
                            scores[benchmark_id] = score
    
    elif isinstance(evaluation_data, list):
        # List of evaluation results
        for item in evaluation_data:
            if isinstance(item, dict):
                benchmark_id = item.get('benchmark_id') or item.get('benchmark', {}).get('id', '').lower()
                score = item.get('score') or item.get('value')
                if benchmark_id and score is not None:
                    benchmark_id = benchmark_id.replace(" ", "-").replace("_", "-")
                    if benchmark_id in [b["id"] for b in BENCHMARKS]:
                        score = score / 100.0 if score > 1 else score
                        scores[benchmark_id] = score
    
    return scores

def fetch_all_benchmarks_batch() -> Optional[Dict]:
    """Try to fetch all benchmarks at once"""
    headers = get_headers()
    
    endpoints = [
        f"{BASE_URL}/v1/benchmarks/all",
        f"{BASE_URL}/v1/evaluations/all",
        f"{BASE_URL}/v1/models/all/benchmarks",
        f"{BASE_URL}/v1/benchmarks/results",
        f"{BASE_URL}/v1/evaluations",
    ]
    
    for endpoint in endpoints:
        try:
            print(f"Trying batch endpoint: {endpoint}")
            response = requests.get(endpoint, headers=headers, timeout=30)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error: {e}")
            continue
    
    return None

def process_models_with_scores(models: List[Dict], max_workers: int = 5) -> List[Dict]:
    """Fetch scores for all models"""
    print(f"\nFetching benchmark scores for {len(models)} models...")
    print("This may take several minutes...\n")
    
    # First try batch fetch
    print("Attempting batch fetch...")
    batch_data = fetch_all_benchmarks_batch()
    
    if batch_data:
        print("✓ Batch fetch successful! Processing...")
        return process_batch_data(models, batch_data)
    
    print("Batch fetch not available. Fetching individual model scores...")
    
    results = []
    successful = 0
    failed = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_model = {
            executor.submit(fetch_model_evaluations, model.get("id") or model.get("model_id") or model.get("name", "").lower().replace(" ", "-")): model
            for model in models
        }
        
        for future in as_completed(future_to_model):
            model = future_to_model[future]
            try:
                eval_data = future.result()
                scores = extract_benchmark_scores(eval_data)
                
                if scores:
                    model["scores"] = scores
                    successful += 1
                    if successful % 10 == 0:
                        print(f"  ✓ Fetched {successful} models...")
                else:
                    failed += 1
            except Exception as e:
                failed += 1
            
            results.append(model)
            time.sleep(0.2)  # Rate limiting
    
    print(f"\n✓ Successfully fetched scores for {successful} models")
    print(f"⚠ Could not fetch scores for {failed} models")
    
    return results

def process_batch_data(models: List[Dict], batch_data: Dict) -> List[Dict]:
    """Process batch response"""
    model_scores_map = {}
    
    # Try to extract model-score mappings from batch data
    if isinstance(batch_data, dict):
        if 'models' in batch_data:
            for model_data in batch_data['models']:
                model_id = model_data.get('id') or model_data.get('model_id')
                scores = extract_benchmark_scores(model_data)
                if model_id and scores:
                    model_scores_map[model_id] = scores
        elif 'results' in batch_data:
            for result in batch_data['results']:
                model_id = result.get('model_id') or result.get('model', {}).get('id')
                scores = extract_benchmark_scores(result)
                if model_id and scores:
                    model_scores_map[model_id] = scores
        elif 'evaluations' in batch_data:
            # Group by model
            for eval_item in batch_data['evaluations']:
                model_id = eval_item.get('model_id') or eval_item.get('model', {}).get('id')
                if model_id:
                    if model_id not in model_scores_map:
                        model_scores_map[model_id] = {}
                    benchmark_id = eval_item.get('benchmark_id') or eval_item.get('benchmark', {}).get('id', '').lower()
                    score = eval_item.get('score') or eval_item.get('value')
                    if benchmark_id and score is not None:
                        benchmark_id = benchmark_id.replace(" ", "-").replace("_", "-")
                        score = score / 100.0 if score > 1 else score
                        model_scores_map[model_id][benchmark_id] = score
    
    # Update models
    for model in models:
        model_id = model.get("id") or model.get("model_id") or model.get("name", "").lower().replace(" ", "-")
        if model_id in model_scores_map:
            model["scores"] = model_scores_map[model_id]
    
    return models

def export_to_csv(models: List[Dict], filename: str = "model_benchmarks.csv"):
    """Export models and scores to CSV"""
    print(f"\nExporting to {filename}...")
    
    # Prepare CSV headers
    headers = ["Model Name", "Provider", "Dataset"]
    headers.extend([benchmark["name"] for benchmark in BENCHMARKS])
    
    # Write CSV
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        
        for model in models:
            row = [
                model.get("name", ""),
                model.get("provider", ""),
                model.get("dataset", ""),
            ]
            
            # Add scores for each benchmark
            scores = model.get("scores", {})
            for benchmark in BENCHMARKS:
                score = scores.get(benchmark["id"])
                if score is not None:
                    # Format as percentage
                    row.append(f"{score * 100:.2f}%")
                else:
                    row.append("N/A")
            
            writer.writerow(row)
    
    print(f"✓ Exported {len(models)} models to {filename}")

def main():
    print("=" * 60)
    print("Fetching All Models and Benchmark Scores")
    print("=" * 60)
    
    # Step 1: Fetch all models
    print("\nStep 1: Fetching all models...")
    models = fetch_all_models()
    
    if not models:
        print("⚠ Could not fetch models from API")
        print("Loading from existing evaluations_data.json...")
        with open("evaluations_data.json", "r") as f:
            data = json.load(f)
        models = data.get("models", [])
    
    print(f"✓ Found {len(models)} models")
    
    # Step 2: Fetch benchmark scores
    models_with_scores = process_models_with_scores(models)
    
    # Step 3: Export to CSV
    export_to_csv(models_with_scores, "model_benchmarks.csv")
    
    # Also save updated JSON
    data = {
        "benchmarks": BENCHMARKS,
        "models": models_with_scores
    }
    
    with open("evaluations_data.json", "w") as f:
        json.dump(data, f, indent=2)
    
    # Summary
    models_with_all_scores = sum(1 for m in models_with_scores if m.get("scores") and len(m.get("scores", {})) == len(BENCHMARKS))
    models_with_some_scores = sum(1 for m in models_with_scores if m.get("scores") and len(m.get("scores", {})) > 0)
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Total models: {len(models_with_scores)}")
    print(f"Models with all 10 benchmarks: {models_with_all_scores}")
    print(f"Models with some benchmarks: {models_with_some_scores}")
    print(f"Models with no benchmarks: {len(models_with_scores) - models_with_some_scores}")
    print(f"\n✓ CSV file: model_benchmarks.csv")
    print(f"✓ JSON file: evaluations_data.json")

if __name__ == "__main__":
    main()




