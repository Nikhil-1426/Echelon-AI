from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ueba.api import router as ueba_router
from agentic_ai_rca.api import router as rca_router

app = FastAPI(title="EY Agentic AI Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ueba_router, prefix="/ueba", tags=["UEBA"])
app.include_router(rca_router, prefix="/rca", tags=["RCA"])

