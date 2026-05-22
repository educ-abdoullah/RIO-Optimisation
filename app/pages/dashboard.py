import streamlit as st

from app import config
from app.components.charts import (
    budget_bar_chart,
    budget_donut_chart,
    channel_share_chart,
    importance_chart,
    investment_outcome_chart,
    roi_gauge,
)
from app.components.kpis import business_note, kpi_card, meaning_card, model_performance_card
from app.services.api_client import ApiHealth
from app.services.data_loader import load_reports
from app.services.prediction_service import build_payload, predict_roi, predict_sales
from app.utils.formatting import dominant_channel, format_number, format_roi, roi_level


def _budget_form(prefix: str, submit_label: str) -> dict:
    with st.form(f"{prefix}_budget_form"):
        st.markdown("### Paramètres de simulation")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            tv = st.number_input("Budget TV", min_value=0.0, value=120.0, step=5.0, key=f"{prefix}_tv")
        with c2:
            radio = st.number_input("Budget Radio", min_value=0.0, value=30.0, step=5.0, key=f"{prefix}_radio")
        with c3:
            social_media = st.number_input(
                "Budget Social Media",
                min_value=0.0,
                value=45.0,
                step=5.0,
                key=f"{prefix}_social_media",
            )
        with c4:
            influencer = st.selectbox("Type d'influenceur", config.INFLUENCERS, index=1, key=f"{prefix}_influencer")
        submitted = st.form_submit_button(submit_label, use_container_width=True)

    return {
        "submitted": submitted,
        "payload": build_payload(tv, radio, social_media, influencer),
    }


def _show_error(result_error: str | None) -> bool:
    if not result_error:
        return False
    st.error(result_error)
    business_note(
        "La simulation n'a pas pu être réalisée. Vérifiez que le budget total est supérieur à zéro "
        "et que le service de prédiction ou les modèles locaux sont disponibles.",
        warning=True,
    )
    return True


def _technical_status(health: ApiHealth) -> None:
    with st.expander("Statut technique", expanded=False):
        if health.available:
            st.success("Service opérationnel")
        else:
            st.warning("Service API indisponible. Repli local tenté lorsque les dépendances et modèles sont disponibles.")


