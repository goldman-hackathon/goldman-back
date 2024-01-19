from typing import List
from openai import OpenAI
import os


def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


class DiffFile:
    def __init__(self, fileA, fileB, name):
        self.name = name
        self.fileA = fileA
        self.fileB = fileB
        self.report = None


# Reading the file contents
new_file1 = read_file("../test_files/helpA.py")
old_file1 = read_file("../test_files/helpB.py")
new_file2 = read_file("../test_files/mainA.py")
old_file2 = read_file("../test_files/mainB.py")
new_file3 = read_file("../test_files/utilsA.py")
old_file3 = read_file("../test_files/utilsB.py")

file1 = DiffFile(new_file1, old_file1, "plik1")
file2 = DiffFile(new_file2, old_file2, "plik2")
file3 = DiffFile(new_file3, old_file3, "plik3")

test_files = [file1, file2, file3]
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()


def get_report_for_the_file(new_file, old_file):
    prompt = "Analyze the following two file versions and provide a concise summary of the changes. Present your summary in brief, numbered points, focusing on key alterations. Keep the summary as succinct as possible."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": f"Old version: {old_file}, new version: {new_file}",
            },
        ],
        max_tokens=1000,
    )
    return response.choices[0].message.content


def summarize_reports(files: List[DiffFile]):
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


def main(files: List[DiffFile]):
    for file in files:
        file.report = get_report_for_the_file(file.fileA, file.fileB)
    reports = [file.report for file in files]
    result = summarize_reports(files)
    return result


print(main(test_files))
