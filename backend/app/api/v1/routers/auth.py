from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from ..schemas.auth import TokenResponse, LoginPayload
from ....core import security

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Demo credentials verification for enterprise fullstack authentication
    if not form_data.username or not form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    user_id = form_data.username.split('@')[0] if '@' in form_data.username else "admin_user"
    access = security.create_access_token(sub=user_id, scopes=["admin", "user"])
    refresh = security.create_refresh_token(sub=user_id)
    
    return TokenResponse(
        access_token=access,
        refresh_token=refresh,
        user_id=user_id
    )

@router.post("/refresh", response_model=TokenResponse)
async def refresh(token: str = Body(..., embed=True)):
    payload = security.decode_token(token)
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token type"
        )
    
    sub = payload.get("sub", "user_1")
    new_access = security.create_access_token(sub=sub, scopes=["user"])
    return TokenResponse(
        access_token=new_access,
        refresh_token=token,
        user_id=sub
    )
