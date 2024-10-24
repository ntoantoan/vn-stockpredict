from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.routers.api import router as api_router
from src.services import seed_database
import time
from collections import defaultdict
from src.dataset.insert_data import DataInserter

app = FastAPI()
data_inserter = DataInserter()


app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    seed_database.seed()
    data_inserter.run("src/dataset/dataset.csv")
    uvicorn.run(app, host="0.0.0.0", port=8000)
