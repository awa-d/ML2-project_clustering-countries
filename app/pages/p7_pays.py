import numpy as np
import pandas as pd
import streamlit as st

from components.charts import country_profile_chart, country_radar_chart, choropleth_map
from data_loader import get_labeled_data
from config import PRIMARY, SECONDARY, ACCENT, DANGER, CLUSTER_COLORS


def render():
    st.markdown(
        f"<h2 style='color:{PRIMARY};margin-bottom:4px;'>Analyse d'un pays</h2>",
        unsafe_allow_html=True,
    )
    st.caption(
        "Selectionnez un pays pour explorer son profil detaille, "
        "son cluster d'appartenance et les pays les plus similaires."
    )

    # ── Selecteur modele ──────────────────────────────────────────────────────
    model_key = st.radio(
        "Modele",
        ["Modele classique", "Modele enrichi"],
        format_func=lambda k: (
            "Modele classique (8 var., k=3)"
            if k == "Modele classique" else
            "Modele enrichi FSI (14 var., k=4)"
        ),
        horizontal=True,
        label_visibility="visible",
    )

    with st.spinner("Chargement…"):
        d = get_labeled_data(model_key)

    df            = d["df"]
    id_col        = d["id_col"]
    iso_col       = d["iso_col"]
    feat_cols     = d["feat_cols"]
    labels        = d["labels"]
    X_scaled      = d["X_scaled"]
    cluster_names = d["cluster_names"]

    countries = sorted(df[id_col].tolist())

    # ── Selecteur pays ────────────────────────────────────────────────────────
    default_idx = countries.index("France") if "France" in countries else 0
    selected = st.selectbox("Choisir un pays", countries, index=default_idx)

    # Retrouver l'index positionnel (le CSV a un index 0-base)
    row_idx = int(df[df[id_col] == selected].index[0])
    row     = df.loc[row_idx]

    cluster_id   = int(row["cluster"])
    cluster_name = cluster_names.get(cluster_id, f"Cluster {cluster_id}")
    color        = CLUSTER_COLORS[cluster_id % len(CLUSTER_COLORS)]

    # ── Badge pays + cluster ──────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="background:white;border-radius:14px;padding:22px 28px;
                    border-left:7px solid {color};
                    box-shadow:0 3px 16px rgba(0,0,0,0.08);margin:16px 0 24px;">
          <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap;">
            <span style="font-size:1.8rem;font-weight:800;color:{PRIMARY};">{selected}</span>
            <span style="background:{color};color:white;padding:6px 16px;
                         border-radius:20px;font-size:0.9rem;font-weight:700;">
              Cluster {cluster_id} — {cluster_name}
            </span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── KPI avec delta vs cluster ──────────────────────────────────────────────
    kpi_targets = [
        ("gdpp_log",       "PIB/hab. (log)"),
        ("life_expec",     "Esperance de vie"),
        ("child_mort_log", "Mortalite infantile"),
    ]
    available = [(f, l) for f, l in kpi_targets if f in feat_cols]

    if available:
        kpi_cols = st.columns(len(available))
        cluster_df   = df[df["cluster"] == cluster_id]
        cluster_mean = cluster_df[feat_cols].mean()

        for col, (feat, label) in zip(kpi_cols, available):
            val   = float(row[feat])
            delta = float(val - cluster_mean[feat])
            with col:
                st.metric(
                    label,
                    f"{val:.3f}",
                    delta=f"{delta:+.3f} vs cluster",
                    delta_color="normal",
                )

    st.divider()

    # ── Profil vs cluster ──────────────────────────────────────────────────────
    tab_bar, = st.tabs(["Comparaison barres"])

    cluster_df   = df[df["cluster"] == cluster_id]
    cluster_mean = cluster_df[feat_cols].mean().values
    country_vals = row[feat_cols].values.astype(float)

    with tab_bar:
        st.markdown(
            f"<p class='section-header'>{selected} vs moyenne du cluster {cluster_id} ({cluster_name})</p>",
            unsafe_allow_html=True,
        )
        fig_bar = country_profile_chart(
            country_vals, cluster_mean, feat_cols, selected, cluster_name,
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.caption(
            "Valeurs dans l'espace original (log-transforme). "
            "Comparaison directe avec la moyenne du cluster d'appartenance."
        )

    

    # ── Pays similaires ───────────────────────────────────────────────────────
    st.markdown(
        f"<p class='section-header'>Pays les plus proches dans le cluster {cluster_id} — {cluster_name}</p>",
        unsafe_allow_html=True,
    )

    cluster_mask = labels == cluster_id
    X_cluster    = X_scaled[cluster_mask]
    idx_in_full  = np.where(cluster_mask)[0]

    x_country = X_scaled[row_idx]
    distances = np.sqrt(((X_cluster - x_country) ** 2).sum(axis=1))

    top_n       = min(10, len(distances) - 1)
    sorted_pos  = np.argsort(distances)
    similar_pos = [p for p in sorted_pos if idx_in_full[p] != row_idx][:top_n]
    similar_idx = idx_in_full[similar_pos]
    similar_dist = distances[similar_pos]

    similar_df = df.iloc[similar_idx][[id_col] + feat_cols].copy()
    similar_df.insert(0, "Distance (espace scale)", np.round(similar_dist, 4))
    st.dataframe(
        similar_df.set_index(id_col).round(3),
        use_container_width=True,
        height=340,
    )
    st.caption(
        "Distance euclidienne dans l'espace normalise (RobustScaler). "
        "Un score proche de 0 indique un profil quasi-identique."
    )

    # ── Tous les pays du meme cluster ─────────────────────────────────────────
    with st.expander(
        f"Voir tous les pays du Cluster {cluster_id} — {cluster_name} "
        f"({int(cluster_mask.sum())} pays)",
        expanded=False,
    ):
        cluster_all = cluster_df[[id_col] + feat_cols].copy().sort_values(id_col)
        st.dataframe(
            cluster_all.set_index(id_col).round(3).style.apply(
                lambda row_s: [
                    "background-color:#dbeafe;font-weight:bold"
                    if row_s.name == selected else "" for _ in row_s
                ],
                axis=1,
            ),
            use_container_width=True,
            height=380,
        )
        st.caption(f"La ligne {selected} est mise en evidence en bleu.")

    # ── Carte monde ───────────────────────────────────────────────────────────
    st.markdown(
        f"<p class='section-header'>Position geographique — {selected} et son cluster</p>",
        unsafe_allow_html=True,
    )
    fig_map = choropleth_map(df, id_col, iso_col, cluster_names=cluster_names)
    st.plotly_chart(fig_map, use_container_width=True)
    st.caption(
        f"{selected} appartient au Cluster {cluster_id} ({cluster_name}). "
        "Passez la souris sur les pays pour voir leur nom et leur cluster."
    )
