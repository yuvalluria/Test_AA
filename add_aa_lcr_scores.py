#!/usr/bin/env python3
"""
Add AA-LCR scores from the website charts to the CSV
Based on the actual website data shown in the user's image
"""
import csv
import json

# Real AA-LCR scores from the website charts
AA_LCR_SCORES = {
    "DeepSeek V3.2 Exp": 0.69,
    "DeepSeek V3.2 Exp (Reasoning)": 0.69,
    "Qwen3 235B A22B 2507": 0.67,
    "Qwen3 235B A22B 2507 (Reasoning)": 0.67,
    "Kimi K2 Thinking": 0.66,
    "MiniMax-M2": 0.61,
    "DeepSeek R1 0528 (May '25)": 0.55,
    "DeepSeek R1 0528": 0.55,
    "GLM-4.6": 0.54,
    "GLM-4.6 (Reasoning)": 0.54,
    "Kimi K2 0905": 0.52,
    "gpt-oss-120B (high)": 0.51,
    "Llama 4 Maverick": 0.46,
    "gpt-oss-20B (high)": 0.34,
    "Llama Nemotron Super 49B v1.5": 0.34,
    "Llama Nemotron Super 49B v1.5 (Reasoning)": 0.34,
    "QwQ 32B": 0.25,
    "QwQ-32B": 0.25,
    "NVIDIA Nemotron Nano 9B V2": 0.21,
    "NVIDIA Nemotron Nano 9B V2 (Reasoning)": 0.21,
    "Apriel-v1.5-15B-Thinker": 0.20,
    "Mistral Small 3.2": 0.17,
    "EXAONE 4.0 32B": 0.14,
    "EXAONE 4.0 32B (Reasoning)": 0.14,
}

def update_csv_with_aa_lcr(input_file: str, output_file: str):
    """Update CSV with AA-LCR scores"""
    print(f"Reading {input_file}...")
    
    # Read CSV
    rows = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)
    
    # Find AA-LCR column index
    try:
        aa_lcr_index = headers.index("AA-LCR")
    except ValueError:
        print("AA-LCR column not found, adding it after MMLU-Pro...")
        mmlu_pro_index = headers.index("MMLU-Pro")
        headers.insert(mmlu_pro_index + 1, "AA-LCR")
        aa_lcr_index = mmlu_pro_index + 1
        # Add empty value for all existing rows
        for i, row in enumerate(rows):
            rows[i] = row[:mmlu_pro_index+1] + ["N/A"] + row[mmlu_pro_index+1:]
    
    # Update rows with AA-LCR scores
    updated_count = 0
    for i, row in enumerate(rows):
        model_name = row[0]  # First column is Model Name
        
        # Check if we have AA-LCR score for this model
        if model_name in AA_LCR_SCORES:
            score = AA_LCR_SCORES[model_name]
            row[aa_lcr_index] = f"{score * 100:.2f}%"
            updated_count += 1
    
    # Write updated CSV
    print(f"Writing {output_file}...")
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    
    print(f"✓ Updated {updated_count} models with AA-LCR scores")
    print(f"✓ Saved to {output_file}")

def update_json_with_aa_lcr():
    """Update JSON file with AA-LCR scores"""
    print("\nUpdating evaluations_data.json...")
    
    with open("evaluations_data.json", "r") as f:
        data = json.load(f)
    
    updated_count = 0
    for model in data.get("models", []):
        model_name = model.get("name", "")
        if model_name in AA_LCR_SCORES:
            if not model.get("scores"):
                model["scores"] = {}
            model["scores"]["aa-lcr"] = AA_LCR_SCORES[model_name]
            updated_count += 1
    
    with open("evaluations_data.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Updated {updated_count} models in JSON file")

if __name__ == "__main__":
    update_csv_with_aa_lcr("model_benchmarks_real.csv", "model_benchmarks_real.csv")
    update_json_with_aa_lcr()
    print("\n✓ All done!")




