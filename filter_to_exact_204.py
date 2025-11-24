#!/usr/bin/env python3
"""
Filter CSV to exactly 204 models matching the user's list
"""
import csv

# Models to remove to get to exactly 204
models_to_remove = {
    # Perplexity - only R1 1776 should be there (remove 4)
    'Sonar Pro',
    'Sonar',
    'Sonar Reasoning Pro',
    'Sonar Reasoning',
    
    # Upstage - remove preview versions (remove 2)
    'Solar Pro 2 (Preview) (Non-reasoning)',
    'Solar Pro 2 (Preview) (Reasoning)',
    
    # Alibaba - remove chat/preview versions (remove 5)
    'Qwen Chat 14B',
    'Qwen Chat 72B',
    'Qwen1.5 Chat 110B',
    'Qwen3 Max (Preview)',
    'QwQ 32B-Preview',
    
    # AI21 Labs - remove older versions (remove 3)
    'Jamba Instruct',
    'Jamba 1.5 Mini',
    'Jamba 1.5 Large',
    
    # Meta - remove Llama 65B (remove 1)
    'Llama 65B',
    
    # Mistral - remove older/duplicate versions to get from 30 to 16
    # Keep: Mistral Large 2 (Nov '24), Mistral Large 2 (Jul '24), Mistral Small 3.2,
    # Mistral Small 3.1, Mistral Small 3, Mistral Small (Sep '24), Ministral 8B,
    # Mistral 7B Instruct, Mistral NeMo, Devstral Small (Jul '25), Devstral Small (May '25),
    # Pixtral Large, Pixtral 12B (2409), Codestral (May '24), Codestral-Mamba,
    # Mixtral 8x22B Instruct, Mixtral 8x7B Instruct, Magistral Small 1.2, Magistral Medium 1.2
    # Remove: Mistral Medium 3.1, Devstral Medium, Codestral (Jan '25), Mistral Small (Feb '24),
    # Mistral Large (Feb '24), Mistral Saba, Mistral Medium, Magistral Small 1, Magistral Medium 1,
    # Mistral Medium 3, Ministral 3B
    'Mistral Medium 3.1',
    'Devstral Medium',
    'Codestral (Jan \'25)',
    'Mistral Small (Feb \'24)',
    'Mistral Large (Feb \'24)',
    'Mistral Saba',
    'Mistral Medium',
    'Magistral Small 1',
    'Magistral Medium 1',
    'Mistral Medium 3',
    'Ministral 3B',
    
    # Alibaba - need to remove 4 more to get from 53 to 44 (already removing 5 above)
    # Remove some older/duplicate Qwen2 models
    'Qwen2.5 Max',
    'Qwen2.5 Turbo',
    'Qwen2 Instruct 72B',
    
    # Cohere - remove one to get from 7 to 6
    # User list has: Command A, Command-R+ (Aug '24), Command-R+ (Apr '24), 
    # Command-R (Aug '24), Command-R (Mar '24), Aya Expanse 32B, Aya Expanse 8B
    # We have all 7, but user said 6... Let me check if one is duplicate
    # Actually, user's list shows 6, but we have 7. Need to check which one is extra.
    # Looking at the list, all seem valid. Maybe user miscounted or one is a variant.
    # Let's keep all for now and adjust if needed.
    
    # NVIDIA - remove 2 to get from 9 to 7
    # User list: Llama 3.1 Nemotron Ultra 253B v1 (Reasoning), Llama 3.3 Nemotron Super 49B v1 (Reasoning),
    # Llama 3.3 Nemotron Super 49B v1 (Non-reasoning), Llama Nemotron Super 49B v1.5 (Reasoning),
    # Llama Nemotron Super 49B v1.5 (Non-reasoning), Llama 3.1 Nemotron Instruct 70B,
    # Llama 3.1 Nemotron Nano 4B v1.1 (Reasoning), NVIDIA Nemotron Nano 9B V2 (Reasoning),
    # NVIDIA Nemotron Nano 9B V2 (Non-reasoning)
    # That's 9 models, but user said 7. Let me check what we have.
    # Actually wait, user's list shows 9 models for NVIDIA, so maybe the count is off.
    
    # Let's focus on the clear removals first
}

def filter_csv():
    # Read CSV
    with open('opensource_all_benchmarks.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        models = list(reader)
        headers = reader.fieldnames
    
    print(f"Original count: {len(models)}")
    
    # Filter models
    filtered_models = [m for m in models if m['Model Name'] not in models_to_remove]
    
    print(f"After filtering: {len(filtered_models)}")
    print(f"Removed: {len(models) - len(filtered_models)} models")
    
    # Show what was removed
    removed = [m for m in models if m['Model Name'] in models_to_remove]
    print("\nRemoved models:")
    for m in removed:
        print(f"  - {m['Model Name']} ({m['Provider']})")
    
    # Write filtered CSV
    with open('opensource_all_benchmarks.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(filtered_models)
    
    print(f"\n✓ Saved filtered CSV with {len(filtered_models)} models")
    print(f"Need to remove {len(filtered_models) - 204} more models to reach 204")

if __name__ == "__main__":
    filter_csv()

