# Use Case Auto-Matching System

## Overview

The system automatically determines the best models for your use case by:
1. **Predefined use cases**: Directly using existing CSV files with pre-calculated scores
2. **Custom use cases**: Automatically matching your description to the most similar predefined use case(s)

**No weights needed!** The system intelligently matches your use case description to the 9 predefined use cases.

## JSON Format

### Simple Format (No Weights!)

```json
{
  "use_case": {
    "type": "predefined" | "custom",
    "name": "string",
    "description": "string (required for custom use cases)"
  }
}
```

### Predefined Use Case

```json
{
  "use_case": {
    "type": "predefined",
    "name": "code_completion"
  }
}
```

**Available predefined use cases:**
- `chatbot_conversational` - Real-time conversational chatbots
- `code_completion` - Fast code completion/autocomplete
- `code_generation_detailed` - Detailed code generation with explanations
- `translation` - Document translation
- `content_generation` - Content creation, marketing copy
- `summarization_short` - Short document summarization
- `document_analysis_rag` - RAG-based document Q&A
- `long_document_summarization` - Long document summarization
- `research_legal_analysis` - Research/legal document analysis

### Custom Use Case

```json
{
  "use_case": {
    "type": "custom",
    "name": "my_custom_task",
    "description": "I need a model for code autocomplete and fast code suggestions"
  }
}
```

**How it works:**
- The system analyzes your description using keyword matching
- It finds the most similar predefined use case(s)
- If similarity is high (≥15%), it uses that use case's CSV directly
- If similarity is lower, it combines the top 2-3 matching use cases with weighted scores

## Usage

```bash
# Predefined use case
python3 get_best_models.py --config usecase_config.json

# Custom use case from file
python3 get_best_models.py --config usecase_config_custom.json

# Custom use case from JSON string
python3 get_best_models.py --json '{"use_case": {"type": "custom", "name": "my_task", "description": "I need code autocomplete"}}'

# Specify output file
python3 get_best_models.py --config usecase_config.json --output my_results.csv
```

## How Auto-Matching Works

### Keyword Matching

Each predefined use case has associated keywords:

- **code_completion**: code completion, autocomplete, code suggestion, intellisense, code hint, fast completion
- **code_generation_detailed**: code generation, code writing, programming, software development, detailed code, code explanation
- **translation**: translation, translate, language translation, multilingual, localization
- **chatbot_conversational**: chatbot, conversation, chat, dialogue, conversational, real-time, interactive
- **content_generation**: content generation, content creation, writing, copywriting, marketing, blog, article
- **summarization_short**: summarization, summary, summarize, brief summary, document summary
- **document_analysis_rag**: rag, document q&a, document question, document analysis, retrieval, qa, question answering
- **long_document_summarization**: long document, long text, extensive document, large document
- **research_legal_analysis**: research, legal, analysis, document analysis, research paper, legal document, academic

### Matching Algorithm

1. **Keyword Matching**: Counts how many keywords from each predefined use case appear in your description
2. **Name Matching**: Checks if the use case name (or variations) appears in your description
3. **Combined Score**: Combines keyword and name matches with weights
4. **Selection**:
   - If best match ≥ 15% similarity: Use that use case's CSV directly
   - Otherwise: Combine top 2-3 matches with weighted scores

### Examples

**Example 1: Clear Match**
```
Description: "I need code autocomplete"
→ Matches: code_completion (23.5%)
→ Result: Uses code_completion CSV directly
```

**Example 2: Multiple Matches**
```
Description: "I need to generate code with detailed explanations"
→ Matches: code_generation_detailed (high), code_completion (medium)
→ Result: Uses code_generation_detailed (best match)
```

**Example 3: Low Similarity**
```
Description: "I need something for my unique task"
→ Matches: All use cases (low similarity)
→ Result: Uses best match anyway (fallback)
```

## Output

The script generates a CSV file with:
- Model Name
- Provider
- Dataset
- Use Case Score (percentage, sorted descending)

**Default filename**: `best_models_{usecase_name}.csv`

## Prerequisites

The 9 predefined use case CSV files must exist. Generate them first:

```bash
python3 create_usecase_scores.py
```

This creates:
- `opensource_chatbot_conversational.csv`
- `opensource_code_completion.csv`
- `opensource_code_generation_detailed.csv`
- `opensource_translation.csv`
- `opensource_content_generation.csv`
- `opensource_summarization_short.csv`
- `opensource_document_analysis_rag.csv`
- `opensource_long_document_summarization.csv`
- `opensource_research_legal_analysis.csv`

## Tips for Best Results

1. **Be specific**: Include key terms like "code", "translation", "document", "chatbot", etc.
2. **Use natural language**: Write as you would describe the task to a colleague
3. **Include context**: Mention prompt length, response type, or specific requirements
4. **Check the match**: The script shows which use case(s) it matched - verify it makes sense

## Example Configurations

### Example 1: Code Autocomplete
```json
{
  "use_case": {
    "type": "custom",
    "name": "autocomplete",
    "description": "I need fast code autocomplete for my IDE"
  }
}
```
→ Matches: `code_completion`

### Example 2: Document Q&A
```json
{
  "use_case": {
    "type": "custom",
    "name": "doc_qa",
    "description": "I need to answer questions from long documents using RAG"
  }
}
```
→ Matches: `document_analysis_rag`

### Example 3: Content Writing
```json
{
  "use_case": {
    "type": "custom",
    "name": "blog_writing",
    "description": "I need to generate blog posts and marketing content"
  }
}
```
→ Matches: `content_generation`

## Comparison with Old System

**Old System (with weights):**
```json
{
  "use_case": {
    "type": "custom",
    "weights": {
      "mmlu_pro": 0.30,
      "hle": 0.25,
      ...
    }
  }
}
```

**New System (auto-matching):**
```json
{
  "use_case": {
    "type": "custom",
    "description": "I need a model for code autocomplete"
  }
}
```

**Benefits:**
- ✅ No need to understand benchmark weights
- ✅ Natural language input
- ✅ Automatically uses expert-tuned weights from predefined use cases
- ✅ Can combine multiple use cases intelligently

