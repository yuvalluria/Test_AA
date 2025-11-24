#!/usr/bin/env python3
"""
Fetch ALL open-source models with ALL datasets from artificialanalysis.ai API
Filters out closed models like Grok 2, 3
"""
import requests
import json
import csv
import time
from typing import Dict, List, Optional, Set

API_KEY = "aa_YLuwDNXOuuOLlROWDUAppHESYUYNQAwP"
BASE_URL = "https://artificialanalysis.ai/api/v2"

# Closed/proprietary models to exclude
CLOSED_MODELS = [
    "grok 2", "grok-2", "grok2",
    "grok 3", "grok-3", "grok3",
    "gpt-4", "gpt-3.5", "gpt-5",
    "o1", "o1-mini", "o1-pro", "o3", "o3-mini", "o3-pro", "o4",
    "gemini", "claude", "sonnet",
]

# Open-source providers
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

def is_closed_model(model_name: str) -> bool:
    """Check if model is closed/proprietary"""
    model_lower = model_name.lower()
    for closed in CLOSED_MODELS:
        if closed.lower() in model_lower:
            # Exception: gpt-oss-* models are open-source
            if "gpt-oss-" in model_lower:
                return False
            return True
    return False

def is_open_source(model: Dict) -> bool:
    """Check if model is open-source"""
    model_name = model.get("name", "")
    
    # Exclude closed models
    if is_closed_model(model_name):
        return False
    
    # Check provider
    creator = model.get("model_creator", {})
    creator_name = creator.get("name", "")
    
    if creator_name in OPEN_SOURCE_PROVIDERS:
        return True
    
    # Check if model has open-source indicators
    model_lower = model_name.lower()
    open_source_indicators = [
        "llama", "qwen", "deepseek", "mistral", "mixtral", "codestral",
        "devstral", "magistral", "ministral", "pixtral", "phi", "gemma",
        "hermes", "nemotron", "glm", "kimi", "solar", "granite", "olmo",
        "molmo", "tulu", "jamba", "arctic", "dbrx", "exaone", "ernie",
        "cogito", "seed", "doubao", "ring", "ling", "apriel", "gpt-oss-",
    ]
    
    for indicator in open_source_indicators:
        if indicator in model_lower:
            return True
    
    return False

def fetch_all_models() -> Optional[List[Dict]]:
    """Fetch all LLM models from the API"""
    headers = get_headers()
    endpoint = f"{BASE_URL}/data/llms/models"
    
    try:
        print(f"Fetching models from {endpoint}...")
        response = requests.get(endpoint, headers=headers, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and "data" in data:
                models = data["data"]
                print(f"✓ Successfully fetched {len(models)} models from API")
                return models
            elif isinstance(data, list):
                print(f"✓ Successfully fetched {len(data)} models from API")
                return data
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

def extract_all_benchmark_scores(model_data: Dict) -> Dict[str, float]:
    """Extract ALL benchmark scores from model data"""
    scores = {}
    
    evaluations = model_data.get("evaluations", {})
    if not evaluations:
        return scores
    
    # Extract all available scores
    for key, value in evaluations.items():
        if value is not None and isinstance(value, (int, float)):
            # Normalize to 0-1 range (if > 1, assume percentage)
            score = value / 100.0 if value > 1 else value
            # Store with normalized key
            normalized_key = key.lower().replace("-", "_").replace(" ", "_")
            scores[normalized_key] = score
    
    return scores

def get_all_benchmark_names(models: List[Dict]) -> Set[str]:
    """Get all unique benchmark names from models"""
    benchmark_names = set()
    
    for model in models:
        scores = model.get("scores", {})
        benchmark_names.update(scores.keys())
    
    return benchmark_names

def process_models(api_models: List[Dict]) -> List[Dict]:
    """Process API models, filter for open-source only"""
    processed_models = []
    open_source_count = 0
    excluded_count = 0
    
    print(f"\nFiltering for open-source models...")
    
    for model in api_models:
        # Filter for open-source only
        if not is_open_source(model):
            excluded_count += 1
            if excluded_count <= 10:  # Show first 10 excluded
                print(f"  Excluding: {model.get('name', 'Unknown')} ({model.get('model_creator', {}).get('name', 'Unknown')})")
            continue
        
        model_id = model.get("id", "")
        name = model.get("name", "")
        creator = model.get("model_creator", {})
        provider = creator.get("name", "Unknown")
        
        # Extract ALL scores
        scores = extract_all_benchmark_scores(model)
        
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
    
    print(f"\n✓ Kept {open_source_count} open-source models")
    print(f"✗ Excluded {excluded_count} closed/proprietary models")
    
    return processed_models

def export_to_csv(models: List[Dict], filename: str = "opensource_all_benchmarks.csv"):
    """Export open-source models with ALL benchmarks to CSV"""
    print(f"\nExporting to {filename}...")
    
    # Get all unique benchmark names
    all_benchmarks = get_all_benchmark_names(models)
    
    # Sort benchmarks for consistent ordering
    sorted_benchmarks = sorted(all_benchmarks)
    
    # Prepare CSV headers
    headers = ["Model Name", "Provider", "Dataset"]
    headers.extend(sorted_benchmarks)
    
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
            for benchmark in sorted_benchmarks:
                score = scores.get(benchmark)
                if score is not None:
                    # Format as percentage
                    row.append(f"{score * 100:.2f}%")
                else:
                    row.append("N/A")
            
            writer.writerow(row)
    
    print(f"✓ Exported {len(models)} open-source models to {filename}")
    print(f"✓ Included {len(sorted_benchmarks)} unique benchmarks")
    
    return sorted_benchmarks

def main():
    print("=" * 60)
    print("Fetching ALL Open-Source Models with ALL Datasets")
    print("=" * 60)
    print(f"API: {BASE_URL}")
    print(f"Filtering: Open-source only (excluding Grok 2, 3, etc.)")
    print()
    
    # Fetch all models from API
    api_models = fetch_all_models()
    
    if not api_models:
        print("\n⚠ Could not fetch models from API")
        return
    
    # Process and filter for open-source
    models = process_models(api_models)
    
    if not models:
        print("\n⚠ No open-source models found")
        return
    
    # Count models with scores
    models_with_scores = sum(1 for m in models if m.get("scores"))
    print(f"\n✓ {models_with_scores} models have benchmark scores")
    
    # Show sample
    print(f"\n=== Sample Models ===")
    for model in models[:5]:
        if model.get("scores"):
            print(f"\n{model['name']} ({model['provider']}):")
            scores = model["scores"]
            # Show first 5 benchmarks
            for i, (bench, score) in enumerate(list(scores.items())[:5]):
                print(f"  {bench}: {score*100:.1f}%")
    
    # Export to CSV
    benchmarks = export_to_csv(models, "opensource_all_benchmarks.csv")
    
    # Save JSON
    data = {
        "benchmarks": list(benchmarks),
        "models": models
    }
    
    with open("opensource_all_benchmarks_data.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✓ Saved to opensource_all_benchmarks_data.json")
    print(f"\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Total open-source models: {len(models)}")
    print(f"Total benchmarks: {len(benchmarks)}")
    print(f"CSV file: opensource_all_benchmarks.csv")
    print(f"JSON file: opensource_all_benchmarks_data.json")

if __name__ == "__main__":
    main()

