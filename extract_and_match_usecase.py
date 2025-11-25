#!/usr/bin/env python3
"""
Extract use case information from plain text and match to best predefined use case
Uses semantic matching with sentence-transformers/all-MiniLM-L6-v2
"""
import json
import re
import sys
import argparse
from typing import Dict, Optional, Tuple, List

# Import extraction functions
from extract_usecase_from_text import (
    extract_user_count,
    extract_priority,
    extract_hardware,
    extract_use_case_description
)

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
except ImportError:
    print("Error: Required packages not installed.")
    print("Please install: pip install sentence-transformers scikit-learn numpy")
    sys.exit(1)

# Predefined use cases with full descriptions for embedding
PREDEFINED_USE_CASES = {
    'chatbot_conversational': {
        'description': 'Real-time conversational chatbots (short prompts, short responses). Fast interactive dialogue systems for customer service, personal assistants, and chat applications.',
        'csv_file': 'opensource_chatbot_conversational.csv',
        'type': 'use_case'
    },
    'code_completion': {
        'description': 'Fast code completion/autocomplete (short prompts, short completions). IDE integration for real-time code suggestions, IntelliSense, and code hinting.',
        'csv_file': 'opensource_code_completion.csv',
        'type': 'use_case'
    },
    'code_generation_detailed': {
        'description': 'Detailed code generation with explanations (medium prompts, long responses). Software development with code explanations, comments, and documentation.',
        'csv_file': 'opensource_code_generation_detailed.csv',
        'type': 'use_case'
    },
    'translation': {
        'description': 'Document translation (medium prompts, medium responses). Multilingual translation, localization, and language conversion tasks.',
        'csv_file': 'opensource_translation.csv',
        'type': 'use_case'
    },
    'content_generation': {
        'description': 'Content creation, marketing copy (medium prompts, medium responses). Blog posts, articles, marketing materials, and creative writing.',
        'csv_file': 'opensource_content_generation.csv',
        'type': 'use_case'
    },
    'summarization_short': {
        'description': 'Short document summarization (medium prompts, short summaries). Brief summaries, executive summaries, and text condensation.',
        'csv_file': 'opensource_summarization_short.csv',
        'type': 'use_case'
    },
    'document_analysis_rag': {
        'description': 'RAG-based document Q&A (long prompts with context, medium responses). Retrieval-augmented generation for answering questions from documents, knowledge bases, and document search.',
        'csv_file': 'opensource_document_analysis_rag.csv',
        'type': 'use_case'
    },
    'long_document_summarization': {
        'description': 'Long document summarization (very long prompts, medium summaries). Processing extensive documents, research papers, and large text files to extract key points.',
        'csv_file': 'opensource_long_document_summarization.csv',
        'type': 'use_case'
    },
    'research_legal_analysis': {
        'description': 'Research/legal document analysis (very long prompts, detailed analysis). Academic research, legal document review, scholarly analysis, and in-depth document examination.',
        'csv_file': 'opensource_research_legal_analysis.csv',
        'type': 'use_case'
    }
}

# Subject-specific CSVs with descriptions for embedding
SUBJECT_CSVS = {
    'mathematics': {
        'description': 'Mathematics problem solving, math calculations, mathematical reasoning, algebra, calculus, geometry, competition math, AIME problems, math tutoring, mathematical analysis, solving math problems, math solver, mathematical computation.',
        'csv_file': 'opensource_mathematics.csv',
        'type': 'subject',
        'benchmark_columns': ['Math 500', 'AIME', 'AIME 2025', 'Math Index']
    },
    'reasoning': {
        'description': 'Logical reasoning, long context reasoning, complex reasoning tasks, reasoning problems, analytical thinking, logical analysis, reasoning benchmarks.',
        'csv_file': 'opensource_reasoning.csv',
        'type': 'subject',
        'benchmark_columns': ['AA-LCR', 'τ²-Bench Telecom']
    },
    'science': {
        'description': 'Scientific reasoning, science problems, scientific code generation, scientific research, physics, chemistry, biology, scientific analysis, GPQA, scientific knowledge.',
        'csv_file': 'opensource_science.csv',
        'type': 'subject',
        'benchmark_columns': ['SciCode', 'GPQA Diamond', 'Humanity\'s Last Exam']
    },
    'computer_science': {
        'description': 'Computer science, programming, coding, software development, code generation, code completion, terminal commands, agentic workflows, coding benchmarks.',
        'csv_file': 'opensource_computer_science.csv',
        'type': 'subject',
        'benchmark_columns': ['LiveCodeBench', 'IFBench', 'Terminal-Bench Hard', 'Coding Index']
    },
    'general_knowledge': {
        'description': 'General knowledge, world knowledge, factual knowledge, knowledge retrieval, MMLU, intelligence, general understanding, knowledge base, factual information.',
        'csv_file': 'opensource_general_knowledge.csv',
        'type': 'subject',
        'benchmark_columns': ['MMLU-Pro', 'Intelligence Index']
    }
}

