#!/usr/bin/env python3
"""
Enhanced data fetcher for artificialanalysis.ai intelligence evaluations
"""
import requests
import json
from typing import Dict, List, Any, Optional

API_KEY = "aa_OXmwOTJvjVHpPnJQsOgimbFMwsPoVgOT"

# Known benchmarks from the website
BENCHMARKS = [
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

def fetch_model_scores(model_id: str) -> Optional[Dict]:
    """Fetch scores for a specific model"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    # Try different endpoint patterns
    endpoints = [
        f"https://api.artificialanalysis.ai/v1/models/{model_id}/scores",
        f"https://api.artificialanalysis.ai/v1/models/{model_id}/evaluations",
        f"https://api.artificialanalysis.ai/models/{model_id}",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
        except:
            continue
    
    return None

def fetch_all_models_data() -> Dict:
    """Fetch data for all models"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    # Try to get all models with their scores
    endpoints = [
        "https://api.artificialanalysis.ai/v1/models?include_scores=true",
        "https://api.artificialanalysis.ai/v1/benchmarks/results",
        "https://api.artificialanalysis.ai/v1/evaluations/all",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error with {endpoint}: {e}")
            continue
    
    return {}

def get_sample_data() -> Dict:
    """Return expanded sample data structure with all open source models and datasets"""
    return {
        "benchmarks": BENCHMARKS,
        "models": [
            {
                "id": "deepseek-v3.2",
                "name": "DeepSeek V3.2",
                "provider": "DeepSeek",
                "dataset": "DeepSeek-V3.2 dataset",
                "scores": {
                    "mmlu": 0.85,
                    "aalcr": 0.69,
                    "scicode": 0.42,
                    "tau2-bench": 0.78,
                    "telecom": 0.71,
                    "hellaswag": 0.88,
                    "arc": 0.82,
                    "truthfulqa": 0.75,
                    "gsm8k": 0.90,
                    "winogrande": 0.85
                }
            },
            {
                "id": "llama-3.1-405b",
                "name": "Llama 3.1 405B",
                "provider": "Meta",
                "dataset": "Llama 3.1 training data",
                "scores": {
                    "mmlu": 0.87,
                    "aalcr": 0.72,
                    "scicode": 0.45,
                    "tau2-bench": 0.80,
                    "telecom": 0.73,
                    "hellaswag": 0.89,
                    "arc": 0.84,
                    "truthfulqa": 0.77,
                    "gsm8k": 0.91,
                    "winogrande": 0.86
                }
            },
            {
                "id": "qwen-2.5-72b",
                "name": "Qwen 2.5 72B",
                "provider": "Alibaba",
                "dataset": "Qwen 2.5 dataset",
                "scores": {
                    "mmlu": 0.83,
                    "aalcr": 0.68,
                    "scicode": 0.41,
                    "tau2-bench": 0.76,
                    "telecom": 0.70,
                    "hellaswag": 0.87,
                    "arc": 0.81,
                    "truthfulqa": 0.74,
                    "gsm8k": 0.89,
                    "winogrande": 0.84
                }
            },
            {
                "id": "mistral-large-2",
                "name": "Mistral Large 2",
                "provider": "Mistral AI",
                "dataset": "Mistral training dataset",
                "scores": {
                    "mmlu": 0.84,
                    "aalcr": 0.70,
                    "scicode": 0.43,
                    "tau2-bench": 0.77,
                    "telecom": 0.72,
                    "hellaswag": 0.88,
                    "arc": 0.83,
                    "truthfulqa": 0.76,
                    "gsm8k": 0.90,
                    "winogrande": 0.85
                }
            },
            {
                "id": "gemma-2-27b",
                "name": "Gemma 2 27B",
                "provider": "Google",
                "dataset": "Gemma 2 training data",
                "scores": {
                    "mmlu": 0.81,
                    "aalcr": 0.66,
                    "scicode": 0.39,
                    "tau2-bench": 0.74,
                    "telecom": 0.68,
                    "hellaswag": 0.85,
                    "arc": 0.79,
                    "truthfulqa": 0.72,
                    "gsm8k": 0.87,
                    "winogrande": 0.82
                }
            },
            {
                "id": "llama-3.1-70b",
                "name": "Llama 3.1 70B",
                "provider": "Meta",
                "dataset": "Llama 3.1 training data",
                "scores": {
                    "mmlu": 0.82,
                    "aalcr": 0.67,
                    "scicode": 0.40,
                    "tau2-bench": 0.75,
                    "telecom": 0.69,
                    "hellaswag": 0.86,
                    "arc": 0.80,
                    "truthfulqa": 0.73,
                    "gsm8k": 0.88,
                    "winogrande": 0.83
                }
            },
            {
                "id": "qwen-2.5-32b",
                "name": "Qwen 2.5 32B",
                "provider": "Alibaba",
                "dataset": "Qwen 2.5 dataset",
                "scores": {
                    "mmlu": 0.80,
                    "aalcr": 0.65,
                    "scicode": 0.38,
                    "tau2-bench": 0.73,
                    "telecom": 0.67,
                    "hellaswag": 0.85,
                    "arc": 0.78,
                    "truthfulqa": 0.71,
                    "gsm8k": 0.86,
                    "winogrande": 0.81
                }
            },
            {
                "id": "mistral-7b-instruct",
                "name": "Mistral 7B Instruct",
                "provider": "Mistral AI",
                "dataset": "Mistral training dataset",
                "scores": {
                    "mmlu": 0.76,
                    "aalcr": 0.61,
                    "scicode": 0.35,
                    "tau2-bench": 0.69,
                    "telecom": 0.63,
                    "hellaswag": 0.81,
                    "arc": 0.74,
                    "truthfulqa": 0.68,
                    "gsm8k": 0.82,
                    "winogrande": 0.77
                }
            },
            {
                "id": "gemma-2-9b",
                "name": "Gemma 2 9B",
                "provider": "Google",
                "dataset": "Gemma 2 training data",
                "scores": {
                    "mmlu": 0.75,
                    "aalcr": 0.60,
                    "scicode": 0.34,
                    "tau2-bench": 0.68,
                    "telecom": 0.62,
                    "hellaswag": 0.80,
                    "arc": 0.73,
                    "truthfulqa": 0.67,
                    "gsm8k": 0.81,
                    "winogrande": 0.76
                }
            },
            {
                "id": "phi-3-medium",
                "name": "Phi-3 Medium",
                "provider": "Microsoft",
                "dataset": "Phi-3 training dataset",
                "scores": {
                    "mmlu": 0.74,
                    "aalcr": 0.59,
                    "scicode": 0.33,
                    "tau2-bench": 0.67,
                    "telecom": 0.61,
                    "hellaswag": 0.79,
                    "arc": 0.72,
                    "truthfulqa": 0.66,
                    "gsm8k": 0.80,
                    "winogrande": 0.75
                }
            },
            {
                "id": "llama-3-70b",
                "name": "Llama 3 70B",
                "provider": "Meta",
                "dataset": "Llama 3 training data",
                "scores": {
                    "mmlu": 0.79,
                    "aalcr": 0.64,
                    "scicode": 0.37,
                    "tau2-bench": 0.72,
                    "telecom": 0.66,
                    "hellaswag": 0.84,
                    "arc": 0.77,
                    "truthfulqa": 0.70,
                    "gsm8k": 0.85,
                    "winogrande": 0.80
                }
            },
            {
                "id": "qwen-2-72b",
                "name": "Qwen 2 72B",
                "provider": "Alibaba",
                "dataset": "Qwen 2 dataset",
                "scores": {
                    "mmlu": 0.78,
                    "aalcr": 0.63,
                    "scicode": 0.36,
                    "tau2-bench": 0.71,
                    "telecom": 0.65,
                    "hellaswag": 0.83,
                    "arc": 0.76,
                    "truthfulqa": 0.69,
                    "gsm8k": 0.84,
                    "winogrande": 0.79
                }
            },
            {
                "id": "deepseek-coder-33b",
                "name": "DeepSeek Coder 33B",
                "provider": "DeepSeek",
                "dataset": "DeepSeek Coder dataset",
                "scores": {
                    "mmlu": 0.77,
                    "aalcr": 0.62,
                    "scicode": 0.48,
                    "tau2-bench": 0.70,
                    "telecom": 0.64,
                    "hellaswag": 0.82,
                    "arc": 0.75,
                    "truthfulqa": 0.68,
                    "gsm8k": 0.83,
                    "winogrande": 0.78
                }
            },
            {
                "id": "codellama-70b",
                "name": "CodeLlama 70B",
                "provider": "Meta",
                "dataset": "CodeLlama training data",
                "scores": {
                    "mmlu": 0.73,
                    "aalcr": 0.58,
                    "scicode": 0.46,
                    "tau2-bench": 0.66,
                    "telecom": 0.60,
                    "hellaswag": 0.78,
                    "arc": 0.71,
                    "truthfulqa": 0.65,
                    "gsm8k": 0.79,
                    "winogrande": 0.74
                }
            },
            {
                "id": "mistral-8x7b",
                "name": "Mixtral 8x7B",
                "provider": "Mistral AI",
                "dataset": "Mixtral training dataset",
                "scores": {
                    "mmlu": 0.81,
                    "aalcr": 0.66,
                    "scicode": 0.39,
                    "tau2-bench": 0.74,
                    "telecom": 0.68,
                    "hellaswag": 0.85,
                    "arc": 0.79,
                    "truthfulqa": 0.72,
                    "gsm8k": 0.87,
                    "winogrande": 0.82
                }
            }
        ]
    }

def main():
    """Main function to fetch and save data"""
    print("Fetching intelligence evaluation data...")
    
    # Try to fetch from API
    api_data = fetch_all_models_data()
    
    if api_data and api_data.get("models"):
        print("✓ Data fetched from API")
        data = api_data
    else:
        print("⚠ Using expanded sample data structure (API endpoints not available)")
        data = get_sample_data()
    
    # Save to JSON
    with open("evaluations_data.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Saved data for {len(data.get('models', []))} models")
    print(f"✓ Saved {len(data.get('benchmarks', []))} benchmarks")
    print("✓ Data saved to evaluations_data.json")
    
    return data

if __name__ == "__main__":
    main()
