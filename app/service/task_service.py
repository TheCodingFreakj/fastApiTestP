from typing import List
import multiprocessing
from fastapi import FastAPI, HTTPException, Response
from datetime import datetime
import logging
from app.schemas.task_schema import ItemInput, ItemResponse
logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TaskService:

    def process_list(self,nested_list):
        with multiprocessing.Pool() as pool:
            results = pool.map(self.sum_inner, nested_list)
        return results
    def sum_inner(self,sublist):
        print(sublist)
        return sum(sublist)
   
    async def create_item(self,item:ItemInput):
        logger.info(item)
        response = {}
        end_at = None
        started_at= None
        try:
            if 'payload' not in item:
                raise HTTPException(status_code=404, detail="Not A Valid Key")
            input_list = item["payload"]
            logger.info(f"Input processed: {input_list}")
            if not isinstance(input_list, list):
                raise HTTPException(status_code=404, detail="Payload Must Be a List")
            started_at = datetime.now()
            results = self.process_list(input_list)
            end_at = datetime.now()

            response["batchid"] = item["batchid"]
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