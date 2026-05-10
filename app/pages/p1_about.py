import streamlit as st
from config import APP_TITLE, APP_SUBTITLE, MODELS_META, TEAM, SUPERVISOR, PRIMARY, SECONDARY


def render():
    # ── Hero image ────────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="position:relative;border-radius:14px;overflow:hidden;
                    height:240px;margin-bottom:36px;">
          <img src="https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?auto=format&fit=crop&w=1400&q=80"
               alt="Aide humanitaire"
               style="width:100%;height:100%;object-fit:cover;display:block;">
          <div style="position:absolute;inset:0;
                      background:linear-gradient(120deg,rgba(15,23,42,0.82) 0%,
                                                        rgba(67,56,202,0.55) 100%);">
          </div>
          <div style="position:absolute;inset:0;display:flex;flex-direction:column;
                      justify-content:flex-end;padding:28px 32px;">
            <p style="font-size:0.65rem;font-weight:600;letter-spacing:0.14em;
                      text-transform:uppercase;color:rgba(255,255,255,0.55);margin:0 0 6px;">
              Machine Learning 2 · Projet academique
            </p>
            <h1 style="font-size:2.1rem;font-weight:800;margin:0;color:#ffffff;
                       letter-spacing:-0.04em;line-height:1.1;">{APP_TITLE}</h1>
            <p style="font-size:0.92rem;color:rgba(255,255,255,0.65);margin:8px 0 0;
                      font-style:italic;font-weight:400;">{APP_SUBTITLE}</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Vision ────────────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="border-left:3px solid {SECONDARY};padding:18px 22px;
                    background:#F8FAFF;border-radius:0 8px 8px 0;margin-bottom:36px;">
          <p style="font-size:0.93rem;color:#374151;font-style:italic;
                    margin:0;line-height:1.80;">
            « L'aide humanitaire de demain ne peut plus reposer uniquement sur des intuitions
            geopolitiques. Avec des ressources limitees, chaque decision d'allocation compte.
            SigmaPulse mobilise la puissance du Machine Learning pour transformer des indicateurs
            complexes en une strategie d'allocation rigoureuse, ethique et data-driven. »
          </p>
          <p style="text-align:right;color:#94A3B8;font-size:0.80rem;
                    margin:10px 0 0;font-weight:500;">— Equipe SigmaPulse</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Contexte ──────────────────────────────────────────────────────────────
    st.markdown('<p class="section-header">Contexte</p>', unsafe_allow_html=True)
    st.markdown(
        """
        Projet de Machine Learning applique a **l'allocation strategique de l'aide humanitaire**.
        L'objectif est de segmenter **167 pays** selon leurs vulnerabilites socio-economiques,
        sanitaires et securitaires afin d'identifier des profils d'intervention prioritaires
        pour l'ONG **HELP**. Le projet combine des indicateurs macro-economiques, sanitaires,
        sociaux et de fragilite etatique, traites par des techniques de clustering non supervise.
        """
    )

    # ── Modeles ───────────────────────────────────────────────────────────────
    st.markdown('<p class="section-header">Pipelines de modelisation</p>',
                unsafe_allow_html=True)

    cols = st.columns(2, gap="medium")
    for col, (key, meta) in zip(cols, MODELS_META.items()):
        with col:
            st.markdown(
                f"""
                <div style="background:#fff;border-radius:10px;
                            box-shadow:0 1px 3px rgba(0,0,0,0.07),0 1px 2px rgba(0,0,0,0.04);
                            padding:24px;height:100%;">
                  <p style="font-size:0.68rem;font-weight:600;letter-spacing:0.10em;
                             text-transform:uppercase;color:{SECONDARY};margin:0 0 8px;">
                    {meta['features']} variables · k = {meta['k']} clusters
                  </p>
                  <p style="font-size:1rem;font-weight:700;color:#0F172A;margin:0 0 10px;">
                    {meta['label']}
                  </p>
                  <p style="font-size:0.875rem;color:#64748B;margin:0;line-height:1.6;">
                    {meta['description']}
                  </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Methodologie ──────────────────────────────────────────────────────────
    st.markdown('<p class="section-header">Methodologie</p>', unsafe_allow_html=True)

    steps = [
        ("Collecte",       "Sources multiples : HELP ONG, WHO, Banque Mondiale, FSI, ACLED."),
        ("Harmonisation",  "Alignement des noms de pays, jointures multi-sources sur 167 pays."),
        ("Pretraitement",  "Imputation KNN/BayesRidge, transformations log, RobustScaler."),
        ("Feature eng.",   "Selection par VIF et correlation, reduction de redondance."),
        ("Clustering",     "KMeans k=3/k=4 — selection via coude, Silhouette, DB-Index, CAH."),
        ("Interpretation", "Profilage par cluster, SHAP sur modele proxy RF, cartes."),
    ]
    cols2 = st.columns(3, gap="medium")
    for i, (step, desc) in enumerate(steps):
        with cols2[i % 3]:
            st.markdown(
                f"""
                <div style="padding:16px 18px;border-radius:10px;margin-bottom:12px;
                            background:#fff;
                            box-shadow:0 1px 3px rgba(0,0,0,0.06),0 1px 2px rgba(0,0,0,0.04);">
                  <p style="font-size:0.68rem;font-weight:700;letter-spacing:0.08em;
                             text-transform:uppercase;color:{SECONDARY};margin:0 0 6px;">
                    {i+1:02d} — {step}
                  </p>
                  <p style="font-size:0.84rem;color:#64748B;margin:0;line-height:1.55;">
                    {desc}
                  </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Equipe ────────────────────────────────────────────────────────────────
    st.markdown('<p class="section-header">Equipe SigmaPulse</p>', unsafe_allow_html=True)

    team_cols = st.columns(len(TEAM), gap="medium")
    for col, member in zip(team_cols, TEAM):
        with col:
            initials = "".join(n[0].upper() for n in member["name"].split()[:2])
            st.markdown(
                f"""
                <div style="background:#fff;border-radius:10px;
                            box-shadow:0 1px 3px rgba(0,0,0,0.07),0 1px 2px rgba(0,0,0,0.04);
                            padding:22px 16px;text-align:center;">
                  <div style="width:46px;height:46px;border-radius:50%;
                              background:linear-gradient(135deg,{SECONDARY},#6366F1);
                              color:white;font-size:0.95rem;
                              font-weight:700;display:flex;align-items:center;
                              justify-content:center;margin:0 auto 14px;">
                    {initials}
                  </div>
                  <p style="font-size:0.875rem;font-weight:600;color:#0F172A;margin:0;">
                    {member['name']}
                  </p>
                  <p style="font-size:0.76rem;color:#94A3B8;margin:4px 0 0;line-height:1.4;">
                    {member['role']}
                  </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        f"""
        <p style="font-size:0.80rem;color:#94A3B8;margin:20px 0 0;text-align:center;">
          <i class="bi bi-mortarboard" style="color:{SECONDARY};"></i>
          &nbsp;Supervision : <strong style="color:#64748B;">{SUPERVISOR}</strong>
        </p>
        """,
        unsafe_allow_html=True,
    )
