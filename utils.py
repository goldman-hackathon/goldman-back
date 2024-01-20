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

    def to_dict(self):
        return {
            "name": self.name,
            "content": self.content,
            "diff": self.diff,
            "report": self.report,
        }


class MergeRequest:
    id: int
    title: str
    description: str
    constents: list[FileContent]
    report: str

    def __init__(self, id, title, description, contents) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.contents = contents
        self.report = ""

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "contents": [
                content.to_dict() for content in self.contents
            ],  # Convert each FileContent object to a dictionary
            "report": self.report,
        }
