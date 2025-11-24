#!/usr/bin/env python3
"""
Get best models from JSON use case definition
Accepts JSON with use case and task information
"""
import json
import sys
import argparse
from get_best_models_semantic import (
    get_embedding_model,
    generate_use_case_embeddings,
    get_best_models_for_usecase,
    save_results
)

def process_usecase_json(json_data):
    """
    Process JSON use case definition and return best models
    
    Expected JSON format:
    {
        "use_case": {
            "name": "string",
            "description": "string",
            "task": "string (optional)"
        }
    }
    
    Or simpler format:
    {
        "use_case": "string description",
        "task": "string (optional)"
    }
    """
    if isinstance(json_data, str):
        json_data = json.loads(json_data)
    
    # Handle different JSON formats
    if 'use_case' in json_data:
        use_case_info = json_data['use_case']
        
        # Format 1: Full object with name and description
        if isinstance(use_case_info, dict):
            name = use_case_info.get('name', 'custom_use_case')
            description = use_case_info.get('description', '')
            task = use_case_info.get('task', '') or json_data.get('task', '')
            
            # Combine description and task if both provided
            if task:
                full_description = f"{description} {task}".strip()
            else:
                full_description = description
            
            if not full_description:
                raise ValueError("Must provide 'description' or 'task' in use case JSON")
            
            return {
                "type": "custom",
                "name": name,
                "description": full_description
            }
        
        # Format 2: Simple string
        elif isinstance(use_case_info, str):
            task = json_data.get('task', '')
            if task:
                full_description = f"{use_case_info} {task}".strip()
            else:
                full_description = use_case_info
            
            return {
                "type": "custom",
                "name": "custom_use_case",
                "description": full_description
            }
    
    # Format 3: Direct description
    elif 'description' in json_data:
        task = json_data.get('task', '')
        description = json_data['description']
        if task:
            full_description = f"{description} {task}".strip()
        else:
            full_description = description
        
        return {
            "type": "custom",
            "name": json_data.get('name', 'custom_use_case'),
            "description": full_description
        }
    
    else:
        raise ValueError("JSON must contain 'use_case' or 'description' field")

def get_models_from_json(json_input, output_file=None):
    """
    Get best models from JSON use case definition
    
    Args:
        json_input: JSON string or dict with use case information
        output_file: Optional output CSV file path
    
    Returns:
        Tuple of (models_list, match_info)
    """
    # Process JSON
    usecase_config = process_usecase_json(json_input)
    
    print("=" * 70)
    print("  Use Case Model Recommendation from JSON")
    print("=" * 70)
    print(f"\nUse Case: {usecase_config['name']}")
    print(f"Description: {usecase_config['description']}")
    
    # Initialize semantic matching
    print("\n🔧 Initializing semantic matching system...")
    model = get_embedding_model()
    use_case_embeddings = generate_use_case_embeddings()
    
    # Get best models
    print("🔍 Finding best models...\n")
    models, match_info = get_best_models_for_usecase(usecase_config, use_case_embeddings)
    
    # Save if output file specified
    if output_file:
        save_results(models, output_file, match_info)
    
    return models, match_info

def main():
    parser = argparse.ArgumentParser(
        description='Get best models from JSON use case definition',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
JSON Format Examples:

Format 1 (Full object):
{
  "use_case": {
    "name": "my_task",
    "description": "I need a model for code autocomplete",
    "task": "for my IDE"
  }
}

Format 2 (Simple):
{
  "use_case": "I need a math problem solver",
  "task": "for solving algebra problems"
}

Format 3 (Direct):
{
  "name": "math_solver",
  "description": "I need a math problem solver",
  "task": "for competition math"
}

Usage:
  python3 get_models_from_json.py --json '{"use_case": {"description": "I need code autocomplete"}}'
  python3 get_models_from_json.py --file usecase.json
  python3 get_models_from_json.py --file usecase.json --output results.csv
        """
    )
    parser.add_argument('--json', '-j', type=str, help='JSON string with use case definition')
    parser.add_argument('--file', '-f', type=str, help='JSON file with use case definition')
    parser.add_argument('--output', '-o', type=str, help='Output CSV file (optional)')
    
    args = parser.parse_args()
    
    if not args.json and not args.file:
        parser.print_help()
        sys.exit(1)
    
    # Load JSON
    if args.json:
        json_data = args.json
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
    
    # Get models
    models, match_info = get_models_from_json(json_data, output_file=args.output)
    
    # Display results
    print("\n" + "=" * 70)
    print("  RESULTS")
    print("=" * 70)
    
    if match_info:
        print("\n📊 Use Case Matching:")
        print("-" * 70)
        for usecase, weight in sorted(match_info.items(), key=lambda x: x[1], reverse=True):
            bar_length = int(weight * 50)
            bar = "█" * bar_length + "░" * (50 - bar_length)
            print(f"  {usecase:30s} {bar} {weight*100:5.1f}%")
    
    print("\n🏆 Top 10 Models:")
    print("-" * 70)
    print(f"{'Rank':<6} {'Model Name':<45} {'Score':<10}")
    print("-" * 70)
    
    models_with_scores = [m for m in models if m.get('Use Case Score', 'N/A') != 'N/A']
    
    for i, model in enumerate(models_with_scores[:10], 1):
        model_name = model['Model Name']
        if len(model_name) > 43:
            model_name = model_name[:40] + "..."
        score = model['Use Case Score']
        print(f"{i:<6} {model_name:<45} {score:<10}")
    
    print("\n" + "=" * 70)
    print(f"Total: {len(models)} models ({len(models_with_scores)} with scores)")
    print("=" * 70)
    
    if not args.output:
        print("\n💡 Tip: Use --output filename.csv to save results")

if __name__ == "__main__":
    main()

