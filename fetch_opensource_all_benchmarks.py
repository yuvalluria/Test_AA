#!/usr/bin/env python3
"""
Fetch ALL open-source models with ALL datasets from artificialanalysis.ai API
Creates opensource_all_benchmarks.csv with all models vs all datasets
"""
import requests
import json
import csv
import time
from typing import Dict, List, Optional, Set

API_KEY = "aa_eSQbIHGJXFMwbTklKCIrIJvMcGdEBrpB"
BASE_URL = "https://artificialanalysis.ai/api/v2"

# Closed/proprietary models to exclude
CLOSED_MODELS = [
    "grok 3", "grok-3", "grok3",
    "grok 4", "grok-4", "grok4", "grok 4.1", "grok-4.1", "grok4.1",
    "grok code", "grok-code",
    "grok beta", "grok-beta",
    "gpt-4", "gpt-3.5", "gpt-5",
    "o1", "o1-mini", "o1-pro", "o3", "o3-mini", "o3-pro", "o4",
    "gemini", "claude", "sonnet",
    "nova pro", "nova lite", "nova micro", "nova premier",
    "palm-2", "palm2",
    "yi-large",
    "reka flash (sep", "reka flash (feb", "reka core", "reka edge",
    "gemma 3n e4b instruct preview",
]

# Additional models to exclude (preview versions, duplicates, etc.)
# Use exact matching to avoid excluding valid versions like "1.2" when excluding "1"
EXCLUDE_EXACT_MODELS = [
    "codestral (jan '25)",
    "devstral medium",
    "jamba 1.5 large",
    "jamba 1.5 mini",
    "jamba instruct",
    "llama 65b",
    "magistral medium 1",  # Exclude version 1, but keep 1.2
    "magistral small 1",   # Exclude version 1, but keep 1.2
    "ministral 3b",
    "mistral large (feb '24)",
    "mistral medium",      # Exclude base version, but keep 3.1
    "mistral medium 3",    # Exclude version 3, but keep 3.1
    "mistral saba",
    "mistral small (feb '24)",
    "qwq 32b-preview",
    "qwen chat 14b",
    "qwen chat 72b",
    "qwen1.5 chat 110b",
    "qwen2 instruct 72b",
    "qwen3 max (preview)",
    "solar pro 2 (preview) (non-reasoning)",
    "solar pro 2 (preview) (reasoning)",
    "sonar",
    "sonar pro",
    "sonar reasoning",
    "sonar reasoning pro",
]

