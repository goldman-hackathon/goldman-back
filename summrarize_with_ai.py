from typing import List
from openai import OpenAI
from get_diff import get_diffs
from utils import *
import os

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()


def get_report_for_the_file(new_file, diff):
    prompt = "Analyze the following file changes provided as a diff and provide a concise summary of the changes. Present your summary in brief, numbered points, focusing on key alterations. Keep the summary as succinct as possible."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": f"File content:\n{new_file}\n\nDiff:\n{diff}",
            },
        ],
        max_tokens=1000,
    )
    return response.choices[0].message.content


def summarize_reports(files: List[FileContent]):
    prompt = (
        "For a group for reports of changes in files summarize those changes in points."
    )
    report_prompt = ""
    for file in files:
        report_prompt += f"File name: {file.name}\n Report: {file.report}\n"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": report_prompt,
            },
        ],
        max_tokens=1000,
    )
    return response.choices[0].message.content


def make_full_report(merges: List[MergeRequest]):
    for merge in merges:
        for file in merge.contents:
            file.report = get_report_for_the_file(file.content, file.diff)
        merge.report = summarize_reports(merge.contents)
        result += f"Report for {merge.title}:\n {merge.report}\n"
    print(result)
    return result


gitlab_url = "https://gitlab.com"
private_token = "glpat-vhW7ZYkRC6JDFLqymUbs"
date = "2020-01-01T00:00:00.000Z"
project_id = "54052610"

diffs = get_diffs(gitlab_url, private_token, date, project_id)

make_full_report(diffs)

# print(make_report(test_files))
