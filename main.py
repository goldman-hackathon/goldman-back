from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests
import json
from pydantic import BaseModel
from get_diff import get_diffs
import uvicorn

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/get_diffs")
async def get_diffs_endpoint(request: Request):
    request_data = await request.json()
    get_diffs(request_data['gitlab_url'], request_data['private_token'], request_data['date'], request_data['project_id'])
    return "CHUJ"

