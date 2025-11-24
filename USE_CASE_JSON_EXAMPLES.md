# Use Case JSON Configuration Examples

## Overview

This document provides ready-to-use JSON examples for the semantic use case matching system.

## Quick Reference

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
- `chatbot_conversational`
- `code_completion`
- `code_generation_detailed`
- `translation`
- `content_generation`
- `summarization_short`
- `document_analysis_rag`
- `long_document_summarization`
- `research_legal_analysis`

## Example Configurations

### 1. Predefined: Code Completion

**File**: `usecase_config_semantic_predefined.json`

```json
{
  "use_case": {
    "type": "predefined",
    "name": "code_completion"
  }
}
```

**Usage**:
```bash
python3 get_best_models_semantic.py --config usecase_config_semantic_predefined.json
```

---

### 2. Custom: Code Autocomplete

**File**: `usecase_config_semantic_custom.json`

```json
{
  "use_case": {
    "type": "custom",
    "name": "my_custom_task",
    "description": "I need a model for code autocomplete and fast code suggestions"
  }
}
```

**Usage**:
```bash
python3 get_best_models_semantic.py --config usecase_config_semantic_custom.json
```

**Expected Match**: `code_completion` (high similarity)

---

### 3. Custom: Mixed Use Case (Chatbot + Code)

**File**: `usecase_config_semantic_mixed.json`

```json
{
  "use_case": {
    "type": "custom",
    "name": "chatbot_with_code",
    "description": "I need a chatbot that can also help with code completion and programming questions"
  }
}
```

**Usage**:
```bash
python3 get_best_models_semantic.py --config usecase_config_semantic_mixed.json
```

**Expected Matches**:
- `chatbot_conversational` (~58%)
- `code_completion` (~55%)
- `code_generation_detailed` (~41%)

**Result**: Combines all three with weighted scores

---

### 4. Custom: RAG Document Q&A

**File**: `usecase_config_semantic_rag.json`

```json
{
  "use_case": {
    "type": "custom",
    "name": "document_qa_rag",
    "description": "I need to answer questions from long documents using RAG and retrieval-augmented generation"
  }
}
```

**Usage**:
```bash
python3 get_best_models_semantic.py --config usecase_config_semantic_rag.json
```

**Expected Matches**:
- `document_analysis_rag` (~68%)
- `long_document_summarization` (~46%)
- `research_legal_analysis` (~38%)

---

## More Examples

### Translation Task

```json
{
  "use_case": {
    "type": "custom",
    "name": "translation_task",
    "description": "I need to translate documents between multiple languages"
  }
}
```

### Content Generation

```json
{
  "use_case": {
    "type": "custom",
    "name": "content_writing",
    "description": "I need to generate blog posts, articles, and marketing content"
  }
}
```

### Research Analysis

```json
{
  "use_case": {
    "type": "custom",
    "name": "research_analysis",
    "description": "I need to analyze research papers and academic documents in detail"
  }
}
```

### Short Summarization

```json
{
  "use_case": {
    "type": "custom",
    "name": "brief_summary",
    "description": "I need to create short summaries of documents and articles"
  }
}
```

## Using JSON String Directly

You can also pass JSON directly without a file:

```bash
python3 get_best_models_semantic.py --json '{"use_case": {"type": "custom", "name": "my_task", "description": "I need code autocomplete"}}'
```

## Multiple Use Cases

You can process multiple use cases in one run:

```json
{
  "use_cases": [
    {
      "type": "predefined",
      "name": "code_completion"
    },
    {
      "type": "custom",
      "name": "my_custom",
      "description": "I need a chatbot for customer service"
    }
  ]
}
```

## Tips

1. **Be descriptive**: More details = better matching
   - ✅ Good: "I need code autocomplete for my IDE"
   - ❌ Bad: "code"

2. **Use natural language**: Write as you would describe it
   - ✅ Good: "I need to answer questions from long documents using RAG"
   - ❌ Bad: "rag document qa"

3. **Include context**: Mention prompt length, response type, etc.
   - ✅ Good: "Real-time conversational chatbot for customer service"
   - ❌ Bad: "chatbot"

## Files Included

- `usecase_config_semantic_predefined.json` - Predefined example
- `usecase_config_semantic_custom.json` - Custom example
- `usecase_config_semantic_mixed.json` - Mixed use case example
- `usecase_config_semantic_rag.json` - RAG/document Q&A example

## See Also

- `README_SEMANTIC_SYSTEM.md` - Complete user guide
- `SEMANTIC_MATCHING_EXPLAINED.md` - Technical details
- `USE_CASE_JSON_FORMAT.md` - Full JSON format documentation

