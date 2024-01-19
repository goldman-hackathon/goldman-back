from fastapi import FastAPI, HTTPException, Form
import requests
import json

def get_diffs(gitlab_url, private_token, date, project_id):
    headers = {
        "Private-Token": private_token
    }

    # Get all project merge requests
    url = f"{gitlab_url}/api/v4/projects/{project_id}/merge_requests?updated_after={date}&status=merged"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="GitLab API request failed")

    merge_requests = json.loads(response.text)
    for merge_request in merge_requests:
        merged_url = f"{gitlab_url}/projects/{project_id}/merge_requests/{merge_request['iid']}/changes"
        merged_response = requests.get(merged_url, headers=headers)
        if merged_response.status_code != 200:
            raise HTTPException(status_code=merged_response.status_code, detail="GitLab changes API request failed")
        merged_changes = json.loads(merged_response.text)["changes"]
        print(merged_changes)