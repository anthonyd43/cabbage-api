from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import plaid_service

app = FastAPI()

origins = [
    "http://localhost:3000",  # Frontend origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins or ["*"] for all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)


app.include_router(plaid_service.router)
