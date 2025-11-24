#!/usr/bin/env python3
"""
Fetch open-source models with subject-specific evaluation datasets
Groups evaluations by subject: Math, Computer Science, Science, Philosophy, History, etc.
"""
import requests
import json
import csv
from typing import Dict, List, Optional
from collections import defaultdict

API_KEY = "aa_OXmwOTJvjVHpPnJQsOgimbFMwsPoVgOT"
BASE_URL = "https://artificialanalysis.ai/api/v2"

# Subject categories and their associated benchmarks
SUBJECT_CATEGORIES = {
    "Mathematics": [
        {"id": "math_500", "name": "Math 500", "api_key": "math_500"},
        {"id": "aime", "name": "AIME", "api_key": "aime"},
        {"id": "aime_25", "name": "AIME 2025", "api_key": "aime_25"},
        {"id": "artificial_analysis_math_index", "name": "Math Index", "api_key": "artificial_analysis_math_index"},
    ],
    "Computer Science": [
        {"id": "livecodebench", "name": "LiveCodeBench", "api_key": "livecodebench"},
        {"id": "ifbench", "name": "IFBench", "api_key": "ifbench"},
        {"id": "terminalbench_hard", "name": "Terminal-Bench Hard", "api_key": "terminalbench_hard"},
        {"id": "artificial_analysis_coding_index", "name": "Coding Index", "api_key": "artificial_analysis_coding_index"},
    ],
    "Science": [
        {"id": "scicode", "name": "SciCode", "api_key": "scicode"},
        {"id": "gpqa", "name": "GPQA Diamond", "api_key": "gpqa"},
        {"id": "hle", "name": "Humanity's Last Exam", "api_key": "hle"},
    ],
    "General Knowledge": [
        {"id": "mmlu_pro", "name": "MMLU-Pro", "api_key": "mmlu_pro"},
        {"id": "artificial_analysis_intelligence_index", "name": "Intelligence Index", "api_key": "artificial_analysis_intelligence_index"},
    ],
    "Reasoning": [
        {"id": "aa_lcr", "name": "AA-LCR", "api_key": "lcr"},
        {"id": "tau2", "name": "τ²-Bench Telecom", "api_key": "tau2"},
    ],
}

