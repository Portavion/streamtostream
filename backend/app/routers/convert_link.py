from fastapi import APIRouter

router = APIRouter()


@router.get("/convert-link/{link: path}", tags=["metadata"])
async def convert_link(link: str):
    return {"link": link}
