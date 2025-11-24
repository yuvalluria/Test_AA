#!/usr/bin/env python3
"""
Filter CSV to include ONLY actual open-source models
Remove proprietary models like GPT-4, Gemini, o1, o3, etc.
"""
import csv
import json

# Models that are NOT open-source (proprietary)
PROPRIETARY_MODELS = [
    "GPT-4", "GPT-4o", "GPT-4 Turbo", "GPT-4.1", "GPT-4.5", "GPT-3.5",
    "o1", "o1-mini", "o1-pro", "o3", "o3-mini", "o3-pro", "o4-mini",
    "Gemini", "Gemini 1.5", "Gemini 2.0", "Gemini 2.5", "Gemini 3",
    "Gemma 3", "Gemma 2",  # These might be open-source, need to check
    "PALM-2",
    "Claude", "Sonnet",  # Anthropic models
    "Grok 2", "Grok-2", "Grok2",  # Closed Grok models
    "Grok 3", "Grok-3", "Grok3",  # Closed Grok models
]

# Only include models from these providers that are known to be open-source
# OR models with specific naming patterns that indicate open-source
OPEN_SOURCE_INDICATORS = [
    "gpt-oss-",  # OpenAI open-source models
    "Llama", "Meta",
    "Qwen", "Alibaba",
    "DeepSeek",
    "Mistral", "Mixtral", "Codestral", "Devstral", "Magistral", "Ministral", "Pixtral",
    "Gemma",  # Google's open-source models
    "Phi", "Microsoft Azure",  # Microsoft open-source
    "Nous Research", "Hermes", "DeepHermes",
    "NVIDIA", "Nemotron",
    "Z AI", "GLM",
    "Moonshot AI", "Kimi",
    "MiniMax",
    "ByteDance Seed", "Seed", "Doubao",
    "ServiceNow", "Apriel",
    "LG AI Research", "EXAONE", "Exaone",
    "InclusionAI", "Ling", "Ring",
    "Allen Institute for AI", "OLMo", "Molmo", "Tulu3",
    "IBM", "Granite",
    "Upstage", "Solar",
    "xAI", "Grok",  # xAI models are open-source
    "Cohere", "Command", "Aya",
    "AI21 Labs", "Jamba",
    "Liquid AI", "LFM",
    "Snowflake", "Arctic",
    "Databricks", "DBRX",
    "OpenChat",
    "Perplexity", "Sonar",  # Perplexity has some open-source
    "Deep Cogito", "Cogito",
    "Baidu", "ERNIE",  # Need to verify
]

def is_open_source(model_name: str, provider: str) -> bool:
    """Check if a model is actually open-source"""
    model_lower = model_name.lower()
    provider_lower = provider.lower()
    
    # Exclude proprietary models
    for proprietary in PROPRIETARY_MODELS:
        if proprietary.lower() in model_lower:
            return False
    
    # Exclude specific proprietary patterns
    if any(x in model_lower for x in ["gpt-4", "gpt-3.5", "gpt-5", "o1", "o3", "o4"]):
        # Exception: gpt-oss-* models ARE open-source
        if "gpt-oss-" in model_lower:
            return True
        return False
    
    if any(x in model_lower for x in ["gemini", "palm"]):
        return False
    
    if "claude" in model_lower or "sonnet" in model_lower:
        return False
    
    # Exclude closed Grok models (Grok 2, 3) but keep Grok-1 and Grok 4 if open-source
    if any(x in model_lower for x in ["grok 2", "grok-2", "grok2", "grok 3", "grok-3", "grok3"]):
        return False
    
    # Check for open-source indicators
    for indicator in OPEN_SOURCE_INDICATORS:
        if indicator.lower() in model_lower or indicator.lower() in provider_lower:
            return True
    
    # Special cases
    # Grok models from xAI are open-source
    if "grok" in model_lower and "xai" in provider_lower:
        return True
    
    # Gemma models from Google are open-source
    if "gemma" in model_lower and "google" in provider_lower:
        return True
    
    # Phi models from Microsoft are open-source
    if "phi" in model_lower and "microsoft" in provider_lower:
        return True
    
    return False

def filter_csv(input_file: str, output_file: str):
    """Filter CSV to only include open-source models"""
    print(f"Reading {input_file}...")
    
    rows = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        rows = list(reader)
    
    print(f"Total models in input: {len(rows)}")
    
    # Filter for open-source only
    open_source_rows = []
    excluded_count = 0
    
    for row in rows:
        model_name = row.get("Model Name", "")
        provider = row.get("Provider", "")
        
        if is_open_source(model_name, provider):
            open_source_rows.append(row)
        else:
            excluded_count += 1
            if excluded_count <= 10:  # Show first 10 excluded
                print(f"  Excluding: {model_name} ({provider})")
    
    print(f"\n✓ Kept {len(open_source_rows)} open-source models")
    print(f"✗ Excluded {excluded_count} proprietary models")
    
    # Write filtered CSV
    print(f"\nWriting {output_file}...")
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(open_source_rows)
    
    print(f"✓ Saved filtered CSV to {output_file}")
    
    return open_source_rows

def main():
    print("=" * 60)
    print("Filtering Open-Source Models Only")
    print("=" * 60)
    
    # Filter the subject-specific CSV
    filtered_models = filter_csv(
        "opensource_subject_specific.csv",
        "opensource_subject_specific_filtered.csv"
    )
    
    # Also filter the main benchmarks CSV if it exists
    import os
    if os.path.exists("opensource_benchmarks.csv"):
        print("\n" + "=" * 60)
        filter_csv(
            "opensource_benchmarks.csv",
            "opensource_benchmarks_filtered.csv"
        )
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"✓ Filtered CSV: opensource_subject_specific_filtered.csv")
    print(f"✓ Contains only actual open-source models")

if __name__ == "__main__":
    main()




