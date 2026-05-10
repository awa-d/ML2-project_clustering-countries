import streamlit as st
from config import PRIMARY, SECONDARY, FEAT_K3, FEAT_K4, FSI_COLS


# Dictionnaire complet des variables avec descriptions
_VAR_DESCRIPTIONS = {
    # Variables classiques
    "life_expec":                   ("Esperance de vie a la naissance (annees)", "classique"),
    "child_mort_log":               ("Mortalite infantile pour 1000 naissances (log)", "classique"),
    "total_fer":                    ("Indice synthetique de fecondite (enfants/femme)", "classique"),
    "gdpp_log":                     ("PIB par habitant en PPA USD (log)", "classique"),
    "health":                       ("Depenses de sante en % du PIB", "classique"),
    "inflation_log":                ("Taux d'inflation annuel % (log signee)", "classique"),
    "exports_log":                  ("Exportations de biens et services % PIB (log)", "classique"),
    "imports_log":                  ("Importations de biens et services % PIB (log)", "classique"),
    # Variables enrichies supplementaires
    "physicians_per_1000":          ("Medecins pour 1000 habitants", "enrichi"),
    "hiv_prevalence_log":           ("Prevalence du VIH % population adulte (log)", "enrichi"),
    "vaccination_dpt_log":          ("Couverture vaccinale DTP % enfants (log)", "enrichi"),
    "social_undernourishment_log":  ("Taux de sous-alimentation % pop. (log)", "enrichi"),
    "social_poverty_2_15_log":      ("Part de la pop. sous 2,15 USD/jour (log)", "enrichi"),
    "social_schooling_log":         ("Duree moyenne de scolarisation annees (log)", "enrichi"),
    # FSI
    "security_apparatus":           ("FSI — Appareil securitaire (0-10, 10=plus fragile)", "fsi"),
    "group_grievance":              ("FSI — Tensions et griefs communautaires (0-10)", "fsi"),
    "refugees_idps":                ("FSI — Refugies et deplaces internes (0-10)", "fsi"),
    "external_intervention":        ("FSI — Intervention de forces etrangeres (0-10)", "fsi"),
}


