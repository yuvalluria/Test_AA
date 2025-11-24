#!/usr/bin/env python3
"""
Interactive Use Case Tester
Type a use case description and get the best models instantly
"""
import sys
import json
from get_best_models_semantic import (
    get_embedding_model,
    generate_use_case_embeddings,
    get_best_models_for_usecase,
    save_results
)

def print_header():
    """Print welcome header"""
    print("=" * 70)
    print("  Use Case Model Recommendation System")
    print("  Semantic Matching with Vector Embeddings")
    print("=" * 70)
    print()

def print_available_usecases():
    """Print available predefined use cases"""
    from get_best_models_semantic import PREDEFINED_USE_CASES
    
    print("Available Predefined Use Cases:")
    print("-" * 70)
    for i, (name, info) in enumerate(PREDEFINED_USE_CASES.items(), 1):
        print(f"  {i}. {name}")
        print(f"     {info['description'][:60]}...")
    print()

def interactive_mode():
    """Interactive mode - ask user for use case"""
    print_header()
    print_available_usecases()
    
    print("Choose an option:")
    print("  1. Use predefined use case (type number or name)")
    print("  2. Describe custom use case (type description)")
    print("  3. Exit")
    print()
    
    choice = input("Your choice (1/2/3): ").strip()
    
    if choice == "3":
        print("\nGoodbye!")
        return None
    
    usecase_config = None
    
    if choice == "1":
        # Predefined use case
        from get_best_models_semantic import PREDEFINED_USE_CASES
        
        usecase_input = input("\nEnter use case name or number: ").strip()
        
        # Try to match by number
        try:
            usecase_num = int(usecase_input)
            usecase_names = list(PREDEFINED_USE_CASES.keys())
            if 1 <= usecase_num <= len(usecase_names):
                usecase_name = usecase_names[usecase_num - 1]
            else:
                print(f"Invalid number. Please choose 1-{len(usecase_names)}")
                return None
        except ValueError:
            # Try to match by name
            usecase_name = usecase_input.lower().replace(" ", "_")
            if usecase_name not in PREDEFINED_USE_CASES:
                print(f"Unknown use case: {usecase_input}")
                print(f"Available: {', '.join(PREDEFINED_USE_CASES.keys())}")
                return None
        
        usecase_config = {
            "type": "predefined",
            "name": usecase_name
        }
        
    elif choice == "2":
        # Custom use case
        print("\nDescribe your use case in natural language:")
        print("(Example: 'I need a model for code autocomplete')")
        description = input("\nYour use case: ").strip()
        
        if not description:
            print("Error: Description cannot be empty")
            return None
        
        usecase_name = input("Name for this use case (optional, press Enter for auto): ").strip()
        if not usecase_name:
            usecase_name = "custom_use_case"
        
        usecase_config = {
            "type": "custom",
            "name": usecase_name,
            "description": description
        }
    else:
        print("Invalid choice")
        return None
    
    return usecase_config

def display_results(models, match_info, usecase_name):
    """Display results in a nice format"""
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
    print(f"{'Rank':<6} {'Model Name':<40} {'Score':<10}")
    print("-" * 70)
    
    models_with_scores = [m for m in models if m.get('Use Case Score', 'N/A') != 'N/A']
    
    for i, model in enumerate(models_with_scores[:10], 1):
        model_name = model['Model Name']
        if len(model_name) > 38:
            model_name = model_name[:35] + "..."
        score = model['Use Case Score']
        print(f"{i:<6} {model_name:<40} {score:<10}")
    
    print("\n" + "=" * 70)
    print(f"Total models: {len(models)} ({len(models_with_scores)} with scores)")
    print("=" * 70)

def main():
    """Main interactive function"""
    try:
        # Get use case configuration
        usecase_config = interactive_mode()
        
        if not usecase_config:
            return
        
        usecase_name = usecase_config.get('name', 'unknown')
        usecase_type = usecase_config.get('type', 'custom')
        
        print("\n" + "=" * 70)
        print(f"  Processing: {usecase_name} ({usecase_type})")
        print("=" * 70)
        
        # Initialize embedding model
        print("\n🔧 Initializing semantic matching system...")
        model = get_embedding_model()
        
        # Generate embeddings for predefined use cases
        print("📊 Generating embeddings...")
        use_case_embeddings = generate_use_case_embeddings()
        
        # Get best models
        print("🔍 Finding best models...")
        models, match_info = get_best_models_for_usecase(usecase_config, use_case_embeddings)
        
        # Display results
        display_results(models, match_info, usecase_name)
        
        # Ask if user wants to save
        save_choice = input("\n💾 Save results to CSV? (y/n): ").strip().lower()
        if save_choice == 'y':
            output_file = f"best_models_{usecase_name}.csv"
            save_results(models, output_file, match_info)
            print(f"\n✅ Saved to {output_file}")
        
        # Ask if user wants to try another
        again = input("\n🔄 Try another use case? (y/n): ").strip().lower()
        if again == 'y':
            print("\n" * 2)
            main()
        else:
            print("\n👋 Thanks for using the system!")
    
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

