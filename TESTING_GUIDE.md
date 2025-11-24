# Testing Guide - Use Case Model Recommendation

## Quick Test Options

### Option 1: Interactive Mode (Recommended)

Run the interactive script and follow the prompts:

```bash
python3 test_usecase_interactive.py
```

**Features:**
- Choose predefined or custom use case
- See available use cases
- View results with matching scores
- Save to CSV option
- Try multiple use cases

**Example Session:**
```
Choose an option:
  1. Use predefined use case (type number or name)
  2. Describe custom use case (type description)
  3. Exit

Your choice (1/2/3): 2

Describe your use case in natural language:
(Example: 'I need a model for code autocomplete')

Your use case: I need a chatbot that can help with code completion

Name for this use case (optional, press Enter for auto): chatbot_code

[System processes and shows results]
```

---

### Option 2: Simple Script (Quick Test)

Edit `test_usecase_simple.py` and modify the `USECASE_CONFIG`:

```python
# Option 1: Predefined
USECASE_CONFIG = {
    "type": "predefined",
    "name": "code_completion"
}

# Option 2: Custom (uncomment to use)
# USECASE_CONFIG = {
#     "type": "custom",
#     "name": "my_task",
#     "description": "I need a model for code autocomplete"
# }
```

Then run:
```bash
python3 test_usecase_simple.py
```

---

### Option 3: Command Line

Use the main script directly:

```bash
# Predefined use case
python3 get_best_models_semantic.py --config configs/usecase_config.json

# Custom use case (JSON string)
python3 get_best_models_semantic.py --json '{"use_case": {"type": "custom", "name": "my_task", "description": "I need code autocomplete"}}'
```

---

## Test Examples

### Example 1: Code Autocomplete

**Input:**
```json
{
  "use_case": {
    "type": "custom",
    "name": "autocomplete",
    "description": "I need code autocomplete for my IDE"
  }
}
```

**Expected Match:** `code_completion` (~77% similarity)

---

### Example 2: Chatbot + Code

**Input:**
```json
{
  "use_case": {
    "type": "custom",
    "name": "chatbot_code",
    "description": "I need a chatbot that can also help with code completion"
  }
}
```

**Expected Matches:**
- `chatbot_conversational`: ~58%
- `code_completion`: ~55%
- `code_generation_detailed`: ~41%

---

### Example 3: Document Q&A with RAG

**Input:**
```json
{
  "use_case": {
    "type": "custom",
    "name": "rag_qa",
    "description": "I need to answer questions from long documents using RAG"
  }
}
```

**Expected Matches:**
- `document_analysis_rag`: ~68%
- `long_document_summarization`: ~46%
- `research_legal_analysis`: ~38%

---

### Example 4: Translation

**Input:**
```json
{
  "use_case": {
    "type": "custom",
    "name": "translation",
    "description": "I need to translate documents between multiple languages"
  }
}
```

**Expected Match:** `translation` (~high similarity)

---

## Understanding the Output

### Semantic Similarity Scores

The system shows how similar your description is to each predefined use case:

```
📊 Use Case Matching:
  code_completion              ████████████████████████████████████░░░░░░░░░░░░ 76.6%
  code_generation_detailed     ████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 50.3%
  chatbot_conversational       ██████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 32.0%
```

### Top Models

Shows the best models ranked by combined score:

```
🏆 Top 10 Models:
Rank   Model Name                                  Score
1      Kimi K2 Thinking                           60.95%
2      gpt-oss-120B (high)                        58.36%
3      MiniMax-M2                                 56.99%
...
```

---

## Troubleshooting

### Error: "Required packages not installed"

```bash
pip install -r requirements.txt
```

### Error: "CSV file not found"

Generate the use case CSV files first:
```bash
python3 create_usecase_scores.py
```

### Model Loading Takes Time

First run downloads the embedding model (~80MB). Subsequent runs are instant.

### Low Similarity Scores

Try being more descriptive:
- ❌ "code"
- ✅ "I need code autocomplete for my IDE"

---

## Quick Test Checklist

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Use case CSVs generated (`python3 create_usecase_scores.py`)
- [ ] Run interactive test (`python3 test_usecase_interactive.py`)
- [ ] Try predefined use case
- [ ] Try custom use case
- [ ] Check similarity scores make sense
- [ ] Verify top models are relevant

---

## Files

- `test_usecase_interactive.py` - Interactive testing script
- `test_usecase_simple.py` - Simple script for quick tests
- `get_best_models_semantic.py` - Main semantic matching system