# Only these Grok models are open-source
OPEN_SOURCE_GROK_MODELS = [
    "grok-1", "grok 2 (dec '24)", "grok 2 (dec 24)", "grok-2 (dec '24)",
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
    
    # Special handling for Grok models
    if "grok" in model_lower:
        for allowed in OPEN_SOURCE_GROK_MODELS:
            if allowed.lower() in model_lower:
                return False
        return True
    
    # Special handling for Reka models
    if "reka" in model_lower:
        if "reka flash 3" in model_lower or "reka flash3" in model_lower:
            return False
        return True
    
    for closed in CLOSED_MODELS:
        if closed.lower() in model_lower:
            if "gpt-oss-" in model_lower:
                return False
            return True
    return False

def is_open_source(model: Dict) -> bool:
    """Check if model is open-source"""
    model_name = model.get("name", "")
    model_lower = model_name.lower()
    
    # Check for excluded models (preview versions, duplicates, etc.)
    # Use exact matching to avoid excluding valid versions
    for exclude in EXCLUDE_EXACT_MODELS:
        # Check if the model name exactly matches or starts with the exclude pattern
        # But be careful not to exclude "1.2" when excluding "1"
        if exclude == model_lower or model_lower.startswith(exclude + " "):
            # Special cases: allow 1.2 versions even if we exclude "1"
            if "magistral medium 1.2" in model_lower or "magistral small 1.2" in model_lower:
                continue
            # Allow 3.1 version even if we exclude "3"
            if "mistral medium 3.1" in model_lower:
                continue
            return False
    
    if "grok" in model_lower:
        for allowed in OPEN_SOURCE_GROK_MODELS:
            if allowed.lower() in model_lower:
                return True
        return False
    
    if is_closed_model(model_name):
        return False
    
    return True

def fetch_all_models() -> Optional[List[Dict]]:
    """Fetch all open-source LLM models from the API"""
    headers = get_headers()
    endpoint = f"{BASE_URL}/data/llms/models?open_source=true"
    
    try:
        print(f"Fetching open-source models from {endpoint}...")
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

def extract_benchmark_scores(model_data: Dict) -> Dict[str, Optional[float]]:
    """Extract benchmark scores from model data"""
    scores = {}
    
    evaluations = model_data.get("evaluations", {})
    if not evaluations:
        return scores
    
    # Map of API keys to CSV column names (matching the correct file format)
    benchmark_mapping = {
        "aime": "aime",
        "aime_25": "aime_25",
        "artificial_analysis_coding_index": "artificial_analysis_coding_index",
        "artificial_analysis_intelligence_index": "artificial_analysis_intelligence_index",
        "artificial_analysis_math_index": "artificial_analysis_math_index",
        "gpqa": "gpqa",
        "hle": "hle",
        "ifbench": "ifbench",
        "lcr": "lcr",
        "livecodebench": "livecodebench",
        "math_500": "math_500",
        "mmlu_pro": "mmlu_pro",
        "scicode": "scicode",
        "tau2": "tau2",
        "terminalbench_hard": "terminalbench_hard",
    }
    
    # Extract scores for each benchmark
    for api_key, csv_name in benchmark_mapping.items():
        # Try different key variations
        value = None
        for key_variant in [api_key, api_key.replace("_", "-"), api_key.upper(), api_key.replace("_", " ")]:
            if key_variant in evaluations:
                value = evaluations[key_variant]
                break
        
        if value is not None:
            # Normalize to 0-1 range (if > 1, assume percentage)
            score = value / 100.0 if value > 1 else value
            scores[csv_name] = score
        else:
            scores[csv_name] = None
    
    return scores

def process_models(api_models: List[Dict]) -> List[Dict]:
    """Process API models, filter for open-source only"""
    processed_models = []
    open_source_count = 0
    excluded_count = 0
    
    print(f"\nFiltering for open-source models...")
    
    for model in api_models:
        if not is_open_source(model):
            excluded_count += 1
            if excluded_count <= 10:
                print(f"  Excluding: {model.get('name', 'Unknown')}")
            continue
        
        model_id = model.get("id", "")
        name = model.get("name", "")
        creator = model.get("model_creator", {})
        provider = creator.get("name", "Unknown")
        
        # Extract scores
        scores = extract_benchmark_scores(model)
        
        processed_model = {
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
    
    # Define all benchmark columns in order (matching the correct file format)
    benchmark_columns = [
        "aime",
        "aime_25",
        "artificial_analysis_coding_index",
        "artificial_analysis_intelligence_index",
        "artificial_analysis_math_index",
        "gpqa",
        "hle",
        "ifbench",
        "lcr",
        "livecodebench",
        "math_500",
        "mmlu_pro",
        "scicode",
        "tau2",
        "terminalbench_hard",
    ]
    
    # Prepare CSV headers
    headers = ["Model Name", "Provider", "Dataset"] + benchmark_columns
    
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
            for benchmark in benchmark_columns:
                score = scores.get(benchmark)
                if score is not None:
                    # Format as percentage
                    row.append(f"{score * 100:.2f}%")
                else:
                    row.append("N/A")
            
            writer.writerow(row)
    
    print(f"✓ Exported {len(models)} open-source models to {filename}")
    print(f"✓ Included {len(benchmark_columns)} benchmarks")
    
    return benchmark_columns

def main():
    print("=" * 70)
    print("Fetching ALL Open-Source Models with ALL Datasets")
    print("=" * 70)
    print(f"API: {BASE_URL}")
    print(f"API Key: {API_KEY[:20]}...")
    print(f"Filtering: Open-source only")
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
    models_with_scores = sum(1 for m in models if any(s is not None for s in m.get("scores", {}).values()))
    print(f"\n✓ {models_with_scores} models have benchmark scores")
    
    # Show sample
    print(f"\n=== Sample Models ===")
    for model in models[:3]:
        if any(s is not None for s in model.get("scores", {}).values()):
            print(f"\n{model['name']} ({model['provider']}):")
            scores = model["scores"]
            for bench, score in list(scores.items())[:5]:
                if score is not None:
                    print(f"  {bench}: {score*100:.1f}%")
    
    # Export to CSV
    benchmarks = export_to_csv(models, "opensource_all_benchmarks.csv")
    
    print(f"\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"Total open-source models: {len(models)}")
    print(f"Total benchmarks: {len(benchmarks)}")
    print(f"CSV file: opensource_all_benchmarks.csv")
    print("=" * 70)

if __name__ == "__main__":
    main()

