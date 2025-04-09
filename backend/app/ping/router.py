from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
async def convert_track():
    return {"msg": "pong"}
