# Use Case Model Recommendation System

## Quick Start

Get the best models for your use case without specifying weights:

```bash
# Predefined use case
python3 get_best_models.py --config usecase_config.json

# Custom use case (auto-matches to predefined)
python3 get_best_models.py --json '{"use_case": {"type": "custom", "name": "my_task", "description": "I need code autocomplete"}}'
```

## JSON Format (No Weights!)

```json
{
  "use_case": {
    "type": "predefined" | "custom",
    "name": "string",
    "description": "string (required for custom)"
  }
}
```

### Example: Predefined
```json
{
  "use_case": {
    "type": "predefined",
    "name": "code_completion"
  }
}
```

### Example: Custom
```json
{
  "use_case": {
    "type": "custom",
    "name": "my_task",
    "description": "I need a model for code autocomplete and fast code suggestions"
  }
}
```

## How It Works

1. **Predefined Use Cases**: Directly uses existing CSV files with pre-calculated scores
2. **Custom Use Cases**: Automatically matches your description to the most similar predefined use case using keyword matching

### The 9 Predefined Use Cases

1. `chatbot_conversational` - Real-time conversational chatbots
2. `code_completion` - Fast code completion/autocomplete
3. `code_generation_detailed` - Detailed code generation with explanations
4. `translation` - Document translation
5. `content_generation` - Content creation, marketing copy
6. `summarization_short` - Short document summarization
7. `document_analysis_rag` - RAG-based document Q&A
8. `long_document_summarization` - Long document summarization
9. `research_legal_analysis` - Research/legal document analysis

## Auto-Matching Examples

| Your Description | Matched Use Case |
|-----------------|------------------|
| "I need code autocomplete" | `code_completion` |
| "I need RAG for document Q&A" | `document_analysis_rag` |
| "I need to translate documents" | `translation` |
| "I need to generate blog posts" | `content_generation` |
| "I need to summarize long documents" | `long_document_summarization` |

## Output

Generates `best_models_{usecase_name}.csv` with:
- Model Name
- Provider
- Dataset
- Use Case Score (sorted by score, descending)

## Prerequisites

Generate the 9 predefined use case CSVs first:

```bash
python3 create_usecase_scores.py
```

## Files

- `get_best_models.py` - Main script for getting best models
- `create_usecase_scores.py` - Generates the 9 predefined use case CSVs
- `usecase_config.json` - Example: predefined use case
- `usecase_config_custom.json` - Example: custom use case
- `USE_CASE_AUTO_MATCHING.md` - Detailed documentation

## Benefits

✅ **No weights needed** - System automatically determines best models  
✅ **Natural language** - Describe your use case in plain English  
✅ **Expert-tuned** - Uses pre-calculated scores from expert-defined use cases  
✅ **Flexible** - Handles variations in descriptions  
✅ **Intelligent** - Combines multiple use cases when needed

