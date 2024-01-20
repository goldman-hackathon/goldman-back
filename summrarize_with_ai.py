from typing import List
from openai import OpenAI
from get_diff import get_diffs
from utils import *
import os
import json

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()


def get_report_for_the_file(new_file, diff):
    prompt = "Analyze the following file changes provided as a diff and provide a concise summary of the changes. Present your summary in brief, numbered points, focusing on key alterations. Keep the summary as succinct as possible."
    # print(new_file)
    # print(diff)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": f"File content:\n{new_file}\n\nDiff:\n{diff}",
            },
        ],
        # max_tokens=1000,
    )
    return response.choices[0].message.content


def summarize_reports(files: List[FileContent]):
    prompt = "Review the provided reports of file changes and summarize the most significant alterations in a clear, organized manner. Focus on highlighting the key modifications in each file, avoiding minor details. Present the summary in a concise, bullet-point format, ensuring each point captures the essence of the change and you include the name of the file in which the change was made."
    report_prompt = ""
    for file in files:
        report_prompt += f"File name: {file.name}\n Report: {file.report}\n"
    # print(report_prompt)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": report_prompt,
            },
        ],
        # max_tokens=1000,
    )
    return response.choices[0].message.content


def finalize_the_report(report):
    prompt = "Review the following detailed reports for each pull request. Provide a high-level summary, focusing on the most significant and impactful changes. Highlight key points in a concise manner. Write the result in markdown."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": report,
            },
        ],
        # max_tokens=1000,
    )
    return response.choices[0].message.content


def make_full_report(merges: List[MergeRequest]):
    result = ""
    for merge in merges:
        for file in merge.contents:
            file.report = get_report_for_the_file(file.content, file.diff)
        merge.report = summarize_reports(merge.contents)
        result += f"Report for {merge.title}: {merge.report}\n"

    final_result = finalize_the_report(result)

    merges_dict = [merge.to_dict() for merge in merges]
    full_report = {"merges": merges_dict, "main_result": final_result}

    # Serialize to JSON
    return json.dumps(full_report)


gitlab_url = "https://gitlab.com"
private_token = "glpat-vhW7ZYkRC6JDFLqymUbs"
date = "2020-01-01T00:00:00.000Z"
project_id = "54052610"

diffs = get_diffs(gitlab_url, private_token, date, project_id)

print(make_full_report(diffs))

# print(make_report(test_files))
