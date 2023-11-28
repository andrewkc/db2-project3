from controllers.gin_ctrl import get_knn_gin
from fastapi import APIRouter, Form
from typing import Optional

routes_gin = APIRouter()

@routes_gin.post('/knn')
async def get_knn(query: str = Form(...), k: str = Form(...), language: str = Form(...)) -> Optional[dict]:
    return await get_knn_gin(query, k, language)