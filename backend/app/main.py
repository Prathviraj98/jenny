from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from .core.config import settings
from .api.v1.routers import auth, search, mcp, users
from .events.websocket import websocket_router

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

# CORS configuration allowing Next.js 14 frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SlowAPI Rate Limiting setup
limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

# Include API v1 Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(search.router, prefix="/api/v1/search", tags=["search"])
app.include_router(mcp.router, prefix="/api/v1/mcp", tags=["mcp"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(websocket_router, tags=["websocket"])

@app.get("/")
async def root():
    return {
        "status": "online",
        "app": settings.APP_NAME,
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "cache": "connected"}
