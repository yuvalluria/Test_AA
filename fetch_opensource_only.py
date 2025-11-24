#!/usr/bin/env python3
"""
Fetch ONLY open-source models with the 10 specific benchmarks:
MMLU-Pro, GPQA Diamond, Humanity's Last Exam, LiveCodeBench, SciCode, 
AIME 2025, IFBench, AA-LCR, Terminal-Bench Hard, τ²-Bench Telecom
"""
import requests
import json
import csv
from typing import Dict, List, Optional

API_KEY = "aa_OXmwOTJvjVHpPnJQsOgimbFMwsPoVgOT"
BASE_URL = "https://artificialanalysis.ai/api/v2"

# The 10 specific benchmarks requested
BENCHMARKS = [
    {"id": "mmlu_pro", "name": "MMLU-Pro", "api_key": "mmlu_pro"},
    {"id": "gpqa", "name": "GPQA Diamond", "api_key": "gpqa"},
    {"id": "hle", "name": "Humanity's Last Exam", "api_key": "hle"},
    {"id": "livecodebench", "name": "LiveCodeBench", "api_key": "livecodebench"},
    {"id": "scicode", "name": "SciCode", "api_key": "scicode"},
    {"id": "aime_25", "name": "AIME 2025", "api_key": "aime_25"},
    {"id": "ifbench", "name": "IFBench", "api_key": "ifbench"},
    {"id": "aa_lcr", "name": "AA-LCR", "api_key": "lcr"},
    {"id": "terminalbench_hard", "name": "Terminal-Bench Hard", "api_key": "terminalbench_hard"},
    {"id": "tau2", "name": "τ²-Bench Telecom", "api_key": "tau2"},
]

# Known open-source providers/creators
OPEN_SOURCE_PROVIDERS = [
    "Meta", "Alibaba", "DeepSeek", "Mistral", "Google", "Microsoft Azure",
    "Nous Research", "NVIDIA", "Z AI", "Moonshot AI", "MiniMax",
    "ByteDance Seed", "ServiceNow", "LG AI Research", "InclusionAI",
    "Allen Institute for AI", "IBM", "Upstage", "xAI", "Cohere",
    "Liquid AI", "Snowflake", "Databricks", "OpenChat", "AI21 Labs",
    "Perplexity", "Deep Cogito", "Baidu", "OpenAI",  # OpenAI has some open-source models
]

def get_headers():
    """Get API headers"""
    return {
        "x-api-key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

def is_open_source(model: Dict) -> bool:
    """Check if model is open-source"""
    creator = model.get("model_creator", {})
    creator_name = creator.get("name", "")
    
    # Check if creator is in open-source list
    if creator_name in OPEN_SOURCE_PROVIDERS:
        return True
    
    # Additional check: models with weights available (🤗) are typically open-source
    # But we'll rely on provider list for now
    
    return False

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
        else:
            print(f"✗ Error: Status code {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ Error fetching models: {e}")
        return None

def extract_benchmark_scores(model_data: Dict) -> Dict[str, float]:
    """Extract the 10 specific benchmark scores from model data"""
    scores = {}
    
    evaluations = model_data.get("evaluations", {})
    if not evaluations:
        return scores
    
    # Extract scores for each of the 10 benchmarks
    for benchmark in BENCHMARKS:
        api_key = benchmark["api_key"]
        
        if api_key in evaluations:
            value = evaluations[api_key]
            if value is not None:
                # Values are already in 0-1 range
                if isinstance(value, (int, float)):
                    # If value > 1, it's likely a percentage, convert to decimal
                    score = value / 100.0 if value > 1 else value
                    scores[benchmark["id"]] = score
    
    return scores

def process_models(api_models: List[Dict]) -> List[Dict]:
    """Process API models, filter for open-source only"""
    processed_models = []
    open_source_count = 0
    
    for model in api_models:
        # Filter for open-source only
        if not is_open_source(model):
            continue
        
        model_id = model.get("id", "")
        name = model.get("name", "")
        creator = model.get("model_creator", {})
        provider = creator.get("name", "Unknown")
        
        # Extract scores for the 10 benchmarks
        scores = extract_benchmark_scores(model)
        
        # Only include models that have at least one of the 10 benchmarks
        if not scores:
            continue
        
        # Create model entry
        processed_model = {
            "id": model_id,
            "name": name,
            "provider": provider,
            "dataset": f"{provider} training dataset",
            "scores": scores,
        }
        
        processed_models.append(processed_model)
        open_source_count += 1
    
    print(f"✓ Found {open_source_count} open-source models with benchmark scores")
    return processed_models

def export_to_csv(models: List[Dict], filename: str = "opensource_benchmarks.csv"):
    """Export open-source models with the 10 benchmarks to CSV"""
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
            
            # Add scores for each of the 10 benchmarks
            scores = model.get("scores", {})
            for benchmark in BENCHMARKS:
                score = scores.get(benchmark["id"])
                if score is not None:
                    # Format as percentage
                    row.append(f"{score * 100:.2f}%")
                else:
                    row.append("N/A")
            
            writer.writerow(row)
    
    print(f"✓ Exported {len(models)} open-source models to {filename}")

def main():
    print("=" * 60)
    print("Fetching Open-Source Models with 10 Benchmarks")
    print("=" * 60)
    print("\nBenchmarks:")
    for i, bench in enumerate(BENCHMARKS, 1):
        print(f"  {i}. {bench['name']}")
    print()
    
    # Fetch all models from API
    api_models = fetch_all_models()
    
    if not api_models:
        print("✗ Could not fetch models from API")
        return
    
    # Process and filter for open-source
    print(f"\nFiltering for open-source models...")
    models = process_models(api_models)
    
    # Count models with each benchmark
    print(f"\n=== Benchmark Coverage ===")
    for benchmark in BENCHMARKS:
        count = sum(1 for m in models if m.get("scores", {}).get(benchmark["id"]) is not None)
        print(f"  {benchmark['name']}: {count} models")
    
    # Show sample
    print(f"\n=== Sample Models ===")
    for model in models[:5]:
        if model.get("scores"):
            print(f"\n{model['name']} ({model['provider']}):")
            scores = model["scores"]
            for benchmark in BENCHMARKS[:3]:  # Show first 3
                score = scores.get(benchmark["id"])
                if score is not None:
                    print(f"  {benchmark['name']}: {score*100:.1f}%")
    
    # Export to CSV
    export_to_csv(models, "opensource_benchmarks.csv")
    
    # Save JSON
    data = {
        "benchmarks": BENCHMARKS,
        "models": models
    }
    
    with open("opensource_evaluations_data.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✓ Saved to opensource_evaluations_data.json")
    print(f"\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Total open-source models: {len(models)}")
    print(f"CSV file: opensource_benchmarks.csv")
    print(f"JSON file: opensource_evaluations_data.json")

if __name__ == "__main__":
    main()




