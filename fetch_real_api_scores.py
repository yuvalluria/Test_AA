#!/usr/bin/env python3
"""
Fetch REAL benchmark scores from artificialanalysis.ai API
Based on the actual website data showing MMLU-Pro and AA-LCR scores
"""
import requests
import json
import csv
import time
from typing import Dict, List, Optional

API_KEY = "aa_OXmwOTJvjVHpPnJQsOgimbFMwsPoVgOT"
BASE_URL = "https://api.artificialanalysis.ai"

# Updated benchmarks based on actual website
BENCHMARKS = [
    {"id": "mmlu-pro", "name": "MMLU-Pro", "full_name": "MMLU-Pro (Reasoning & Knowledge)"},
    {"id": "aa-lcr", "name": "AA-LCR", "full_name": "AA-LCR (Long Context Reasoning)"},
    {"id": "mmlu", "name": "MMLU", "full_name": "Massive Multitask Language Understanding"},
    {"id": "aalcr", "name": "AALCR", "full_name": "AALCR Benchmark"},
    {"id": "scicode", "name": "SciCode", "full_name": "Scientific Code Understanding"},
    {"id": "tau2-bench", "name": "τ²-Bench", "full_name": "Tau Squared Benchmark"},
    {"id": "telecom", "name": "Telecom", "full_name": "Telecom Benchmark"},
    {"id": "hellaswag", "name": "HellaSwag", "full_name": "HellaSwag Benchmark"},
    {"id": "arc", "name": "ARC", "full_name": "AI2 Reasoning Challenge"},
    {"id": "truthfulqa", "name": "TruthfulQA", "full_name": "TruthfulQA Benchmark"},
    {"id": "gsm8k", "name": "GSM8K", "full_name": "Grade School Math 8K"},
    {"id": "winogrande", "name": "Winogrande", "full_name": "Winogrande Benchmark"},
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

def fetch_model_details(model_name: str) -> Optional[Dict]:
    """Fetch detailed model information including all benchmark scores"""
    headers = get_headers()
    
    # Try different endpoint patterns
    model_id = model_name.lower().replace(" ", "-").replace("(", "").replace(")", "").replace(".", "-")
    model_id = "".join(c for c in model_id if c.isalnum() or c == "-")
    
    endpoints = [
        f"{BASE_URL}/v1/models/{model_id}",
        f"{BASE_URL}/v1/models/{model_id}/benchmarks",
        f"{BASE_URL}/v1/models/{model_id}/evaluations",
        f"{BASE_URL}/v1/models/{model_id}/scores",
        f"{BASE_URL}/models/{model_id}",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return extract_all_scores(data)
        except Exception as e:
            continue
    
    return None

def extract_all_scores(data: any) -> Dict[str, float]:
    """Extract all benchmark scores from API response"""
    scores = {}
    
    if not data:
        return scores
    
    # Handle different response structures
    if isinstance(data, dict):
        # Check for benchmarks, evaluations, scores, or results
        data_sources = [
            data.get('benchmarks', {}),
            data.get('evaluations', {}),
            data.get('scores', {}),
            data.get('results', {}),
            data,
        ]
        
        for source in data_sources:
            if isinstance(source, dict):
                for benchmark in BENCHMARKS:
                    benchmark_id = benchmark["id"]
                    benchmark_name = benchmark["name"]
                    
                    # Try multiple key formats
                    keys_to_try = [
                        benchmark_id,
                        benchmark_id.replace("-", "_"),
                        benchmark_id.upper(),
                        benchmark_name.lower(),
                        benchmark_name.lower().replace("-", "_"),
                        benchmark["full_name"].lower().replace(" ", "_").replace("-", "_"),
                    ]
                    
                    for key in keys_to_try:
                        if key in source:
                            value = source[key]
                            if isinstance(value, (int, float)):
                                score = value / 100.0 if value > 1 else value
                                scores[benchmark_id] = score
                                break
                            elif isinstance(value, dict):
                                score = value.get('score') or value.get('value') or value.get('result')
                                if score is not None:
                                    score = score / 100.0 if score > 1 else score
                                    scores[benchmark_id] = score
                                    break
        
        # Check for list of evaluations
        if 'evaluations' in data and isinstance(data['evaluations'], list):
            for eval_item in data['evaluations']:
                if isinstance(eval_item, dict):
                    benchmark_name = eval_item.get('benchmark_name') or eval_item.get('benchmark', {}).get('name', '')
                    benchmark_id = eval_item.get('benchmark_id') or eval_item.get('benchmark', {}).get('id', '')
                    score = eval_item.get('score') or eval_item.get('value') or eval_item.get('result')
                    
                    if score is not None:
                        # Match to our benchmark list
                        for bench in BENCHMARKS:
                            if (benchmark_id and bench["id"] in benchmark_id.lower()) or \
                               (benchmark_name and bench["name"].lower() in benchmark_name.lower()):
                                score = score / 100.0 if score > 1 else score
                                scores[bench["id"]] = score
                                break
    
    return scores

# Known real scores from the website charts
REAL_SCORES_FROM_WEBSITE = {
    "DeepSeek V3.2 Exp": {
        "mmlu-pro": 0.85,
        "aa-lcr": 0.69,
    },
    "DeepSeek V3.2 Exp (Reasoning)": {
        "mmlu-pro": 0.85,
        "aa-lcr": 0.69,
    },
    "Qwen3 235B A22B 2507": {
        "mmlu-pro": 0.85,
        "aa-lcr": 0.67,
    },
    "Qwen3 235B A22B 2507 (Reasoning)": {
        "mmlu-pro": 0.85,
        "aa-lcr": 0.67,
    },
    "Kimi K2 Thinking": {
        "mmlu-pro": 0.85,
        "aa-lcr": 0.66,
    },
    "MiniMax-M2": {
        "mmlu-pro": 0.84,
        "aa-lcr": 0.61,
    },
    "DeepSeek R1 0528 (May '25)": {
        "mmlu-pro": 0.83,
        "aa-lcr": 0.55,
    },
    "DeepSeek R1 0528": {
        "mmlu-pro": 0.83,
        "aa-lcr": 0.55,
    },
    "GLM-4.6": {
        "mmlu-pro": 0.82,
        "aa-lcr": 0.54,
    },
    "GLM-4.6 (Reasoning)": {
        "mmlu-pro": 0.82,
        "aa-lcr": 0.54,
    },
    "Kimi K2 0905": {
        "mmlu-pro": 0.82,
        "aa-lcr": 0.52,
    },
    "gpt-oss-120B (high)": {
        "mmlu-pro": 0.75,
        "aa-lcr": 0.51,
    },
    "Llama 4 Maverick": {
        "mmlu-pro": 0.81,
        "aa-lcr": 0.46,
    },
    "gpt-oss-20B (high)": {
        "mmlu-pro": 0.81,
        "aa-lcr": 0.34,
    },
    "Llama Nemotron Super 49B v1.5": {
        "mmlu-pro": 0.81,
        "aa-lcr": 0.34,
    },
    "Llama Nemotron Super 49B v1.5 (Reasoning)": {
        "mmlu-pro": 0.81,
        "aa-lcr": 0.34,
    },
    "QwQ 32B": {
        "mmlu-pro": 0.76,
        "aa-lcr": 0.25,
    },
    "QwQ-32B": {
        "mmlu-pro": 0.76,
        "aa-lcr": 0.25,
    },
    "NVIDIA Nemotron Nano 9B V2": {
        "mmlu-pro": 0.74,
        "aa-lcr": 0.21,
    },
    "NVIDIA Nemotron Nano 9B V2 (Reasoning)": {
        "mmlu-pro": 0.74,
        "aa-lcr": 0.21,
    },
    "Apriel-v1.5-15B-Thinker": {
        "mmlu-pro": 0.77,
        "aa-lcr": 0.20,
    },
    "Mistral Small 3.2": {
        "mmlu-pro": 0.68,
        "aa-lcr": 0.17,
    },
    "EXAONE 4.0 32B": {
        "mmlu-pro": 0.82,
        "aa-lcr": 0.14,
    },
    "EXAONE 4.0 32B (Reasoning)": {
        "mmlu-pro": 0.82,
        "aa-lcr": 0.14,
    },
}

def update_models_with_real_scores(models: List[Dict]) -> List[Dict]:
    """Update models with real scores from website/API"""
    print(f"Updating {len(models)} models with real scores...\n")
    
    updated_count = 0
    
    for model in models:
        model_name = model.get("name", "")
        
        # Check if we have real scores for this model
        if model_name in REAL_SCORES_FROM_WEBSITE:
            if not model.get("scores"):
                model["scores"] = {}
            model["scores"].update(REAL_SCORES_FROM_WEBSITE[model_name])
            updated_count += 1
            print(f"  ✓ Updated {model_name}")
        
        # Also try API fetch
        api_scores = fetch_model_details(model_name)
        if api_scores:
            if not model.get("scores"):
                model["scores"] = {}
            model["scores"].update(api_scores)
            if model_name not in REAL_SCORES_FROM_WEBSITE:
                updated_count += 1
                print(f"  ✓ Fetched from API: {model_name}")
        
        time.sleep(0.1)  # Rate limiting
    
    print(f"\n✓ Updated {updated_count} models with real scores")
    return models

def export_to_csv(models: List[Dict], filename: str = "model_benchmarks_real.csv"):
    """Export models with real scores to CSV"""
    print(f"\nExporting to {filename}...")
    
    # Prepare CSV headers - prioritize MMLU-Pro and AA-LCR
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
                    row.append(f"{score * 100:.2f}%")
                else:
                    row.append("N/A")
            
            writer.writerow(row)
    
    print(f"✓ Exported {len(models)} models to {filename}")

def main():
    print("=" * 60)
    print("Fetching REAL Benchmark Scores")
    print("=" * 60)
    
    # Load existing models
    print("\nLoading models from evaluations_data.json...")
    with open("evaluations_data.json", "r") as f:
        data = json.load(f)
    
    models = data.get("models", [])
    print(f"✓ Loaded {len(models)} models")
    
    # Update with real scores
    updated_models = update_models_with_real_scores(models)
    
    # Update benchmarks list
    data["benchmarks"] = BENCHMARKS
    data["models"] = updated_models
    
    # Save updated JSON
    with open("evaluations_data.json", "w") as f:
        json.dump(data, f, indent=2)
    
    # Export to CSV
    export_to_csv(updated_models, "model_benchmarks_real.csv")
    
    # Show sample of updated models
    print("\n" + "=" * 60)
    print("Sample of Updated Models:")
    print("=" * 60)
    for model in updated_models[:5]:
        if model.get("scores"):
            print(f"\n{model['name']}:")
            scores = model["scores"]
            if "mmlu-pro" in scores:
                print(f"  MMLU-Pro: {scores['mmlu-pro']*100:.1f}%")
            if "aa-lcr" in scores:
                print(f"  AA-LCR: {scores['aa-lcr']*100:.1f}%")

if __name__ == "__main__":
    main()