# Combine all for semantic matching
ALL_CSVS = {**PREDEFINED_USE_CASES, **SUBJECT_CSVS}

# Embedding model
EMBEDDING_MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'
_embedding_model = None
_use_case_embeddings = None

def get_embedding_model():
    """Get or initialize the embedding model"""
    global _embedding_model
    if _embedding_model is None:
        print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}...")
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        print("✓ Model loaded")
    return _embedding_model

def generate_use_case_embeddings():
    """Generate embeddings for all use cases and subjects"""
    global _use_case_embeddings
    if _use_case_embeddings is not None:
        return _use_case_embeddings
    
    model = get_embedding_model()
    
    # Collect all descriptions
    all_names = []
    all_descriptions = []
    
    for name, info in ALL_CSVS.items():
        all_names.append(name)
        all_descriptions.append(info['description'])
    
    # Generate embeddings
    print(f"Generating embeddings for {len(all_descriptions)} use cases/subjects...")
    embeddings = model.encode(all_descriptions, show_progress_bar=True)
    
    _use_case_embeddings = dict(zip(all_names, embeddings))
    print("✓ Embeddings generated")
    
    return _use_case_embeddings

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

def extract_and_match_usecase(user_text: str) -> Dict:
    """
    Extract use case information from plain text and match to best predefined use case
    
    Args:
        user_text: Plain text description from user
    
    Returns:
        Dictionary with:
        - use_case: Full description extracted from text
        - user_count: Number of users (optional)
        - priority: Priority level (optional)
        - hardware: Hardware requirements (optional)
        - matched_use_case: Best matching predefined use case name
        - matched_use_case_description: Description of matched use case
        - similarity_score: Semantic similarity score (0-1)
        - top_matches: List of top 3 matches with scores
    """
    # Step 1: Extract information from plain text
    use_case_description = extract_use_case_description(user_text)
    user_count = extract_user_count(user_text)
    priority = extract_priority(user_text)
    hardware = extract_hardware(user_text)
    
    # Step 2: Generate embeddings and find best match
    use_case_embeddings = generate_use_case_embeddings()
    similarities = calculate_semantic_similarity(use_case_description, use_case_embeddings)
    
    # Get top match
    best_match_name, best_match_score = similarities[0]
    best_match_info = ALL_CSVS[best_match_name]
    
    # Get top 3 matches
    top_matches = [
        {
            'name': name,
            'description': ALL_CSVS[name]['description'],
            'similarity_score': round(score, 4),
            'type': ALL_CSVS[name]['type']
        }
        for name, score in similarities[:3]
    ]
    
    # Build result
    result = {
        "use_case": use_case_description,
        "matched_use_case": best_match_name,
        "matched_use_case_description": best_match_info['description'],
        "similarity_score": round(best_match_score, 4),
        "top_matches": top_matches
    }
    
    # Add optional fields only if present
    if user_count is not None:
        result["user_count"] = user_count
    if priority is not None:
        result["priority"] = priority
    if hardware is not None:
        result["hardware"] = hardware
    
    return result

def main():
    parser = argparse.ArgumentParser(
        description='Extract use case from plain text and match to best predefined use case',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 extract_and_match_usecase.py --text "I need a chatbot for 100 users with high priority"
  python3 extract_and_match_usecase.py --text "I need code autocomplete for my IDE, needs GPU"
  python3 extract_and_match_usecase.py --file input.txt --output output.json

Input: Plain text (e.g., "I need a math solver for 50 users, high priority, needs cloud")
Output: JSON with use_case, user_count, priority, hardware, matched_use_case, similarity_score
        """
    )
    parser.add_argument('--text', '-t', type=str, help='Plain text input')
    parser.add_argument('--file', '-f', type=str, help='File with plain text input')
    parser.add_argument('--output', '-o', type=str, help='Output JSON file (optional)')
    
    args = parser.parse_args()
    
    if not args.text and not args.file:
        parser.print_help()
        sys.exit(1)
    
    # Get input text
    if args.text:
        user_text = args.text
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            user_text = f.read().strip()
    
    print("=" * 70)
    print("  Use Case Extraction & Semantic Matching")
    print("=" * 70)
    print(f"\n📝 Input Text: {user_text}")
    
    # Extract and match
    print("\n🔍 Extracting information and matching to use cases...")
    result = extract_and_match_usecase(user_text)
    
    # Display results
    print("\n" + "=" * 70)
    print("  EXTRACTED & MATCHED JSON")
    print("=" * 70)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Save if output file specified
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Saved to {args.output}")
    else:
        print("\n💡 Tip: Use --output filename.json to save")
    
    return result

if __name__ == "__main__":
    main()

