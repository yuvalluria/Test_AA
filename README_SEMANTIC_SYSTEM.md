# Semantic Use Case Matching System

## Overview

This system uses **vector embeddings and cosine similarity** to intelligently match user descriptions to the 9 predefined use cases, then combines results with weighted scores.

**No keyword matching!** Uses semantic understanding via transformer models.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Predefined use case
python3 get_best_models_semantic.py --config usecase_config.json

# Custom use case (semantic matching)
python3 get_best_models_semantic.py --json '{"use_case": {"type": "custom", "name": "my_task", "description": "I need code autocomplete"}}'
```

## How It Works

1. **Generates Embeddings**: Converts use case descriptions to 384-dimensional vectors using `all-MiniLM-L6-v2`
2. **Calculates Similarity**: Uses cosine similarity to measure semantic closeness
3. **Weighted Combination**: Uses similarity scores as weights to combine CSV results

### Example

**Input**: "I need a chatbot that can also help with code completion"

**Semantic Similarity**:
- `chatbot_conversational`: 57.8%
- `code_completion`: 54.9%
- `code_generation_detailed`: 40.6%

**Result**: Combines all three use cases with weighted scores:
```
Final Score = (chatbot_score × 0.578 + code_completion_score × 0.549 + code_generation_score × 0.406) / (0.578 + 0.549 + 0.406)
```

## Model Used: `sentence-transformers/all-MiniLM-L6-v2`

### Why This Model?

✅ **Optimized for semantic similarity** - Purpose-built for this task  
✅ **Small and fast** - 80MB, ~20-25 sentences/sec on CPU  
✅ **High accuracy** - 84.4% on STS Benchmark  
✅ **Perfect balance** - Not too small (loses accuracy) or too large (too slow)

### Technical Details

- **Architecture**: MiniLM (distilled transformer)
- **Embedding Dimension**: 384
- **Training**: 1B+ sentence pairs
- **Performance**: Excellent on semantic similarity benchmarks

See `SEMANTIC_MATCHING_EXPLAINED.md` for detailed technical explanation.

## JSON Format

```json
{
  "use_case": {
    "type": "predefined" | "custom",
    "name": "string",
    "description": "string (required for custom)"
  }
}
```

### Predefined Use Cases

- `chatbot_conversational`
- `code_completion`
- `code_generation_detailed`
- `translation`
- `content_generation`
- `summarization_short`
- `document_analysis_rag`
- `long_document_summarization`
- `research_legal_analysis`

### Custom Use Case Example

```json
{
  "use_case": {
    "type": "custom",
    "name": "mixed_task",
    "description": "I need a chatbot that can also help with code completion"
  }
}
```

## Real Examples

### Example 1: Code Autocomplete
```bash
python3 get_best_models_semantic.py --json '{"use_case": {"type": "custom", "name": "autocomplete", "description": "I need code autocomplete"}}'
```

**Result**:
- `code_completion`: 76.6% (primary match)
- `code_generation_detailed`: 50.3% (secondary)
- Combines both with weighted scores

### Example 2: Document Q&A with RAG
```bash
python3 get_best_models_semantic.py --json '{"use_case": {"type": "custom", "name": "rag_qa", "description": "I need to answer questions from long documents using RAG"}}'
```

**Result**:
- `document_analysis_rag`: 67.7% (primary match)
- `long_document_summarization`: 45.7% (secondary)
- `research_legal_analysis`: 37.9% (tertiary)

### Example 3: Mixed Use Case
```bash
python3 get_best_models_semantic.py --json '{"use_case": {"type": "custom", "name": "chatbot_code", "description": "I need a chatbot that can also help with code completion"}}'
```

**Result**:
- `chatbot_conversational`: 57.8%
- `code_completion`: 54.9%
- `code_generation_detailed`: 40.6%
- Intelligently combines all three!

## Output

Generates `best_models_{usecase_name}.csv` with:
- Model Name
- Provider
- Dataset
- Use Case Score (weighted combination, sorted descending)

Also shows:
- Semantic similarity scores for each use case
- Final weights used for combination
- Top 10 models

## Advantages Over Keyword Matching

| Feature | Keyword Matching | Semantic Matching |
|---------|------------------|-------------------|
| Understands synonyms | ❌ | ✅ |
| Handles variations | ❌ | ✅ |
| Context awareness | ❌ | ✅ |
| Natural language | ❌ | ✅ |
| Weighted combination | Manual | Automatic |

## Files

- `get_best_models_semantic.py` - Main semantic matching script
- `SEMANTIC_MATCHING_EXPLAINED.md` - Detailed technical explanation
- `requirements.txt` - Python dependencies
- `usecase_config.json` - Example configs

## Prerequisites

1. Generate the 9 predefined use case CSVs:
   ```bash
   python3 create_usecase_scores.py
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Model Information

View detailed model information:
```bash
python3 get_best_models_semantic.py --model-info
```

## Performance

- **First run**: Downloads model (~80MB), takes ~10-20 seconds
- **Subsequent runs**: Model cached, instant loading
- **Embedding generation**: ~20-25 sentences/second
- **Total processing**: < 1 second for matching + CSV combination

## Why This Approach?

1. **Semantic Understanding**: Understands meaning, not just keywords
2. **Flexible**: Handles natural language descriptions
3. **Intelligent**: Automatically combines multiple use cases
4. **Accurate**: Uses state-of-the-art transformer models
5. **Fast**: Optimized for production use

Perfect for users who want to describe their use case in natural language without understanding benchmark weights or technical details!

