from pathlib import Path


class PromptRepository:

    def __init__(self) -> None:
        self.prompts_path = Path("config/prompts")

    def get(self, prompt_name: str) -> str:
        prompt_path = self.prompts_path / f"{prompt_name}.txt"

        if not prompt_path.is_file():
            raise FileNotFoundError(
                f"Prompt file not found: {prompt_path}"
            )

        return prompt_path.read_text(encoding="utf-8")