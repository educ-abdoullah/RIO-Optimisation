from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from app.config import MODEL_ORDER

COLORWAY = ["#2463eb", "#0f8a70", "#f59e0b", "#94a3b8"]


def _polish(fig):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#1f2937"),
        title_font=dict(size=18, color="#182230", family="Arial"),
        margin=dict(l=24, r=24, t=58, b=34),
        hoverlabel=dict(bgcolor="#ffffff", font_color="#182230", bordercolor="#dbe5f2"),
        legend=dict(font=dict(color="#1f2937"), bgcolor="rgba(255,255,255,0)"),
        uniformtext=dict(mode="show", minsize=11),
    )
    fig.update_xaxes(title_font=dict(color="#1f2937"), tickfont=dict(color="#1f2937"))
    fig.update_yaxes(title_font=dict(color="#1f2937"), tickfont=dict(color="#1f2937"))
    return fig


def budget_bar_chart(tv: float, radio: float, social_media: float):
    df = pd.DataFrame(
        {
            "Canal": ["TV", "Radio", "Social Media"],
            "Budget": [tv, radio, social_media],
        }
    )
    fig = px.bar(
        df,
        x="Canal",
        y="Budget",
        color="Canal",
        text="Budget",
        color_discrete_sequence=COLORWAY,
        title="Répartition du budget par canal",
    )
    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside",
        textfont=dict(color="#182230", size=13),
        marker_line_width=0,
    )
    fig.update_layout(showlegend=False, yaxis_title="Budget", xaxis_title="", height=350, bargap=.28)
    fig.update_yaxes(gridcolor="#eef2f7", zerolinecolor="#dbe5f2")
    return _polish(fig)


def budget_donut_chart(tv: float, radio: float, social_media: float):
    df = pd.DataFrame(
        {
            "Canal": ["TV", "Radio", "Social Media"],
            "Budget": [tv, radio, social_media],
        }
    )
    fig = px.pie(
        df,
        names="Canal",
        values="Budget",
        hole=0.58,
        color_discrete_sequence=COLORWAY,
        title="Mix budgétaire",
    )
    fig.update_traces(
        textinfo="percent+label",
        textposition="outside",
        textfont=dict(color="#182230", size=13),
        marker=dict(line=dict(color="#ffffff", width=3)),
        automargin=True,
    )
    fig.update_layout(
        height=350,
        showlegend=True,
        annotations=[dict(text="Budget", x=.5, y=.5, showarrow=False, font_size=15, font_color="#182230")],
    )
    return _polish(fig)


def roi_gauge(roi: float | None):
    value = 0 if roi is None else max(0, min(float(roi), 1.5))
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={"valueformat": ".4f"},
            title={"text": "ROI prédit", "font": {"size": 18, "color": "#182230"}},
            gauge={
                "axis": {"range": [0, 1.5]},
                "bar": {"color": "#0f8a70", "thickness": .28},
                "bgcolor": "#ffffff",
                "borderwidth": 1,
                "bordercolor": "#dbe5f2",
                "steps": [
                    {"range": [0, 0.4], "color": "#fff1f2"},
                    {"range": [0.4, 0.7], "color": "#fff7ed"},
                    {"range": [0.7, 1.0], "color": "#eff6ff"},
                    {"range": [1.0, 1.5], "color": "#ecfdf5"},
                ],
                "threshold": {"line": {"color": "#2463eb", "width": 4}, "value": 1},
            },
        )
    )
    fig.update_layout(height=320, margin=dict(l=20, r=20, t=50, b=10), paper_bgcolor="rgba(0,0,0,0)")
    return _polish(fig)


def model_comparison_chart(df: pd.DataFrame | None, title: str, final_model: str):
    if df is None or df.empty:
        return None
    chart_df = df.copy()
    chart_df["model"] = pd.Categorical(chart_df["model"], categories=MODEL_ORDER, ordered=True)
    chart_df = chart_df.sort_values("model")
    chart_df["Statut"] = chart_df["model"].astype(str).eq(final_model).map({True: "Modèle final", False: "Modèle testé"})
    fig = px.bar(
        chart_df,
        x="model",
        y="R2",
        color="Statut",
        hover_data=["MAE", "RMSE"],
        color_discrete_map={"Modèle final": "#0f766e", "Modèle testé": "#cbd5e1"},
        title=title,
    )
    fig.update_layout(xaxis_title="", yaxis_title="R² test", height=390, legend_title="")
    fig.update_xaxes(tickangle=-25)
    return _polish(fig)


