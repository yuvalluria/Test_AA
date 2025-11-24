# How to Define a Use Case

## Quick Start

Create a JSON file with your use case definition and run:

```bash
python3 get_best_models_semantic.py --config configs/usecase_config.json
```

## JSON Format

### Simple Format

```json
{
  "use_case": {
    "type": "predefined" | "custom",
    "name": "your_use_case_name",
    "description": "Your description here (required for custom)"
  }
}
```

## Two Types of Use Cases

### 1. Predefined Use Case

Use one of the 9 predefined use cases directly:

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

### 2. Custom Use Case

Describe your use case in natural language. The system will automatically match it to the most similar predefined use case(s) using semantic similarity:

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
- System uses vector embeddings to understand semantic meaning
- Calculates similarity to all 9 predefined use cases
- Automatically combines multiple use cases with weighted scores
- No need to specify weights manually!

## Examples

### Example 1: Predefined Use Case

**File**: `configs/usecase_config.json`

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
python3 get_best_models_semantic.py --config configs/usecase_config.json
```

---

### Example 2: Custom Use Case - Code Autocomplete

**File**: `configs/my_code_autocomplete.json`

```json
{
  "use_case": {
    "type": "custom",
    "name": "code_autocomplete",
    "description": "I need a model for code autocomplete and fast code suggestions"
  }
}
```

**Result**: Matches `code_completion` with ~77% similarity

---

### Example 3: Custom Use Case - Mixed Task

**File**: `configs/chatbot_with_code.json`

```json
{
  "use_case": {
    "type": "custom",
    "name": "chatbot_with_code",
    "description": "I need a chatbot that can also help with code completion and programming questions"
  }
}
```

**Result**: Combines multiple use cases:
- `chatbot_conversational`: 57.8%
- `code_completion`: 54.9%
- `code_generation_detailed`: 40.6%

---

### Example 4: Custom Use Case - RAG Document Q&A

**File**: `configs/document_qa.json`

```json
{
  "use_case": {
    "type": "custom",
    "name": "document_qa",
    "description": "I need to answer questions from long documents using RAG and retrieval-augmented generation"
  }
}
```

**Result**: Matches `document_analysis_rag` with ~68% similarity

---

## Best Practices

### ✅ DO:

1. **Be descriptive**: Include key details about your use case
   ```json
   "description": "I need code autocomplete for my IDE with fast suggestions"
   ```

2. **Use natural language**: Write as you would describe it to someone
   ```json
   "description": "I need to translate documents between multiple languages"
   ```

3. **Include context**: Mention prompt length, response type, etc.
   ```json
   "description": "Real-time conversational chatbot for customer service with short responses"
   ```

4. **Mention specific technologies**: If relevant (RAG, autocomplete, etc.)
   ```json
   "description": "I need RAG for document question answering"
   ```

### ❌ DON'T:

1. **Too vague**: 
   ```json
   "description": "code"  ❌
   ```

2. **Too technical without context**:
   ```json
   "description": "transformer model"  ❌
   ```

3. **Single word**:
   ```json
   "description": "chatbot"  ❌
   ```

## Using JSON String Directly

You can also pass JSON directly without creating a file:

```bash
python3 get_best_models_semantic.py --json '{"use_case": {"type": "custom", "name": "my_task", "description": "I need code autocomplete"}}'
```

## Multiple Use Cases

Process multiple use cases in one run:

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

## File Organization

Recommended structure:

```
configs/
  ├── usecase_config.json          # Your main config (default)
  └── examples/
      ├── predefined.json          # Predefined example
      ├── custom.json               # Custom example
      ├── mixed.json                # Mixed use case example
      └── rag.json                  # RAG example
```

## Output

Each use case generates a CSV file:
- `best_models_{usecase_name}.csv`

Contains:
- Model Name
- Provider
- Dataset
- Use Case Score (sorted by score, descending)

## See Also

- `README_SEMANTIC_SYSTEM.md` - Complete system guide
- `USE_CASE_JSON_EXAMPLES.md` - More examples
- `SEMANTIC_MATCHING_EXPLAINED.md` - How semantic matching works

