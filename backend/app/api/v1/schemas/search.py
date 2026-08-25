from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class SearchQueryRequest(BaseModel):
    query: str = Field(..., example="Explain quantum computing algorithms")
    task_mode: str = Field("quick", example="quick") # quick, deep, code, eli5
    reading_level: Optional[str] = "standard"

class HybridRetrievalScoreResponse(BaseModel):
    bm25_score: float
    dense_score: float
    rrf_rank: str
    cross_encoder_score: float
    prefix_cache_kv: str = "94% KV"
    speculative_speedup: str = "2.4x"

class CodeExecutionRequest(BaseModel):
    code: str

class CodeExecutionResponse(BaseModel):
    success: bool
    stdout: str
    stderr: str
    result: Optional[str] = None
