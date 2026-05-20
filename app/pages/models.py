import streamlit as st

from app.components.charts import importance_chart, model_comparison_chart
from app.components.kpis import business_note
from app.services.data_loader import best_model_names, load_reports


def _show_dataframe(df, label: str) -> None:
    if df is None:
        st.warning(f"{label} indisponible.")
        return
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_models_page() -> None:
    st.title("Comparaison des modèles & interprétabilité")
    st.write(
        "Cette page synthétise les résultats sauvegardés dans le dossier `reports` et les modèles retenus "
        "dans le dossier `models`."
    )

    reports = load_reports()
    sales_model_name, roi_model_name = best_model_names()
    sales_test, sales_error = reports["sales_test"]
    roi_test, roi_error = reports["roi_test"]
    sales_imp, sales_imp_error = reports["sales_importance"]
    roi_imp, roi_imp_error = reports["roi_importance"]

    if sales_error:
        st.warning(sales_error)
    if roi_error:
        st.warning(roi_error)

    tab_sales, tab_roi, tab_interpretation = st.tabs(["Sales", "ROI", "Lecture métier"])

    with tab_sales:
        st.subheader("Prédiction des ventes")
        st.info("Modèle final : Linear Regression | MAE ≈ 2.36 | RMSE ≈ 2.96 | R² ≈ 0.99898")
        fig = model_comparison_chart(sales_test, "Comparaison des modèles Sales", sales_model_name)
        if fig:
            st.plotly_chart(fig, use_container_width=True, key="models_sales_comparison")
        _show_dataframe(sales_test, "Résultats Sales")

        if sales_imp_error:
            st.warning(sales_imp_error)
        fig_imp = importance_chart(sales_imp, "Importance des variables pour Sales")
        if fig_imp:
            st.plotly_chart(fig_imp, use_container_width=True, key="models_sales_importance")

    with tab_roi:
        st.subheader("Estimation du ROI")
        st.info("Modèle final : MLP Regressor | MAE ≈ 0.0465 | RMSE ≈ 0.0672 | R² ≈ 0.9412")
        fig = model_comparison_chart(roi_test, "Comparaison des modèles ROI", roi_model_name)
        if fig:
            st.plotly_chart(fig, use_container_width=True, key="models_roi_comparison")
        _show_dataframe(roi_test, "Résultats ROI")

        if roi_imp_error:
            st.warning(roi_imp_error)
        fig_imp = importance_chart(roi_imp, "Importance des variables pour ROI")
        if fig_imp:
            st.plotly_chart(fig_imp, use_container_width=True, key="models_roi_importance")

    with tab_interpretation:
        st.subheader("Interprétation métier")
        business_note(
            "Pour la prédiction des ventes, le budget TV ressort comme le facteur dominant. "
            "Le modèle Linear Regression est donc cohérent avec une lecture simple et actionnable."
        )
        st.write("")
        business_note(
            "Pour l'estimation du ROI, TV et Radio sont les variables les plus importantes. "
            "Social Media a un effet plus faible dans ce dataset, et le type d'influenceur semble peu influent."
        )
        st.write(
            "Ces résultats ne signifient pas que les influenceurs ou le social media sont inutiles dans tous les contextes. "
            "Ils indiquent simplement que, dans les données disponibles ici, leur contribution marginale est moins marquée."
        )
