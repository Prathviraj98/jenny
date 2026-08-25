from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
import httpx
import json
from ..schemas.search import SearchQueryRequest, HybridRetrievalScoreResponse, CodeExecutionRequest, CodeExecutionResponse
from ....core.config import settings
from ....core.dependencies import get_current_user
from ....services.hybrid_search import hybrid_search_service
from ....services.graph_rag import graph_rag_service
from ....services.code_sandbox import code_sandbox_service

router = APIRouter()

@router.post("/stream")
async def stream_ai_search(
    req: SearchQueryRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Streams AI completion tokens using backend secret GROQ_API_KEY.
    Keys are 100% hidden from client browser.
    """
    query = req.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Search query cannot be empty")

    async def generate_sse_stream():
        async with httpx.AsyncClient(timeout=60.0) as client:
            payload = {
                "model": settings.GROQ_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": f"You are Nexus AI Search. Mode: {req.task_mode}. Provide direct, synthesis with citations [1], [2]. Never output conversational preamble."
                    },
                    {"role": "user", "content": query}
                ],
                "stream": True
            }
            
            headers = {
                "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                "Content-Type": "application/json"
            }

            try:
                async with client.stream("POST", "https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers) as resp:
                    if resp.status_code != 200:
                        yield f"data: {json.dumps({'error': f'Groq API Status {resp.status_code}'})}\n\n"
                        return
                    
                    async for line in resp.aiter_lines():
                        if line.startswith("data: "):
                            yield f"{line}\n\n"
            except Exception as err:
                yield f"data: {json.dumps({'error': str(err)})}\n\n"

    return StreamingResponse(generate_sse_stream(), media_type="text/event-stream")

@router.post("/hybrid-scores", response_model=HybridRetrievalScoreResponse)
async def get_hybrid_scores(req: SearchQueryRequest):
    bm25 = hybrid_search_service.compute_bm25_score(req.query, req.query)
    dense = hybrid_search_service.compute_dense_score(req.query, req.query)
    rrf = hybrid_search_service.compute_rrf_rank(bm25, dense)
    cross = hybrid_search_service.compute_cross_encoder_score(bm25, dense)
    
    return HybridRetrievalScoreResponse(
        bm25_score=bm25,
        dense_score=dense,
        rrf_rank=rrf,
        cross_encoder_score=cross
    )

@router.post("/graph-nodes")
async def get_graph_nodes(req: SearchQueryRequest):
    nodes = graph_rag_service.extract_entity_triples(req.query, req.query * 5)
    return {"nodes": nodes}

@router.post("/execute-code", response_model=CodeExecutionResponse)
async def execute_code(req: CodeExecutionRequest):
    res = code_sandbox_service.execute_python_code(req.code)
    return CodeExecutionResponse(
        success=res["success"],
        stdout=res["stdout"],
        stderr=res["stderr"],
        result=res.get("result")
    )
