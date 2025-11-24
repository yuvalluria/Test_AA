# Use Case Configuration Files

This directory contains JSON configuration files for defining use cases.

## Structure

```
configs/
  ├── usecase_config.json          # Main/default config file
  └── examples/
      ├── predefined.json          # Predefined use case example
      ├── custom.json               # Custom use case example
      ├── mixed.json                # Mixed use case (combines multiple)
      └── rag.json                  # RAG/document Q&A example
```

## Quick Start

1. **Copy an example**:
   ```bash
   cp configs/examples/custom.json configs/my_usecase.json
   ```

2. **Edit the file** with your use case description

3. **Run**:
   ```bash
   python3 get_best_models_semantic.py --config configs/my_usecase.json
   ```

## File Format

### Predefined Use Case
```json
{
  "use_case": {
    "type": "predefined",
    "name": "code_completion"
  }
}
```

### Custom Use Case
```json
{
  "use_case": {
    "type": "custom",
    "name": "my_task",
    "description": "Describe your use case in natural language"
  }
}
```

## Available Predefined Use Cases

- `chatbot_conversational`
- `code_completion`
- `code_generation_detailed`
- `translation`
- `content_generation`
- `summarization_short`
- `document_analysis_rag`
- `long_document_summarization`
- `research_legal_analysis`

## Documentation

See `HOW_TO_DEFINE_USECASE.md` in the project root for detailed instructions.

