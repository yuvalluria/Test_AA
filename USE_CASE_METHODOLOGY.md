# Use-Case Specific Model Ranking Methodology

## Overview

This document explains how we create use-case specific CSV files that rank the 204 open-source models based on their performance for specific tasks.

## Methodology

### Data Source
- **Master CSV**: `opensource_all_benchmarks.csv` (204 open-source models)
- **Benchmark Source**: [Artificial Analysis Intelligence Index](https://artificialanalysis.ai/methodology/intelligence-benchmarking)

### Weighting Strategy

Each use case has a custom weighting scheme that emphasizes relevant benchmarks based on the task requirements. The weights sum to 1.0 for each use case.

### Available Benchmarks

From the Artificial Analysis Intelligence Index Evaluation Suite:

1. **MMLU-Pro** - Multi-task language understanding (12,032 questions)
2. **HLE** - Humanity's Last Exam (2,684 questions)
3. **AA-LCR** - Long Context Reasoning (100 questions, 3 repeats)
4. **GPQA Diamond** - Scientific reasoning (198 questions, 5 repeats)
5. **AIME 2025** - Competition math (30 questions, 10 repeats)
6. **IFBench** - Instruction following (294 questions, 5 repeats)
7. **SciCode** - Scientific code generation (338 subproblems, 3 repeats)
8. **LiveCodeBench** - Code generation (315 questions, 3 repeats)
9. **Terminal-Bench Hard** - Agentic workflows (47 tasks, 3 repeats)
10. **τ²-Bench Telecom** - Agentic workflows (114 tasks, 3 repeats)
11. **Artificial Analysis Intelligence Index** - Composite score (all 10 benchmarks)
12. **Artificial Analysis Coding Index** - Composite score (LiveCodeBench, SciCode, Terminal-Bench Hard)
13. **Artificial Analysis Math Index** - Composite score (AIME 2025)

## Use Case Weightings

### 1. chatbot_conversational
**Description**: Real-time conversational chatbots (short prompts, short responses)

**Weights**:
- MMLU-Pro: 30% (General knowledge critical for conversations)
- HLE: 25% (Reasoning important for coherent responses)
- IFBench: 20% (Instruction following for proper chatbot behavior)
- Intelligence Index: 15% (Overall intelligence)
- GPQA: 10% (Some reasoning capability)

**Rationale**: Fast conversational responses require good general knowledge and reasoning, but not complex coding or math. Instruction following ensures the model responds appropriately.

---

### 2. code_completion
**Description**: Fast code completion/autocomplete (short prompts, short completions)

**Weights**:
- LiveCodeBench: 40% (Primary code benchmark)
- SciCode: 30% (Scientific code understanding)
- Coding Index: 20% (Overall coding ability)
- Terminal-Bench Hard: 10% (Agentic workflows)

**Rationale**: Code completion needs strong code understanding. Fast autocomplete doesn't require deep reasoning or long context, just code pattern recognition.

---

### 3. code_generation_detailed
**Description**: Detailed code generation with explanations (medium prompts, long responses)

**Weights**:
- LiveCodeBench: 30% (Code generation)
- SciCode: 25% (Scientific code)
- IFBench: 20% (Instruction following for explanations)
- Coding Index: 15% (Overall coding)
- HLE: 10% (Reasoning for explanations)

**Rationale**: Detailed code generation needs both code ability and the capacity to follow detailed instructions and provide explanations. Reasoning helps with explaining code logic.

---

### 4. translation
**Description**: Document translation (medium prompts, medium responses)

**Weights**:
- IFBench: 35% (Instruction following critical for accurate translation)
- MMLU-Pro: 30% (Language understanding)
- HLE: 20% (Reasoning)
- Intelligence Index: 15% (Overall intelligence)

**Rationale**: Translation requires precise instruction following and strong language understanding. Less need for coding or math capabilities.

---

### 5. content_generation
**Description**: Content creation, marketing copy (medium prompts, medium responses)

**Weights**:
- MMLU-Pro: 30% (General knowledge)
- HLE: 25% (Reasoning)
- IFBench: 25% (Instruction following)
- Intelligence Index: 20% (Overall intelligence)

**Rationale**: Content generation needs a balanced combination of knowledge, reasoning, and instruction following. Creative tasks benefit from overall intelligence.

---

### 6. summarization_short
**Description**: Short document summarization (medium prompts, short summaries)

**Weights**:
- MMLU-Pro: 30% (Understanding content)
- HLE: 25% (Reasoning)
- IFBench: 25% (Instruction following)
- Intelligence Index: 20% (Overall intelligence)

**Rationale**: Similar to content generation but focused on summarization. Needs to understand content, reason about what's important, and follow summarization instructions.

---

### 7. document_analysis_rag
**Description**: RAG-based document Q&A (long prompts with context, medium responses)

**Weights**:
- AA-LCR: 30% (Long context reasoning - **CRITICAL**)
- MMLU-Pro: 25% (Knowledge retrieval)
- HLE: 20% (Reasoning)
- IFBench: 15% (Instruction following)
- τ²-Bench: 10% (Agentic workflows for complex queries)

**Rationale**: RAG systems need to process long documents and retrieve relevant information. Long context reasoning is absolutely critical. Agentic workflows help with complex multi-step queries.

---

### 8. long_document_summarization
**Description**: Long document summarization (very long prompts, medium summaries)

**Weights**:
- AA-LCR: 40% (Long context reasoning - **CRITICAL**)
- MMLU-Pro: 25% (Understanding)
- HLE: 20% (Reasoning)
- IFBench: 15% (Instruction following)

**Rationale**: Processing very long documents requires exceptional long context reasoning. The model must extract key points from extensive text.

---

### 9. research_legal_analysis
**Description**: Research/legal document analysis (very long prompts, detailed analysis)

**Weights**:
- AA-LCR: 30% (Long context reasoning - **CRITICAL**)
- MMLU-Pro: 25% (Knowledge - **CRITICAL**)
- HLE: 20% (Reasoning - **CRITICAL**)
- GPQA: 10% (Scientific reasoning)
- IFBench: 10% (Instruction following)
- τ²-Bench: 5% (Agentic workflows for complex analysis)

**Rationale**: Deep analysis of long documents requires all three critical capabilities: long context processing, extensive knowledge, and strong reasoning. Scientific reasoning helps with research tasks.

---

## Score Calculation

For each model and use case:

1. Extract benchmark scores from the master CSV
2. Apply use-case specific weights to each available benchmark
3. Calculate weighted average: `score = Σ(benchmark_score × weight) / Σ(weight)`
4. Normalize by total weight (handles missing benchmarks gracefully)
5. Convert to percentage (0-100%)

**Missing Scores**: If a benchmark score is missing (N/A), it's excluded from the calculation. The final score is normalized by the sum of available weights.

## Output Files

Each use case generates a CSV file with:
- Model Name
- Provider
- Dataset
- Use Case Score (percentage)

Models are sorted by score (descending), with top performers listed first.

## Files Generated

1. `opensource_chatbot_conversational.csv`
2. `opensource_code_completion.csv`
3. `opensource_code_generation_detailed.csv`
4. `opensource_translation.csv`
5. `opensource_content_generation.csv`
6. `opensource_summarization_short.csv`
7. `opensource_document_analysis_rag.csv`
8. `opensource_long_document_summarization.csv`
9. `opensource_research_legal_analysis.csv`

## Usage

To regenerate all use-case CSV files:

```bash
python3 create_usecase_scores.py
```

## Notes

- Weights are based on the Artificial Analysis Intelligence Index methodology
- Weights are manually tuned based on use case requirements
- The methodology can be refined based on real-world performance feedback
- All weights sum to 1.0 for consistency
- Missing benchmarks are handled gracefully (excluded from calculation)

