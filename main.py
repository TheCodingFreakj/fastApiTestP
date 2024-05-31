from datetime import datetime
import multiprocessing
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from typing import List
import logging
app = FastAPI()

logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ItemResponse(BaseModel):
    batchid: str
    response: List[int]
    status: str
    started_at: datetime
    end_at: datetime

class ItemInput(BaseModel):
    batchid: str
    payload: List


@app.get("/")
def root():
    return "todooo"



def sum_inner(sublist):
    print(sublist)
    return sum(sublist)

def process_list(nested_list):
    with multiprocessing.Pool() as pool:
        results = pool.map(sum_inner, nested_list)
    return results


@app.post("/items", response_model=ItemResponse)
async def create_item(item:ItemInput):
    logger.info(item)
    inputParameter={}
    inputParameter["payload"] = item.payload
    inputParameter["batchid"] = item.batchid
    response = {}
    end_at = None
    started_at= None
    try:
        if 'payload' not in inputParameter:
            raise HTTPException(status_code=404, detail="Not A Valid Key")
        input_list = inputParameter["payload"]
        logger.info(f"Input processed: {input_list}")
        if not isinstance(input_list, list):
            raise HTTPException(status_code=404, detail="Payload Must Be a List")
        started_at = datetime.now()
        results = process_list(input_list)
        end_at = datetime.now()

        response["batchid"] = inputParameter["batchid"]
        response["response"] = results
        response["started_at"] = started_at
        response["end_at"] = end_at
        response["status"] = "complete"

        logger.info(f"Response processed: {response}")

        return response
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        response["batchid"] = None
        response["response"] = str(e)
        response["started_at"] = started_at
        response["end_at"] = end_at
        response["status"] = "incomplete"
        raise HTTPException(status_code=500, detail=response)
     


