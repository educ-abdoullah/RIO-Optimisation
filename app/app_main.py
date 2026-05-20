import streamlit as st

from app.config import DEFAULT_API_URL
from app.pages.home import render_home_page
from app.pages.dashboard import render_dashboard_page
from app.services.api_client import check_api_health
from app.ui.styles import apply_global_styles


def main() -> None:
    st.set_page_config(
        page_title="Marketing ROI Optimizer",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    apply_global_styles()

    with st.sidebar:
        st.markdown("### Marketing ROI Optimizer")
        st.caption("Simulation business des ventes et du ROI")
        page = st.radio(
            "Navigation",
            ["Accueil", "Dashboard"],
            label_visibility="collapsed",
        )
        api_url = DEFAULT_API_URL
        health = check_api_health(api_url)

    if page == "Accueil":
        render_home_page(health=health)
    else:
        render_dashboard_page(api_url=api_url, health=health)


if __name__ == "__main__":
    main()
