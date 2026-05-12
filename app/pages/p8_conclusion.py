import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from data_loader import get_labeled_data
from config import PRIMARY, SECONDARY, CLUSTER_COLORS


def render():
    st.markdown(
        f"<h2 style='color:{PRIMARY};margin-bottom:4px;'>Conclusion</h2>",
        unsafe_allow_html=True,
    )
    st.caption(
        "Identification methodologique des pays prioritaires a partir du modele enrichi "
        "(14 variables, k=4). Score de vulnerabilite = distance euclidienne au centroide "
        "Developpes stables dans l'espace normalise par RobustScaler."
    )

    # ── Introduction ─────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="background:#F8FAFF;border-radius:10px;padding:16px 20px;
                    margin-bottom:20px;border-left:3px solid {SECONDARY};
                    box-shadow:0 1px 3px rgba(0,0,0,0.05);
                    font-size:0.88rem;color:#475569;line-height:1.65;">
        Repondre a la question "quels pays sont les plus vulnerables ?" exige d'abord
        de definir ce que l'on entend par vulnerabilite.
        L'approche retenue n'est pas normative — elle ne selectionne pas a priori
        un indicateur comme le PIB ou la mortalite infantile — mais geometrique :
        elle mesure la distance de chaque pays, dans l'espace a 14 dimensions du
        modele enrichi, au prototype que constitue le cluster Developpes stables.
        Cette distance est calculee dans l'espace normalise par RobustScaler, ce qui
        la rend directement interpretable , elle quantifie, en unites interquartiles,
        le degre d'eloignement global d'un pays par rapport au profil de reference,
        sur l'ensemble des dimensions simultanement.

        Ce score composite presente trois avantages sur un classement monovariable.
        Il est coherent avec la logique interne du clustering , le score est defini
        dans le meme espace que celui utilise par KMeans. Il est exhaustif : les
        14 dimensions — economiques, sanitaires et institutionnelles — contribuent
        proportionnellement a leur signal discriminant. Et il est continu , il permet
        un classement fin a l'interieur des clusters, la ou la seule appartenance au
        cluster ne distingue pas les cas les plus aigus.
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.spinner("Chargement du modele enrichi..."):
        d = get_labeled_data("Modele enrichi")

    df            = d["df"].copy()
    X             = d["X_scaled"]
    labels        = d["labels"]
    cluster_names = d["cluster_names"]
    id_col        = d["id_col"]
    iso_col       = d["iso_col"]

    # ── Cluster IDs ──────────────────────────────────────────────────────────
    dev_id  = next(k for k, v in cluster_names.items() if v == "Developpes stables")
    hiv_id  = next(k for k, v in cluster_names.items() if v == "Crise VIH")
    sec_id  = next(k for k, v in cluster_names.items() if v == "Etats fragiles")
    vuln_id = next(k for k, v in cluster_names.items() if v == "Intermediaires vulnerables")

    # ── Score de vulnerabilite ────────────────────────────────────────────────
    dev_centroid     = X[labels == dev_id].mean(axis=0)
    df["vuln_score"] = np.round(np.linalg.norm(X - dev_centroid, axis=1), 3)

    # ── Distance moyenne par cluster ─────────────────────────────────────────
    st.markdown(
        f"<p class='section-header'>Distance moyenne au pole de reference par cluster</p>",
        unsafe_allow_html=True,
    )

    cols_m = st.columns(4)
    for col, cid in zip(cols_m, [dev_id, vuln_id, hiv_id, sec_id]):
        cname  = cluster_names[cid]
        avg_d  = float(df[df["cluster"] == cid]["vuln_score"].mean())
        n_pays = int((labels == cid).sum())
        with col:
            st.metric(cname, f"{avg_d:.2f}", f"{n_pays} pays")

    st.markdown(
        f"""
        <div style="font-size:0.83rem;color:#475569;line-height:1.60;margin-top:8px;">
        La distance augmente de facon monotone du pole developpe vers les clusters
        prioritaires.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Carte mondiale ────────────────────────────────────────────────────────
    st.markdown(
        f"<p class='section-header'>Distribution geographique des clusters</p>",
        unsafe_allow_html=True,
    )

    color_map = {
        cluster_names[k]: CLUSTER_COLORS[k % len(CLUSTER_COLORS)]
        for k in cluster_names
    }

    fig_map = px.choropleth(
        df,
        locations=iso_col,
        color="cluster_name",
        hover_name=id_col,
        hover_data={"vuln_score": ":.3f", iso_col: False},
        color_discrete_map=color_map,
        labels={"cluster_name": "Cluster", "vuln_score": "Score"},
    )
    fig_map.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        height=420,
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
            y=-0.12,
            xanchor="center",
            x=0.5,
            font=dict(size=11),
        ),
    )
    st.plotly_chart(fig_map, width="stretch")

    st.markdown(
        f"""
        <div style="font-size:0.83rem;color:#475569;line-height:1.60;margin-top:4px;">
        La carte confirme les deux concentrations geographiques majeures identifiees
        par le modele. L'Afrique subsaharienne concentre la quasi-totalite des pays
        prioritaires, avec une differentiation spatiale nette : la bande australe et
        orientale du continent — Zimbabwe, Zambie, Mozambique, Lesotho, Malawi —
        est dominee par la Crise VIH, tandis que la zone sahelo-centrale et la
        Corne — Tchad, Republique centrafricaine, Soudan, Eritree — regroupe les
        Etats fragiles. En dehors de l'Afrique, les Etats fragiles se localisent
        principalement en Afghanistan, en Iraq,etc, et,
        en Irak et en Ukraine du fait de leurs scores FSI particulierement eleves.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Classement pays prioritaires ──────────────────────────────────────────
    st.markdown(
        f"<p class='section-header'>Classement des pays prioritaires par score de vulnerabilite</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div style="font-size:0.87rem;color:#475569;line-height:1.65;margin-bottom:12px;">
        Le classement ci-dessous couvre les 45 pays des deux clusters prioritaires —
        Etats fragiles (22 pays) et Crise VIH (23 pays) — tries par score decroissant.
        Ce perimetre constitue le groupe d'intervention prioritaire identifie par le modele.
        A l'interieur de ce groupe, le score reflete l'intensite cumulee de la defaillance
        sur l'ensemble des 14 dimensions simultanement : un score eleve correspond a un pays
        dont le profil s'ecarte de la reference sur la majorite des axes du modele.
        </div>
        """,
        unsafe_allow_html=True,
    )

    priority_ids = [hiv_id, sec_id]
    df_priority = (
        df[df["cluster"].isin(priority_ids)]
        .sort_values("vuln_score", ascending=False)
        .reset_index(drop=True)
    )
    df_priority.index = range(1, len(df_priority) + 1)

    col_chart, col_table = st.columns([1.3, 1])

    with col_chart:
        bar_colors = [
            CLUSTER_COLORS[int(row["cluster"]) % len(CLUSTER_COLORS)]
            for _, row in df_priority.iterrows()
        ]
        fig_rank = go.Figure(go.Bar(
            y=df_priority[id_col],
            x=df_priority["vuln_score"],
            orientation="h",
            marker_color=bar_colors,
            hovertemplate="%{y}<br>Score : %{x:.3f}<extra></extra>",
        ))
        fig_rank.update_layout(
            height=max(460, len(df_priority) * 22 + 80),
            margin=dict(l=0, r=20, t=10, b=20),
            xaxis_title="Score de vulnerabilite",
            yaxis=dict(autorange="reversed", tickfont=dict(size=10)),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            font=dict(size=11),
        )
        fig_rank.update_xaxes(showgrid=True, gridcolor="#F1F5F9")
        st.plotly_chart(fig_rank, width="stretch")

    with col_table:
        display_df = df_priority[[id_col, "cluster_name", "vuln_score"]].rename(columns={
            id_col:          "Pays",
            "cluster_name":  "Cluster",
            "vuln_score":    "Score",
        })
        st.dataframe(display_df, height=520, width="stretch")

    # ── Lecture des profils extremes ──────────────────────────────────────────
    st.markdown(
        f"<p class='section-header'>Lecture des profils extremes</p>",
        unsafe_allow_html=True,
    )

    top5 = df_priority.head(5)[id_col].tolist()
    top5_str = ", ".join(top5[:4]) + f" et {top5[4]}"

    st.markdown(
        f"""
        <div style="font-size:0.87rem;color:#475569;line-height:1.65;">
        Les cinq pays affichant les scores les plus eleves sont {top5_str}. Leur
        positionnement en tete du classement tient a des mecanismes differents selon leur
        cluster d'appartenance.

        L'Ukraine constitue un cas methodologiquement instructif. Son score de vulnerabilite
        est le plus eleve du dataset, mais pour des raisons asymetriques : ses indicateurs
        sociaux et sanitaires — scolarisation, couverture medicale, esperance de vie —
        restent proches du perimetre intermediaire, tandis que ses scores FSI d'intervention
        exterieure et d'appareil securitaire, en lien avec le conflit de 2014-2015 present
        dans les donnees, sont parmi les plus extremes du dataset. Ce cas illustre une
        limite a retenir du score composite : il ne distingue pas la nature de la
        vulnerabilite, seulement son intensite cumulee. Une lecture par cluster reste
        necessaire pour interpreter correctement la distance.

        Pour les Etats fragiles du haut du classement — Liberia, Republique centrafricaine,
        Tchad, Nigeria —, la vulnerabilite est distribuee sur l'ensemble des 14 dimensions :
        mortalite infantile et maternelle dans les premiers deciles du dataset,
        quasi-absence de couverture medicale et vaccinale, sous-nutrition severe, et
        indicateurs FSI aux niveaux les plus eleves. Ce sont des pays pour lesquels aucun
        secteur d'intervention n'est epargne.

        Pour les pays du cluster Crise VIH — Lesotho, Mozambique, Zambie —, le score
        est principalement tire par la variable hiv_prevalence ,
        qui atteint des niveaux faisant basculer le systeme de sante dans une gestion
        chronique de l'epidemie. Leur profil institutionnel et economique est moins
        degrade que celui des Etats fragiles du meme rang, mais la charge sanitaire
        specifique du VIH justifie leur classification prioritaire et appelle des
        interventions differentes de celles requises dans les zones de conflit.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Synthese finale ───────────────────────────────────────────────────────
    st.markdown(
        f"<p class='section-header'>Synthese et implications</p>",
        unsafe_allow_html=True,
    )

    n_sec = int((labels == sec_id).sum())
    n_hiv = int((labels == hiv_id).sum())

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(
            f"""
            <div style="background:white;border-radius:12px;padding:20px 22px;
                        box-shadow:0 1px 3px rgba(0,0,0,0.07);
                        border-top:3px solid {CLUSTER_COLORS[sec_id % len(CLUSTER_COLORS)]};">
              <p style="font-size:0.78rem;font-weight:600;text-transform:uppercase;
                        letter-spacing:0.08em;color:#94A3B8;margin:0 0 8px;">
                Etats fragiles — {n_sec} pays
              </p>
              <p style="font-size:0.85rem;color:#475569;line-height:1.60;margin:0;">
                Ce cluster regroupe des pays dont la vulnerabilite est avant tout
                institutionnelle et securitaire. La contrainte principale n'est pas
                l'absence de ressources, mais la defaillance de l'appareil d'etat :
                des investissements sectoriels dans la sante ou l'education sans
                adresser la gouvernance et la securite produisent des gains ephemeres.
                Le perimetre se concentre en Afrique centrale et de l'Ouest, avec
                des cas specifiques en Asie (Afghanistan, Pakistan) et au
                Proche-Orient (Irak).
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_b:
        st.markdown(
            f"""
            <div style="background:white;border-radius:12px;padding:20px 22px;
                        box-shadow:0 1px 3px rgba(0,0,0,0.07);
                        border-top:3px solid {CLUSTER_COLORS[hiv_id % len(CLUSTER_COLORS)]};">
              <p style="font-size:0.78rem;font-weight:600;text-transform:uppercase;
                        letter-spacing:0.08em;color:#94A3B8;margin:0 0 8px;">
                Crise VIH — {n_hiv} pays
              </p>
              <p style="font-size:0.85rem;color:#475569;line-height:1.60;margin:0;">
                Ce cluster regroupe des pays dont les structures etatiques sont
                relativement plus fonctionnelles, mais dont le systeme de sante est
                entierement redimensionne par une epidemie de VIH de forte intensite.
                La charge sanitaire est si severe qu'elle ecrase les capacites
                systemiques du pays et compromet les trajectoires de developpement
                long terme. Le perimetre se concentre en Afrique australe et
                orientale — la region la plus touchee au monde par l'epidemie.
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div style="background:#F8FAFF;border-radius:10px;padding:18px 22px;
                    margin-top:16px;font-size:0.87rem;color:#475569;
                    line-height:1.70;border-left:3px solid {SECONDARY};
                    box-shadow:0 1px 3px rgba(0,0,0,0.05);">
        Ce projet apporte une reponse en deux temps a la question posee par l'ONG.
        Sur le plan structurel, le monde se divise en trois grandes strates de
        developpement que le modele classique identifiait deja. Cette structure constitue une base
        fiable pour l'allocation de ressources a grande echelle.

        Sur le plan operationnel, le modele enrichi affine ce diagnostic en distinguant,
        au sein du perimetre prioritaire, deux types de crise qui n'appellent pas les
        memes priorites d'action. Les 45 pays identifies forment le perimetre
        d'intervention prioritaire. A l'interieur de ce groupe, le classement par
        score de vulnerabilite permet d'identifier les situations les plus aigues,
        avec la distinction essentielle entre fragilite institutionnelle et crise
        sanitaire epidemique.

        La classification produite est interpretable, justifiable methodologiquement,
        et actualisable a chaque nouvelle edition des donnees FSI et des indicateurs
        de developpement de la Banque mondiale. Elle ne remplace pas une analyse terrain,
        mais elle fournit un cadre rigoureux et transparent pour prioriser les
        interventions a partir de donnees publiques et reproductibles.
        </div>
        """,
        unsafe_allow_html=True,
    )
