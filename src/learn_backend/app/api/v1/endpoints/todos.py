from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_todos():
    return {"message": "Get all todos"}


@router.post("/")
async def create_todo():
    return {"message": "Create a new todo"}
