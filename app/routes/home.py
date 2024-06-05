from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.schemas.task_schema import ItemInput, ItemResponse
from app.service.task_service import TaskService


router = APIRouter()
service = TaskService()


@router.post("/", response_model=ItemResponse)
async def create_item(item: ItemInput):
   data = {
    'batchid': item.batchid,
    'payload': item.payload
   }

   print(data)
   return await service.create_item(data)
