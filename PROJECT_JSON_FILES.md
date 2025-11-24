# Project JSON Files - Clean Structure

## Current JSON Files

### 1. Configuration Files (in `configs/`)

**Purpose**: Use case definitions for semantic matching

- `configs/usecase_config.json` - Main/default config file
- `configs/examples/predefined.json` - Predefined use case example
- `configs/examples/custom.json` - Custom use case example
- `configs/examples/mixed.json` - Mixed use case example
- `configs/examples/rag.json` - RAG/document Q&A example

**Status**: ✅ Tracked in Git (allowed by .gitignore)

### 2. Data Files

- `opensource_all_benchmarks_data.json` - Large data file (130KB)
  - **Status**: ❌ Ignored by Git (in .gitignore)
  - **Reason**: Large file, generated data

## File Organization

```
project/
├── configs/                          # Use case configurations
│   ├── README.md                     # Config directory guide
│   ├── usecase_config.json           # Main config (default)
│   └── examples/                     # Example configs
│       ├── predefined.json
│       ├── custom.json
│       ├── mixed.json
│       └── rag.json
│
├── opensource_all_benchmarks_data.json  # Large data (gitignored)
│
└── .gitignore                        # Allows configs/**/*.json
```

## How to Define a Use Case

### Quick Start

1. **Create a config file**:
   ```bash
   cp configs/examples/custom.json configs/my_usecase.json
   ```

2. **Edit with your description**:
   ```json
   {
     "use_case": {
       "type": "custom",
       "name": "my_task",
       "description": "I need a model for code autocomplete"
     }
   }
   ```

3. **Run**:
   ```bash
   python3 get_best_models_semantic.py --config configs/my_usecase.json
   ```

### Two Types

#### 1. Predefined (Simple)
```json
{
  "use_case": {
    "type": "predefined",
    "name": "code_completion"
  }
}
```

#### 2. Custom (Semantic Matching)
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

1. `chatbot_conversational` - Real-time conversational chatbots
2. `code_completion` - Fast code completion/autocomplete
3. `code_generation_detailed` - Detailed code generation with explanations
4. `translation` - Document translation
5. `content_generation` - Content creation, marketing copy
6. `summarization_short` - Short document summarization
7. `document_analysis_rag` - RAG-based document Q&A
8. `long_document_summarization` - Long document summarization
9. `research_legal_analysis` - Research/legal document analysis

## Documentation

- `HOW_TO_DEFINE_USECASE.md` - Complete guide on defining use cases
- `configs/README.md` - Config directory guide
- `README_SEMANTIC_SYSTEM.md` - System overview

## Clean Structure Benefits

✅ **Organized**: All configs in one directory  
✅ **Examples**: Clear examples in `examples/` subdirectory  
✅ **Documented**: README files explain structure  
✅ **Git-friendly**: Only configs tracked, large data files ignored  
✅ **Easy to use**: Simple copy-paste workflow

