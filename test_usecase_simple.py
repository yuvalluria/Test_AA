#!/usr/bin/env python3
"""
Simple Use Case Tester - Quick test script
Just modify the description below and run
"""
from get_best_models_semantic import (
    get_embedding_model,
    generate_use_case_embeddings,
    get_best_models_for_usecase
)

# ============================================
# MODIFY THIS SECTION
# ============================================

# Option 1: Use predefined use case
USECASE_CONFIG = {
    "type": "predefined",
    "name": "code_completion"
}

# Option 2: Use custom use case (uncomment to use)
# USECASE_CONFIG = {
#     "type": "custom",
#     "name": "my_task",
#     "description": "I need a model for code autocomplete and fast code suggestions"
# }

# ============================================
# RUN THE SCRIPT
# ============================================

if __name__ == "__main__":
    print("=" * 70)
    print("  Use Case Model Recommendation")
    print("=" * 70)
    
    usecase_name = USECASE_CONFIG.get('name', 'unknown')
    usecase_type = USECASE_CONFIG.get('type', 'custom')
    
    print(f"\nUse Case: {usecase_name} ({usecase_type})")
    
    if usecase_type == 'custom':
        print(f"Description: {USECASE_CONFIG.get('description', 'N/A')}")
    
    print("\nInitializing...")
    
    # Initialize
    model = get_embedding_model()
    use_case_embeddings = generate_use_case_embeddings()
    
    # Get best models
    print("Finding best models...\n")
    models, match_info = get_best_models_for_usecase(USECASE_CONFIG, use_case_embeddings)
    
    # Display results
    print("=" * 70)
    print("  TOP 10 MODELS")
    print("=" * 70)
    
    if match_info:
        print("\nUse Case Weights:")
        for usecase, weight in sorted(match_info.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {usecase}: {weight*100:.1f}%")
    
    print("\nRank | Model Name                                    | Score")
    print("-" * 70)
    
    models_with_scores = [m for m in models if m.get('Use Case Score', 'N/A') != 'N/A']
    
    for i, model in enumerate(models_with_scores[:10], 1):
        model_name = model['Model Name']
        if len(model_name) > 40:
            model_name = model_name[:37] + "..."
        score = model['Use Case Score']
        print(f"{i:4d} | {model_name:<45} | {score}")
    
    print("\n" + "=" * 70)
    print(f"Total: {len(models)} models ({len(models_with_scores)} with scores)")

