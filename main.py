from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def read_health():
    return {"status": "ok"}

@app.get("/users")
async def read_users():
    return {"users": []}
