import sys
from pathlib import Path

APP_DIR  = Path(__file__).resolve().parent
ROOT_DIR = APP_DIR.parent
sys.path.insert(0, str(APP_DIR))
sys.path.insert(0, str(ROOT_DIR))

import streamlit as st

st.set_page_config(
    page_title="SigmaPulse",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap"
          rel="stylesheet">

    <style>

    /* ─── Masquer nav auto Streamlit ─────────────────────────────────────── */
    [data-testid="stSidebarNav"],
    [data-testid="stSidebarNavItems"],
    [data-testid="stSidebarNavSeparator"] { display: none !important; }

    /* ─── Base ───────────────────────────────────────────────────────────── */
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', sans-serif !important;
        background: #F1F5F9 !important;
        color: #1E293B !important;
    }

    /* ─── Sidebar — fond clair ───────────────────────────────────────────── */
    [data-testid="stSidebar"] > div:first-child {
        background: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
        min-width: 256px !important;
        padding: 0 !important;
    }
    [data-testid="stSidebar"] * { color: #64748B !important; }

    /* ─── Boutons nav sidebar ─────────────────────────────────────────────── */
    [data-testid="stSidebar"] .stButton { margin: 0 !important; padding: 0 !important; }
    [data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        color: #64748B !important;
        border: none !important;
        border-radius: 6px !important;
        text-align: left !important;
        font-size: 0.875rem !important;
        font-weight: 400 !important;
        padding: 8px 14px !important;
        width: 100% !important;
        box-shadow: none !important;
        margin: 0 !important;
        transition: background 0.15s, color 0.15s !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: #F8FAFC !important;
        color: #1E293B !important;
    }
    [data-testid="stSidebar"] .stButton > button:focus,
    [data-testid="stSidebar"] .stButton > button:active {
        background: #F8FAFC !important;
        box-shadow: none !important;
        outline: none !important;
        color: #1E293B !important;
    }

    /* ─── Main content ────────────────────────────────────────────────────── */
    .main .block-container {
        padding: 36px 44px 64px;
        max-width: 1360px;
    }

    /* ─── Titres ──────────────────────────────────────────────────────────── */
    h1, h2, h3, h4 { color: #0F172A !important; font-weight: 700; }
    h1 { font-size: 1.75rem; letter-spacing: -0.03em; }
    h2 { font-size: 1.35rem; letter-spacing: -0.02em; }

    /* ─── Section header ──────────────────────────────────────────────────── */
    .section-header {
        font-size: 0.70rem;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.10em;
        margin: 32px 0 14px;
        padding: 0;
    }

    /* ─── Cards génériques ────────────────────────────────────────────────── */
    .card {
        background: #ffffff;
        border-radius: 10px;
        padding: 22px 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
    }

    /* ─── Dataframes ──────────────────────────────────────────────────────── */
    .stDataFrame { border-radius: 8px !important; }

    /* ─── Tabs ────────────────────────────────────────────────────────────── */
    [data-baseweb="tab-list"] {
        background: transparent !important;
        border-bottom: 1px solid #E2E8F0 !important;
        gap: 0 !important;
    }
    [data-baseweb="tab"] {
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        color: #94A3B8 !important;
        padding: 8px 18px !important;
        border-radius: 0 !important;
        border-bottom: 2px solid transparent !important;
    }
    [aria-selected="true"] {
        color: #4338CA !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #4338CA !important;
    }

    /* ─── Boutons principaux ──────────────────────────────────────────────── */
    .main .stButton > button {
        background: #4338CA !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        padding: 8px 18px !important;
        transition: background 0.15s !important;
    }
    .main .stButton > button:hover { background: #3730A3 !important; }

    /* ─── Inputs ──────────────────────────────────────────────────────────── */
    .stTextInput > div > div > input,
    .stSelectbox > div > div {
        border: 1px solid #CBD5E1 !important;
        border-radius: 6px !important;
        font-size: 0.875rem !important;
        background: white !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #4338CA !important;
        box-shadow: 0 0 0 2px rgba(67,56,202,0.10) !important;
        outline: none !important;
    }

    /* ─── Radio ───────────────────────────────────────────────────────────── */
    .main .stRadio label {
        font-size: 0.875rem !important;
        color: #374151 !important;
    }
    .main [data-baseweb="radio"] > div:first-child {
        border-color: #CBD5E1 !important;
    }
    .main [aria-checked="true"] > div:first-child {
        border-color: #4338CA !important;
        background-color: #4338CA !important;
    }

    /* ─── Metriques ───────────────────────────────────────────────────────── */
    [data-testid="stMetricValue"] {
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: #0F172A !important;
        letter-spacing: -0.03em !important;
    }
    [data-testid="stMetricLabel"] { font-size: 0.78rem !important; color: #94A3B8 !important; }
    [data-testid="stMetricDelta"] { font-size: 0.78rem !important; }

    /* ─── Info / warning / success ────────────────────────────────────────── */
    .stAlert {
        border-radius: 8px !important;
        border-left-width: 3px !important;
        font-size: 0.875rem !important;
    }

    /* ─── Spinner ─────────────────────────────────────────────────────────── */
    .stSpinner > div { border-top-color: #4338CA !important; }

    /* ─── Scrollbar ───────────────────────────────────────────────────────── */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #94A3B8; }

    /* ─── Divider ─────────────────────────────────────────────────────────── */
    hr { border: none; border-top: 1px solid #E2E8F0; margin: 24px 0; }

    /* ─── Expander ────────────────────────────────────────────────────────── */
    details > summary { font-weight: 600; font-size: 0.9rem; color: #1E293B; }
    details { border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px 16px;
              background: white; }

    /* ─── Caption ─────────────────────────────────────────────────────────── */
    .stCaption { font-size: 0.78rem !important; color: #94A3B8 !important; }

    </style>
    """,
    unsafe_allow_html=True,
)

# ── Imports pages ─────────────────────────────────────────────────────────────
from pages import (
    p1_about, p2_vue_globale, p3_exploration,
    p4_shap, p5_comparaison, p6_documentation, p7_pays, p8_conclusion,
)

# ── Pages ─────────────────────────────────────────────────────────────────────
NAV_ITEMS = [
    ("A propos du projet",       "house",            p1_about.render,        "Projet"),
    ("Vue globale",              "globe2",           p2_vue_globale.render,  "Analyse"),
    ("Exploration des clusters", "diagram-3",        p3_exploration.render,  "Analyse"),
    ("Analyse d'un pays",        "search",           p7_pays.render,         "Analyse"),
    ("Interpretabilite SHAP",    "cpu",              p4_shap.render,         "Analyse"),
    ("Comparaison des modeles",  "bar-chart-line",   p5_comparaison.render,  "Resultats"),
    ("Conclusion",               "flag",             p8_conclusion.render,   "Resultats"),
    ("Documentation",            "book",             p6_documentation.render,"Resultats"),
]

if "page" not in st.session_state:
    st.session_state.page = NAV_ITEMS[0][0]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:

    # ── Marque ────────────────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="padding:28px 20px 22px;border-bottom:1px solid #F1F5F9;">
          <p style="font-size:1rem;font-weight:700;margin:0;color:#0F172A;
                    letter-spacing:-0.02em;">SigmaPulse</p>
          <p style="font-size:0.70rem;color:#94A3B8;margin:3px 0 0;font-weight:500;
                    letter-spacing:0.04em;text-transform:uppercase;">
            Clustering humanitaire · ML2
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Navigation ────────────────────────────────────────────────────────────
    st.markdown('<div style="padding:16px 10px 8px;">', unsafe_allow_html=True)

    current_group = None
    for label, icon, render_fn, group in NAV_ITEMS:
        if group != current_group:
            current_group = group
            st.markdown(
                f'<p style="font-size:0.60rem;font-weight:600;letter-spacing:0.12em;'
                f'text-transform:uppercase;color:#CBD5E1;'
                f'margin:18px 0 4px 10px;padding:0;">{group}</p>',
                unsafe_allow_html=True,
            )

        is_active = st.session_state.page == label

        if is_active:
            st.markdown(
                f"""
                <div style="display:flex;align-items:center;gap:10px;
                            padding:9px 14px;margin:1px 0;
                            background:#EEF2FF;
                            border-left:3px solid #4338CA;
                            border-radius:0 8px 8px 0;">
                  <i class="bi bi-{icon}"
                     style="font-size:0.85rem;color:#4338CA;flex-shrink:0;"></i>
                  <span style="font-size:0.875rem;font-weight:600;
                               color:#3730A3;">{label}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            clicked = st.button(label, key=f"nav_{label}", width="stretch")
            if clicked:
                st.session_state.page = label
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="position:absolute;bottom:0;left:0;right:0;
                    padding:16px 20px;border-top:1px solid #F1F5F9;">
          <p style="font-size:0.67rem;color:#CBD5E1;margin:0;font-weight:500;
                    letter-spacing:0.03em;">
            Equipe SigmaPulse · 2025
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Rendu page ────────────────────────────────────────────────────────────────
render_map = {label: fn for label, _, fn, _ in NAV_ITEMS}
render_map[st.session_state.page]()
