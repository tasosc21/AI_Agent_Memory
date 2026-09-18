import json
from pathlib import Path

class JSONRepository():

    def __init__(self) -> None:
        self.json_path = self._path()

    def _path(self):
        path = Path("data/conversation.json")
        if not path.is_file():
            with path.open("w", encoding="utf-8") as f:
                json.dump([], f, indent=4)
        return path

    def get(self, username) -> list[dict[str, str]]:
        with self.json_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get(username)

    def save(self, username, message):
        with self.json_path.open("r+", encoding="utf-8") as file:
            data = json.load(file)
            data[username].append(message)

            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()


            

        
