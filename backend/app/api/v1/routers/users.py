from fastapi import APIRouter, Depends
from ....core.dependencies import get_current_user
from ..schemas.auth import UserProfileResponse

router = APIRouter()

@router.get("/me", response_model=UserProfileResponse)
async def get_me(user: dict = Depends(get_current_user)):
    return UserProfileResponse(
        id=user.get("sub", "guest"),
        email=f"{user.get('sub', 'guest')}@nexusai.search",
        roles=user.get("scopes", ["user"])
    )
