import uvicorn
from fastapi import FastAPI, routing
from src.api.tasks.endpoints import router as router

app = FastAPI()
app.include_router(router)

if __name__ == '__main__':
    uvicorn.run("main:app", port=8080, reload=True)