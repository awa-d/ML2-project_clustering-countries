import pandas as pd
import streamlit as st

from components.charts import (
    choropleth_map, radar_chart, boxplot_variable, pca_scatter,
)
from data_loader import get_labeled_data, auto_describe_cluster
from config import PRIMARY, SECONDARY, CLUSTER_COLORS


def render():
    st.markdown(
        f"<h2 style='color:{PRIMARY};margin-bottom:4px;'>Exploration des clusters</h2>",
        unsafe_allow_html=True,
    )

    # ── Selecteurs ────────────────────────────────────────────────────────────
    col_m, col_c = st.columns([2, 1])

    with col_m:
        model_key = st.radio(
            "Modele",
            ["Modele classique", "Modele enrichi"],
            format_func=lambda k: "Classique" if k == "Modele classique" else "Enrichi",
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
    k             = d["k"]
    cluster_names = d["cluster_names"]

    with col_c:
        cluster_id = st.selectbox(
            "Cluster",
            options=sorted(cluster_names.keys()),
            format_func=lambda c: f"Cluster {c} — {cluster_names[c]}",
        )

    # ── Recherche pays ────────────────────────────────────────────────────────
    search = st.text_input("Rechercher un pays", placeholder="ex. Senegal, France, Chad…")

    if search:
        mask = df[id_col].str.contains(search, case=False, na=False)
        hits = df[mask]
        if hits.empty:
            st.warning(f"Aucun pays correspondant a « {search} ».")
        else:
            for _, row in hits.iterrows():
                c    = int(row["cluster"])
                cname = cluster_names.get(c, f"Cluster {c}")
                color = CLUSTER_COLORS[c % len(CLUSTER_COLORS)]
                st.markdown(
                    f"""
                    <div style="background:white;border-radius:10px;padding:14px 18px;
                                border-left:5px solid {color};margin-bottom:10px;
                                box-shadow:0 2px 8px rgba(0,0,0,0.06);">
                      <strong style="font-size:1.05rem;color:{PRIMARY};">{row[id_col]}</strong>
                      &nbsp;&nbsp;
                      <span style="background:{color};color:white;padding:3px 12px;
                                   border-radius:12px;font-size:0.82rem;font-weight:600;">
                        Cluster {c} — {cname}
                      </span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        st.divider()

    # ── Profil cluster selectionne ────────────────────────────────────────────
    color      = CLUSTER_COLORS[cluster_id % len(CLUSTER_COLORS)]
    cname      = cluster_names.get(cluster_id, f"Cluster {cluster_id}")
    desc       = auto_describe_cluster(df, cluster_id, id_col, feat_cols)
    count      = int((labels == cluster_id).sum())

    st.markdown(
        f"""
        <div style="background:white;border-radius:14px;padding:22px 26px;
                    border-left:6px solid {color};box-shadow:0 2px 12px rgba(0,0,0,0.07);
                    margin-bottom:20px;">
          <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;">
            <h3 style="color:{PRIMARY};margin:0;font-size:1.3rem;">
              Cluster {cluster_id} — {cname}
            </h3>
            <span style="background:{color};color:white;padding:4px 14px;
                         border-radius:16px;font-size:0.85rem;font-weight:600;">
              {count} pays
            </span>
          </div>
          <p style="color:#4a5568;margin:10px 0 0;font-size:0.9rem;">{desc}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Stats moyennes ────────────────────────────────────────────────────────
    st.markdown(f"<p class='section-header'>Statistiques — Cluster {cluster_id} : {cname}</p>",
                unsafe_allow_html=True)
    c_df  = df[df["cluster"] == cluster_id][feat_cols]
    stats = pd.concat(
        [c_df.mean().rename("Moyenne"), c_df.median().rename("Mediane"),
         c_df.std().rename("Ecart-type")],
        axis=1,
    ).round(3)
    st.dataframe(stats.style.background_gradient(cmap="Blues", axis=0),
                 width="stretch")

    # ── Radar + Boxplot ───────────────────────────────────────────────────────
    col_radar, col_box = st.columns([1.2, 1])

    with col_radar:
        st.markdown(f"<p class='section-header'>Radar — comparaison des clusters</p>",
                    unsafe_allow_html=True)
        radar_cols = feat_cols[:8] if len(feat_cols) > 8 else feat_cols
        fig_radar  = radar_chart(df, radar_cols, cluster_names=cluster_names)
        st.plotly_chart(fig_radar, width="stretch")

    with col_box:
        st.markdown(f"<p class='section-header'>Distribution par cluster</p>",
                    unsafe_allow_html=True)
        var = st.selectbox("Variable", feat_cols, key="box_var")
        fig_box = boxplot_variable(df, var, cluster_names=cluster_names)
        st.plotly_chart(fig_box, width="stretch")

    # ── Pays du cluster ───────────────────────────────────────────────────────
    st.markdown(
        f"<p class='section-header'>Pays du Cluster {cluster_id} — {cname}</p>",
        unsafe_allow_html=True,
    )
    c_countries  = df[df["cluster"] == cluster_id].copy()
    display_cols = [id_col] + feat_cols
    if iso_col and iso_col in c_countries.columns and iso_col not in (id_col, "iso3"):
        display_cols = [id_col, iso_col] + feat_cols

    st.dataframe(
        c_countries[display_cols].set_index(id_col).round(3),
        width="stretch",
        height=320,
    )

    # ── ACP cluster ───────────────────────────────────────────────────────────
    st.markdown(
        f"<p class='section-header'>Projection ACP — tous clusters</p>",
        unsafe_allow_html=True,
    )
    fig_pca = pca_scatter(
        d["X_scaled"], labels,
        country_names=df[id_col].tolist(),
        cluster_names=cluster_names,
        title=f"ACP — Cluster {cluster_id} ({cname})",
    )
    st.plotly_chart(fig_pca, width="stretch")

    # ── Carte ─────────────────────────────────────────────────────────────────
    st.markdown(
        f"<p class='section-header'>Carte — Cluster {cluster_id} : {cname}</p>",
        unsafe_allow_html=True,
    )
    fig_map = choropleth_map(df, id_col, iso_col, cluster_names=cluster_names)
    st.plotly_chart(fig_map, width="stretch")
    st.caption(
        f"Cluster {cluster_id} ({cname}) . "
        "Passez la souris sur les pays pour voir leur nom et cluster."
    )
