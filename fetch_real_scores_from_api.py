#!/usr/bin/env python3
"""
Fetch REAL benchmark scores from artificialanalysis.ai API v2
Based on official API documentation: https://artificialanalysis.ai/documentation
"""
import requests
import json
import csv
import time
from typing import Dict, List, Optional

API_KEY = "aa_OXmwOTJvjVHpPnJQsOgimbFMwsPoVgOT"
BASE_URL = "https://artificialanalysis.ai/api/v2"

# All benchmarks available in the API
BENCHMARKS = [
    {"id": "artificial_analysis_intelligence_index", "name": "Intelligence Index", "api_key": "artificial_analysis_intelligence_index"},
    {"id": "artificial_analysis_coding_index", "name": "Coding Index", "api_key": "artificial_analysis_coding_index"},
    {"id": "artificial_analysis_math_index", "name": "Math Index", "api_key": "artificial_analysis_math_index"},
    {"id": "mmlu_pro", "name": "MMLU-Pro", "api_key": "mmlu_pro"},
    {"id": "gpqa", "name": "GPQA", "api_key": "gpqa"},
    {"id": "hle", "name": "HLE", "api_key": "hle"},
    {"id": "livecodebench", "name": "LiveCodeBench", "api_key": "livecodebench"},
    {"id": "scicode", "name": "SciCode", "api_key": "scicode"},
    {"id": "math_500", "name": "Math 500", "api_key": "math_500"},
    {"id": "aime", "name": "AIME", "api_key": "aime"},
    # Additional benchmarks that might be in the data
    {"id": "aa-lcr", "name": "AA-LCR", "api_key": "lcr"},  # Long Context Reasoning (API uses "lcr")
    {"id": "tau2", "name": "τ²-Bench", "api_key": "tau2"},  # API uses "tau2"
    {"id": "mmlu", "name": "MMLU", "api_key": "mmlu"},
    {"id": "aalcr", "name": "AALCR", "api_key": "aalcr"},
    {"id": "tau2-bench", "name": "τ²-Bench", "api_key": "tau2_bench"},
    {"id": "telecom", "name": "Telecom", "api_key": "telecom"},
    {"id": "hellaswag", "name": "HellaSwag", "api_key": "hellaswag"},
    {"id": "arc", "name": "ARC", "api_key": "arc"},
    {"id": "truthfulqa", "name": "TruthfulQA", "api_key": "truthfulqa"},
    {"id": "gsm8k", "name": "GSM8K", "api_key": "gsm8k"},
    {"id": "winogrande", "name": "Winogrande", "api_key": "winogrande"},
]

