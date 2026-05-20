from __future__ import annotations

import streamlit as st


def kpi_card(label: str, value: str, help_text: str = "") -> None:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-help">{help_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def business_note(text: str, warning: bool = False) -> None:
    css_class = "warning-note" if warning else "business-note"
    st.markdown(f'<div class="{css_class}">{text}</div>', unsafe_allow_html=True)


def model_performance_card(model_name: str, mae: str, rmse: str, r2: str) -> None:
    st.markdown(
        f"""
        <div class="model-card">
            <div class="model-card-title">Informations modèle</div>
            <div class="model-badges">
                <div class="model-badge">
                    <div class="model-badge-label">Modèle final</div>
                    <div class="model-badge-value">{model_name}</div>
                </div>
                <div class="model-badge">
                    <div class="model-badge-label">MAE</div>
                    <div class="model-badge-value">{mae}</div>
                </div>
                <div class="model-badge">
                    <div class="model-badge-label">RMSE</div>
                    <div class="model-badge-value">{rmse}</div>
                </div>
                <div class="model-badge">
                    <div class="model-badge-label">R²</div>
                    <div class="model-badge-value">{r2}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def meaning_card(text: str) -> None:
    st.markdown(f'<div class="meaning-card">{text}</div>', unsafe_allow_html=True)