# Open-source providers
OPEN_SOURCE_PROVIDERS = [
    "Meta", "Alibaba", "DeepSeek", "Mistral", "Google", "Microsoft Azure",
    "Nous Research", "NVIDIA", "Z AI", "Moonshot AI", "MiniMax",
    "ByteDance Seed", "ServiceNow", "LG AI Research", "InclusionAI",
    "Allen Institute for AI", "IBM", "Upstage", "xAI", "Cohere",
    "Liquid AI", "Snowflake", "Databricks", "OpenChat", "AI21 Labs",
    "Perplexity", "Deep Cogito", "Baidu", "OpenAI",
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
    return creator_name in OPEN_SOURCE_PROVIDERS

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
            print(f"✗ Error: Status code {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ Error fetching models: {e}")
        return None

def extract_subject_scores(model_data: Dict) -> Dict[str, Dict[str, float]]:
    """Extract subject-specific scores organized by category"""
    scores_by_subject = defaultdict(dict)
    
    evaluations = model_data.get("evaluations", {})
    if not evaluations:
        return scores_by_subject
    
    # Extract scores for each subject category
    for subject, benchmarks in SUBJECT_CATEGORIES.items():
        for benchmark in benchmarks:
            api_key = benchmark["api_key"]
            
            if api_key in evaluations:
                value = evaluations[api_key]
                if value is not None and isinstance(value, (int, float)):
                    # Normalize to 0-1 range
                    score = value / 100.0 if value > 1 else value
                    scores_by_subject[subject][benchmark["id"]] = {
                        "name": benchmark["name"],
                        "score": score
                    }
    
    return scores_by_subject

def process_models(api_models: List[Dict]) -> List[Dict]:
    """Process API models, filter for open-source only"""
    processed_models = []
    
    for model in api_models:
        if not is_open_source(model):
            continue
        
        model_id = model.get("id", "")
        name = model.get("name", "")
        creator = model.get("model_creator", {})
        provider = creator.get("name", "Unknown")
        
        # Extract subject-specific scores
        subject_scores = extract_subject_scores(model)
        
        # Only include models that have at least one subject score
        if not subject_scores:
            continue
        
        processed_model = {
            "id": model_id,
            "name": name,
            "provider": provider,
            "dataset": f"{provider} training dataset",
            "subject_scores": subject_scores,
        }
        
        processed_models.append(processed_model)
    
    print(f"✓ Found {len(processed_models)} open-source models with subject-specific scores")
    return processed_models

def export_to_csv(models: List[Dict], filename: str = "opensource_subject_specific.csv"):
    """Export models with subject-specific scores to CSV"""
    print(f"\nExporting to {filename}...")
    
    # Build headers: Model Name, Provider, Dataset, then all benchmarks grouped by subject
    headers = ["Model Name", "Provider", "Dataset"]
    
    # Add all benchmarks organized by subject
    for subject in SUBJECT_CATEGORIES.keys():
        for benchmark in SUBJECT_CATEGORIES[subject]:
            headers.append(f"{subject} - {benchmark['name']}")
    
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
            
            # Add scores for each benchmark in order
            subject_scores = model.get("subject_scores", {})
            for subject in SUBJECT_CATEGORIES.keys():
                for benchmark in SUBJECT_CATEGORIES[subject]:
                    bench_id = benchmark["id"]
                    if subject in subject_scores and bench_id in subject_scores[subject]:
                        score = subject_scores[subject][bench_id]["score"]
                        row.append(f"{score * 100:.2f}%")
                    else:
                        row.append("N/A")
            
            writer.writerow(row)
    
    print(f"✓ Exported {len(models)} models to {filename}")

def export_by_subject_csv(models: List[Dict]):
    """Export separate CSV files for each subject category"""
    print(f"\nExporting separate CSV files by subject...")
    
    for subject, benchmarks in SUBJECT_CATEGORIES.items():
        filename = f"opensource_{subject.lower().replace(' ', '_')}.csv"
        
        headers = ["Model Name", "Provider", "Dataset"]
        headers.extend([benchmark["name"] for benchmark in benchmarks])
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            
            for model in models:
                subject_scores = model.get("subject_scores", {})
                
                # Only include models that have at least one score for this subject
                if subject not in subject_scores:
                    continue
                
                row = [
                    model.get("name", ""),
                    model.get("provider", ""),
                    model.get("dataset", ""),
                ]
                
                for benchmark in benchmarks:
                    bench_id = benchmark["id"]
                    if bench_id in subject_scores[subject]:
                        score = subject_scores[subject][bench_id]["score"]
                        row.append(f"{score * 100:.2f}%")
                    else:
                        row.append("N/A")
                
                writer.writerow(row)
        
        # Count models with scores for this subject
        count = sum(1 for m in models if subject in m.get("subject_scores", {}))
        print(f"  ✓ {subject}: {count} models -> {filename}")

def main():
    print("=" * 60)
    print("Fetching Open-Source Models with Subject-Specific Evaluations")
    print("=" * 60)
    print("\nSubject Categories:")
    for subject, benchmarks in SUBJECT_CATEGORIES.items():
        print(f"\n  {subject}:")
        for bench in benchmarks:
            print(f"    - {bench['name']}")
    
    # Fetch all models from API
    api_models = fetch_all_models()
    
    if not api_models:
        print("✗ Could not fetch models from API")
        return
    
    # Process and filter for open-source
    print(f"\nFiltering for open-source models...")
    models = process_models(api_models)
    
    # Count models by subject
    print(f"\n=== Subject Coverage ===")
    for subject in SUBJECT_CATEGORIES.keys():
        count = sum(1 for m in models if subject in m.get("subject_scores", {}))
        print(f"  {subject}: {count} models")
    
    # Show sample
    print(f"\n=== Sample Model ===")
    for model in models[:1]:
        if model.get("subject_scores"):
            print(f"\n{model['name']} ({model['provider']}):")
            for subject, scores in model["subject_scores"].items():
                print(f"  {subject}:")
                for bench_id, bench_data in scores.items():
                    print(f"    {bench_data['name']}: {bench_data['score']*100:.1f}%")
    
    # Export combined CSV
    export_to_csv(models, "opensource_subject_specific.csv")
    
    # Export separate CSVs by subject
    export_by_subject_csv(models)
    
    # Save JSON
    data = {
        "subject_categories": SUBJECT_CATEGORIES,
        "models": models
    }
    
    with open("opensource_subject_specific_data.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✓ Saved to opensource_subject_specific_data.json")
    print(f"\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Total open-source models: {len(models)}")
    print(f"Combined CSV: opensource_subject_specific.csv")
    print(f"Separate CSVs by subject: opensource_<subject>.csv")
    print(f"JSON file: opensource_subject_specific_data.json")

if __name__ == "__main__":
    main()




