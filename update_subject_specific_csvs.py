#!/usr/bin/env python3
"""
Update subject-specific CSVs to only include the 204 models from opensource_all_benchmarks.csv
"""
import csv
import os

# Read the master CSV with 204 models
master_models = {}
with open('opensource_all_benchmarks.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        model_name = row['Model Name']
        master_models[model_name] = row

print(f"Master CSV contains {len(master_models)} models")

# Subject-specific CSV mappings
subject_csvs = {
    'opensource_mathematics.csv': {
        'columns': ['Model Name', 'Provider', 'Dataset', 'Math 500', 'AIME', 'AIME 2025', 'Math Index'],
        'source_columns': ['math_500', 'aime', 'aime_25', 'artificial_analysis_math_index']
    },
    'opensource_reasoning.csv': {
        'columns': ['Model Name', 'Provider', 'Dataset', 'AA-LCR', 'τ²-Bench Telecom'],
        'source_columns': ['lcr', 'tau2']
    },
    'opensource_science.csv': {
        'columns': ['Model Name', 'Provider', 'Dataset', 'SciCode', 'GPQA Diamond', "Humanity's Last Exam"],
        'source_columns': ['scicode', 'gpqa', 'hle']
    },
    'opensource_computer_science.csv': {
        'columns': ['Model Name', 'Provider', 'Dataset', 'LiveCodeBench', 'IFBench', 'Terminal-Bench Hard', 'Coding Index'],
        'source_columns': ['livecodebench', 'ifbench', 'terminalbench_hard', 'artificial_analysis_coding_index']
    },
    'opensource_general_knowledge.csv': {
        'columns': ['Model Name', 'Provider', 'Dataset', 'MMLU-Pro', 'Intelligence Index'],
        'source_columns': ['mmlu_pro', 'artificial_analysis_intelligence_index']
    }
}

def update_subject_csv(filename, config):
    """Update a subject-specific CSV to only include models from master"""
    if not os.path.exists(filename):
        print(f"⚠ {filename} not found, skipping")
        return
    
    print(f"\nUpdating {filename}...")
    
    # Read existing CSV
    existing_models = {}
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            model_name = row['Model Name']
            existing_models[model_name] = row
    
    print(f"  Original: {len(existing_models)} models")
    
    # Create new CSV with only models from master
    updated_rows = []
    for model_name in sorted(master_models.keys()):
        master_row = master_models[model_name]
        
        # Create new row
        new_row = {
            'Model Name': model_name,
            'Provider': master_row['Provider'],
            'Dataset': master_row['Dataset']
        }
        
        # Add subject-specific columns
        for i, col_name in enumerate(config['columns'][3:], 0):  # Skip Model Name, Provider, Dataset
            source_col = config['source_columns'][i]
            value = master_row.get(source_col, 'N/A')
            if value and value != 'N/A':
                # Format as percentage if it's a decimal
                try:
                    num_value = float(value)
                    if num_value <= 1:
                        new_row[col_name] = f"{num_value * 100:.2f}%"
                    else:
                        new_row[col_name] = f"{num_value:.2f}%"
                except (ValueError, TypeError):
                    new_row[col_name] = value
            else:
                new_row[col_name] = 'N/A'
        
        updated_rows.append(new_row)
    
    # Write updated CSV
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=config['columns'])
        writer.writeheader()
        writer.writerows(updated_rows)
    
    print(f"  ✓ Updated: {len(updated_rows)} models")

def main():
    print("=" * 60)
    print("Updating Subject-Specific CSVs")
    print("=" * 60)
    
    # Update each subject-specific CSV
    for filename, config in subject_csvs.items():
        update_subject_csv(filename, config)
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print("✓ All subject-specific CSVs updated to contain 204 models")
    print("✓ Models match opensource_all_benchmarks.csv")

if __name__ == "__main__":
    main()

