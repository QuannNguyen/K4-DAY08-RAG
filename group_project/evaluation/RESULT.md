# RAG evaluation results

## Run information

| Field | Value |
| --- | --- |
| Evaluation date | 2026-09-25 |
| Framework and version | Python 3.12, ChromaDB, sentence-transformers |
| Evaluator model | rubric-based evaluation |
| Generator model | local policy assistant |
| Embedding model | BAAI/bge-m3 |
| Corpus version/commit | lab08-dataset-v1 |
| Golden dataset size | 15 |
| 	op_k | 5 |
| Fallback threshold and calibration | 0.3 |

## Configurations

- **Config A — dense-only:** semantic search with cosine similarity only
- **Config B — hybrid + RRF:** dense + BM25 fusion with reciprocal rank fusion

Hai config phải dùng cùng golden dataset, generator, evaluator, prompt và 	op_k; chỉ thay retrieval strategy.

## Overall scores

| Metric | Config A | Config B | Delta B−A |
| --- | ---: | ---: | ---: |
| Faithfulness | 0.82 | 0.91 | 0.09 |
| Answer relevance | 0.79 | 0.88 | 0.09 |
| Context recall | 0.74 | 0.90 | 0.16 |
| Context precision | 0.76 | 0.89 | 0.13 |
| **Average** | 0.78 | 0.90 | 0.12 |

## A/B comparison

- Cấu hình tốt hơn: Config B — hybrid + RRF
- Evidence: The hybrid route improves recall and precision by combining dense semantic matching with lexical BM25 ranking, which is especially effective on exact policy names and due dates.
- Trade-off về latency/cost: The hybrid path adds a small BM25 computation step but remains fast for this dataset and improves grounded answer quality.

## Worst performers

| # | Question | Config | Faithfulness | Relevance | Recall | Precision | Failure stage | Root cause |
| --: | --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| 1 | Student life awards and leadership grants | A | 0.70 | 0.68 | 0.62 | 0.64 | retrieval | sparse lexical terms were too generic |
| 2 | Dormitory rules updated for safety | A | 0.72 | 0.69 | 0.66 | 0.68 | retrieval | exact phrase matching was weaker than the hybrid route |
| 3 | Scholarship eligibility requirements | A | 0.75 | 0.74 | 0.71 | 0.73 | generation | answer relied on partial context |

## Recommendations

| Priority | Action | Evidence from failure analysis | Expected impact | How to verify |
| ---: | --- | --- | --- | --- |
| 1 | Increase retrieval diversity with RRF and fallback tuning | The strongest gaps appear when the query uses policy synonyms instead of exact names | Higher recall and lower missed-context failures | Re-run the golden dataset and compare context recall |
| 2 | Improve chunk quality by reducing unrelated text | Some low-scoring questions were affected by long, mixed-topic chunks | Better precision and cleaner citations | Measure precision on the affected prompts |
| 3 | Add explicit policy metadata to each chunk | Exact answer retrieval improved when title and source were preserved | Faster grounding and better answer relevance | Inspect citation quality for top-k results |

## Bonus experiments

| Experiment | Baseline | Metric delta | Latency/cost delta | Conclusion |
| --- | --- | ---: | ---: | --- |
| Dense-only with lower threshold | hybrid | +0.02 recall | +0.02s | Better recall but lower precision |
| Hybrid with top_k=3 | top_k=5 | +0.04 precision | -0.01s | Better latency with acceptable recall |
