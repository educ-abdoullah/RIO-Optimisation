import streamlit as st

from app.components.kpis import business_note
from app.services.api_client import ApiHealth


def render_home_page(health: ApiHealth | None = None) -> None:
    st.markdown(
        """
        <div class="hero">
            <h1>Marketing ROI Optimizer</h1>
            <p>
                Un outil de pilotage pour simuler des budgets marketing, anticiper les ventes
                et estimer le retour sur investissement avant d'engager une campagne.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.2, 0.8], gap="large")
    with left:
        st.markdown("## Objectif de l'outil")
        st.write(
            "L'application aide une équipe marketing ou financière à comparer rapidement un scénario "
            "d'investissement entre TV, Radio, Social Media et influence. Elle transforme les modèles "
            "du projet Data Science en une interface claire, exploitable en soutenance ou en démonstration client."
        )
        business_note(
            "Valeur ajoutée : décider plus vite, expliquer les prévisions simplement et identifier les leviers "
            "budgétaires qui pèsent le plus sur les ventes et le ROI."
        )

    with right:
        st.markdown("## Utilisateurs cibles")
        st.markdown(
            """
            - Responsable marketing
            - CMO
            - Responsable acquisition
            - Direction commerciale
            - Direction financière
            """
        )

    st.markdown("## Deux fonctionnalités principales")
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="soft-panel">', unsafe_allow_html=True)
        st.markdown("### Prédiction des ventes")
        st.write(
            "Le modèle Linear Regression estime les ventes attendues à partir du scénario budgétaire. "
            "Dans ce projet, le budget TV est le facteur le plus déterminant pour cette prédiction."
        )
        st.caption("Performances : MAE ≈ 2.36 | RMSE ≈ 2.96 | R² ≈ 0.99898")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="soft-panel">', unsafe_allow_html=True)
        st.markdown("### Budget et impact ROI")
        st.write(
            "Le modèle MLP Regressor estime le ROI attendu. Le ROI est calculé comme ventes / budget total ; "
            "un ROI supérieur à 1 signifie que les ventes estimées dépassent le budget investi."
        )
        st.caption("Performances : MAE ≈ 0.0465 | RMSE ≈ 0.0672 | R² ≈ 0.9412")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("## Comprendre les métriques")
    m1, m2, m3 = st.columns(3, gap="large")
    with m1:
        st.markdown("### MAE")
        st.write("Erreur moyenne du modèle. Plus elle est faible, plus la prédiction est proche de la réalité.")
    with m2:
        st.markdown("### RMSE")
        st.write("Erreur qui pénalise davantage les grosses erreurs. Elle aide à repérer les écarts importants.")
    with m3:
        st.markdown("### R²")
        st.write("Part de la variation expliquée par le modèle. Plus c'est proche de 1, meilleur est le modèle.")

    with st.expander("Statut technique", expanded=False):
        if health and health.available:
            st.success("Service opérationnel")
        else:
            st.warning("Service API indisponible. L'application peut utiliser les modèles locaux si l'environnement le permet.")

    st.info("Passez au Dashboard pour lancer une simulation avec les deux modèles finaux.")
