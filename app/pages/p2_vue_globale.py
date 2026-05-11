import numpy as np
import streamlit as st

from components.kpi_card import kpi_row
from components.charts import (
    choropleth_map, pca_scatter, cluster_bar, cluster_pie, heatmap_cluster_profiles,
)
from data_loader import get_labeled_data
from config import PRIMARY, SECONDARY, DANGER, ACCENT, FSI_COLS


def render():
    st.markdown(
        "<h2 style='font-size:1.35rem;font-weight:700;color:#0F172A;"
        "margin-bottom:4px;letter-spacing:-0.02em;'>Vue globale</h2>",
        unsafe_allow_html=True,
    )
    st.caption("Selectionnez un modele pour explorer la repartition mondiale des clusters.")

    # ── Selecteur modele ──────────────────────────────────────────────────────
    model_key = st.radio(
        "Modele",
        ["Modele classique", "Modele enrichi"],
        format_func=lambda k: (
            "Modele classique — 8 variables socio-economiques · k = 3 clusters"
            if k == "Modele classique" else
            "Modele enrichi FSI — 14 variables · k = 4 clusters"
        ),
        horizontal=True,
        label_visibility="collapsed",
    )

    with st.spinner("Chargement des donnees…"):
        d = get_labeled_data(model_key)

    df            = d["df"]
    id_col        = d["id_col"]
    iso_col       = d["iso_col"]
    feat_cols     = d["feat_cols"]
    labels        = d["labels"]
    k             = d["k"]
    cluster_names = d["cluster_names"]

    # ── KPI cards ─────────────────────────────────────────────────────────────
    counts     = np.bincount(labels)
    # Cluster prioritaire = celui avec child_mort_log le plus eleve
    pri_id     = int(df.groupby("cluster")["child_mort_log"].mean().idxmax())
    n_priority = int(counts[pri_id])

    fsi_mean = None
    for col in FSI_COLS:
        if col in df.columns:
            fsi_mean = round(float(df[col].mean()), 2)
            break

    kpi_cards = [
        {"label": "Pays analyses",    "value": len(df),         "icon": "globe",                     "color": PRIMARY},
        {"label": "Clusters",         "value": k,               "icon": "diagram-3",                  "color": SECONDARY},
        {"label": "Variables",        "value": len(feat_cols),  "icon": "sliders",                    "color": ACCENT},
        {"label": "Pays prioritaires","value": n_priority,      "icon": "exclamation-triangle-fill",  "color": DANGER},
    ]
    if fsi_mean is not None:
        kpi_cards.append({
            "label": "Score FSI moyen",
            "value": fsi_mean,
            "icon":  "shield-exclamation",
            "color": "#264653",
        })
    kpi_row(kpi_cards)

    # ── Legende clusters ──────────────────────────────────────────────────────
    from config import CLUSTER_COLORS
    legend_cols = st.columns(k)
    for i, (cid, name) in enumerate(sorted(cluster_names.items())):
        with legend_cols[i % k]:
            count = int((labels == cid).sum())
            color = CLUSTER_COLORS[cid % len(CLUSTER_COLORS)]
            st.markdown(
                f"""
                <div style="background:#fff;border-radius:8px;
                            border-left:3px solid {color};
                            box-shadow:0 1px 3px rgba(0,0,0,0.06);
                            padding:10px 14px;margin-bottom:8px;">
                  <span style="font-size:0.875rem;font-weight:600;color:#0F172A;">
                    {name}
                  </span>
                  <span style="font-size:0.73rem;color:#94A3B8;margin-left:8px;">
                    {count} pays
                  </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Carte monde ───────────────────────────────────────────────────────────
    st.markdown(
        f"<p class='section-header'>Repartition mondiale des clusters</p>",
        unsafe_allow_html=True,
    )
    fig_map = choropleth_map(df, id_col, iso_col, cluster_names=cluster_names)
    st.plotly_chart(fig_map, width="stretch")

    # ── Distribution + ACP ────────────────────────────────────────────────────
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown(
            f"<p class='section-header'>Distribution des clusters</p>",
            unsafe_allow_html=True,
        )
        tab_bar, tab_pie = st.tabs(["Barres", "Camembert"])
        with tab_bar:
            st.plotly_chart(
                cluster_bar(df, cluster_names=cluster_names),
                width="stretch",
            )
        with tab_pie:
            st.plotly_chart(
                cluster_pie(df, cluster_names=cluster_names),
                width="stretch",
            )

    with col_right:
        st.markdown(
            f"<p class='section-header'>Projection ACP 2D</p>",
            unsafe_allow_html=True,
        )
        fig_pca = pca_scatter(
            d["X_scaled"], labels,
            country_names=df[id_col].tolist(),
            cluster_names=cluster_names,
        )
        st.plotly_chart(fig_pca, width="stretch")

    # ── Heatmap profils ───────────────────────────────────────────────────────
    st.markdown(
        f"<p class='section-header'>Profils moyens par cluster (normalises)</p>",
        unsafe_allow_html=True,
    )
    fig_heat = heatmap_cluster_profiles(df, feat_cols, cluster_names=cluster_names)
    st.plotly_chart(fig_heat, width="stretch")
    st.caption(
        "Valeurs affichees = moyennes brutes (espace log). "
        "Couleurs = valeurs normalisees [0–1] pour comparaison inter-variables. "
        "RdYlGn : vert = valeur elevee, rouge = valeur basse."
    )
