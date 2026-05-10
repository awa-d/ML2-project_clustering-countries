import numpy as np
import streamlit as st

from components.charts import feature_importance_bar, pca_scatter
from data_loader import get_labeled_data
from config import PRIMARY, SECONDARY, CLUSTER_COLORS


def _train_proxy(X, y):
    from sklearn.ensemble import RandomForestClassifier
    rf = RandomForestClassifier(n_estimators=300, max_depth=8, random_state=42, n_jobs=-1)
    rf.fit(X, y)
    return rf


@st.cache_resource
def _get_shap(model_key: str):
    d = get_labeled_data(model_key)
    X, y      = d["X_scaled"], d["labels"]
    feat_cols = d["feat_cols"]
    rf        = _train_proxy(X, y)

    shap_vals = None
    try:
        import shap
        explainer = shap.TreeExplainer(rf)
        raw = explainer.shap_values(X)
        # SHAP 0.40+ returns 3-D array (n_samples, n_features, n_classes)
        # Older versions return list[k] of (n_samples, n_features)
        if isinstance(raw, np.ndarray) and raw.ndim == 3:
            shap_vals = [raw[:, :, k] for k in range(raw.shape[2])]
        elif isinstance(raw, list):
            shap_vals = raw
        else:
            shap_vals = [raw]
    except Exception:
        shap_vals = None

    return rf, shap_vals, feat_cols, X, y, d["df"], d["id_col"], d["cluster_names"]


def render():
    st.markdown(
        f"<h2 style='color:{PRIMARY};margin-bottom:4px;'>Interpretabilite</h2>",
        unsafe_allow_html=True,
    )
    st.caption(
        "Un modele Random Forest proxy est entraine a reproduire les labels de cluster. "
        "SHAP (SHapley Additive exPlanations) quantifie la contribution de chaque variable "
        "a l'appartenance aux clusters."
    )

    model_key = st.radio(
        "Modele source",
        ["Modele classique", "Modele enrichi"],
        format_func=lambda k: "Classique (8 var.)" if k == "Modele classique" else "Enrichi FSI (14 var.)",
        horizontal=True,
        label_visibility="visible",
    )

    with st.spinner("Entrainement du modele proxy et calcul SHAP (premiere fois)…"):
        rf, shap_vals, feat_cols, X, y, df, id_col, cluster_names = _get_shap(model_key)

    # ── Accuracy proxy ────────────────────────────────────────────────────────
    from sklearn.metrics import accuracy_score
    acc = accuracy_score(y, rf.predict(X))
    st.markdown(
        f"""
        <div style="background:#F8FAFF;border-radius:10px;padding:14px 20px;
                    margin-bottom:20px;border-left:3px solid {SECONDARY};
                    box-shadow:0 1px 3px rgba(0,0,0,0.05);">
          <strong style="color:#0F172A;">Modele proxy RF :</strong>
          <span style="color:#475569;"> Precision sur les donnees d'entrainement : </span>
          <strong style="color:{SECONDARY};">{acc*100:.1f} %</strong>
          <span style="color:#94A3B8;font-size:0.83rem;"> — sert uniquement a expliquer
          les clusters, non a les predire.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Importance globale + ACP ───────────────────────────────────────────────
    st.markdown(f"<p class='section-header'>Importance globale des variables</p>",
                unsafe_allow_html=True)

    col_fi, col_pca = st.columns([1, 1])

    with col_fi:
        if shap_vals is not None:
            mean_abs = np.mean([np.abs(sv).mean(axis=0) for sv in shap_vals], axis=0)
            fig_fi   = feature_importance_bar(
                feat_cols, mean_abs,
                title="Importance SHAP moyenne (toutes classes)",
            )
        else:
            fig_fi = feature_importance_bar(
                feat_cols, rf.feature_importances_,
                title="Importance RF (shap non disponible)",
            )
        st.plotly_chart(fig_fi, use_container_width=True)

    with col_pca:
        st.markdown(f"<p class='section-header'>Projection ACP</p>",
                    unsafe_allow_html=True)
        fig_pca = pca_scatter(X, y,
                              country_names=df[id_col].tolist(),
                              cluster_names=cluster_names)
        st.plotly_chart(fig_pca, use_container_width=True)

    # ── SHAP par cluster ──────────────────────────────────────────────────────
    if shap_vals is not None:
        st.markdown(f"<p class='section-header'>Contribution SHAP par cluster</p>",
                    unsafe_allow_html=True)
        k = len(shap_vals)

        tab_labels = [
            f"Cluster {i} — {cluster_names.get(i, '')}" for i in range(k)
        ]
        tabs = st.tabs(tab_labels)

        for i, tab in enumerate(tabs):
            with tab:
                sv         = shap_vals[i]
                mean_abs_c = np.abs(sv).mean(axis=0)
                cname      = cluster_names.get(i, f"Cluster {i}")
                color      = CLUSTER_COLORS[i % len(CLUSTER_COLORS)]

                # Badge cluster
                st.markdown(
                    f"""
                    <div style="display:inline-block;background:{color};color:white;
                                padding:4px 14px;border-radius:16px;font-size:0.85rem;
                                font-weight:600;margin-bottom:12px;">
                      {cname} · {int((y == i).sum())} pays
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                col_bar, col_tbl = st.columns([1.2, 1])

                with col_bar:
                    fig_c = feature_importance_bar(
                        feat_cols, mean_abs_c,
                        title=f"|SHAP| moyen — {cname}",
                    )
                    st.plotly_chart(fig_c, use_container_width=True)

                with col_tbl:
                    st.caption("Top pays — contribution SHAP la plus forte :")
                    total_shap = np.abs(sv).sum(axis=1)
                    top_idx    = np.argsort(total_shap)[::-1][:10]
                    import pandas as pd
                    top_df = df.iloc[top_idx][[id_col, "cluster"]].copy()
                    top_df["Cluster"]         = top_df["cluster"].map(cluster_names)
                    top_df["|SHAP| total"]    = np.round(total_shap[top_idx], 4)
                    top_df = top_df.drop(columns="cluster")
                    st.dataframe(top_df.set_index(id_col), use_container_width=True,
                                 height=320)
    else:
        st.warning(
            "Le package `shap` n'est pas disponible ou a rencontre une erreur. "
            "L'importance RF est affichee a la place."
        )

    # ── Lecture des resultats ─────────────────────────────────────────────────
    st.markdown(f"<p class='section-header'>Lecture des resultats</p>",
                unsafe_allow_html=True)
    st.markdown(
        """
        - **Importance elevee** : la variable discrimine fortement les clusters — c'est un critere structurant du modele.
        - **SHAP eleve pour un cluster** : la variable pousse vers l'appartenance a ce cluster.
        - Pour le modele enrichi, les indicateurs FSI (`security_apparatus`, `refugees_idps`, etc.)
          apparaissent avec une importance distincte, justifiant leur ajout pour une segmentation institutionnelle.
        - Les variables sanitaires (`child_mort_log`, `life_expec`) dominent dans le modele classique.
        """
    )
