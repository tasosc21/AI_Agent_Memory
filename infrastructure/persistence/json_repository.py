import json
from pathlib import Path

class JSONRepository:

    def __init__(self) -> None:
        self.json_path = Path("C:/Users/Anast/Desktop/Python/A_PROJECT/data/conversation.json")
        self.data: list = self.load()

    
    # def load(self):
    #     if self.json_path.is_file():
    #         with self.json_path.open("r", encoding="utf-8") as f:
    #             return json.load(f)       
    #     return []

    def load(self) -> list[dict[str, str]]:
        if self.json_path.is_file():
            with self.json_path.open("r", encoding="utf-8") as f:
                return json.load(f)

        self.json_path.parent.mkdir(parents=True, exist_ok=True)

        with self.json_path.open("w", encoding="utf-8") as f:
            json.dump([], f, indent=4)

        return []

    def add_message(self, role, message):
        self.data.append({"role": role, "content":message})

    def save(self):
        with self.json_path.open("w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4)

            

        
