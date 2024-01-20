from typing import List
from openai import OpenAI
from get_diff import get_diffs
from utils import *
import os
import json

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()


def get_report_for_the_file(new_file, diff):
    prompt = """
    Analyze the following file changes provided as a diff and provide a concise summary of the changes.
    Present your summary in brief points, focusing on key alterations. Make one point per file. Keep the summary as succinct as possible.
    """
    # print(new_file)
    # print(diff)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": f"File content:\n{new_file}\n\nDiff:\n{diff}",
            },
        ],
        temperature=0,
        top_p=0.1,
        # max_tokens=1000,
    )
    return response.choices[0].message.content


def summarize_reports(files: List[FileContent], description):
    prompt = """
    Review the provided reports of file changes and summarize the most significant alterations in a clear, 
    organized manner. Focus on highlighting the key modifications in each file, avoiding minor details. 
    Present the summary in a concise, bullet-point format, ensuring each point captures the essence of the
    change and you include the name of the file in which the change was made.
    """
    report_prompt = ""
    for file in files:
        report_prompt += f"Report description: {description}\n File name: {file.name}\n Report: {file.report}\n"
    # print(report_prompt)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": report_prompt,
            },
        ],
        temperature=0,
        top_p=0.1,
        # max_tokens=1000,
    )
    return response.choices[0].message.content


def finalize_the_report(report):
    prompt = "Review the following detailed reports for each pull request. Provide a high-level summary, focusing on the most significant and impactful changes. Highlight key points in a concise manner. Write the result in markdown."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": report,
            },
        ],
        temperature=0,
        top_p=0.1,
        # max_tokens=1000,
    )
    return response.choices[0].message.content


def unpack_report(json_report: str) -> List[MergeRequest]:
    report_dict = json.loads(json_report)
    return [MergeRequest.from_dict(item) for item in report_dict["merges"]]


def answer_for_a_question(prompt, json_report):
    unpacked = unpack_report(json_report)
    diffs = ""
    for merge in unpacked:
        for file in merge.contents:
            diffs += f"pull request: {merge.title}, file name: {file.name}, file diff: {file.diff}\n"
    prompt = f"Answer based on file diffs on {prompt}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": diffs,
            },
        ],
        # max_tokens=1000,
    )
    result_dict = {"main_result": response.choices[0].message.content.strip()}

    return result_dict


def make_full_report(merges: List[MergeRequest]):
    result = ""
    for merge in merges:
        for file in merge.contents:
            file.report = get_report_for_the_file(file.content, file.diff)
        merge.report = summarize_reports(merge.contents, merge.description)
        result += f"Report for {merge.title}: {merge.report}\n"
    print(result)
    final_result = finalize_the_report(result)

    merges_dict = [merge.to_dict() for merge in merges]
    full_report = {"merges": merges_dict, "main_result": final_result}
    # print(final_result)
    # Serialize to JSON
    result = json.dumps(full_report)
    # print(
    #     answer_for_a_question(
    #         "Explain the idea of search function in the best solution?", result
    #     )
    # )
    return result


gitlab_url = "https://gitlab.com"
private_token = "glpat-vhW7ZYkRC6JDFLqymUbs"
date = "2020-01-01T00:00:00.000Z"
project_id = "54057294"

diffs = get_diffs(gitlab_url, private_token, date, project_id)

make_full_report(diffs)

# print(make_report(test_files))
