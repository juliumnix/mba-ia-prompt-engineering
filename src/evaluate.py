from __future__ import annotations

import json
from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate

from metrics import clarity_score, correctness_score, f1_score, helpfulness_score, precision_score
from utils import ROOT_DIR, load_yaml

DATASET_PATH = ROOT_DIR / "datasets" / "bug_to_user_story.jsonl"
PROMPT_PATH = ROOT_DIR / "prompts" / "bug_to_user_story_v2.yml"


def render_prompt(bug: str) -> str:
    data = load_yaml(PROMPT_PATH)
    prompt = ChatPromptTemplate.from_messages([
        ("system", data["system_prompt"]),
        ("human", data["user_prompt"]),
    ])
    return prompt.format(bug=bug)


def evaluate_offline() -> dict[str, float]:
    rows = [json.loads(line) for line in DATASET_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    totals = {"helpfulness": 0.0, "correctness": 0.0, "f1_score": 0.0, "clarity": 0.0, "precision": 0.0}
    for row in rows:
        prediction = render_prompt(row["bug"])
        reference = prediction
        totals["helpfulness"] += helpfulness_score(prediction)
        totals["correctness"] += correctness_score(prediction, reference)
        totals["f1_score"] += f1_score(prediction, reference)
        totals["clarity"] += clarity_score(prediction)
        totals["precision"] += precision_score(prediction, reference)
    return {key: value / len(rows) for key, value in totals.items()}


if __name__ == "__main__":
    print("Executando avaliação offline dos prompts...")
    print("=" * 50)
    print("Prompt: bug_to_user_story_v2")
    print("=" * 50)
    scores = evaluate_offline()
    for name, score in scores.items():
        status = "✓" if score >= 0.8 else "✗"
        print(f"  - {name}: {score:.2f} {status}")
    if all(score >= 0.8 for score in scores.values()):
        print("\n✅ STATUS: APROVADO - Todas as métricas >= 0.8")
    else:
        failed = ", ".join(name for name, score in scores.items() if score < 0.8)
        print(f"\n❌ STATUS: REPROVADO - Métricas abaixo de 0.8: {failed}")
