#!/usr/bin/env python3
"""
Get best models for a use case based on existing CSV files
Automatically matches custom use cases to predefined ones using semantic analysis
"""
import csv
import json
import sys
import argparse
from typing import List, Dict, Tuple
from collections import Counter

# Predefined use cases with keywords for matching
PREDEFINED_USE_CASES = {
    'chatbot_conversational': {
        'description': 'Real-time conversational chatbots (short prompts, short responses)',
        'keywords': ['chatbot', 'conversation', 'chat', 'dialogue', 'conversational', 'real-time', 'short response', 'interactive'],
        'csv_file': 'opensource_chatbot_conversational.csv'
    },
    'code_completion': {
        'description': 'Fast code completion/autocomplete (short prompts, short completions)',
        'keywords': ['code completion', 'autocomplete', 'code suggestion', 'intellisense', 'code hint', 'fast completion'],
        'csv_file': 'opensource_code_completion.csv'
    },
    'code_generation_detailed': {
        'description': 'Detailed code generation with explanations (medium prompts, long responses)',
        'keywords': ['code generation', 'code writing', 'programming', 'software development', 'detailed code', 'code explanation', 'code with comments'],
        'csv_file': 'opensource_code_generation_detailed.csv'
    },
    'translation': {
        'description': 'Document translation (medium prompts, medium responses)',
        'keywords': ['translation', 'translate', 'language translation', 'multilingual', 'localization', 'document translation'],
        'csv_file': 'opensource_translation.csv'
    },
    'content_generation': {
        'description': 'Content creation, marketing copy (medium prompts, medium responses)',
        'keywords': ['content generation', 'content creation', 'writing', 'copywriting', 'marketing', 'blog', 'article', 'creative writing'],
        'csv_file': 'opensource_content_generation.csv'
    },
    'summarization_short': {
        'description': 'Short document summarization (medium prompts, short summaries)',
        'keywords': ['summarization', 'summary', 'summarize', 'brief summary', 'short summary', 'document summary', 'text summary'],
        'csv_file': 'opensource_summarization_short.csv'
    },
    'document_analysis_rag': {
        'description': 'RAG-based document Q&A (long prompts with context, medium responses)',
        'keywords': ['rag', 'document q&a', 'document question', 'document analysis', 'retrieval', 'qa', 'question answering', 'document search', 'answer questions', 'q&a', 'question answer'],
        'csv_file': 'opensource_document_analysis_rag.csv'
    },
    'long_document_summarization': {
        'description': 'Long document summarization (very long prompts, medium summaries)',
        'keywords': ['long document', 'long text', 'extensive document', 'large document', 'document summarization', 'long summary'],
        'csv_file': 'opensource_long_document_summarization.csv'
    },
    'research_legal_analysis': {
        'description': 'Research/legal document analysis (very long prompts, detailed analysis)',
        'keywords': ['research', 'legal', 'analysis', 'document analysis', 'research paper', 'legal document', 'academic', 'scholarly'],
        'csv_file': 'opensource_research_legal_analysis.csv'
    }
}

def calculate_similarity(text: str, keywords: List[str]) -> float:
    """Calculate similarity score between text and keywords"""
    text_lower = text.lower()
    
    # Count keyword matches (partial matches count too)
    matches = 0
    for keyword in keywords:
        keyword_lower = keyword.lower()
        # Exact match
        if keyword_lower in text_lower:
            matches += 1
        # Partial match (check if key parts of keyword are in text)
        else:
            # Split keyword and check if parts match
            keyword_parts = keyword_lower.split()
            if len(keyword_parts) > 1:
                # If multiple words, check if at least one word matches
                if any(part in text_lower for part in keyword_parts if len(part) > 3):
                    matches += 0.5
    
    # Also check reverse - if text words are in keywords
    text_words = [w for w in text_lower.split() if len(w) > 3]
    for word in text_words:
        if any(word in kw.lower() or kw.lower() in word for kw in keywords):
            matches += 0.3
    
    # Normalize by number of keywords, but cap at 1.0
    similarity = min(matches / len(keywords) if keywords else 0.0, 1.0)
    return similarity

