# Use Case JSON Configuration - Quick Reference

## JSON Structure

### Predefined Use Case (Choose from 9 options)

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

### Custom Use Case (Define your own weights)

```json
{
  "use_case": {
    "type": "custom",
    "name": "my_custom_use_case",
    "description": "Description of your use case",
    "weights": {
      "mmlu_pro": 0.30,
      "hle": 0.25,
      "lcr": 0.20,
      "ifbench": 0.15,
      "artificial_analysis_intelligence_index": 0.10
    }
  }
}
```

**Available benchmarks for weights:**
- `mmlu_pro`, `hle`, `lcr`, `gpqa`, `aime`, `aime_25`
- `ifbench`, `livecodebench`, `scicode`
- `terminalbench_hard`, `tau2`
- `artificial_analysis_intelligence_index`
- `artificial_analysis_coding_index`
- `artificial_analysis_math_index`
- `math_500`

**Note:** Weights are automatically normalized to sum to 1.0. You can use any numeric values.

### Multiple Use Cases

```json
{
  "use_cases": [
    { "type": "predefined", "name": "code_completion" },
    { "type": "predefined", "name": "translation" },
    { "type": "custom", "name": "my_custom", "weights": {...} }
  ]
}
```

## Usage

```bash
# All predefined use cases (default)
python3 create_usecase_scores.py

# From JSON file
python3 create_usecase_scores.py --config usecase_config.json

# From JSON string
python3 create_usecase_scores.py --json '{"use_case": {"type": "predefined", "name": "code_completion"}}'
```

## Output

Each use case generates: `opensource_{usecase_name}.csv`

## Examples

See:
- `usecase_config.json` - Predefined example
- `usecase_config_custom.json` - Custom example
- `usecase_config_multiple.json` - Multiple use cases

For detailed documentation, see `USE_CASE_JSON_FORMAT.md`

