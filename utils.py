class FileContent:
    name: str
    content: str
    report: str
    diff: str

    def __init__(self, name, content, diff) -> None:
        self.name = name
        self.content = content
        self.diff = diff
        self.report = ""

class MergeRequest:
    id: int
    title: str
    description: str
    constents: list[FileContent]

    def __init__(self, id, title, description, contents) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.contents = contents