from fastapi import FastAPI

app = FastAPI()


@app.post("/", status_code="200")
async def root():
    return {"message": "Hello World"}
