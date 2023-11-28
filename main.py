from fastapi import FastAPI
# from pydantic import BaseModel
from fastapi import Request

app = FastAPI()


@app.post("/", status_code=200)
async def process_task(request: Request):
    payload = await request.body()
    # Process the payload here
    print('### PAYLOAD', payload)
    return {"message": "UR MOM"}
