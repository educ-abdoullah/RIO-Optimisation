import streamlit as st


def apply_global_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --brand: #2463eb;
            --brand-dark: #1d4ed8;
            --brand-soft: #eff6ff;
            --green: #0f8a70;
            --green-soft: #ecfdf5;
            --ink: #182230;
            --muted: #667085;
            --line: #dbe5f2;
            --soft: #f6f9ff;
            --accent: #f59e0b;
            --accent-soft: #fff7ed;
            --panel: #ffffff;
        }

        html, body, .stApp, [data-testid="stAppViewContainer"] {
            background: linear-gradient(180deg, #f8fbff 0%, #eef5ff 100%);
            color: var(--ink);
        }

        [data-testid="stHeader"] {
            background: rgba(248, 251, 255, .86);
            color: var(--ink);
        }

        [data-testid="stToolbar"], [data-testid="stDecoration"] {
            background: transparent;
        }

        [data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid var(--line);
        }

        [data-testid="stSidebar"] *,
        [data-testid="stMarkdownContainer"],
        label,
        p,
        span {
            color: var(--ink);
        }

        .block-container {
            padding-top: 1.6rem;
            padding-bottom: 3rem;
            max-width: 1220px;
        }

        h1, h2, h3, h4 {
            color: var(--ink);
            letter-spacing: 0;
        }

        .hero {
            padding: 2.4rem 2.5rem;
            border: 1px solid var(--line);
            border-radius: 8px;
            background: linear-gradient(135deg, #ffffff 0%, #eff6ff 58%, #ecfdf5 100%);
            margin-bottom: 1.4rem;
            box-shadow: 0 16px 38px rgba(37, 99, 235, .08);
        }

        .hero h1 {
            margin-bottom: .5rem;
            font-size: 2.35rem;
        }

        .hero p, .muted {
            color: var(--muted);
            font-size: 1.02rem;
            line-height: 1.6;
        }

        .section {
            padding: 1.4rem 0 .5rem 0;
        }

        .soft-panel {
            border: 1px solid var(--line);
            border-radius: 8px;
            background: var(--panel);
            padding: 1rem 1.1rem;
            box-shadow: 0 8px 24px rgba(15, 23, 42, .04);
        }

        .page-intro {
            border: 1px solid var(--line);
            border-radius: 8px;
            background: linear-gradient(135deg, #ffffff 0%, #eff6ff 72%, #ecfdf5 100%);
            padding: 1.35rem 1.45rem;
            margin-bottom: 1.2rem;
            box-shadow: 0 14px 34px rgba(31, 78, 121, .07);
        }

        .page-intro p {
            color: var(--muted);
            margin-bottom: 0;
            line-height: 1.55;
        }

        .kpi-card {
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 1.05rem 1.1rem;
            background: #ffffff;
            min-height: 118px;
            box-shadow: 0 12px 32px rgba(31, 78, 121, .07);
        }

        .kpi-label {
            color: var(--muted);
            font-size: .82rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: .04em;
            margin-bottom: .35rem;
        }

        .kpi-value {
            color: var(--brand-dark);
            font-size: 1.75rem;
            font-weight: 800;
            line-height: 1.15;
        }

        .kpi-help {
            color: var(--muted);
            font-size: .88rem;
            margin-top: .45rem;
        }

        .business-note {
            border-left: 4px solid var(--brand);
            background: #eff6ff;
            padding: 1.05rem 1.15rem;
            border-radius: 0 8px 8px 0;
            color: #1e3a8a;
            line-height: 1.55;
            margin: .65rem 0 1rem;
        }

        .warning-note {
            border-left: 4px solid var(--accent);
            background: #fffbeb;
            padding: .9rem 1rem;
            border-radius: 0 8px 8px 0;
            color: #78350f;
        }

        .model-card {
            border: 1px solid var(--line);
            border-radius: 8px;
            background: rgba(255, 255, 255, .88);
            padding: .95rem 1rem;
            margin-top: 1rem;
            box-shadow: 0 8px 22px rgba(31, 78, 121, .05);
        }

        .model-card-title {
            font-size: .86rem;
            color: var(--muted);
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: .04em;
            margin-bottom: .65rem;
        }

        .model-badges {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: .55rem;
        }

        .model-badge {
            background: #f8fbff;
            border: 1px solid #dbeafe;
            border-radius: 8px;
            padding: .68rem .72rem;
        }

        .model-badge-label {
            color: var(--muted);
            font-size: .76rem;
            font-weight: 700;
            margin-bottom: .18rem;
        }

        .model-badge-value {
            color: var(--ink);
            font-size: .98rem;
            font-weight: 800;
        }

        .meaning-card {
            border: 1px solid #d1fae5;
            border-radius: 8px;
            background: linear-gradient(135deg, #ffffff 0%, #ecfdf5 100%);
            padding: 1rem 1.1rem;
            color: #064e3b;
            line-height: 1.55;
        }

        .chart-shell {
            border: 1px solid var(--line);
            border-radius: 8px;
            background: white;
            padding: .65rem .7rem .25rem;
            box-shadow: 0 10px 28px rgba(31, 78, 121, .055);
        }

        div[data-testid="stMetric"] {
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: .85rem 1rem;
            background: white;
        }

        div[data-testid="stTabs"] button p {
            font-size: 1rem;
            font-weight: 700;
        }

        div[data-testid="stTabs"] [role="tablist"] {
            gap: .4rem;
            border-bottom: 1px solid var(--line);
        }

        div[data-testid="stTabs"] [role="tab"] {
            background: #ffffff;
            border: 1px solid var(--line);
            border-bottom: 0;
            border-radius: 8px 8px 0 0;
            padding: .45rem .75rem;
        }

        .stButton > button, .stFormSubmitButton > button {
            background: var(--brand);
            color: white;
            border-radius: 8px;
            border: 0;
            font-weight: 700;
        }

        .stButton > button:hover, .stFormSubmitButton > button:hover {
            background: var(--brand-dark);
            color: white;
            border: 0;
        }

        .stButton > button *, .stFormSubmitButton > button * {
            color: white;
        }

        input, textarea, select {
            color: var(--ink) !important;
            background: white !important;
        }

        [data-baseweb="select"],
        [data-baseweb="select"] > div,
        [data-baseweb="select"] div {
            background-color: #ffffff !important;
            color: var(--ink) !important;
            border-color: var(--line) !important;
        }

        [data-baseweb="select"] span,
        [data-baseweb="select"] input,
        [data-baseweb="select"] div[role="button"],
        [data-baseweb="select"] [aria-selected] {
            color: var(--ink) !important;
        }

        [data-baseweb="select"] svg {
            fill: var(--ink) !important;
            color: var(--ink) !important;
        }

        [data-baseweb="popover"],
        [data-baseweb="popover"] *,
        [role="listbox"],
        [role="option"] {
            background-color: #ffffff !important;
            color: var(--ink) !important;
        }

        [role="option"]:hover {
            background-color: var(--brand-soft) !important;
            color: var(--ink) !important;
        }

        div[data-testid="stSelectbox"] label,
        div[data-testid="stSelectbox"] p,
        div[data-testid="stSelectbox"] span {
            color: var(--ink) !important;
        }

        .small-caption {
            color: var(--muted);
            font-size: .9rem;
            line-height: 1.5;
        }

        @media (max-width: 760px) {
            .model-badges {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
