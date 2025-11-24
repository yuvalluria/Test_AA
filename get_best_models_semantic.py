#!/usr/bin/env python3
"""
Get best models for a use case using semantic similarity (vector embeddings)
Uses sentence-transformers for semantic matching instead of keyword-based search
"""
import csv
import json
import sys
import argparse
import numpy as np
from typing import List, Dict, Tuple
from collections import Counter

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    print("Error: Required packages not installed.")
    print("Please install: pip install sentence-transformers scikit-learn")
    sys.exit(1)

# Predefined use cases with full descriptions for embedding
PREDEFINED_USE_CASES = {
    'chatbot_conversational': {
        'description': 'Real-time conversational chatbots (short prompts, short responses). Fast interactive dialogue systems for customer service, personal assistants, and chat applications.',
        'csv_file': 'opensource_chatbot_conversational.csv'
    },
    'code_completion': {
        'description': 'Fast code completion/autocomplete (short prompts, short completions). IDE integration for real-time code suggestions, IntelliSense, and code hinting.',
        'csv_file': 'opensource_code_completion.csv'
    },
    'code_generation_detailed': {
        'description': 'Detailed code generation with explanations (medium prompts, long responses). Software development with code explanations, comments, and documentation.',
        'csv_file': 'opensource_code_generation_detailed.csv'
    },
    'translation': {
        'description': 'Document translation (medium prompts, medium responses). Multilingual translation, localization, and language conversion tasks.',
        'csv_file': 'opensource_translation.csv'
    },
    'content_generation': {
        'description': 'Content creation, marketing copy (medium prompts, medium responses). Blog posts, articles, marketing materials, and creative writing.',
        'csv_file': 'opensource_content_generation.csv'
    },
    'summarization_short': {
        'description': 'Short document summarization (medium prompts, short summaries). Brief summaries, executive summaries, and text condensation.',
        'csv_file': 'opensource_summarization_short.csv'
    },
    'document_analysis_rag': {
        'description': 'RAG-based document Q&A (long prompts with context, medium responses). Retrieval-augmented generation for answering questions from documents, knowledge bases, and document search.',
        'csv_file': 'opensource_document_analysis_rag.csv'
    },
    'long_document_summarization': {
        'description': 'Long document summarization (very long prompts, medium summaries). Processing extensive documents, research papers, and large text files to extract key points.',
        'csv_file': 'opensource_long_document_summarization.csv'
    },
    'research_legal_analysis': {
        'description': 'Research/legal document analysis (very long prompts, detailed analysis). Academic research, legal document review, scholarly analysis, and in-depth document examination.',
        'csv_file': 'opensource_research_legal_analysis.csv'
    }
}

# Embedding model configuration
EMBEDDING_MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'
EMBEDDING_MODEL = None

def get_embedding_model():
    """Get or initialize the embedding model"""
    global EMBEDDING_MODEL
    if EMBEDDING_MODEL is None:
        print(f"\nLoading embedding model: {EMBEDDING_MODEL_NAME}")
        print("  Model: all-MiniLM-L6-v2 (80MB, optimized for semantic similarity)")
        print("  First load may take a moment...")
        EMBEDDING_MODEL = SentenceTransformer(EMBEDDING_MODEL_NAME)
        print("  ✓ Model loaded successfully")
    return EMBEDDING_MODEL

def generate_use_case_embeddings():
    """Generate embeddings for all predefined use case descriptions"""
    model = get_embedding_model()
    
    use_case_texts = []
    use_case_names = []
    
    for name, info in PREDEFINED_USE_CASES.items():
        use_case_texts.append(info['description'])
        use_case_names.append(name)
    
    print(f"\nGenerating embeddings for {len(use_case_texts)} predefined use cases...")
    embeddings = model.encode(use_case_texts, show_progress_bar=True)
    
    return dict(zip(use_case_names, embeddings))

def calculate_semantic_similarity(user_description: str, use_case_embeddings: Dict[str, np.ndarray]) -> List[Tuple[str, float]]:
    """Calculate cosine similarity between user description and all use case embeddings"""
    model = get_embedding_model()
    
    # Generate embedding for user description
    user_embedding = model.encode([user_description], show_progress_bar=False)
    user_embedding = user_embedding[0].reshape(1, -1)
    
    # Calculate cosine similarity with all use cases
    similarities = []
    
    for usecase_name, usecase_embedding in use_case_embeddings.items():
        usecase_embedding_2d = usecase_embedding.reshape(1, -1)
        similarity = cosine_similarity(user_embedding, usecase_embedding_2d)[0][0]
        similarities.append((usecase_name, float(similarity)))
    
    # Sort by similarity (descending)
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    return similarities

def load_models_from_csv(csv_file: str) -> List[Dict]:
    """Load models from a use case CSV file"""
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        print(f"Warning: {csv_file} not found.")
        return []

