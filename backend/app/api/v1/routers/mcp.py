from fastapi import APIRouter

router = APIRouter()

@router.get("/tools")
async def list_mcp_tools():
    return {
        "jsonrpc": "2.0",
        "result": {
            "tools": [
                {"name": "web_search", "description": "Executes live web retrieval", "status": "active"},
                {"name": "code_interpreter", "description": "Executes REPL code sandbox", "status": "active"},
                {"name": "graph_query", "description": "Queries GraphRAG topology", "status": "active"},
                {"name": "database_sql", "description": "Queries relational databases", "status": "active"},
                {"name": "threat_intel", "description": "Inspects threat intelligence feeds", "status": "active"}
            ],
            "resources": [
                {"uri": "resource://live_product_catalog", "name": "Live Product Catalog"},
                {"uri": "resource://user_rbac_session", "name": "User RBAC Session"}
            ],
            "prompts": [
                {"name": "deep_synthesis_tpl", "description": "Deep synthesis prompt template"},
                {"name": "code_review_tpl", "description": "Code review prompt template"}
            ]
        }
    }
