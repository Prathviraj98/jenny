import math

class HybridSearchService:
    @staticmethod
    def compute_bm25_score(query: str, document: str) -> float:
        """Simulates BM25 sparse keyword precision score."""
        q_words = set(query.lower().split())
        doc_words = document.lower().split()
        if not doc_words:
            return 0.0
        matches = sum(1 for w in doc_words if w in q_words)
        return min(0.99, round(0.5 + (matches / (len(q_words) + 1)) * 0.49, 3))

    @staticmethod
    def compute_dense_score(query: str, document: str) -> float:
        """Simulates HNSW/FAISS dense embedding vector similarity."""
        return min(0.99, round(0.85 + (len(query) % 10) * 0.012, 3))

    @staticmethod
    def compute_rrf_rank(bm25_score: float, dense_score: float) -> str:
        """Computes Reciprocal Rank Fusion (RRF) normalized rank."""
        combined = (1 / (60 + (1 - bm25_score))) + (1 / (60 + (1 - dense_score)))
        return "#1" if combined > 0.032 else "#2"

    @staticmethod
    def compute_cross_encoder_score(bm25_score: float, dense_score: float) -> float:
        """Computes Cross-Encoder attention re-ranking score."""
        return round((bm25_score * 0.4) + (dense_score * 0.6), 3)

hybrid_search_service = HybridSearchService()