def find_best_matching_usecases(description: str, top_n: int = 3) -> List[Tuple[str, float]]:
    """Find the most similar predefined use cases based on description"""
    similarities = []
    
    for usecase_name, usecase_info in PREDEFINED_USE_CASES.items():
        # Check description similarity
        desc_similarity = calculate_similarity(description, usecase_info['keywords'])
        
        # Also check if use case name appears in description
        name_similarity = 1.0 if usecase_name.replace('_', ' ') in description.lower() else 0.0
        
        # Combined score (weight name match higher)
        combined_score = (name_similarity * 0.7) + (desc_similarity * 0.3)
        
        similarities.append((usecase_name, combined_score))
    
    # Sort by similarity (descending)
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    # Return top N matches
    return similarities[:top_n]

def load_models_from_csv(csv_file: str) -> List[Dict]:
    """Load models from a use case CSV file"""
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        print(f"Warning: {csv_file} not found. Generating it first...")
        return []

def combine_model_scores(models_list: List[List[Dict]], weights: List[float] = None) -> List[Dict]:
    """Combine scores from multiple use case CSVs"""
    if weights is None:
        # Equal weights
        weights = [1.0 / len(models_list)] * len(models_list)
    
    # Normalize weights
    total_weight = sum(weights)
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
            score_str = model.get('Use Case Score', 'N/A')
            if score_str != 'N/A':
                try:
                    score = float(score_str.replace('%', '')) / 100.0
                except (ValueError, AttributeError):
                    score = 0.0
            else:
                score = 0.0
            
            if key not in model_map:
                model_map[key] = {
                    'Model Name': model_name,
                    'Provider': provider,
                    'Dataset': dataset,
                    'raw_score': 0.0,
                    'weight_sum': 0.0
                }
            
            # Weighted average
            model_map[key]['raw_score'] += score * weight
            model_map[key]['weight_sum'] += weight
    
    # Convert to list and normalize
    combined_models = []
    for key, model_data in model_map.items():
        if model_data['weight_sum'] > 0:
            # Normalize by actual weight sum (in case some models missing from some CSVs)
            normalized_score = model_data['raw_score'] / model_data['weight_sum']
            model_data['Use Case Score'] = f"{normalized_score * 100:.2f}%"
        else:
            model_data['Use Case Score'] = 'N/A'
        
        del model_data['raw_score']
        del model_data['weight_sum']
        combined_models.append(model_data)
    
    # Sort by score
    combined_models.sort(key=lambda x: float(x['Use Case Score'].replace('%', '')) if x['Use Case Score'] != 'N/A' else 0.0, reverse=True)
    
    return combined_models