def render_dashboard_page(api_url: str, health: ApiHealth) -> None:
    st.markdown(
        """
        <div class="page-intro">
            <h1>Dashboard de pilotage marketing</h1>
            <p>
                Testez une combinaison budgétaire et obtenez une réponse métier claire :
                ventes attendues, retour sur investissement, canal dominant et leviers prioritaires.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    reports = load_reports()
    sales_imp, sales_imp_error = reports["sales_importance"]
    roi_imp, roi_imp_error = reports["roi_importance"]

    sales_tab, roi_tab = st.tabs(["Prédiction des ventes", "Budget & impact ROI"])

    with sales_tab:
        st.markdown("## Quel volume de ventes peut-on attendre ?")
        st.write(
            "Renseignez un scénario budgétaire pour estimer les ventes générées par la campagne. "
            "Le résultat sert à cadrer un niveau d'activité attendu avant arbitrage."
        )

        state = _budget_form("sales", "Prédire les ventes")
        payload = state["payload"]
        total_budget = payload["tv"] + payload["radio"] + payload["social_media"]

        if not state["submitted"]:
            c1, c2, c3 = st.columns(3)
            with c1:
                kpi_card("Budget total", format_number(total_budget, 2), "Scénario prêt à simuler")
            with c2:
                kpi_card("Ventes prédites", "À calculer", "Cliquez sur le bouton de simulation")
            with c3:
                kpi_card("Canal dominant", dominant_channel(payload["tv"], payload["radio"], payload["social_media"]))

            st.markdown('<div class="chart-shell">', unsafe_allow_html=True)
            st.plotly_chart(
                budget_bar_chart(payload["tv"], payload["radio"], payload["social_media"]),
                use_container_width=True,
                key="sales_initial_budget_distribution",
            )
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown('<div class="chart-shell">', unsafe_allow_html=True)
            st.plotly_chart(
                channel_share_chart(payload["tv"], payload["radio"], payload["social_media"]),
                use_container_width=True,
                key="sales_initial_channel_share",
            )
            st.markdown("</div>", unsafe_allow_html=True)
            model_performance_card("Linear Regression", "≈ 2.36", "≈ 2.96", "≈ 0.99898")
        else:
            result = predict_sales(payload, api_url, health)
            if not _show_error(result.error):
                c1, c2, c3 = st.columns(3)
                with c1:
                    kpi_card("Ventes prédites", format_number(result.predicted_sales, 2), "Résultat attendu du scénario")
                with c2:
                    kpi_card("Budget total", format_number(result.total_budget, 2), "TV + Radio + Social Media")
                with c3:
                    kpi_card("Canal dominant", dominant_channel(payload["tv"], payload["radio"], payload["social_media"]))

                business_note(
                    f"Le scénario prévoit environ <strong>{format_number(result.predicted_sales, 2)}</strong> de ventes. "
                    "Dans ce dataset, le budget TV est le levier le plus déterminant pour expliquer les ventes."
                )
                meaning_card(
                    "Ce que cela signifie : le scénario budgétaire peut être utilisé comme base de discussion "
                    "pour dimensionner les objectifs commerciaux et ajuster les arbitrages média."
                )

                c1, c2 = st.columns(2, gap="large")
                with c1:
                    st.markdown('<div class="chart-shell">', unsafe_allow_html=True)
                    st.plotly_chart(
                        budget_bar_chart(payload["tv"], payload["radio"], payload["social_media"]),
                        use_container_width=True,
                        key="sales_budget_distribution",
                    )
                    st.markdown("</div>", unsafe_allow_html=True)
                with c2:
                    st.markdown('<div class="chart-shell">', unsafe_allow_html=True)
                    st.plotly_chart(
                        investment_outcome_chart(result.total_budget, result.predicted_sales, "Ventes estimées"),
                        use_container_width=True,
                        key="sales_investment_outcome",
                    )
                    st.markdown("</div>", unsafe_allow_html=True)

                st.markdown('<div class="chart-shell">', unsafe_allow_html=True)
                st.plotly_chart(
                    channel_share_chart(payload["tv"], payload["radio"], payload["social_media"]),
                    use_container_width=True,
                    key="sales_channel_share",
                )
                st.markdown("</div>", unsafe_allow_html=True)

                fig_imp = importance_chart(sales_imp, "Variables importantes pour les ventes")
                if fig_imp:
                    st.markdown('<div class="chart-shell">', unsafe_allow_html=True)
                    st.plotly_chart(fig_imp, use_container_width=True, key="sales_feature_importance")
                    st.markdown("</div>", unsafe_allow_html=True)
                elif sales_imp_error:
                    st.warning("Le fichier d'importance des variables Sales est indisponible.")

                model_performance_card("Linear Regression", "≈ 2.36", "≈ 2.96", "≈ 0.99898")

    with roi_tab:
        st.markdown("## Quel ROI génère cette combinaison budgétaire ?")
        st.write(
            "Cet onglet répond directement à la question de rendement : pour le budget investi, "
            "quel retour sur investissement peut-on attendre ?"
        )
        meaning_card(
            "ROI = ventes / budget total. Un ROI supérieur à 1 signifie que les ventes estimées dépassent "
            "le budget investi. Plus le ROI est élevé, plus le scénario est rentable."
        )

        state = _budget_form("roi", "Estimer le ROI")
        payload = state["payload"]
        total_budget = payload["tv"] + payload["radio"] + payload["social_media"]

        if not state["submitted"]:
            c1, c2, c3 = st.columns(3)
            with c1:
                kpi_card("Budget total", format_number(total_budget, 2), "Investissement simulé")
            with c2:
                kpi_card("ROI prédit", "À calculer", "Simulation ROI à lancer")
            with c3:
                kpi_card("Niveau de rendement", "À évaluer", "Faible, moyen ou élevé")

            st.markdown('<div class="chart-shell">', unsafe_allow_html=True)
            st.plotly_chart(
                budget_donut_chart(payload["tv"], payload["radio"], payload["social_media"]),
                use_container_width=True,
                key="roi_initial_budget_distribution",
            )
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown('<div class="chart-shell">', unsafe_allow_html=True)
            st.plotly_chart(
                channel_share_chart(payload["tv"], payload["radio"], payload["social_media"]),
                use_container_width=True,
                key="roi_initial_channel_share",
            )
            st.markdown("</div>", unsafe_allow_html=True)
            model_performance_card("MLP Regressor", "≈ 0.0465", "≈ 0.0672", "≈ 0.9412")
        else:
            result = predict_roi(payload, api_url, health)
            if not _show_error(result.error):
                level, comment = roi_level(result.predicted_roi)
                c1, c2, c3 = st.columns(3)
                with c1:
                    kpi_card("ROI prédit", format_roi(result.predicted_roi), "Ventes / budget total")
                with c2:
                    kpi_card("Budget total", format_number(result.total_budget, 2), "Investissement simulé")
                with c3:
                    kpi_card("Niveau de rendement", level, "Lecture business du ROI")

                business_note(
                    f"Le ROI estimé est <strong>{format_roi(result.predicted_roi)}</strong>. {comment} "
                    "Les budgets TV et Radio sont les leviers qui pèsent le plus dans l'estimation du ROI."
                )
                meaning_card(
                    "Aide à la décision : utilisez ce score pour juger la qualité du budget simulé. "
                    "Un ROI faible invite à revoir le mix média ; un ROI supérieur à 1 signale un scénario plus attractif."
                )

                c1, c2 = st.columns(2, gap="large")
                with c1:
                    st.markdown('<div class="chart-shell">', unsafe_allow_html=True)
                    st.plotly_chart(roi_gauge(result.predicted_roi), use_container_width=True, key="roi_gauge_chart")
                    st.markdown("</div>", unsafe_allow_html=True)
                with c2:
                    st.markdown('<div class="chart-shell">', unsafe_allow_html=True)
                    st.plotly_chart(
                        budget_donut_chart(payload["tv"], payload["radio"], payload["social_media"]),
                        use_container_width=True,
                        key="roi_budget_distribution",
                    )
                    st.markdown("</div>", unsafe_allow_html=True)

                fig_imp = importance_chart(roi_imp, "Variables importantes pour le ROI")
                if fig_imp:
                    st.markdown('<div class="chart-shell">', unsafe_allow_html=True)
                    st.plotly_chart(fig_imp, use_container_width=True, key="roi_feature_importance")
                    st.markdown("</div>", unsafe_allow_html=True)
                elif roi_imp_error:
                    st.warning("Le fichier d'importance des variables ROI est indisponible.")

                model_performance_card("MLP Regressor", "≈ 0.0465", "≈ 0.0672", "≈ 0.9412")

    _technical_status(health)
