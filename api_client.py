#!/usr/bin/env python3
"""
API Client for artificialanalysis.ai to fetch real intelligence evaluation scores
"""
import requests
import json
from typing import Dict, List, Optional, Any

API_KEY = "aa_OXmwOTJvjVHpPnJQsOgimbFMwsPoVgOT"
BASE_URL = "https://api.artificialanalysis.ai"

class ArtificialAnalysisClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "X-API-Key": api_key,
            "api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_models(self) -> Optional[List[Dict]]:
        """Get list of all models"""
        endpoints = [
            f"{BASE_URL}/v1/models",
            f"{BASE_URL}/models",
            f"{BASE_URL}/v1/models/open-source",
            f"{BASE_URL}/open-source/models"
        ]
        
        for endpoint in endpoints:
            try:
                response = self.session.get(endpoint, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list):
                        return data
                    elif isinstance(data, dict) and 'models' in data:
                        return data['models']
                    elif isinstance(data, dict) and 'data' in data:
                        return data['data']
            except Exception as e:
                print(f"Error with {endpoint}: {e}")
                continue
        
        return None

    def get_benchmarks(self) -> Optional[List[Dict]]:
        """Get list of all benchmarks"""
        endpoints = [
            f"{BASE_URL}/v1/benchmarks",
            f"{BASE_URL}/benchmarks",
            f"{BASE_URL}/v1/benchmarks/list"
        ]
        
        for endpoint in endpoints:
            try:
                response = self.session.get(endpoint, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list):
                        return data
                    elif isinstance(data, dict) and 'benchmarks' in data:
                        return data['benchmarks']
            except Exception as e:
                print(f"Error with {endpoint}: {e}")
                continue
        
        return None

    def get_model_scores(self, model_id: str) -> Optional[Dict]:
        """Get scores for a specific model"""
        endpoints = [
            f"{BASE_URL}/v1/models/{model_id}/scores",
            f"{BASE_URL}/v1/models/{model_id}/evaluations",
            f"{BASE_URL}/models/{model_id}/scores",
            f"{BASE_URL}/v1/evaluations?model_id={model_id}"
        ]
        
        for endpoint in endpoints:
            try:
                response = self.session.get(endpoint, timeout=10)
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                print(f"Error with {endpoint}: {e}")
                continue
        
        return None

    def get_all_evaluations(self) -> Optional[Dict]:
        """Get all evaluations (models with their scores)"""
        endpoints = [
            f"{BASE_URL}/v1/evaluations",
            f"{BASE_URL}/v1/benchmarks/results",
            f"{BASE_URL}/v1/models/evaluations",
            f"{BASE_URL}/evaluations/all"
        ]
        
        for endpoint in endpoints:
            try:
                response = self.session.get(endpoint, timeout=10)
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                print(f"Error with {endpoint}: {e}")
                continue
        
        return None

    def fetch_complete_data(self) -> Dict:
        """Fetch complete evaluation data structure"""
        print("Fetching models...")
        models = self.get_models()
        
        print("Fetching benchmarks...")
        benchmarks = self.get_benchmarks()
        
        print("Fetching evaluations...")
        evaluations = self.get_all_evaluations()
        
        # If we got evaluations directly, use that
        if evaluations:
            if isinstance(evaluations, dict):
                if 'models' in evaluations and 'benchmarks' in evaluations:
                    return evaluations
                elif 'data' in evaluations:
                    return self._process_evaluations_data(evaluations['data'])
        
        # Otherwise, build from models and benchmarks
        result = {
            "benchmarks": benchmarks or self._get_default_benchmarks(),
            "models": []
        }
        
        if models:
            print(f"Processing {len(models)} models...")
            for model in models[:20]:  # Limit to first 20 for testing
                model_id = model.get('id') or model.get('model_id') or model.get('name', '').lower().replace(' ', '-')
                print(f"  Fetching scores for {model.get('name', model_id)}...")
                scores = self.get_model_scores(model_id)
                
                model_data = {
                    "id": model_id,
                    "name": model.get('name') or model.get('model_name') or model_id,
                    "provider": model.get('provider') or model.get('organization') or "Unknown"
                }
                
                if scores:
                    if isinstance(scores, dict):
                        if 'scores' in scores:
                            model_data['scores'] = scores['scores']
                        elif 'evaluations' in scores:
                            model_data['scores'] = self._extract_scores_from_evaluations(scores['evaluations'])
                        else:
                            model_data['scores'] = scores
                
                result["models"].append(model_data)
        
        return result

    def _process_evaluations_data(self, data: Any) -> Dict:
        """Process raw evaluations data into structured format"""
        benchmarks = set()
        models_dict = {}
        
        if isinstance(data, list):
            for item in data:
                model_id = item.get('model_id') or item.get('model', {}).get('id')
                benchmark_id = item.get('benchmark_id') or item.get('benchmark', {}).get('id')
                score = item.get('score') or item.get('value')
                
                if model_id and benchmark_id and score is not None:
                    benchmarks.add(benchmark_id)
                    if model_id not in models_dict:
                        models_dict[model_id] = {
                            "id": model_id,
                            "name": item.get('model', {}).get('name') or model_id,
                            "provider": item.get('model', {}).get('provider') or "Unknown",
                            "scores": {}
                        }
                    models_dict[model_id]['scores'][benchmark_id] = score
        
        return {
            "benchmarks": [{"id": b, "name": b.upper()} for b in sorted(benchmarks)],
            "models": list(models_dict.values())
        }

    def _extract_scores_from_evaluations(self, evaluations: List[Dict]) -> Dict:
        """Extract scores from evaluations list"""
        scores = {}
        for eval in evaluations:
            benchmark_id = eval.get('benchmark_id') or eval.get('benchmark', {}).get('id')
            score = eval.get('score') or eval.get('value')
            if benchmark_id and score is not None:
                scores[benchmark_id] = score
        return scores

    def _get_default_benchmarks(self) -> List[Dict]:
        """Return default benchmark list"""
        return [
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


def main():
    client = ArtificialAnalysisClient(API_KEY)
    
    print("=" * 60)
    print("Artificial Analysis API Client")
    print("=" * 60)
    
    data = client.fetch_complete_data()
    
    if data and data.get('models'):
        print(f"\n✓ Successfully fetched data for {len(data['models'])} models")
        print(f"✓ Found {len(data['benchmarks'])} benchmarks")
        
        # Save to file
        with open("evaluations_data.json", "w") as f:
            json.dump(data, f, indent=2)
        
        print("\n✓ Data saved to evaluations_data.json")
        
        # Print summary
        print("\n=== Models ===")
        for model in data['models'][:5]:
            print(f"  - {model['name']}: {len(model.get('scores', {}))} scores")
    else:
        print("\n⚠ Could not fetch data from API")
        print("Using sample data structure...")
        
        # Create sample data
        from data_fetcher import get_sample_data
        sample_data = get_sample_data()
        with open("evaluations_data.json", "w") as f:
            json.dump(sample_data, f, indent=2)
        print("✓ Sample data saved to evaluations_data.json")


if __name__ == "__main__":
    main()