def parse_score(score_str: str) -> float:
    """Parse score string to float"""
    if score_str == 'N/A' or not score_str:
        return 0.0
    try:
        return float(score_str.replace('%', '')) / 100.0
    except (ValueError, AttributeError):
        return 0.0

def combine_model_scores_weighted(models_list: List[List[Dict]], weights: List[float]) -> List[Dict]:
    """Combine scores from multiple use case CSVs with weighted averaging"""
    # Normalize weights to sum to 1.0
    total_weight = sum(weights)
    if total_weight == 0:
        weights = [1.0 / len(models_list)] * len(models_list)
    else:
        weights = [w / total_weight for w in weights]
    
    # Create a model map
    model_map = {}
    
    for models, weight in zip(models_list, weights):
        for model in models:
            model_name = model['Model Name']
            provider = model['Provider']
            dataset = model['Dataset']
            key = (model_name, provider, dataset)
            
            # Parse score
            score = parse_score(model.get('Use Case Score', 'N/A'))
            
            if key not in model_map:
                model_map[key] = {
                    'Model Name': model_name,
                    'Provider': provider,
                    'Dataset': dataset,
                    'weighted_score': 0.0,
                    'total_weight': 0.0
                }
            
            # Weighted average
            model_map[key]['weighted_score'] += score * weight
            model_map[key]['total_weight'] += weight
    
    # Convert to list and calculate final scores
    combined_models = []
    for key, model_data in model_map.items():
        if model_data['total_weight'] > 0:
            # Normalize by actual weight sum
            final_score = model_data['weighted_score'] / model_data['total_weight']
            model_data['Use Case Score'] = f"{final_score * 100:.2f}%"
        else:
            model_data['Use Case Score'] = 'N/A'
        
        del model_data['weighted_score']
        del model_data['total_weight']
        combined_models.append(model_data)
    
    # Sort by score (descending)
    combined_models.sort(
        key=lambda x: parse_score(x['Use Case Score']), 
        reverse=True
    )
    
    return combined_models

def get_best_models_for_usecase(usecase_config: Dict, use_case_embeddings: Dict[str, np.ndarray]) -> Tuple[List[Dict], Dict]:
    """Get best models for a use case configuration using semantic similarity"""
    usecase_type = usecase_config.get('type', 'predefined')
    usecase_name = usecase_config.get('name', '')
    description = usecase_config.get('description', '')
    
    if usecase_type == 'predefined':
        # Direct match to predefined use case
        if usecase_name not in PREDEFINED_USE_CASES:
            raise ValueError(f"Unknown predefined use case: {usecase_name}. Available: {list(PREDEFINED_USE_CASES.keys())}")
        
        csv_file = PREDEFINED_USE_CASES[usecase_name]['csv_file']
        models = load_models_from_csv(csv_file)
        
        if not models:
            raise FileNotFoundError(f"CSV file {csv_file} not found. Please run create_usecase_scores.py first.")
        
        return models, {usecase_name: 1.0}
    
    elif usecase_type == 'custom':
        # Use semantic similarity to find best matches
        if not description:
            raise ValueError("Custom use case must provide a 'description' field")
        
        print(f"\nAnalyzing custom use case using semantic similarity...")
        print(f"  Description: {description}")
        
        # Calculate semantic similarities
        similarities = calculate_semantic_similarity(description, use_case_embeddings)
        
        print(f"\n  Semantic similarity scores:")
        for i, (match_name, score) in enumerate(similarities, 1):
            print(f"    {i}. {match_name}: {score:.3f} ({score*100:.1f}%)")
        
        # Use all similarities as weights (they're already normalized by cosine similarity)
        # But we'll use a threshold to only include relevant matches
        threshold = 0.3  # Minimum similarity to include
        
        relevant_matches = [(name, score) for name, score in similarities if score >= threshold]
        
        if not relevant_matches:
            # If no matches above threshold, use top 3 anyway
            print(f"  → No matches above {threshold} threshold, using top 3 matches")
            relevant_matches = similarities[:3]
        else:
            print(f"  → Using {len(relevant_matches)} matches above {threshold} threshold")
        
        # Load models from relevant use cases
        models_list = []
        weights = []
        match_info = {}
        
        for match_name, similarity_score in relevant_matches:
            csv_file = PREDEFINED_USE_CASES[match_name]['csv_file']
            models = load_models_from_csv(csv_file)
            if models:
                models_list.append(models)
                weights.append(similarity_score)
                match_info[match_name] = similarity_score
        
        if not models_list:
            raise ValueError("No matching use cases found. Please provide a more descriptive use case.")
        
        # Combine with weighted scores
        combined_models = combine_model_scores_weighted(models_list, weights)
        
        return combined_models, match_info
    
    else:
        raise ValueError(f"Unknown use case type: {usecase_type}. Must be 'predefined' or 'custom'")