def render():
    st.markdown(
        f"<h2 style='color:{PRIMARY};margin-bottom:4px;'>Documentation & Ressources</h2>",
        unsafe_allow_html=True,
    )

    # ── Dictionnaire des variables ─────────────────────────────────────────────
    st.markdown(f"<p class='section-header'>Dictionnaire des variables</p>",
                unsafe_allow_html=True)

    tab_cls, tab_enr, tab_fsi = st.tabs([
        f"Modele classique ({len(FEAT_K3)} var.)",
        f"Modele enrichi supplementaires",
        f"Indicateurs FSI ({len(FSI_COLS)} var.)",
    ])

    with tab_cls:
        st.markdown(
            f"""
            <p style="color:#4a5568;font-size:0.9rem;margin-bottom:16px;">
              Variables du dataset HELP ONG. Transformations log appliquees sur les
              distributions a fort biais (|skewness| &gt; 1) pour normaliser les echelles.
            </p>
            """,
            unsafe_allow_html=True,
        )
        for var in FEAT_K3:
            desc, _ = _VAR_DESCRIPTIONS.get(var, (var, ""))
            st.markdown(
                f"""
                <div style="background:white;border-radius:8px;padding:12px 16px;
                            margin-bottom:8px;border-left:3px solid {SECONDARY};
                            box-shadow:0 1px 4px rgba(0,0,0,0.05);">
                  <code style="background:#f0f4ff;color:{PRIMARY};padding:2px 8px;
                               border-radius:4px;font-size:0.88rem;">{var}</code>
                  &nbsp;&nbsp;
                  <span style="color:#4a5568;font-size:0.9rem;">{desc}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with tab_enr:
        supplementaires = [v for v in FEAT_K4 if v not in FEAT_K3 and v not in FSI_COLS]
        st.markdown(
            f"""
            <p style="color:#4a5568;font-size:0.9rem;margin-bottom:16px;">
              Variables ajoutees dans le modele enrichi (sources WHO, Banque Mondiale, ACLED).
              Ces {len(supplementaires)} variables complementent les 8 classiques
              et les 4 indicateurs FSI.
            </p>
            """,
            unsafe_allow_html=True,
        )
        for var in supplementaires:
            desc, _ = _VAR_DESCRIPTIONS.get(var, (var, ""))
            st.markdown(
                f"""
                <div style="background:white;border-radius:8px;padding:12px 16px;
                            margin-bottom:8px;border-left:3px solid #9B59B6;
                            box-shadow:0 1px 4px rgba(0,0,0,0.05);">
                  <code style="background:#f8f0ff;color:#6b21a8;padding:2px 8px;
                               border-radius:4px;font-size:0.88rem;">{var}</code>
                  &nbsp;&nbsp;
                  <span style="color:#4a5568;font-size:0.9rem;">{desc}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with tab_fsi:
        st.markdown(
            f"""
            <p style="color:#4a5568;font-size:0.9rem;margin-bottom:16px;">
              Indicateurs du <strong>Fragile States Index (FSI)</strong> publie par le Fund for Peace.
              Score de 0 a 10 : 10 = etat le plus fragile. Ces 4 indicateurs capturent
              la dimension institutionnelle et securitaire absente du dataset classique.
            </p>
            """,
            unsafe_allow_html=True,
        )
        for var in FSI_COLS:
            desc, _ = _VAR_DESCRIPTIONS.get(var, (var, ""))
            st.markdown(
                f"""
                <div style="background:white;border-radius:8px;padding:12px 16px;
                            margin-bottom:8px;border-left:3px solid #e76f51;
                            box-shadow:0 1px 4px rgba(0,0,0,0.05);">
                  <code style="background:#fff5f0;color:#c2410c;padding:2px 8px;
                               border-radius:4px;font-size:0.88rem;">{var}</code>
                  &nbsp;&nbsp;
                  <span style="color:#4a5568;font-size:0.9rem;">{desc}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()

    # ── Sources ────────────────────────────────────────────────────────────────
    st.markdown(f"<p class='section-header'>Sources des donnees</p>", unsafe_allow_html=True)

    sources = [
        ("HELP ONG",             "clipboard-data",  "#2a9d8f",
         "Dataset pays de base — indicateurs socio-economiques (167 pays).",           ""),
        ("OMS / WHO",            "heart-pulse",     "#1e3c72",
         "Esperance de vie, depenses sante, medecins pour 1000 hab.",                   "https://www.who.int/data"),
        ("Banque Mondiale",      "bank",            "#e9c46a",
         "PIB/hab., pauvrete multidimensionnelle, scolarisation.",                      "https://data.worldbank.org"),
        ("FSI — Fund for Peace", "shield-half",     "#e76f51",
         "Fragile States Index — 4 sous-indices de fragilite institutionnelle.",        "https://fragilestatesindex.org"),
        ("ACLED",                "exclamation-triangle", "#9B59B6",
         "Armed Conflict Location & Event Data — violences politiques.",                "https://acleddata.com"),
    ]

    src_cols = st.columns(len(sources))
    for col, (src, icon, color, desc, url) in zip(src_cols, sources):
        with col:
            link = f'<a href="{url}" target="_blank" style="color:{SECONDARY};font-size:0.8rem;">Acceder</a>' if url else ""
            st.markdown(
                f"""
                <div style="background:white;border-radius:12px;padding:16px;
                            text-align:center;box-shadow:0 1px 8px rgba(0,0,0,0.06);
                            border-top:4px solid {color};height:100%;">
                  <i class="bi bi-{icon}" style="font-size:1.6rem;color:{color};"></i>
                  <p style="font-weight:700;color:{PRIMARY};font-size:0.9rem;margin:8px 0 6px;">
                    {src}
                  </p>
                  <p style="color:#718096;font-size:0.8rem;margin:0;">{desc}</p>
                  <div style="margin-top:10px;">{link}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()

    # ── Stack technique ────────────────────────────────────────────────────────
    st.markdown(f"<p class='section-header'>Stack technique</p>", unsafe_allow_html=True)

    stack = [
        ("Python 3.11",     "Langage principal",                     "cpu",                PRIMARY),
        ("pandas / numpy",  "Manipulation et calcul numerique",       "table",              SECONDARY),
        ("scikit-learn",    "KMeans, RobustScaler, metriques",        "gear",               "#2563eb"),
        ("SHAP 0.51",       "Interpretabilite du modele proxy",       "eye",                "#9B59B6"),
        ("Plotly 6",        "Visualisations interactives",            "bar-chart-line",     "#e9c46a"),
        ("Streamlit",       "Dashboard web interactif",               "window-fullscreen",  "#e76f51"),
        ("joblib",          "Serialisation et cache des modeles",     "box-arrow-in-down",  "#2a9d8f"),
        ("geopandas",       "Cartes choroplethes (notebooks)",        "globe",              "#264653"),
    ]

    tech_cols = st.columns(4)
    for i, (tech, desc, icon, color) in enumerate(stack):
        with tech_cols[i % 4]:
            st.markdown(
                f"""
                <div style="background:white;border-radius:10px;padding:16px;
                            margin-bottom:14px;text-align:center;
                            box-shadow:0 1px 6px rgba(0,0,0,0.06);
                            border-bottom:3px solid {color};">
                  <i class="bi bi-{icon}" style="font-size:1.6rem;color:{color};"></i>
                  <p style="font-weight:700;color:{PRIMARY};margin:8px 0 4px;font-size:0.9rem;">
                    {tech}
                  </p>
                  <p style="color:#718096;font-size:0.78rem;margin:0;">{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
