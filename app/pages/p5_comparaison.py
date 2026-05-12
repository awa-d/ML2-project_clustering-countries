import pandas as pd
import streamlit as st

from components.charts import (
    pca_scatter, cluster_bar, metrics_comparison_bar, heatmap_cluster_profiles,
    pca_correlation_circle,
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
        width="stretch",
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
    st.plotly_chart(fig_metrics, width="stretch")

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
        st.plotly_chart(fig_pca_cls, width="stretch")

    with col_r:
        n_pays2 = d_enr["df"][d_enr["id_col"]].nunique()
        st.markdown(f"**Modele enrichi** — {n_pays2} pays · 14 variables · k = 4")
        fig_pca_enr = pca_scatter(
            d_enr["X_scaled"], d_enr["labels"],
            country_names=d_enr["df"][d_enr["id_col"]].tolist(),
            cluster_names=d_enr["cluster_names"],
            title="ACP — Enrichi FSI",
        )
        st.plotly_chart(fig_pca_enr, width="stretch")

    # ── Cercles de corrélation ────────────────────────────────────────────────
    st.markdown(f"<p class='section-header'>Cercles de corrélation ACP</p>",
                unsafe_allow_html=True)

    col_cc1, col_cc2 = st.columns(2)
    with col_cc1:
        st.markdown("**Modele classique** — 8 variables")
        fig_cc_cls = pca_correlation_circle(
            d_cls["X_scaled"], d_cls["feat_cols"],
            title="Cercle de corrélation — Classique",
        )
        st.plotly_chart(fig_cc_cls, width="stretch")
        st.markdown(
            """
            <div style="font-size:0.83rem;color:#475569;background:#F8FAFF;
                        border-radius:8px;padding:12px;margin-top:4px;">
            PC1 synthétise le gradient de développement humain global : les variables
            gdpp_log et life_expec pointent vers la gauche (pôle développé), tandis que
            child_mort_log et total_fer pointent vers la droite (pôle vulnérable). Les
            flèches opposées confirment leur corrélation négative forte. PC2 capte une
            dimension orthogonale liée aux échanges commerciaux : exports_log et imports_log
            se distinguent sur cet axe. Les flèches courtes (inflation_log) indiquent des
            variables dont la variance est distribuée sur des composantes tardives.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_cc2:
        st.markdown("**Modele enrichi** — 14 variables")
        fig_cc_enr = pca_correlation_circle(
            d_enr["X_scaled"], d_enr["feat_cols"],
            title="Cercle de corrélation — Enrichi FSI",
        )
        st.plotly_chart(fig_cc_enr, width="stretch")
        st.markdown(
            """
            <div style="font-size:0.83rem;color:#475569;background:#F8FAFF;
                        border-radius:8px;padding:12px;margin-top:4px;">
            PC1 (≈ 50 % de variance) reste un axe de développement renforcé : gdpp_log,
            physicians_per_1000 et social_schooling_log forment un faisceau opposé à
            child_mort_log et social_poverty_2_15_log. La nouveauté est PC2 : hiv_prevalence_log
            se distingue des autres variables par une direction quasi-orthogonale à l'axe de
            développement, de même que refugees_idps. Cette orthogonalité révèle que la
            prévalence VIH et les déplacements de populations sont partiellement indépendants
            du niveau de revenu — c'est précisément ce signal que k=4 exploite pour
            séparer deux formes de vulnérabilité que le modèle classique confondait.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Taille des clusters ────────────────────────────────────────────────────
    st.markdown(f"<p class='section-header'>Taille des clusters</p>", unsafe_allow_html=True)

    col_l2, col_r2 = st.columns(2)
    with col_l2:
        st.caption("Classique (k=3)")
        st.plotly_chart(
            cluster_bar(d_cls["df"], cluster_names=d_cls["cluster_names"]),
            width="stretch",
        )
    with col_r2:
        st.caption("Enrichi FSI (k=4)")
        st.plotly_chart(
            cluster_bar(d_enr["df"], cluster_names=d_enr["cluster_names"]),
            width="stretch",
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
            width="stretch",
        )
    with col_h2:
        st.caption("Enrichi FSI")
        st.plotly_chart(
            heatmap_cluster_profiles(d_enr["df"], d_enr["feat_cols"],
                                     cluster_names=d_enr["cluster_names"]),
            width="stretch",
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

    #  Définition du dictionnaire de correspondance par mapping Manuel
    # On réaligne les IDs du modèle enrichi pour qu'ils correspondent au classique
    mapping_enrichi = {
        3: 0,  # "Developpes stables" devient ID 0
        0: 1,  # "Intermediaires vulnerables" devient ID 1
        1: 2,  # "Crise VIH" devient ID 2 (Prioritaires)
        2: 2   # "Etats fragiles" devient ID 2 (Prioritaires)
    }

    #  Application du mapping sur une nouvelle colonne technique
    df_m["cluster_enrichi_realigne"] = df_m["cluster_enrichi"].map(mapping_enrichi)

    #  Calcul de la migration sur les IDs réalignés
    migres = df_m[df_m["cluster_classique"] != df_m["cluster_enrichi_realigne"]]

    col_stat, col_tbl = st.columns([1, 2])
    with col_stat:
        st.metric("Pays ayant change de cluster", len(migres))
        st.metric("Pays stables", len(df_m) - len(migres))
        st.markdown(
            f"""
            <div style="background:#F8FAFF;border-radius:10px;padding:14px;
                        margin-top:12px;font-size:0.84rem;color:#475569;
                        box-shadow:0 1px 2px rgba(0,0,0,0.04);">
              Pour comparer les deux modélisations, nous appliquons un mapping  visant à harmoniser les segments.

Le principe repose sur l'alignement des nouveaux clusters sur les strates socio-économiques initiales :

* Le pôle de richesse est stabilisé comme référent commun.
* Les scissions observées dans le pôle de pauvreté (distinction entre fragilité étatique et crises sanitaires) sont traitées comme une stabilité de profil.

Un pays est donc comptabilisé comme "migrant" uniquement lorsqu'il bascule d'une strate à une autre.
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
                width="stretch",
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