def save_results(models: List[Dict], output_file: str, match_info: Dict = None):
    """Save results to CSV"""
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        if models:
            writer = csv.DictWriter(f, fieldnames=['Model Name', 'Provider', 'Dataset', 'Use Case Score'])
            writer.writeheader()
            writer.writerows(models)
        else:
            writer = csv.writer(f)
            writer.writerow(['Model Name', 'Provider', 'Dataset', 'Use Case Score'])
    
    print(f"\n✓ Saved results to {output_file}")
    print(f"  Total models: {len(models)}")
    
    # Show top 10
    models_with_scores = [m for m in models if m.get('Use Case Score', 'N/A') != 'N/A']
    print(f"  Models with scores: {len(models_with_scores)}")
    
    if match_info:
        print(f"\n  Use case weights used:")
        for usecase, weight in sorted(match_info.items(), key=lambda x: x[1], reverse=True):
            print(f"    - {usecase}: {weight:.3f} ({weight*100:.1f}%)")
    
    print(f"\n  Top 10 models:")
    for i, model in enumerate(models_with_scores[:10], 1):
        print(f"    {i}. {model['Model Name']} ({model['Provider']}): {model['Use Case Score']}")

def process_json_config(config_file=None, json_string=None):
    """Process JSON configuration"""
    if json_string:
        config_data = json.loads(json_string)
    elif config_file:
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
    else:
        raise ValueError("Must provide either config_file or json_string")
    
    # Handle single or multiple use cases
    if 'use_case' in config_data:
        return [config_data['use_case']]
    elif 'use_cases' in config_data:
        return config_data['use_cases']
    else:
        raise ValueError("JSON config must contain 'use_case' or 'use_cases' key")

def print_model_info():
    """Print information about the embedding model used"""
    print("=" * 60)
    print("Semantic Similarity Model Information")
    print("=" * 60)
    print(f"Model: {EMBEDDING_MODEL_NAME}")
    print("\nWhy this model?")
    print("  ✓ Optimized for semantic similarity tasks")
    print("  ✓ Small and fast (80MB, ~22M parameters)")
    print("  ✓ Based on MiniLM architecture (distilled from larger models)")
    print("  ✓ Trained on 1B+ sentence pairs")
    print("  ✓ Excellent performance on semantic similarity benchmarks")
    print("  ✓ Perfect balance of speed and accuracy for this use case")
    print("\nHow it works:")
    print("  1. Converts text descriptions to 384-dimensional vectors")
    print("  2. Uses cosine similarity to measure semantic closeness")
    print("  3. Higher similarity = more semantically similar use cases")
    print("  4. Similarity scores become weights for combining CSV results")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(
        description='Get best models for a use case using semantic similarity (vector embeddings)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Predefined use case
  python3 get_best_models_semantic.py --config usecase_config.json

  # Custom use case (semantic matching)
  python3 get_best_models_semantic.py --json '{"use_case": {"type": "custom", "name": "my_task", "description": "I need a model for code autocomplete"}}'

JSON Format:
  {
    "use_case": {
      "type": "predefined" | "custom",
      "name": "string",
      "description": "string (required for custom)"
    }
  }
        """
    )
    parser.add_argument('--config', '-c', type=str, help='Path to JSON configuration file')
    parser.add_argument('--json', '-j', type=str, help='JSON configuration as string')
    parser.add_argument('--output', '-o', type=str, help='Output CSV file (default: best_models_{usecase_name}.csv)')
    parser.add_argument('--model-info', action='store_true', help='Show information about the embedding model')
    
    args = parser.parse_args()
    
    if args.model_info:
        print_model_info()
        return
    
    if not args.config and not args.json:
        parser.print_help()
        sys.exit(1)
    
    print("=" * 60)
    print("Getting Best Models Using Semantic Similarity")
    print("=" * 60)
    
    # Generate embeddings for all predefined use cases (cached after first call)
    use_case_embeddings = generate_use_case_embeddings()
    
    # Process configuration
    usecase_configs = process_json_config(config_file=args.config, json_string=args.json)
    
    for usecase_config in usecase_configs:
        usecase_name = usecase_config.get('name', 'unknown')
        usecase_type = usecase_config.get('type', 'predefined')
        
        print(f"\n{'='*60}")
        print(f"Processing: {usecase_name} ({usecase_type})")
        print(f"{'='*60}")
        
        # Get best models
        models, match_info = get_best_models_for_usecase(usecase_config, use_case_embeddings)
        
        # Determine output file
        if args.output:
            output_file = args.output
        else:
            output_file = f"best_models_{usecase_name}.csv"
        
        # Save results
        save_results(models, output_file, match_info)
    
    print("\n" + "=" * 60)
    print("Complete!")
    print("=" * 60)
    print(f"\nEmbedding model used: {EMBEDDING_MODEL_NAME}")
    print("Run with --model-info to see detailed model information")

if __name__ == "__main__":
    main()

