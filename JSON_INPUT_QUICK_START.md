# JSON Input - Quick Start

## Simple Usage

### From JSON File

```bash
python3 get_models_from_json.py --file your_usecase.json
```

### From JSON String

```bash
python3 get_models_from_json.py --json '{"use_case": {"description": "I need code autocomplete"}}'
```

## JSON Format (Simplest)

```json
{
  "use_case": {
    "description": "I need a math problem solver"
  }
}
```

## JSON Format (With Task)

```json
{
  "use_case": {
    "name": "my_task",
    "description": "I need code autocomplete",
    "task": "for my IDE"
  }
}
```

## Python Function

```python
from get_models_from_json import get_models_from_json

json_data = {
    "use_case": {
        "description": "I need a math problem solver"
    }
}

models, match_info = get_models_from_json(json_data)
print(f"Top model: {models[0]['Model Name']}")
```

## Examples

### Math Solver
```json
{"use_case": {"description": "I need a math problem solver"}}
```

### Code Autocomplete
```json
{"use_case": {"description": "I need code autocomplete"}}
```

### Chatbot
```json
{"use_case": {"description": "I need a chatbot for customer service"}}
```

## Output

Returns top models ranked by score, with semantic matching to use cases and subjects.

