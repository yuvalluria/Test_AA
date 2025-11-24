# Use Case JSON Input Guide

## Overview

You can provide use case definitions in JSON format, and the system will automatically find the best models using semantic matching.

## JSON Formats

### Format 1: Full Object (Recommended)

```json
{
  "use_case": {
    "name": "math_solver",
    "description": "I need a model for solving math problems",
    "task": "including algebra, calculus, and competition math"
  }
}
```

### Format 2: Simple String

```json
{
  "use_case": "I need a chatbot for customer service",
  "task": "with fast response times"
}
```

### Format 3: Direct Description

```json
{
  "name": "code_helper",
  "description": "I need a model for code autocomplete",
  "task": "for my IDE"
}
```

## Usage

### Command Line

```bash
# From JSON file
python3 get_models_from_json.py --file configs/example_usecase.json

# From JSON string
python3 get_models_from_json.py --json '{"use_case": {"description": "I need code autocomplete"}}'

# Save to CSV
python3 get_models_from_json.py --file usecase.json --output results.csv
```

### Python Code

```python
from get_models_from_json import get_models_from_json

# JSON as dict
json_data = {
    "use_case": {
        "name": "my_task",
        "description": "I need a math problem solver",
        "task": "for competition math"
    }
}

models, match_info = get_models_from_json(json_data)

# Access results
print(f"Top model: {models[0]['Model Name']} - {models[0]['Use Case Score']}")
print(f"Matched to: {list(match_info.keys())}")
```

### JSON String

```python
from get_models_from_json import get_models_from_json

json_string = '{"use_case": "I need code autocomplete"}'
models, match_info = get_models_from_json(json_string)
```

## Examples

### Example 1: Math Problem Solver

```json
{
  "use_case": {
    "name": "math_solver",
    "description": "I need a model for solving math problems",
    "task": "including algebra, calculus, and competition math"
  }
}
```

**Result**: Matches `mathematics` (59.2%), `reasoning` (45.5%), `science` (40.3%)

### Example 2: Code Autocomplete

```json
{
  "use_case": "I need code autocomplete",
  "task": "for my IDE with fast suggestions"
}
```

**Result**: Matches `code_completion` (high similarity)

### Example 3: Chatbot + Code

```json
{
  "use_case": {
    "name": "chatbot_code",
    "description": "I need a chatbot",
    "task": "that can also help with code completion"
  }
}
```

**Result**: Combines `chatbot_conversational` + `code_completion`

### Example 4: RAG Document Q&A

```json
{
  "use_case": {
    "description": "I need to answer questions from documents",
    "task": "using RAG and retrieval-augmented generation"
  }
}
```

**Result**: Matches `document_analysis_rag` (high similarity)

## Field Descriptions

- **name** (optional): Identifier for the use case
- **description** (required): Main use case description
- **task** (optional): Additional task details (combined with description)

## Output

Returns:
- **models**: List of models sorted by score
- **match_info**: Dictionary of matched use cases/subjects with similarity scores

Each model has:
- `Model Name`
- `Provider`
- `Dataset`
- `Use Case Score` (percentage)

## Integration

### As a Function

```python
from get_models_from_json import get_models_from_json

def find_best_model_for_task(use_case_json):
    """Find best model for a given task"""
    models, match_info = get_models_from_json(use_case_json)
    return models[0] if models else None

# Usage
best_model = find_best_model_for_task({
    "use_case": {"description": "I need code autocomplete"}
})
print(f"Best model: {best_model['Model Name']}")
```

### As an API Endpoint

```python
from flask import Flask, request, jsonify
from get_models_from_json import get_models_from_json

app = Flask(__name__)

@app.route('/recommend', methods=['POST'])
def recommend_models():
    json_data = request.json
    models, match_info = get_models_from_json(json_data)
    
    return jsonify({
        'top_models': models[:10],
        'matches': match_info
    })
```

## Files

- `get_models_from_json.py` - Main script for JSON input
- `configs/example_usecase.json` - Full format example
- `configs/example_usecase_simple.json` - Simple format example

