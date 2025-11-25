#!/usr/bin/env python3
"""
Fetch latency and performance metrics (TTFT, ITL, E2E, Throughput) from artificialanalysis.ai API
"""
import requests
import json
import csv
import time
from typing import Dict, List, Optional

API_KEY = "aa_HrMuMHsMjZnPBAmrQfNiaeiyHPyYjwaH"
BASE_URL = "https://artificialanalysis.ai/api/v2"

def get_headers():
    """Get API headers"""
    return {
        "x-api-key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

def fetch_all_models() -> Optional[List[Dict]]:
    """Fetch all open-source models from API"""
    headers = get_headers()
    endpoint = f"{BASE_URL}/data/llms/models?open_source=true"
    
    print(f"Fetching models from {endpoint}...")
    
    try:
        response = requests.get(endpoint, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            
            # Handle different response structures
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                if "models" in data:
                    return data["models"]
                elif "data" in data:
                    return data["data"]
                elif "results" in data:
                    return data["results"]
            
            return data
        else:
            print(f"Error: Status code {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return None
    except Exception as e:
        print(f"Error fetching models: {e}")
        return None

def extract_latency_metrics(model_data: Dict) -> Dict[str, Optional[float]]:
    """
    Extract latency and performance metrics from model data
    
    Looks for:
    - TTFT (Time to First Token) / TFCR (Time to First Character/Token Response)
    - ITL (Inter-Token Latency) / TPOT (Time Per Output Token)
    - E2E (End-to-End Latency) / TRT (Total Response Time)
    - Throughput (tokens per second)
    """
    metrics = {
        "ttft_ms": None,
        "itl_ms_per_token": None,
        "e2e_ms": None,
        "throughput_tokens_per_sec": None,
    }
    
    # Check evaluations object
    evaluations = model_data.get("evaluations", {})
    if not evaluations:
        evaluations = model_data.get("scores", {})
    
    # Check for latency fields in various formats
    # TTFT variations
    ttft_keys = [
        "ttft", "ttft_ms", "time_to_first_token", "tfcr", "tfcr_ms",
        "first_token_latency", "first_token_ms", "latency_ttft"
    ]
    for key in ttft_keys:
        value = evaluations.get(key) or evaluations.get(key.upper()) or evaluations.get(key.lower())
        if value is not None:
            # Convert to milliseconds if needed
            if isinstance(value, (int, float)):
                metrics["ttft_ms"] = float(value) * 1000 if value < 10 else float(value)
                break
    
    # ITL variations
    itl_keys = [
        "itl", "itl_ms", "inter_token_latency", "tpot", "tpot_ms",
        "time_per_output_token", "token_latency", "per_token_latency"
    ]
    for key in itl_keys:
        value = evaluations.get(key) or evaluations.get(key.upper()) or evaluations.get(key.lower())
        if value is not None:
            if isinstance(value, (int, float)):
                metrics["itl_ms_per_token"] = float(value) * 1000 if value < 10 else float(value)
                break
    
    # E2E variations
    e2e_keys = [
        "e2e", "e2e_ms", "end_to_end_latency", "trt", "trt_ms",
        "total_response_time", "total_latency", "response_time"
    ]
    for key in e2e_keys:
        value = evaluations.get(key) or evaluations.get(key.upper()) or evaluations.get(key.lower())
        if value is not None:
            if isinstance(value, (int, float)):
                # Convert seconds to milliseconds if needed
                metrics["e2e_ms"] = float(value) * 1000 if value < 100 else float(value)
                break
    
    # Throughput variations
    throughput_keys = [
        "throughput", "throughput_tps", "tokens_per_second", "tps",
        "generation_speed", "token_rate", "output_rate"
    ]
    for key in throughput_keys:
        value = evaluations.get(key) or evaluations.get(key.upper()) or evaluations.get(key.lower())
        if value is not None:
            if isinstance(value, (int, float)):
                metrics["throughput_tokens_per_sec"] = float(value)
                break
    
    # Also check in model_data root level
    for key in ["ttft", "itl", "e2e", "throughput", "latency", "performance"]:
        if key in model_data:
            value = model_data[key]
            if isinstance(value, dict):
                # Nested structure
                if "ttft" in value and metrics["ttft_ms"] is None:
                    metrics["ttft_ms"] = float(value["ttft"]) * 1000 if value["ttft"] < 10 else float(value["ttft"])
                if "itl" in value and metrics["itl_ms_per_token"] is None:
                    metrics["itl_ms_per_token"] = float(value["itl"]) * 1000 if value["itl"] < 10 else float(value["itl"])
                if "e2e" in value and metrics["e2e_ms"] is None:
                    metrics["e2e_ms"] = float(value["e2e"]) * 1000 if value["e2e"] < 100 else float(value["e2e"])
                if "throughput" in value and metrics["throughput_tokens_per_sec"] is None:
                    metrics["throughput_tokens_per_sec"] = float(value["throughput"])
    
    # Calculate ITL from throughput if available
    if metrics["itl_ms_per_token"] is None and metrics["throughput_tokens_per_sec"] is not None:
        if metrics["throughput_tokens_per_sec"] > 0:
            metrics["itl_ms_per_token"] = 1000.0 / metrics["throughput_tokens_per_sec"]
    
    # Calculate throughput from ITL if available
    if metrics["throughput_tokens_per_sec"] is None and metrics["itl_ms_per_token"] is not None:
        if metrics["itl_ms_per_token"] > 0:
            metrics["throughput_tokens_per_sec"] = 1000.0 / metrics["itl_ms_per_token"]
    
    return metrics

def process_models(api_models: List[Dict]) -> List[Dict]:
    """Process API models and extract latency metrics"""
    processed_models = []
    
    print(f"\nProcessing {len(api_models)} models for latency metrics...")
    
    for i, model in enumerate(api_models, 1):
        model_id = model.get("id", "")
        name = model.get("name", "")
        provider = model.get("model_creator", {}).get("name", "Unknown")
        
        # Extract latency metrics
        metrics = extract_latency_metrics(model)
        
        # Create model entry
        processed_model = {
            "model_id": model_id,
            "model_name": name,
            "provider": provider,
            **metrics
        }
        
        processed_models.append(processed_model)
        
        if i % 50 == 0:
            print(f"  Processed {i}/{len(api_models)} models...")
    
    return processed_models

def export_to_csv(models: List[Dict], filename: str = "model_latency_performance.csv"):
    """Export models with latency metrics to CSV"""
    print(f"\nExporting to {filename}...")
    
    headers = [
        "Model Name", "Provider", "Model ID",
        "TTFT (ms)", "ITL (ms/token)", "E2E (ms)", "Throughput (tokens/sec)"
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        
        for model in models:
            row = [
                model.get("model_name", ""),
                model.get("provider", ""),
                model.get("model_id", ""),
                model.get("ttft_ms") or "",
                model.get("itl_ms_per_token") or "",
                model.get("e2e_ms") or "",
                model.get("throughput_tokens_per_sec") or "",
            ]
            writer.writerow(row)
    
    # Count models with metrics
    with_ttft = sum(1 for m in models if m.get("ttft_ms") is not None)
    with_itl = sum(1 for m in models if m.get("itl_ms_per_token") is not None)
    with_e2e = sum(1 for m in models if m.get("e2e_ms") is not None)
    with_throughput = sum(1 for m in models if m.get("throughput_tokens_per_sec") is not None)
    
    print(f"✓ Exported {len(models)} models to {filename}")
    print(f"  - Models with TTFT: {with_ttft}")
    print(f"  - Models with ITL: {with_itl}")
    print(f"  - Models with E2E: {with_e2e}")
    print(f"  - Models with Throughput: {with_throughput}")

def export_to_json(models: List[Dict], filename: str = "model_latency_performance.json"):
    """Export models with latency metrics to JSON"""
    print(f"\nExporting to {filename}...")
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(models, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Exported {len(models)} models to {filename}")

def main():
    print("=" * 70)
    print("  Fetching Latency & Performance Metrics from Artificial Analysis")
    print("=" * 70)
    
    # Fetch all models
    api_models = fetch_all_models()
    
    if not api_models:
        print("\n❌ Failed to fetch models from API")
        return
    
    print(f"\n✓ Fetched {len(api_models)} models")
    
    # Process models
    processed_models = process_models(api_models)
    
    # Export to CSV and JSON
    export_to_csv(processed_models)
    export_to_json(processed_models)
    
    # Print sample
    print("\n" + "=" * 70)
    print("  Sample Models with Latency Metrics")
    print("=" * 70)
    
    models_with_metrics = [m for m in processed_models if any([
        m.get("ttft_ms"), m.get("itl_ms_per_token"), 
        m.get("e2e_ms"), m.get("throughput_tokens_per_sec")
    ])]
    
    if models_with_metrics:
        print(f"\nFound {len(models_with_metrics)} models with latency metrics:\n")
        for model in models_with_metrics[:10]:
            print(f"  {model['model_name']}")
            if model.get("ttft_ms"):
                print(f"    TTFT: {model['ttft_ms']:.2f} ms")
            if model.get("itl_ms_per_token"):
                print(f"    ITL: {model['itl_ms_per_token']:.2f} ms/token")
            if model.get("e2e_ms"):
                print(f"    E2E: {model['e2e_ms']:.2f} ms")
            if model.get("throughput_tokens_per_sec"):
                print(f"    Throughput: {model['throughput_tokens_per_sec']:.2f} tokens/sec")
            print()
    else:
        print("\n⚠ No models found with latency metrics in API response")
        print("   This may require checking the API documentation for the correct field names")

if __name__ == "__main__":
    main()

