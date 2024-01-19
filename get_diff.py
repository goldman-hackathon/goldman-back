import requests
import json
from utils import *

# gitlab_url = "https://gitlab.com"
# private_token = "glpat-vhW7ZYkRC6JDFLqymUbs" 
# date = "2020-01-01T00:00:00.000Z"
# project_id = "54052610"

def get_diffs(gitlab_url, private_token, date, project_id):
    headers = {
        "Private-Token": private_token
    }

    # Get all project merge requests
    url = f"{gitlab_url}/api/v4/projects/{project_id}/merge_requests?updated_after={date}&status=merged"
    response = requests.get(url, headers=headers)

    merge_requests = json.loads(response.text)
    merge_reqs = []
    for merge_request in merge_requests:
        merged_url = f"{gitlab_url}/api/v4/projects/{project_id}/merge_requests/{merge_request['iid']}/changes"
        merged_response = requests.get(merged_url, headers=headers)
        
        merged_changes = json.loads(merged_response.text)["changes"]
        file_changes = []
        for change in merged_changes:
            file_url = f"{gitlab_url}/api/v4/projects/{project_id}/repository/files/{change['new_path']}/raw?ref={merge_request['target_branch']}"
            file_response = requests.get(file_url, headers=headers)
            file_changes.append(FileContent(change['new_path'], file_response.text, change['diff']))

        merge_reqs.append(MergeRequest(merge_request['iid'], merge_request['title'], merge_request['description'], file_changes))

    return merge_reqs

#get_diffs(gitlab_url, private_token, date, project_id)
