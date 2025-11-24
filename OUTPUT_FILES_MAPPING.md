# Output CSV Files - What They're Based On

## Summary

All `best_models_*.csv` files are **output files** generated from the **9 predefined use case CSVs**.

## File Mapping

### `best_models_rag_test.csv`
- **Based on**: `opensource_document_analysis_rag.csv`
- **Type**: Direct copy (single use case match)
- **Description**: "I need RAG for document question answering"
- **Match**: `document_analysis_rag` (high similarity)
- **Can delete**: ✅ Yes (regeneratable)

### `best_models_document_qa.csv`
- **Based on**: `opensource_document_analysis_rag.csv` + `opensource_long_document_summarization.csv` + others
- **Type**: Combined (multiple use cases)
- **Description**: "I need to answer questions from long documents"
- **Matches**: Multiple use cases combined with weights
- **Can delete**: ✅ Yes (regeneratable)

### `best_models_doc_qa_test.csv`
- **Based on**: Similar to `best_models_document_qa.csv`
- **Type**: Combined
- **Description**: Similar description, different test run
- **Can delete**: ✅ Yes (duplicate/test file)

### `best_models_code_completion.csv`
- **Based on**: `opensource_code_completion.csv`
- **Type**: Direct copy
- **Description**: Predefined use case "code_completion"
- **Can delete**: ✅ Yes (same as source file)

### `best_models_code_autocomplete.csv`
- **Based on**: `opensource_code_completion.csv` + `opensource_code_generation_detailed.csv` + others
- **Type**: Combined
- **Description**: "I need code autocomplete"
- **Matches**: Multiple code-related use cases
- **Can delete**: ✅ Yes (regeneratable)

### `best_models_mixed_task.csv`
- **Based on**: `opensource_chatbot_conversational.csv` + `opensource_code_completion.csv` + `opensource_code_generation_detailed.csv`
- **Type**: Combined
- **Description**: "I need a chatbot that can also help with code completion"
- **Matches**: 
  - chatbot_conversational (57.8%)
  - code_completion (54.9%)
  - code_generation_detailed (40.6%)
- **Can delete**: ✅ Yes (regeneratable)

### `best_models_my_custom_use_case.csv`
- **Based on**: Various (depends on description)
- **Type**: Combined
- **Description**: Custom test description
- **Can delete**: ✅ Yes (test file)

## Source Files (Keep These!)

These are the **real data files** that output files are based on:

1. ✅ `opensource_chatbot_conversational.csv`
2. ✅ `opensource_code_completion.csv`
3. ✅ `opensource_code_generation_detailed.csv`
4. ✅ `opensource_translation.csv`
5. ✅ `opensource_content_generation.csv`
6. ✅ `opensource_summarization_short.csv`
7. ✅ `opensource_document_analysis_rag.csv`
8. ✅ `opensource_long_document_summarization.csv`
9. ✅ `opensource_research_legal_analysis.csv`

## Cleanup

### Delete All Output Files

```bash
# Option 1: Use cleanup script
./cleanup_output_csvs.sh

# Option 2: Manual delete
rm -f best_models_*.csv
```

### Why It's Safe to Delete

- ✅ They're just output files
- ✅ Can be regenerated anytime
- ✅ Source files (9 use case CSVs) are kept
- ✅ No data loss

## Regeneration

To regenerate any output file:

```bash
# Example: Regenerate rag_test
python3 get_best_models_semantic.py --json '{"use_case": {"type": "custom", "name": "rag_test", "description": "I need RAG for document question answering"}}'
```

## Data Flow

```
9 Predefined Use Case CSVs (SOURCE - KEEP)
    ↓
Semantic Matching System
    ↓
best_models_*.csv (OUTPUT - CAN DELETE)
```

## Recommendation

**Delete all `best_models_*.csv` files** - They're test outputs and duplicates.

**Keep the 9 `opensource_*_*.csv` files** - These are the source of truth.

