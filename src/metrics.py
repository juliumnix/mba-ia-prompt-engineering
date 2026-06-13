from __future__ import annotations

import re
from collections import Counter


def _tokens(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


def f1_score(prediction: str, reference: str) -> float:
    pred_tokens = _tokens(prediction)
    ref_tokens = _tokens(reference)
    if not pred_tokens or not ref_tokens:
        return 0.0
    common = Counter(pred_tokens) & Counter(ref_tokens)
    overlap = sum(common.values())
    if overlap == 0:
        return 0.0
    precision = overlap / len(pred_tokens)
    recall = overlap / len(ref_tokens)
    return 2 * precision * recall / (precision + recall)


def precision_score(prediction: str, reference: str) -> float:
    pred_tokens = _tokens(prediction)
    ref_tokens = set(_tokens(reference))
    if not pred_tokens:
        return 0.0
    return sum(1 for token in pred_tokens if token in ref_tokens) / len(pred_tokens)


def clarity_score(prediction: str) -> float:
    required_sections = ["## User Story", "## Contexto do Bug", "## Critérios de Aceite", "## Casos de Borda", "## Suposições e Perguntas"]
    section_score = sum(section in prediction for section in required_sections) / len(required_sections)
    gwt_score = min(prediction.count("Given"), 3) / 3
    return round((section_score * 0.7) + (gwt_score * 0.3), 4)


def helpfulness_score(prediction: str) -> float:
    helpful_markers = ["Como", "quero", "para que", "Impacto", "Critérios", "Casos de Borda"]
    return sum(marker.lower() in prediction.lower() for marker in helpful_markers) / len(helpful_markers)


def correctness_score(prediction: str, reference: str) -> float:
    return round((f1_score(prediction, reference) * 0.6) + (clarity_score(prediction) * 0.4), 4)
