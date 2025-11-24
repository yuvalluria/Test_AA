# Use Case JSON Configuration Format

## Overview

The use case scoring system accepts JSON configuration files to specify which use cases to generate. You can use predefined use cases or create custom ones with your own benchmark weights.

## JSON Schema

### Single Use Case

```json
{
  "use_case": {
    "type": "predefined" | "custom",
    "name": "string",
    "description": "string (optional, for custom only)",
    "weights": { "benchmark": weight, ... } (required for custom)
  }
}
```

### Multiple Use Cases

```json
{
  "use_cases": [
    { "type": "predefined", "name": "code_completion" },
    { "type": "custom", "name": "my_custom", "weights": {...} }
  ]
}
```

## Predefined Use Cases

You can use any of these 9 predefined use cases by name:

1. **chatbot_conversational** - Real-time conversational chatbots
2. **code_completion** - Fast code completion/autocomplete
3. **code_generation_detailed** - Detailed code generation with explanations
4. **translation** - Document translation
5. **content_generation** - Content creation, marketing copy
6. **summarization_short** - Short document summarization
7. **document_analysis_rag** - RAG-based document Q&A
8. **long_document_summarization** - Long document summarization
9. **research_legal_analysis** - Research/legal document analysis

### Example: Predefined Use Case

```json
{
  "use_case": {
    "type": "predefined",
    "name": "code_completion"
  }
}
```

## Custom Use Cases

For custom use cases, you must provide:
- `type`: Must be `"custom"`
- `name`: A unique identifier (will be used in the output filename)
- `description`: Human-readable description (optional but recommended)
- `weights`: Dictionary of benchmark weights

### Available Benchmarks

You can use any of these benchmark names in your weights:

- `mmlu_pro` - Multi-task language understanding
- `hle` - Humanity's Last Exam (reasoning)
- `lcr` - Long Context Reasoning
- `gpqa` - Scientific reasoning
- `aime` or `aime_25` - Competition math
- `ifbench` - Instruction following
- `livecodebench` - Code generation
- `scicode` - Scientific code generation
- `terminalbench_hard` - Agentic workflows
- `tau2` - Agentic workflows (τ²-Bench Telecom)
- `artificial_analysis_intelligence_index` - Composite intelligence score
- `artificial_analysis_coding_index` - Composite coding score
- `artificial_analysis_math_index` - Composite math score
- `math_500` - Math benchmark (legacy)

### Example: Custom Use Case

```json
{
  "use_case": {
    "type": "custom",
    "name": "my_custom_use_case",
    "description": "Custom use case for specific task requirements",
    "weights": {
      "mmlu_pro": 0.25,
      "hle": 0.20,
      "lcr": 0.30,
      "ifbench": 0.15,
      "artificial_analysis_intelligence_index": 0.10
    }
  }
}
```

**Note**: Weights will be automatically normalized to sum to 1.0. You can provide any values, and they will be normalized proportionally.

### Example: Custom Use Case with Partial Weights

```json
{
  "use_case": {
    "type": "custom",
    "name": "code_focused_task",
    "description": "Task that heavily emphasizes code",
    "weights": {
      "livecodebench": 50,
      "scicode": 30,
      "artificial_analysis_coding_index": 20
    }
  }
}
```

The weights `50, 30, 20` will be normalized to `0.50, 0.30, 0.20` automatically.

## Multiple Use Cases

You can process multiple use cases in a single JSON file:

```json
{
  "use_cases": [
    {
      "type": "predefined",
      "name": "code_completion"
    },
    {
      "type": "predefined",
      "name": "translation"
    },
    {
      "type": "custom",
      "name": "my_custom_task",
      "description": "A custom task with specific requirements",
      "weights": {
        "mmlu_pro": 0.30,
        "hle": 0.25,
        "lcr": 0.20,
        "ifbench": 0.15,
        "artificial_analysis_intelligence_index": 0.10
      }
    }
  ]
}
```

## Usage

### From Command Line

```bash
# Generate all predefined use cases (default)
python3 create_usecase_scores.py

# Generate from JSON config file
python3 create_usecase_scores.py --config usecase_config.json

# Generate from JSON string
python3 create_usecase_scores.py --json '{"use_case": {"type": "predefined", "name": "code_completion"}}'
```

### From Python Code

```python
import json
from create_usecase_scores import process_json_config, create_usecase_csv

# Load from file
use_cases = process_json_config(config_file='usecase_config.json')

# Or from string
config_json = '{"use_case": {"type": "predefined", "name": "code_completion"}}'
use_cases = process_json_config(json_string=config_json)

# Process each use case
for usecase_name, weights_config in use_cases:
    create_usecase_csv(usecase_name, weights_config)
```

## Output

Each use case generates a CSV file named `opensource_{usecase_name}.csv` with:
- Model Name
- Provider
- Dataset
- Use Case Score (percentage, sorted descending)

## Examples

See the example files:
- `usecase_config.json` - Predefined use case example
- `usecase_config_custom.json` - Custom use case example
- `usecase_config_multiple.json` - Multiple use cases example

## Validation

The script will:
- Validate benchmark names (invalid ones are ignored with a warning)
- Normalize weights to sum to 1.0
- Handle missing benchmark scores gracefully
- Provide error messages for invalid configurations

## Tips

1. **Start with predefined**: Use predefined use cases first to understand the system
2. **Copy and modify**: Copy a predefined use case's weights as a starting point for custom use cases
3. **Focus on relevant benchmarks**: Only include benchmarks relevant to your task
4. **Test with small weights**: You can use any numeric values; they'll be normalized
5. **Check available benchmarks**: Use the list above to ensure you're using valid benchmark names