def get_headers():
    """Get API headers according to documentation"""
    return {
        "x-api-key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

def fetch_all_models() -> Optional[List[Dict]]:
    """Fetch all LLM models from the API"""
    headers = get_headers()
    endpoint = f"{BASE_URL}/data/llms/models"
    
    try:
        print(f"Fetching models from {endpoint}...")
        response = requests.get(endpoint, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and "data" in data:
                models = data["data"]
                print(f"✓ Successfully fetched {len(models)} models from API")
                return models
            else:
                print(f"Unexpected response structure: {type(data)}")
                return None
        elif response.status_code == 401:
            print("✗ Authentication failed. Please check your API key.")
            return None
        elif response.status_code == 429:
            print("✗ Rate limit exceeded. Please wait before trying again.")
            return None
        else:
            print(f"✗ Error: Status code {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return None
    except Exception as e:
        print(f"✗ Error fetching models: {e}")
        return None

def extract_benchmark_scores(model_data: Dict) -> Dict[str, float]:
    """Extract benchmark scores from model data"""
    scores = {}
    
    evaluations = model_data.get("evaluations", {})
    if not evaluations:
        return scores
    
    # Extract scores for each benchmark
    for benchmark in BENCHMARKS:
        api_key = benchmark["api_key"]
        
        # Try the API key directly
        if api_key in evaluations:
            value = evaluations[api_key]
            if value is not None:
                # Values are already in 0-1 range or percentage
                if isinstance(value, (int, float)):
                    # If value > 1, it's likely a percentage, convert to decimal
                    score = value / 100.0 if value > 1 else value
                    scores[benchmark["id"]] = score
        
        # Also try variations
        for key_variant in [api_key.replace("_", "-"), api_key.upper(), api_key.lower()]:
            if key_variant in evaluations:
                value = evaluations[key_variant]
                if value is not None and isinstance(value, (int, float)):
                    score = value / 100.0 if value > 1 else value
                    scores[benchmark["id"]] = score
                    break
    
    return scores

def process_models(api_models: List[Dict]) -> List[Dict]:
    """Process API models into our format"""
    processed_models = []
    
    for model in api_models:
        model_id = model.get("id", "")
        name = model.get("name", "")
        creator = model.get("model_creator", {})
        provider = creator.get("name", "Unknown")
        
        # Extract scores
        scores = extract_benchmark_scores(model)
        
        # Create model entry
        processed_model = {
            "id": model_id,
            "name": name,
            "provider": provider,
            "dataset": f"{provider} training dataset",  # Default, can be updated
            "scores": scores,
            "api_data": {
                "slug": model.get("slug", ""),
                "creator_id": creator.get("id", ""),
            }
        }
        
        processed_models.append(processed_model)
    
    return processed_models

def export_to_csv(models: List[Dict], filename: str = "model_benchmarks_real.csv"):
    """Export models with real scores to CSV"""
    print(f"\nExporting to {filename}...")
    
    # Prepare CSV headers - prioritize important benchmarks
    headers = ["Model Name", "Provider", "Dataset"]
    
    # Add benchmarks in order of importance
    priority_benchmarks = [
        "mmlu_pro", "aa-lcr", "artificial_analysis_intelligence_index",
        "artificial_analysis_coding_index", "artificial_analysis_math_index",
        "scicode", "mmlu", "aalcr", "tau2-bench", "telecom",
        "hellaswag", "arc", "truthfulqa", "gsm8k", "winogrande",
        "gpqa", "hle", "livecodebench", "math_500", "aime"
    ]
    
    # Get benchmark names in order
    benchmark_map = {b["id"]: b["name"] for b in BENCHMARKS}
    for bench_id in priority_benchmarks:
        if bench_id in benchmark_map:
            headers.append(benchmark_map[bench_id])
    
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
            
            # Add scores for each benchmark in header order
            scores = model.get("scores", {})
            for bench_id in priority_benchmarks:
                if bench_id in benchmark_map:
                    score = scores.get(bench_id)
                    if score is not None:
                        # Format as percentage
                        row.append(f"{score * 100:.2f}%")
                    else:
                        row.append("N/A")
            
            writer.writerow(row)
    
    print(f"✓ Exported {len(models)} models to {filename}")

def main():
    print("=" * 60)
    print("Fetching REAL Benchmark Scores from API v2")
    print("=" * 60)
    print(f"API Documentation: https://artificialanalysis.ai/documentation")
    print()
    
    # Fetch all models from API
    api_models = fetch_all_models()
    
    if not api_models:
        print("\n⚠ Could not fetch models from API")
        print("Loading from existing evaluations_data.json as fallback...")
        with open("evaluations_data.json", "r") as f:
            data = json.load(f)
        models = data.get("models", [])
    else:
        # Process API models
        print(f"\nProcessing {len(api_models)} models...")
        models = process_models(api_models)
        
        # Count models with scores
        models_with_scores = sum(1 for m in models if m.get("scores"))
        models_with_mmlu_pro = sum(1 for m in models if m.get("scores", {}).get("mmlu_pro") is not None)
        
        print(f"✓ Processed {len(models)} models")
        print(f"✓ {models_with_scores} models have benchmark scores")
        print(f"✓ {models_with_mmlu_pro} models have MMLU-Pro scores")
        
        # Show sample
        print("\n=== Sample Models with Real Scores ===")
        for model in models[:5]:
            if model.get("scores"):
                print(f"\n{model['name']} ({model['provider']}):")
                scores = model["scores"]
                if "mmlu_pro" in scores:
                    print(f"  MMLU-Pro: {scores['mmlu_pro']*100:.1f}%")
                if "artificial_analysis_intelligence_index" in scores:
                    print(f"  Intelligence Index: {scores['artificial_analysis_intelligence_index']:.1f}")
                if "aa-lcr" in scores or "aa_lcr" in scores:
                    aa_lcr = scores.get("aa-lcr") or scores.get("aa_lcr")
                    if aa_lcr:
                        print(f"  AA-LCR: {aa_lcr*100:.1f}%")
    
    # Export to CSV
    export_to_csv(models, "model_benchmarks_real.csv")
    
    # Save updated JSON
    data = {
        "benchmarks": BENCHMARKS,
        "models": models
    }
    
    with open("evaluations_data.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✓ Saved updated data to evaluations_data.json")
    print(f"\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Total models: {len(models)}")
    print(f"CSV file: model_benchmarks_real.csv")
    print(f"JSON file: evaluations_data.json")

if __name__ == "__main__":
    main()