def get_best_models_for_usecase(usecase_config: Dict) -> List[Dict]:
    """Get best models for a use case configuration"""
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
        
        return models
    
    elif usecase_type == 'custom':
        # Find best matching predefined use cases
        if not description:
            raise ValueError("Custom use case must provide a 'description' field")
        
        print(f"\nAnalyzing custom use case: {description}")
        matches = find_best_matching_usecases(description, top_n=3)
        
        print(f"  Top matches:")
        for i, (match_name, score) in enumerate(matches, 1):
            print(f"    {i}. {match_name} (similarity: {score:.2%})")
        
        # Use the best match if similarity is high enough, otherwise combine top matches
        best_match_name, best_score = matches[0]
        
        if best_score >= 0.15:  # Lower threshold for good match
            print(f"  → Using best match: {best_match_name}")
            csv_file = PREDEFINED_USE_CASES[best_match_name]['csv_file']
            models = load_models_from_csv(csv_file)
            
            if not models:
                raise FileNotFoundError(f"CSV file {csv_file} not found. Please run create_usecase_scores.py first.")
            
            return models
        else:
            # Combine top 2-3 matches with weighted scores
            print(f"  → Combining top {min(3, len(matches))} matches")
            models_list = []
            weights = []
            
            for match_name, score in matches[:3]:
                if score > 0.05:  # Lower threshold - include if any similarity
                    csv_file = PREDEFINED_USE_CASES[match_name]['csv_file']
                    models = load_models_from_csv(csv_file)
                    if models:
                        models_list.append(models)
                        weights.append(max(score, 0.1))  # Minimum weight of 0.1
            
            if not models_list:
                # Fallback: use the best match anyway, even if score is low
                print(f"  → Using best match as fallback: {best_match_name}")
                csv_file = PREDEFINED_USE_CASES[best_match_name]['csv_file']
                models = load_models_from_csv(csv_file)
                if not models:
                    raise FileNotFoundError(f"CSV file {csv_file} not found. Please run create_usecase_scores.py first.")
                return models
            
            return combine_model_scores(models_list, weights)
    
    else:
        raise ValueError(f"Unknown use case type: {usecase_type}. Must be 'predefined' or 'custom'")

def save_results(models: List[Dict], output_file: str):
    """Save results to CSV"""
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        if models:
            writer = csv.DictWriter(f, fieldnames=['Model Name', 'Provider', 'Dataset', 'Use Case Score'])
            writer.writeheader()
            writer.writerows(models)
        else:
            writer = csv.writer(f)
            writer.writerow(['Model Name', 'Provider', 'Dataset', 'Use Case Score'])
    
    print(f"✓ Saved results to {output_file}")
    print(f"  Total models: {len(models)}")
    
    # Show top 10
    models_with_scores = [m for m in models if m.get('Use Case Score', 'N/A') != 'N/A']
    print(f"  Models with scores: {len(models_with_scores)}")
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

def main():
    parser = argparse.ArgumentParser(
        description='Get best models for a use case based on existing CSV files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Predefined use case
  python3 get_best_models.py --config usecase_config.json

  # Custom use case (auto-matches to predefined)
  python3 get_best_models.py --json '{"use_case": {"type": "custom", "name": "my_task", "description": "I need a model for code autocomplete"}}'

JSON Format:
  {
    "use_case": {
      "type": "predefined" | "custom",
      "name": "string",
      "description": "string (required for custom)"
    }
  }

Predefined use cases:
  - chatbot_conversational
  - code_completion
  - code_generation_detailed
  - translation
  - content_generation
  - summarization_short
  - document_analysis_rag
  - long_document_summarization
  - research_legal_analysis
        """
    )
    parser.add_argument('--config', '-c', type=str, help='Path to JSON configuration file')
    parser.add_argument('--json', '-j', type=str, help='JSON configuration as string')
    parser.add_argument('--output', '-o', type=str, help='Output CSV file (default: best_models_{usecase_name}.csv)')
    
    args = parser.parse_args()
    
    if not args.config and not args.json:
        parser.print_help()
        sys.exit(1)
    
    print("=" * 60)
    print("Getting Best Models for Use Case")
    print("=" * 60)
    
    # Process configuration
    usecase_configs = process_json_config(config_file=args.config, json_string=args.json)
    
    for usecase_config in usecase_configs:
        usecase_name = usecase_config.get('name', 'unknown')
        usecase_type = usecase_config.get('type', 'predefined')
        
        print(f"\n{'='*60}")
        print(f"Processing: {usecase_name} ({usecase_type})")
        print(f"{'='*60}")
        
        # Get best models
        models = get_best_models_for_usecase(usecase_config)
        
        # Determine output file
        if args.output:
            output_file = args.output
        else:
            output_file = f"best_models_{usecase_name}.csv"
        
        # Save results
        save_results(models, output_file)
    
    print("\n" + "=" * 60)
    print("Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()

