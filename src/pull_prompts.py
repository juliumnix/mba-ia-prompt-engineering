from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate

from utils import PROMPTS_DIR, save_yaml

PROMPT_REF = "leonanluppi/bug_to_user_story_v1"
OUTPUT_PATH = PROMPTS_DIR / "bug_to_user_story_v1.yml"


def _message_to_dict(message: Any) -> dict[str, str]:
    prompt = getattr(message, "prompt", message)
    role = getattr(message, "role", None) or getattr(message, "type", None) or getattr(message, "__class__", type("", (), {})).__name__.replace("MessagePromptTemplate", "").lower()
    template = getattr(prompt, "template", None) or getattr(message, "template", None) or str(message)
    return {"role": role, "template": template}


def prompt_to_yaml(prompt: Any) -> dict[str, Any]:
    messages = []
    system_prompt = ""
    user_prompt = ""

    if isinstance(prompt, ChatPromptTemplate) or hasattr(prompt, "messages"):
        for message in getattr(prompt, "messages", []):
            item = _message_to_dict(message)
            messages.append(item)
            role = item["role"].lower()
            if "system" in role and not system_prompt:
                system_prompt = item["template"]
            if ("human" in role or "user" in role) and not user_prompt:
                user_prompt = item["template"]
    else:
        user_prompt = getattr(prompt, "template", None) or str(prompt)

    return {
        "name": "bug_to_user_story_v1",
        "version": "v1",
        "description": "Prompt original de baixa qualidade importado do LangSmith Prompt Hub.",
        "metadata": {"source": PROMPT_REF, "quality": "low"},
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "messages": messages,
    }


def pull_prompt(prompt_ref: str = PROMPT_REF, output_path: Path = OUTPUT_PATH) -> dict[str, Any]:
    load_dotenv()
    prompt = hub.pull(prompt_ref)
    data = prompt_to_yaml(prompt)
    save_yaml(output_path, data)
    return data


if __name__ == "__main__":
    result = pull_prompt()
    print(f"Prompt salvo em {OUTPUT_PATH}")
    print(f"Origem: {result['metadata']['source']}")
