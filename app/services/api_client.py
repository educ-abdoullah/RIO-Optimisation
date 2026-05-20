from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests


@dataclass
class ApiHealth:
    available: bool
    sales_model_loaded: bool = False
    roi_model_loaded: bool = False
    message: str = ""
    raw: dict[str, Any] | None = None


def check_api_health(api_url: str) -> ApiHealth:
    try:
        response = requests.get(f"{api_url.rstrip('/')}/health", timeout=2)
        if response.status_code != 200:
            return ApiHealth(False, message=f"Statut API {response.status_code}")
        payload = response.json()
        return ApiHealth(
            available=True,
            sales_model_loaded=bool(payload.get("sales_model_loaded")),
            roi_model_loaded=bool(payload.get("roi_model_loaded")),
            message=str(payload.get("status", "ok")),
            raw=payload,
        )
    except requests.exceptions.RequestException as exc:
        return ApiHealth(False, message=str(exc))


def post_prediction(api_url: str, endpoint: str, payload: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    try:
        response = requests.post(f"{api_url.rstrip('/')}{endpoint}", json=payload, timeout=5)
    except requests.exceptions.RequestException as exc:
        return None, f"API indisponible : {exc}"

    if response.status_code == 200:
        return response.json(), None

    try:
        detail = response.json().get("detail", response.text)
    except ValueError:
        detail = response.text
    return None, f"Erreur API {response.status_code} : {detail}"
