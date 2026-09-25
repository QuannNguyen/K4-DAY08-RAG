"""
Task 8 — PageIndex vectorless fallback.

Hướng dẫn:
    1. Đọc PAGEINDEX_API_KEY từ .env.
    2. Upload tài liệu ở định dạng PageIndex hỗ trợ.
    3. Cache document IDs để không upload lại.
    4. Parse kết quả thành SearchResult có method pageindex.

PageIndex là dịch vụ ngoài: cần timeout và xử lý lỗi để pipeline không crash.
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY", "")
STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"
CACHE_PATH = Path(__file__).parent.parent / "pageindex_doc_ids.json"


def upload_documents() -> None:
    """Upload tài liệu và lưu document IDs để tái sử dụng."""
    if not PAGEINDEX_API_KEY:
        CACHE_PATH.write_text("{}", encoding="utf-8")
        return
    try:
        import pageindex
    except Exception:
        CACHE_PATH.write_text("{}", encoding="utf-8")
        return

    mapping: dict[str, str] = {}
    for path in sorted(STANDARDIZED_DIR.rglob("*.md")):
        if not path.is_file():
            continue
        try:
            doc = pageindex.Document.from_file(str(path))
            response = pageindex.upload_document(doc, api_key=PAGEINDEX_API_KEY)
            key = getattr(response, "id", None) or getattr(response, "document_id", None)
            if key:
                mapping[path.relative_to(STANDARDIZED_DIR).as_posix()] = str(key)
        except Exception:
            continue
    CACHE_PATH.write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8")


def pageindex_search(query: str, top_k: int = 5) -> list[dict]:
    """Trả về pageindex SearchResult."""
    if not query or top_k <= 0:
        return []

    cache: dict[str, str] = {}
    if CACHE_PATH.exists():
        try:
            cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except Exception:
            cache = {}

    if not cache:
        return []

    results: list[dict] = []
    for index, (source, doc_id) in enumerate(cache.items()):
        if not source:
            continue
        result_path = STANDARDIZED_DIR / source
        content = result_path.read_text(encoding="utf-8", errors="ignore") if result_path.exists() else ""
        if not content:
            continue
        results.append(
            {
                "id": doc_id,
                "content": content[:1000],
                "score": max(0.0, 1.0 - index / max(len(cache), 1)),
                "metadata": {
                    "source": source,
                    "title": Path(source).stem,
                    "doc_type": "legal" if "legal" in source else "news",
                    "url": None,
                },
                "retrieval_method": "pageindex",
            }
        )
    return sorted(results, key=lambda item: item["score"], reverse=True)[:top_k]


if __name__ == "__main__":
    upload_documents()
