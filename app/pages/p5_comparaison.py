import pandas as pd
import streamlit as st

from components.charts import (
    pca_scatter, cluster_bar, metrics_comparison_bar, heatmap_cluster_profiles,
)
from data_loader import get_both_labeled, compute_metrics
from config import PRIMARY, SECONDARY, ACCENT, MODELS_META


def render():
    st.markdown(
        f"<h2 style='color:{PRIMARY};margin-bottom:4px;'>Comparaison des modelisations</h2>",
        unsafe_allow_html=True,
    )
    st.caption(
        "Analyse comparative entre le modele classique (8 variables, k=3) "
        "et le modele enrichi FSI (14 variables, k=4)."
    )

    with st.spinner("Calcul des metriques…"):
        d_cls, d_enr = get_both_labeled()

    metrics_cls = compute_metrics(d_cls["X_scaled"], d_cls["labels"])
    metrics_enr = compute_metrics(d_enr["X_scaled"], d_enr["labels"])

    # ── Table metriques ───────────────────────────────────────────────────────
    st.markdown(f"<p class='section-header'>Metriques de qualite</p>", unsafe_allow_html=True)

    df_metrics = pd.DataFrame(
        {
            "Modele classique (k=3)":    metrics_cls,
            "Modele enrichi FSI (k=4)":  metrics_enr,
        }
    )
    st.dataframe(
        df_metrics.style
            .highlight_max(axis=1, color="#d4edda")
            .highlight_min(axis=1, color="#f8d7da"),
        use_container_width=True,
    )
    st.caption(
        "Silhouette : plus eleve = meilleure coherence intra-cluster. "
        "Davies-Bouldin : plus bas = meilleure separation. "
        "Calinski-Harabasz : plus eleve = clusters plus compacts et separes."
    )

    # ── Graphique metriques ───────────────────────────────────────────────────
    compare_cls = {k: v for k, v in metrics_cls.items() if k != "Equilibre (min/max)"}
    compare_enr = {k: v for k, v in metrics_enr.items() if k != "Equilibre (min/max)"}

    fig_metrics = metrics_comparison_bar(compare_cls, compare_enr,
                                         "Classique (k=3)", "Enrichi FSI (k=4)")
    st.plotly_chart(fig_metrics, use_container_width=True)

    # ── ACP cote a cote ────────────────────────────────────────────────────────
    st.markdown(f"<p class='section-header'>Projections ACP (2D)</p>", unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    with col_l:
        n_pays = d_cls["df"][d_cls["id_col"]].nunique()
        st.markdown(f"**Modele classique** — {n_pays} pays · 8 variables · k = 3")
        fig_pca_cls = pca_scatter(
            d_cls["X_scaled"], d_cls["labels"],
            country_names=d_cls["df"][d_cls["id_col"]].tolist(),
            cluster_names=d_cls["cluster_names"],
            title="ACP — Classique",
        )
        st.plotly_chart(fig_pca_cls, use_container_width=True)

    with col_r:
        n_pays2 = d_enr["df"][d_enr["id_col"]].nunique()
        st.markdown(f"**Modele enrichi** — {n_pays2} pays · 14 variables · k = 4")
        fig_pca_enr = pca_scatter(
            d_enr["X_scaled"], d_enr["labels"],
            country_names=d_enr["df"][d_enr["id_col"]].tolist(),
            cluster_names=d_enr["cluster_names"],
            title="ACP — Enrichi FSI",
        )
        st.plotly_chart(fig_pca_enr, use_container_width=True)

    # ── Taille des clusters ────────────────────────────────────────────────────
    st.markdown(f"<p class='section-header'>Taille des clusters</p>", unsafe_allow_html=True)

    col_l2, col_r2 = st.columns(2)
    with col_l2:
        st.caption("Classique (k=3)")
        st.plotly_chart(
            cluster_bar(d_cls["df"], cluster_names=d_cls["cluster_names"]),
            use_container_width=True,
        )
    with col_r2:
        st.caption("Enrichi FSI (k=4)")
        st.plotly_chart(
            cluster_bar(d_enr["df"], cluster_names=d_enr["cluster_names"]),
            use_container_width=True,
        )

    # ── Profils moyens ─────────────────────────────────────────────────────────
    st.markdown(f"<p class='section-header'>Profils moyens par cluster</p>",
                unsafe_allow_html=True)

    col_h1, col_h2 = st.columns(2)
    with col_h1:
        st.caption("Classique")
        st.plotly_chart(
            heatmap_cluster_profiles(d_cls["df"], d_cls["feat_cols"],
                                     cluster_names=d_cls["cluster_names"]),
            use_container_width=True,
        )
    with col_h2:
        st.caption("Enrichi FSI")
        st.plotly_chart(
            heatmap_cluster_profiles(d_enr["df"], d_enr["feat_cols"],
                                     cluster_names=d_enr["cluster_names"]),
            use_container_width=True,
        )

    # ── Migration pays entre modeles ──────────────────────────────────────────
    st.markdown(f"<p class='section-header'>Migration entre les deux modeles</p>",
                unsafe_allow_html=True)

    id_cls = d_cls["id_col"]
    id_enr = d_enr["id_col"]

    df_m = (
        d_cls["df"][[id_cls, "cluster", "cluster_name"]]
        .rename(columns={"cluster": "cluster_classique", "cluster_name": "nom_classique"})
        .merge(
            d_enr["df"][[id_enr, "cluster", "cluster_name"]]
            .rename(columns={
                "cluster":      "cluster_enrichi",
                "cluster_name": "nom_enrichi",
                id_enr:         id_cls,
            }),
            on=id_cls, how="inner",
        )
    )
    migres = df_m[df_m["cluster_classique"] != df_m["cluster_enrichi"]]

    col_stat, col_tbl = st.columns([1, 2])
    with col_stat:
        st.metric("Pays ayant change de cluster", len(migres))
        st.metric("Pays stables", len(df_m) - len(migres))
        st.markdown(
            f"""
            <div style="background:#F8FAFF;border-radius:10px;padding:14px;
                        margin-top:12px;font-size:0.84rem;color:#475569;
                        box-shadow:0 1px 2px rgba(0,0,0,0.04);">
              Un changement peut refleter une vraie migration semantique (ex. pays
              passant de "Intermediaires" a "Etats fragiles") ou un simple swap de
              label numerique sans changement de groupe reel.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_tbl:
        if not migres.empty:
            st.dataframe(
                migres.set_index(id_cls).rename(columns={
                    "cluster_classique": "Cluster classique",
                    "nom_classique":     "Nom classique",
                    "cluster_enrichi":   "Cluster enrichi",
                    "nom_enrichi":       "Nom enrichi",
                }),
                use_container_width=True,
                height=320,
            )

    # ── Synthese ──────────────────────────────────────────────────────────────
    st.markdown(f"<p class='section-header'>Synthese comparative</p>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    for col, meta_key, metrics, d in [
        (col_a, "Modele classique", metrics_cls, d_cls),
        (col_b, "Modele enrichi",  metrics_enr, d_enr),
    ]:
        meta = MODELS_META[meta_key]
        with col:
            names_html = "".join(
                f'<li style="color:#4a5568;font-size:0.85rem;margin-bottom:2px;">'
                f'Cluster {cid} : <strong>{name}</strong></li>'
                for cid, name in sorted(d["cluster_names"].items())
            )
            st.markdown(
                f"""
                <div style="background:white;border-radius:12px;padding:22px;
                            box-shadow:0 1px 3px rgba(0,0,0,0.07),0 1px 2px rgba(0,0,0,0.05);
                            border-top:3px solid {SECONDARY};">
                  <h4 style="color:#0F172A;margin-top:0;font-size:1rem;">{meta['label']}</h4>
                  <ul style="padding-left:18px;margin-bottom:14px;">
                    <li style="color:#475569;font-size:0.85rem;">
                      <strong>{meta['features']}</strong> variables · k = <strong>{meta['k']}</strong>
                    </li>
                    <li style="color:#475569;font-size:0.85rem;">
                      Silhouette : <strong>{metrics['Silhouette']}</strong>
                    </li>
                    <li style="color:#475569;font-size:0.85rem;">
                      Davies-Bouldin : <strong>{metrics['Davies-Bouldin']}</strong>
                    </li>
                    <li style="color:#475569;font-size:0.85rem;">
                      Equilibre : <strong>{metrics['Equilibre (min/max)']}</strong>
                    </li>
                  </ul>
                  <strong style="color:#0F172A;font-size:0.85rem;">Clusters :</strong>
                  <ul style="padding-left:18px;margin-top:6px;">{names_html}</ul>
                </div>
                """,
                unsafe_allow_html=True,
            )