def importance_chart(df: pd.DataFrame | None, title: str):
    if df is None or df.empty:
        return None
    chart_df = df.copy()
    chart_df["importance_mean"] = chart_df["importance_mean"].clip(lower=0)
    chart_df = chart_df.sort_values("importance_mean", ascending=True)
    fig = px.bar(
        chart_df,
        x="importance_mean",
        y="feature",
        orientation="h",
        error_x="importance_std" if "importance_std" in chart_df.columns else None,
        color="importance_mean",
        color_continuous_scale=["#dbeafe", "#2463eb"],
        title=title,
    )
    fig.update_layout(xaxis_title="Importance moyenne", yaxis_title="", height=330, coloraxis_showscale=False)
    fig.update_xaxes(gridcolor="#eef2f7")
    fig.update_traces(marker_line_width=0, textfont=dict(color="#182230"))
    return _polish(fig)


def budget_vs_sales_chart(dataset: pd.DataFrame | None, predicted_sales: float | None, total_budget: float):
    if dataset is None or dataset.empty or "total_budget" not in dataset.columns or "sales" not in dataset.columns:
        return None
    sample = dataset.sample(min(600, len(dataset)), random_state=7)
    fig = px.scatter(
        sample,
        x="total_budget",
        y="sales",
        opacity=0.45,
        color_discrete_sequence=["#94a3b8"],
        title="Budget total vs ventes observées",
    )
    if predicted_sales is not None:
        fig.add_trace(
            go.Scatter(
                x=[total_budget],
                y=[predicted_sales],
                mode="markers",
                marker=dict(size=15, color="#0f766e", line=dict(width=2, color="#ffffff")),
                name="Scénario simulé",
            )
        )
    fig.update_layout(height=380, xaxis_title="Budget total", yaxis_title="Sales")
    return _polish(fig)


def investment_outcome_chart(total_budget: float, predicted_value: float | None, outcome_label: str):
    df = pd.DataFrame(
        {
            "Indicateur": ["Budget investi", outcome_label],
            "Valeur": [total_budget, predicted_value or 0],
        }
    )
    fig = px.bar(
        df,
        x="Indicateur",
        y="Valeur",
        color="Indicateur",
        text="Valeur",
        color_discrete_sequence=["#94a3b8", "#0f8a70"],
        title="Budget investi vs résultat estimé",
    )
    fig.update_traces(texttemplate="%{text:.2f}", textposition="outside", textfont=dict(color="#182230", size=13), marker_line_width=0)
    fig.update_layout(showlegend=False, height=330, xaxis_title="", yaxis_title="Valeur", bargap=.36)
    fig.update_yaxes(gridcolor="#eef2f7", zerolinecolor="#dbe5f2")
    return _polish(fig)


def channel_share_chart(tv: float, radio: float, social_media: float):
    total = tv + radio + social_media
    values = [tv, radio, social_media]
    shares = [0 if total == 0 else value / total * 100 for value in values]
    df = pd.DataFrame(
        {
            "Canal": ["TV", "Radio", "Social Media"],
            "Part du budget": shares,
        }
    )
    fig = px.bar(
        df,
        y="Canal",
        x="Part du budget",
        orientation="h",
        color="Canal",
        text="Part du budget",
        color_discrete_sequence=COLORWAY,
        title="Poids de chaque canal dans le budget",
    )
    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        textfont=dict(color="#182230", size=13),
        marker_line_width=0,
    )
    fig.update_layout(showlegend=False, height=310, xaxis_title="Part du budget (%)", yaxis_title="")
    fig.update_xaxes(range=[0, max(100, max(shares) + 12)], gridcolor="#eef2f7", zerolinecolor="#dbe5f2")
    return _polish(fig)

