from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .security import decode_token

bearer = HTTPBearer(auto_error=False)

def get_current_user(cred: HTTPAuthorizationCredentials = Depends(bearer)) -> dict:
    if not cred:
        # Default fallback user for development/guest queries
        return {"sub": "guest_user_1", "scopes": ["user"]}
    
    payload = decode_token(cred.credentials)
    return {
        "sub": payload.get("sub", "guest_user_1"),
        "scopes": payload.get("scopes", ["user"])
    }

def has_permission(required_scopes: list[str]):
    def dependency(user: dict = Depends(get_current_user)):
        user_scopes = user.get("scopes", [])
        if not any(scope in user_scopes for scope in required_scopes):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permission scope"
            )
        return user
    return dependency
