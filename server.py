import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import router as api_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=4000, reload=True)
