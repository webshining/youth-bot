import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import router as api_router
from data.config import ROOT_PATH

app = FastAPI(root_path=ROOT_PATH)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://webshining.tech"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("server:app", reload=True, host="0.0.0.0", port=4000, log_level="warning", root_path=ROOT_PATH)
