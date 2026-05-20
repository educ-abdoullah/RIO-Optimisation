from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from app import config


@st.cache_data(show_spinner=False)
def load_csv(path: Path) -> tuple[pd.DataFrame | None, str | None]:
    if not path.exists():
        return None, f"Fichier absent : {path}"
    try:
        return pd.read_csv(path), None
    except Exception as exc:
        return None, f"Impossible de lire {path.name} : {exc}"


@st.cache_data(show_spinner=False)
def read_text(path: Path, default: str) -> str:
    try:
        return path.read_text(encoding="utf-8").strip() or default
    except Exception:
        return default


def load_reports() -> dict[str, tuple[pd.DataFrame | None, str | None]]:
    return {
        "sales_test": load_csv(config.SALES_TEST_RESULTS_PATH),
        "sales_cv": load_csv(config.SALES_CV_RESULTS_PATH),
        "roi_test": load_csv(config.ROI_TEST_RESULTS_PATH),
        "roi_cv": load_csv(config.ROI_CV_RESULTS_PATH),
        "sales_importance": load_csv(config.SALES_IMPORTANCE_PATH),
        "roi_importance": load_csv(config.ROI_IMPORTANCE_PATH),
        "dataset": load_csv(config.PROCESSED_DATA_PATH),
    }


def best_model_names() -> tuple[str, str]:
    return (
        read_text(config.SALES_MODEL_NAME_PATH, "Linear Regression"),
        read_text(config.ROI_MODEL_NAME_PATH, "MLP Regressor"),
    )
