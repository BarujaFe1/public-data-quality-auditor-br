"""Score calculation for quality dimensions."""

from __future__ import annotations

from app.config import DIMENSION_WEIGHTS
from app.schemas.audit import QualityIssue, Severity

SEVERITY_PENALTY = {
    Severity.INFO: 1,
    Severity.WARNING: 4,
    Severity.HIGH: 8,
    Severity.CRITICAL: 15,
}


def score_dimension(issues: list[QualityIssue], dimension: str) -> float:
    """Start at 100 and subtract severity-weighted penalties for the dimension."""
    relevant = [i for i in issues if i.dimension == dimension]
    penalty = 0.0
    for issue in relevant:
        base = SEVERITY_PENALTY[issue.severity]
        # Scale lightly by affected rows (capped)
        row_factor = min(issue.affected_rows_count / 10.0, 3.0) if issue.affected_rows_count else 1.0
        penalty += base * max(row_factor, 1.0)
    return max(0.0, min(100.0, round(100.0 - penalty, 2)))


def compute_all_scores(issues: list[QualityIssue]) -> dict[str, float]:
    scores = {dim: score_dimension(issues, dim) for dim in DIMENSION_WEIGHTS}
    overall = 0.0
    for dim, weight in DIMENSION_WEIGHTS.items():
        overall += scores[dim] * (weight / 100.0)
    scores["overall"] = round(overall, 2)
    return scores


def executive_recommendation(overall: float, issues: list[QualityIssue]) -> str:
    critical = sum(1 for i in issues if i.severity == Severity.CRITICAL)
    high = sum(1 for i in issues if i.severity == Severity.HIGH)
    if overall >= 85 and critical == 0:
        return (
            "A base apresenta qualidade boa para exploração inicial. "
            "Revise os avisos restantes e documente o dicionário antes de publicar análises."
        )
    if overall >= 70:
        return (
            "A base é utilizável com ressalvas. Priorize correção de issues de severidade alta/crítica "
            "e normalize categorias e datas antes de análises sensíveis."
        )
    if overall >= 50:
        return (
            "Qualidade moderada/baixa. Não use para decisões críticas sem limpeza. "
            f"Há {critical} issue(s) crítica(s) e {high} de alta severidade a tratar."
        )
    return (
        "Qualidade insuficiente para uso analítico confiável. "
        "Trate duplicidades, nulos estruturais e validações de domínio antes de qualquer publicação."
    )
