from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import user, farming

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/auth")
app.include_router(farming.router, prefix="/farming")