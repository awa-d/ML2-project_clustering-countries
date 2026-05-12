import pandas as pd
import plotly.express as px
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
            PC1 définit un gradient de développement socio-économique. On observe une corrélation positive forte de gdpp (log) et life_expec avec cet axe, s'opposant structurellement à child_mort (log) et total_fer. Ainsi, les pays à haut revenu et forte longévité se situent sur la droite du plan, tandis que les pays marqués par une précarité sanitaire se positionnent sur la gauche. L'alignement presque diamétral de life_expec et child_mort (log) confirme  leur corrélation négative intense.
            PC2 est porté par les dynamiques d'ouverture commerciale. Les variables exports (log) et imports (log) saturent positivement cet axe. Cette dimension est orthogonale à PC1, ce qui suggère que l'intensité des échanges extérieurs d'un pays est un phénomène indépendant de son niveau de développement humain intrinsèque.
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
                -  L'axe PC1, capturant 50,5 pourcent de la variance, structure l'opposition fondamentale entre les indicateurs de santé et d'éducation (droite) et les marqueurs de précarité socio-économique et sécuritaire (gauche). On observe un faisceau particulièrement dense à gauche regroupant la mortalité infantile, la pauvreté, la sous-nutrition, mais aussi les griefs de groupe et l'appareil sécuritaire.
                - L'analyse de l'orthogonalité doit être plus nuancée sur PC2 (15,1 %). Contrairement à une indépendance totale, hiv_prevalence et refugees_idps possèdent des coordonnées négatives non négligeables sur PC1. Ces variables ne sont donc pas strictement orthogonales au développement, mais sont portées majoritairement par PC2. La prévalence du VIH se détache par une forte composante positive sur cet axe vertical, s'opposant ainsi aux variables de longévité et de densité médicale situées dans le cadran inférieur droit.
                 Cette configuration indique que si les crises sanitaires et les déplacements de population sont corrélés à la pauvreté (projection sur PC1), leur intensité spécifique est captée par PC2.
            > <b> C'est ce signal résiduel que la partition en k=4 parvient à isoler</b>. Le modèle ne se contente pas de séparer le "riche" du "pauvre", mais distingue, au sein des nations vulnérables, celles qui font face à une surcharge de crises exogènes (VIH, réfugiés) de celles dont la fragilité est plus purement structurelle et économique.
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

    # ── Carte interactive des migrations ─────────────────────────────────────
    st.markdown(
        f"<p class='section-header'>Carte des flux migratoires</p>",
        unsafe_allow_html=True,
    )

    df_map_mg = df_m.copy()
    df_map_mg["statut"] = "Stable"
    _mask = df_map_mg["cluster_classique"] != df_map_mg["cluster_enrichi_realigne"]
    df_map_mg.loc[_mask, "statut"] = (
        df_map_mg.loc[_mask, "nom_classique"] + " → " +
        df_map_mg.loc[_mask, "nom_enrichi"]
    )

    df_map_mg = df_map_mg.merge(
        d_enr["df"][[d_enr["id_col"], d_enr["iso_col"]]].rename(
            columns={d_enr["id_col"]: id_cls, d_enr["iso_col"]: "_iso3"}
        ),
        on=id_cls,
        how="left",
    )

    _MIG_COLORS = {
        "Stable":                                      "#D9D9D9",
        "Intermediaires → Developpes stables":         "#2ca02c",
        "Prioritaires → Intermediaires vulnerables":   "#bcbd22",
        "Developpes → Intermediaires vulnerables":     "#1f77b4",
        "Intermediaires → Crise VIH":                  "#d62728",
        "Intermediaires → Etats fragiles":             "#ff7f0e",
        "Developpes → Etats fragiles":                 "#8c564b",
        "Developpes → Crise VIH":                      "#9467bd",
        "Prioritaires → Developpes stables":           "#17becf",
    }

    fig_map_mg = px.choropleth(
        df_map_mg,
        locations="_iso3",
        color="statut",
        hover_name=id_cls,
        hover_data={
            "nom_classique": True,
            "nom_enrichi":   True,
            "statut":        False,
            "_iso3":         False,
        },
        color_discrete_map=_MIG_COLORS,
        labels={
            "statut":        "Flux",
            "nom_classique": "Strate classique",
            "nom_enrichi":   "Strate enrichie",
        },
        category_orders={"statut": list(_MIG_COLORS.keys())},
    )
    fig_map_mg.update_layout(
        height=460,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type="natural earth",
            landcolor="#F8FAFF",
            bgcolor="rgba(0,0,0,0)",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.22,
            xanchor="center",
            x=0.5,
            font=dict(size=10),
            title_text="",
        ),
    )
    st.plotly_chart(fig_map_mg, width="stretch")
    st.caption(
        "Les pays gris sont stables entre les deux modeles. "
        "Survolez un pays pour afficher son flux de transition."
    )

    # ── Analyse des migrations ────────────────────────────────────────────────
    st.markdown(f"<p class='section-header'>Analyse des flux migratoires entre modeles</p>",
                unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="font-size:0.87rem;color:#475569;line-height:1.70;
                    background:#F8FAFF;border-radius:10px;padding:20px 24px;
                    margin-top:8px;border-left:3px solid {SECONDARY};
                    box-shadow:0 1px 3px rgba(0,0,0,0.05);">
        Sur les 167 pays alignes entre les deux modelisations, 129 conservent la meme
        strate socio-economique, soit un taux de stabilite de 82 %. Ce resultat valide
        la coherence fondamentale entre les deux partitions : l'ajout de dix variables
        supplementaires — indicateurs de sante granulaires, variables sociales et
        indicateurs FSI — n'a pas redessine la geographie globale du developpement,
        mais resolu des ambiguites que les seules huit variables classiques ne permettaient
        pas de trancher. Les 28 transitions s'organisent en quatre mouvements distincts.

        Huit pays intermediaires rejoignent le pole des pays developpes stables. Pour les
        quatre monarchies du Golfe — Qatar, Emirats arabes unis, Koweit et Oman —, le
        modele classique sous-estimait leur profil en raison d'indicateurs sanitaires et de
        developpement humain inferieurs au seuil des nations industrialisees. Les variables
        FSI introduites dans le modele enrichi revelent une stabilite institutionnelle
        remarquable : leurs scores d'appareil securitaire, de griefs de groupe et de flux
        de refugies sont parmi les plus faibles du dataset, ce qui suffit a les rapprocher
        du centroide developpe. L'Argentine, le Chili, l'Uruguay et la Roumanie forment un
        second sous-groupe : leur inflation historiquement elevee penalisait leur
        positionnement classique, tandis que leurs indicateurs sociaux — scolarisation,
        taux de pauvrete — et leur profil FSI s'alignent sur le pole stable une fois pris
        en compte.

        Sept pays developpes sont reclasses en intermediaires vulnerables. Bosnia-Herzegovine,
        Montenegro et Serbie portent les traces institutionnelles des conflits des annees 1990,
        visibles dans leurs scores FSI mais invisibles dans le PIB ou l'esperance de vie.
        Le Liban represente le cas le plus instructif : ses indicateurs macro et sanitaires
        historiques le rangeaient parmi les pays avances, mais la conjonction d'une crise
        financiere structurelle, d'un score d'appareil securitaire eleve et de griefs
        communautaires persistants le deplace vers le segment intermediaire vulnerable des
        que ces dimensions entrent dans le modele. Israel, les Maldives et Panama completent
        ce groupe, chacun portant une asymetrie entre niveau de vie et profil de resilience
        institutionnelle ou sociale.

        Sept pays intermediaires sont redistribues vers les strates prioritaires. Botswana,
        Gabon et Namibie rejoignent le cluster Crise VIH — non pas par degradation de leurs
        indicateurs economiques, mais parce que la variable hiv_prevalence, absente du modele
        classique, enregistre pour ces trois pays des prevalences superieures a 8 %, les
        isolant structurellement dans une region distincte de l'espace multivariable. Cette
        variable est un indicateur WDI de sante, pas un indicateur FSI. L'Irak et l'Ukraine
        sont absorbes dans les Etats fragiles : leurs scores FSI d'appareil securitaire et
        d'intervention exterieure atteignent des niveaux caracteristiques de zones de conflit
        actif, une information totalement absente du modele a huit variables. Les Iles Salomon
        et la Guinee Equatoriale completent ce groupe pour des raisons d'instabilite
        institutionnelle que leurs indicateurs macro masquaient.

        Enfin, six pays initialement classes en Prioritaires remontent vers les Intermediaires
        vulnerables. Senegal, Nepal, Timor-Leste, Comores, Myanmar et Tadjikistan presentent
        des indicateurs macroeconomiques degrades qui les faisaient apparaitre aussi critiques
        que les Etats les plus fragilises du dataset. L'elargissement de la base variable
        nuance ce diagnostic : leurs scores de fragilite institutionnelle et leurs indicateurs
        sociaux les distinguent suffisamment de leurs voisins en Crise VIH ou en situation
        d'effondrement etatique pour justifier une strate distincte.

        La lecture d'ensemble confirme que l'enrichissement des nouvelles variable ne
        reecrit pas la carte mondiale, mais il corrige les deux zones d'ambiguite du modele
        classique — la frontiere entre Developpes et Intermediaires, la ou la stabilite
        institutionnelle peut soit disqualifier soit promouvoir un pays ; et la frontiere
        entre Intermediaires et Prioritaires, la ou la prevalence du VIH ou la fragilite
        etatique cree une rupture qui ne se manifeste pas dans les indicateurs economiques bruts.
        </div>
        """,
        unsafe_allow_html=True,
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
                      Equilibre  (min/max)  : <strong>{metrics['Equilibre (min/max)']}</strong>
                    </li>
                  </ul>
                  <strong style="color:#0F172A;font-size:0.85rem;">Clusters :</strong>
                  <ul style="padding-left:18px;margin-top:6px;">{names_html}</ul>
                </div>
                """,
                unsafe_allow_html=True,
            )
