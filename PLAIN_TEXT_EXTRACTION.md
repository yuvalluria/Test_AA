# Plain Text to JSON Extraction

## Overview

Convert plain text user descriptions into structured JSON format. The system extracts:
- **use_case**: The main use case description
- **user_count**: Number of users (optional, only if mentioned)
- **priority**: Priority level (optional, only if mentioned)
- **hardware**: Hardware requirements (optional, only if mentioned)

## Quick Start

### Command Line Usage

```bash
# Basic usage
python3 extract_usecase_from_text.py --text "I need a chatbot for 100 users with high priority"

# Save to file
python3 extract_usecase_from_text.py --text "I need code autocomplete" --output my_usecase.json

# From file input
python3 extract_usecase_from_text.py --file input.txt --output output.json
```

### Interactive Mode

```bash
python3 extract_usecase_simple.py
```

Then type your use case description and press Enter. The JSON will be saved to `usecase_extracted.json`.

## Examples

### Example 1: Full Information

**Input:**
```
I need a chatbot for 100 users with high priority
```

**Output JSON:**
```json
{
  "use_case": "I need a chatbot",
  "user_count": 100,
  "priority": "high"
}
```

### Example 2: With Hardware

**Input:**
```
I need code autocomplete for my IDE, needs GPU
```

**Output JSON:**
```json
{
  "use_case": "I need code autocomplete for my IDE",
  "hardware": "gpu"
}
```

### Example 3: User Count Only

**Input:**
```
I need a math solver for 50 employees
```

**Output JSON:**
```json
{
  "use_case": "I need a math solver",
  "user_count": 50
}
```

### Example 4: Minimal (Use Case Only)

**Input:**
```
I need a translation service
```

**Output JSON:**
```json
{
  "use_case": "I need a translation service"
}
```

## Extraction Rules

### User Count

Extracts numbers when mentioned with:
- "X users"
- "for X users"
- "X people"
- "X employees"
- "X team members"
- "serving X"
- "X end users"
- "X customers"

**Examples:**
- "for 100 users" → `"user_count": 100`
- "50 employees" → `"user_count": 50`
- "serving 500" → `"user_count": 500`

### Priority

Extracts priority levels:
- **High**: "critical", "urgent", "high priority", "important", "asap", "immediately"
- **Medium**: "medium", "normal", "standard", "moderate"
- **Low**: "low priority", "low", "nice to have", "optional"

**Examples:**
- "with high priority" → `"priority": "high"`
- "urgent" → `"priority": "high"`
- "low priority" → `"priority": "low"`

### Hardware

Detects hardware requirements:
- **gpu**: "gpu", "graphics card", "nvidia", "cuda"
- **cpu**: "cpu", "processor", "intel", "amd"
- **memory**: "ram", "memory", "gb ram", "mb ram"
- **cloud**: "cloud", "aws", "azure", "gcp", "google cloud"
- **edge**: "edge", "edge device", "raspberry pi", "embedded"
- **mobile**: "mobile", "phone", "smartphone", "ios", "android"
- **server**: "server", "datacenter", "on-premise", "on premise"

**Examples:**
- "needs GPU" → `"hardware": "gpu"`
- "needs cloud infrastructure" → `"hardware": "cloud"`
- "with GPU and cloud" → `"hardware": "gpu, cloud"`

## Integration with Model Selection

After extracting the JSON, you can use it with the model selection system:

```python
from extract_usecase_from_text import extract_usecase_json
from get_models_from_json import get_models_from_json

# Step 1: Extract JSON from plain text
user_text = "I need a chatbot for 100 users with high priority"
extracted_json = extract_usecase_json(user_text)

# Step 2: Get best models based on extracted JSON
best_models, matching_info = get_models_from_json(extracted_json)

print(f"Found {len(best_models)} models")
for model in best_models[:5]:
    print(f"- {model['model_name']}: {model['score']:.2f}")
```

## Files

- **`extract_usecase_from_text.py`**: Main extraction script (command-line)
- **`extract_usecase_simple.py`**: Interactive version
- **`PLAIN_TEXT_EXTRACTION.md`**: This documentation

## Notes

- Optional fields (`user_count`, `priority`, `hardware`) are only included if detected in the text
- The `use_case` field always contains the cleaned description
- The system is case-insensitive
- Multiple hardware types can be detected and combined

