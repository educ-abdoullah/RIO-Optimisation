from __future__ import annotations


def format_number(value: float | None, decimals: int = 2, suffix: str = "") -> str:
    if value is None:
        return "N/A"
    formatted = f"{value:,.{decimals}f}".replace(",", " ")
    return f"{formatted}{suffix}"


def format_roi(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{value:.4f}"


def dominant_channel(tv: float, radio: float, social_media: float) -> str:
    budgets = {"TV": tv, "Radio": radio, "Social Media": social_media}
    return max(budgets, key=budgets.get)


def roi_level(roi: float | None) -> tuple[str, str]:
    if roi is None:
        return "Non calculable", "Le budget total est nul, le ROI ne peut pas être calculé."
    if roi >= 1:
        return "Très favorable", "Le scénario génère plus de ventes que le budget investi."
    if roi >= 0.7:
        return "Solide", "Le scénario semble intéressant, avec un ROI proche du seuil de rentabilité."
    if roi >= 0.4:
        return "À optimiser", "Le scénario mérite d'être ajusté avant arbitrage budgétaire."
    return "Faible", "Le rendement estimé est limité : il faut revoir le mix média."
