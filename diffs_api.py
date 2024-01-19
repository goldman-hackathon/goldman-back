from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import JSONResponse
import requests
import json
from get_diff import get_diffs

app = FastAPI()


@app.post("/get_diffs")
async def get_diffs_endpoint(
    gitlab_url: str = Form(...),
    private_token: str = Form(...),
    date: str = Form(...),
    project_id: str = Form(...),
):
    try:
        get_diffs(gitlab_url, private_token, date, project_id)
        return JSONResponse(
            content={"message": "Merge request changes fetched successfully"}
        )
    except HTTPException as e:
        return JSONResponse(content={"error": str(e.detail)}, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
