import streamlit as st
import requests
import pandas as pd
import plotly.express as px


# ==============================
# Configuration
# ==============================

st.set_page_config(
    page_title="Marketing ROI Dashboard",
    page_icon="📊",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"


# ==============================
# Titre
# ==============================

st.title("📊 Dashboard Marketing : Sales & ROI")

st.markdown("""
Ce dashboard permet de simuler des scénarios marketing à partir des budgets investis 
en **TV**, **Radio**, **Social Media** et du type d'**influenceur**.

L'interface est séparée en deux parties :
- un onglet pour prédire les **ventes** ;
- un onglet pour estimer le **ROI**.
""")


# ==============================
# Vérification API
# ==============================

st.sidebar.header("État de l'API")

try:
    health_response = requests.get(f"{API_URL}/health", timeout=3)

    if health_response.status_code == 200:
        health_data = health_response.json()

        if health_data.get("sales_model_loaded"):
            st.sidebar.success("Modèle Sales chargé")
        else:
            st.sidebar.error("Modèle Sales non chargé")

        if health_data.get("roi_model_loaded"):
            st.sidebar.success("Modèle ROI chargé")
        else:
            st.sidebar.error("Modèle ROI non chargé")

    else:
        st.sidebar.error("API inaccessible")

except requests.exceptions.RequestException:
    st.sidebar.error("Impossible de contacter l'API")
    st.sidebar.info("Lance l'API avec : uvicorn api.main:app --reload")


# ==============================
# Fonction commune
# ==============================

def display_budget_chart(tv, radio, social_media, key_prefix):
    scenario_df = pd.DataFrame({
        "Canal": ["TV", "Radio", "Social Media"],
        "Budget": [tv, radio, social_media]
    })

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(
            scenario_df,
            use_container_width=True,
            key=f"{key_prefix}_budget_table"
        )

    with col2:
        fig = px.pie(
            scenario_df,
            names="Canal",
            values="Budget",
            title="Répartition du budget marketing"
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            key=f"{key_prefix}_budget_chart"
        )


def get_form_values(prefix: str):
    tv = st.number_input(
        "Budget TV",
        min_value=0.0,
        value=120.0,
        step=5.0,
        key=f"{prefix}_tv"
    )

    radio = st.number_input(
        "Budget Radio",
        min_value=0.0,
        value=30.0,
        step=5.0,
        key=f"{prefix}_radio"
    )

    social_media = st.number_input(
        "Budget Social Media",
        min_value=0.0,
        value=45.0,
        step=5.0,
        key=f"{prefix}_social"
    )

    influencer = st.selectbox(
        "Type d'influenceur",
        ["Mega", "Macro", "Micro", "Nano"],
        key=f"{prefix}_influencer"
    )

    payload = {
        "tv": tv,
        "radio": radio,
        "social_media": social_media,
        "influencer": influencer
    }

    return tv, radio, social_media, influencer, payload


# ==============================
# Onglets
# ==============================

tab_sales, tab_roi = st.tabs(["📈 Prédiction Sales", "💰 Estimation ROI"])


# ==============================
# Onglet Sales
# ==============================

with tab_sales:
    st.header("📈 Prédiction des ventes")

    st.markdown("""
    Cet onglet utilise le modèle entraîné pour prédire la variable **Sales** à partir des budgets marketing.
    """)

    tv, radio, social_media, influencer, payload = get_form_values("sales")

    st.subheader("Scénario sélectionné")
    display_budget_chart(tv, radio, social_media, key_prefix="sales")

    if st.button("Prédire les ventes", key="btn_sales"):
        try:
            response = requests.post(
                f"{API_URL}/predict/sales",
                json=payload,
                timeout=5
            )

            if response.status_code == 200:
                result = response.json()

                predicted_sales = result["predicted_sales"]
                total_budget = result["total_budget"]
                calculated_roi = result["calculated_roi_from_sales"]

                kpi1, kpi2, kpi3 = st.columns(3)

                with kpi1:
                    st.metric("Ventes prédites", f"{predicted_sales} M")

                with kpi2:
                    st.metric("Budget total", f"{total_budget} M")

                with kpi3:
                    st.metric("ROI calculé depuis Sales", calculated_roi)

                st.success("Prédiction des ventes réalisée avec succès.")

                st.markdown("### Interprétation")
                st.write(
                    f"Avec un budget TV de **{tv}**, Radio de **{radio}**, "
                    f"Social Media de **{social_media}** et un influenceur **{influencer}**, "
                    f"le modèle prédit environ **{predicted_sales} millions** de ventes."
                )

            else:
                st.error("Erreur API")
                st.json(response.json())

        except requests.exceptions.RequestException as e:
            st.error("Impossible d'appeler l'API Sales.")
            st.write(e)


# ==============================
# Onglet ROI
# ==============================

with tab_roi:
    st.header("💰 Estimation du ROI")

    st.markdown("""
    Cet onglet utilise un modèle dédié pour estimer directement le **ROI marketing**.
    """)

    tv, radio, social_media, influencer, payload = get_form_values("roi")

    st.subheader("Scénario sélectionné")
    display_budget_chart(tv, radio, social_media, key_prefix="roi")

    if st.button("Estimer le ROI", key="btn_roi"):
        try:
            response = requests.post(
                f"{API_URL}/predict/roi",
                json=payload,
                timeout=5
            )

            if response.status_code == 200:
                result = response.json()

                predicted_roi = result["predicted_roi"]
                total_budget = result["total_budget"]
                estimated_sales = result["estimated_sales_from_roi"]

                kpi1, kpi2, kpi3 = st.columns(3)

                with kpi1:
                    st.metric("ROI prédit", predicted_roi)

                with kpi2:
                    st.metric("Budget total", f"{total_budget} M")

                with kpi3:
                    st.metric("Ventes estimées depuis ROI", f"{estimated_sales} M")

                st.success("Estimation du ROI réalisée avec succès.")

                st.markdown("### Interprétation")
                st.write(
                    f"Avec un budget total de **{total_budget} millions**, "
                    f"le modèle estime un ROI de **{predicted_roi}**. "
                    f"Cela correspond à environ **{estimated_sales} millions** de ventes estimées "
                    f"à partir du ROI prédit."
                )

            else:
                st.error("Erreur API")
                st.json(response.json())

        except requests.exceptions.RequestException as e:
            st.error("Impossible d'appeler l'API ROI.")
            st.write(e)


# ==============================
# Informations modèles
# ==============================

st.markdown("---")
st.subheader("Informations techniques")

try:
    info_response = requests.get(f"{API_URL}/model-info", timeout=3)

    if info_response.status_code == 200:
        st.json(info_response.json())
    else:
        st.warning("Impossible de récupérer les informations des modèles.")

except requests.exceptions.RequestException:
    st.warning("API non disponible.")