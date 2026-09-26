from pathlib import Path

import pytest

from infrastructure.persistence.txt.prompt_repository import PromptRepository


def test_get_prompt(tmp_path: Path):
    prompts_path = tmp_path / "prompts"
    prompts_path.mkdir()

    prompt_file = prompts_path / "system.txt"
    prompt_file.write_text(
        "You are AI_Agent.",
        encoding="utf-8",
    )

    repository = PromptRepository()
    repository.prompts_path = prompts_path

    result = repository.get("system")

    assert result == "You are AI_Agent."


def test_get_missing_prompt_raises_error(tmp_path: Path):
    repository = PromptRepository()
    repository.prompts_path = tmp_path

    with pytest.raises(
        FileNotFoundError,
        match="Prompt file not found",
    ):
        repository.get("system")