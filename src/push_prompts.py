from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate

from utils import PROMPTS_DIR, load_yaml

PROMPT_PATH = PROMPTS_DIR / "bug_to_user_story_v2.yml"
DEFAULT_OWNER_ENV = "LANGSMITH_PROMPT_OWNER"


def build_chat_prompt(prompt_data: dict) -> ChatPromptTemplate:
    messages = []
    system_prompt = prompt_data.get("system_prompt", "").strip()
    user_prompt = prompt_data.get("user_prompt", "").strip()
    if system_prompt:
        messages.append(("system", system_prompt))
    if user_prompt:
        messages.append(("human", user_prompt))
    if not messages:
        raise ValueError("O YAML deve conter system_prompt e/ou user_prompt.")
    return ChatPromptTemplate.from_messages(messages)


def push_prompt(prompt_path: Path = PROMPT_PATH, owner: str | None = None) -> str:
    load_dotenv()
    data = load_yaml(prompt_path)
    prompt_owner = owner or os.getenv(DEFAULT_OWNER_ENV)
    if not prompt_owner:
        raise ValueError(f"Defina {DEFAULT_OWNER_ENV} no .env para publicar no LangSmith.")

    repo_name = f"{prompt_owner}/bug_to_user_story_v2"
    chat_prompt = build_chat_prompt(data)
    metadata = data.get("metadata", {})
    description = data.get("description", "Prompt otimizado para converter bugs em user stories.")

    try:
        hub.push(repo_name, chat_prompt, new_repo_description=description, tags=metadata.get("tags", []))
    except TypeError:
        hub.push(repo_name, chat_prompt, new_repo_description=description)
    return repo_name


if __name__ == "__main__":
    pushed = push_prompt()
    print(f"Prompt publicado no LangSmith Prompt Hub: {pushed}")
