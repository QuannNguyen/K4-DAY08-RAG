# Individual contribution report

## Thông tin

- Họ và tên: Nguyễn Đức Anh Quân
- Mã học viên: 2A202602405
- Nhóm: K4-DAY08-RAG
- Repository/branch: K4-DAY08-RAG / `main`

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Retrieval pipeline | Hoàn thiện dense search, BM25 lexical search, reciprocal rank fusion và fallback retrieval; bảo đảm kết quả được sắp xếp và xử lý lỗi graceful. | [src/task4_chunking_indexing.py](../src/task4_chunking_indexing.py), [src/task5_semantic_search.py](../src/task5_semantic_search.py), [src/task6_lexical_search.py](../src/task6_lexical_search.py), [src/task7_reranking.py](../src/task7_reranking.py), [src/task9_retrieval_pipeline.py](../src/task9_retrieval_pipeline.py) | Done |
| Generation and UI integration | Hoàn thiện format context, dispatch tới các LLM provider, safe refusal và hiển thị câu trả lời kèm citation trong Streamlit UI. | [src/task10_generation.py](../src/task10_generation.py), [app.py](../app.py) | Done |
| Corpus and evaluation artifacts | Bổ sung dữ liệu legal/news, standardized Markdown, golden dataset và evaluation result để đáp ứng acceptance checks của lab. | [data/landing](../data/landing), [data/standardized](../data/standardized), [group_project/evaluation/golden_dataset.json](../group_project/evaluation/golden_dataset.json), [group_project/evaluation/RESULT.md](../group_project/evaluation/RESULT.md) | Done |

Các thay đổi hiện đang ở working tree; chưa có commit hoặc pull request riêng để ghi nhận.

## Quyết định kỹ thuật quan trọng

1. **Quyết định:** Kết hợp dense retrieval và BM25 bằng reciprocal rank fusion.
   **Lý do/evidence:** Dense search hỗ trợ truy vấn ngữ nghĩa, còn BM25 giữ được các từ khóa chính xác; contract tests xác nhận output có cấu trúc và thứ tự hợp lệ.
   **Trade-off:** Pipeline phức tạp hơn và cần duy trì hai nguồn retrieval, nhưng ổn định hơn với cả truy vấn diễn đạt tự nhiên và truy vấn chứa thuật ngữ cụ thể.

2. **Quyết định:** Dùng fallback local khi external service hoặc API key không khả dụng.
   **Lý do/evidence:** Các task collection, crawling, PageIndex và generation vẫn có đường chạy cục bộ; acceptance tests không còn phụ thuộc vào mạng hoặc secret bên ngoài.
   **Trade-off:** Dữ liệu fallback không thay thế hoàn toàn dữ liệu production và có thể làm giảm độ đa dạng evaluation, đổi lại việc demo và kiểm thử được tái lập.

## Kiểm thử và kết quả

- Test hoặc query tôi đã dùng: `python -m pytest tests/test_contracts.py -q`, `python -m pytest tests/test_acceptance.py -q`, `python -m pytest -q`.
- Kết quả trước/sau: contract suite đạt `15 passed`; sau khi bổ sung artifact, acceptance suite đạt `5 passed`; full suite đạt `20 passed`.
- Lỗi đã phát hiện và cách xử lý: acceptance tests ban đầu fail do thiếu corpus, golden dataset và report evaluation. Đã bổ sung các artifact bắt buộc và chạy lại toàn bộ test suite thành công.

## Điều còn hạn chế

- Một hạn chế cụ thể của phần tôi làm: corpus fallback và các news source hiện có thể chưa phản ánh đầy đủ dữ liệu production; các kết quả evaluation vẫn phụ thuộc vào chất lượng và phạm vi corpus.
- Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện: bổ sung nguồn dữ liệu thật có kiểm soát, metadata chuẩn hóa và đánh giá retrieval theo từng nhóm truy vấn để cải thiện recall.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 25/09/2026
- Tên thành viên: Nguyễn Đức Anh Quân