import numpy as np
import pandas as pd
import streamlit as st

from components.charts import (
    country_profile_chart, country_radar_chart, choropleth_map,
)
from data_loader import get_labeled_data
from config import PRIMARY, SECONDARY, ACCENT, DANGER, CLUSTER_COLORS


def _badge(name: str, cluster_id: int, cluster_name: str, color: str) -> str:
    return (
        f"<div style='background:white;border-radius:12px;padding:16px 22px;"
        f"border-left:6px solid {color};"
        f"box-shadow:0 2px 10px rgba(0,0,0,0.07);margin-bottom:8px;'>"
        f"<span style='font-size:1.4rem;font-weight:800;color:{PRIMARY};'>{name}</span>"
        f"<span style='background:{color};color:white;padding:4px 12px;"
        f"border-radius:16px;font-size:0.85rem;font-weight:700;margin-left:12px;'>"
        f"Cluster {cluster_id} — {cluster_name}</span></div>"
    )


def _model_selector(key_suffix: str) -> tuple:
    model_key = st.radio(
        "Modele",
        ["Modele classique", "Modele enrichi"],
        format_func=lambda k: (
            "Modele classique "
            if k == "Modele classique" else
            "Modele enrichi"
        ),
        horizontal=True,
        label_visibility="visible",
        key=f"model_{key_suffix}",
    )
    with st.spinner("Chargement…"):
        d = get_labeled_data(model_key)
    return d


def render():
    st.markdown(
        f"<h2 style='color:{PRIMARY};margin-bottom:4px;'>Analyse d'un pays</h2>",
        unsafe_allow_html=True,
    )

    tab_single, tab_compare = st.tabs(["Analyse individuelle", "Comparer deux pays"])

    # ── ONGLET 1 : Analyse individuelle ──────────────────────────────────────
    with tab_single:
        st.caption(
            "Selectionnez un pays pour explorer son profil detaille, "
            "son cluster d'appartenance et les pays les plus similaires."
        )

        d             = _model_selector("single")
        df            = d["df"]
        id_col        = d["id_col"]
        iso_col       = d["iso_col"]
        feat_cols     = d["feat_cols"]
        labels        = d["labels"]
        X_scaled      = d["X_scaled"]
        cluster_names = d["cluster_names"]

        countries   = sorted(df[id_col].tolist())
        default_idx = countries.index("France") if "France" in countries else 0
        selected    = st.selectbox("Choisir un pays", countries, index=default_idx,
                                   key="country_single")

        row_idx      = int(df[df[id_col] == selected].index[0])
        row          = df.loc[row_idx]
        cluster_id   = int(row["cluster"])
        cluster_name = cluster_names.get(cluster_id, f"Cluster {cluster_id}")
        color        = CLUSTER_COLORS[cluster_id % len(CLUSTER_COLORS)]

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

        kpi_targets = [
            ("gdpp_log",       "PIB/hab. (log)"),
            ("life_expec",     "Esperance de vie"),
            ("child_mort_log", "Mortalite infantile"),
        ]
        available = [(f, l) for f, l in kpi_targets if f in feat_cols]

        if available:
            kpi_cols     = st.columns(len(available))
            cluster_df   = df[df["cluster"] == cluster_id]
            cluster_mean = cluster_df[feat_cols].mean()
            for col, (feat, label) in zip(kpi_cols, available):
                val   = float(row[feat])
                delta = float(val - cluster_mean[feat])
                with col:
                    st.metric(label, f"{val:.3f}",
                              delta=f"{delta:+.3f} vs cluster", delta_color="normal")

        st.divider()

        cluster_df   = df[df["cluster"] == cluster_id]
        cluster_mean = cluster_df[feat_cols].mean().values
        country_vals = row[feat_cols].values.astype(float)

        (tab_bar,) = st.tabs(["Comparaison barres"])
        with tab_bar:
            st.markdown(
                f"<p class='section-header'>{selected} vs moyenne du cluster "
                f"{cluster_id} ({cluster_name})</p>",
                unsafe_allow_html=True,
            )
            fig_bar = country_profile_chart(
                country_vals, cluster_mean, feat_cols, selected, cluster_name,
            )
            st.plotly_chart(fig_bar, width="stretch")
            st.caption(
                "Valeurs dans l'espace original (log-transforme). "
                "Comparaison directe avec la moyenne du cluster d'appartenance."
            )

        st.markdown(
            f"<p class='section-header'>Pays les plus proches dans le cluster "
            f"{cluster_id} — {cluster_name}</p>",
            unsafe_allow_html=True,
        )

        cluster_mask = labels == cluster_id
        X_cluster    = X_scaled[cluster_mask]
        idx_in_full  = np.where(cluster_mask)[0]
        x_country    = X_scaled[row_idx]
        distances    = np.sqrt(((X_cluster - x_country) ** 2).sum(axis=1))

        top_n        = min(10, len(distances) - 1)
        sorted_pos   = np.argsort(distances)
        similar_pos  = [p for p in sorted_pos if idx_in_full[p] != row_idx][:top_n]
        similar_idx  = idx_in_full[similar_pos]
        similar_dist = distances[similar_pos]

        similar_df = df.iloc[similar_idx][[id_col] + feat_cols].copy()
        similar_df.insert(0, "Distance (espace scale)", np.round(similar_dist, 4))
        st.dataframe(similar_df.set_index(id_col).round(3), width="stretch", height=340)
        st.caption(
            "Distance euclidienne dans l'espace normalise (RobustScaler). "
            "Un score proche de 0 indique un profil quasi-identique."
        )

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
                width="stretch", height=380,
            )
            st.caption(f"La ligne {selected} est mise en evidence en bleu.")

        st.markdown(
            f"<p class='section-header'>Position geographique — {selected} et son cluster</p>",
            unsafe_allow_html=True,
        )
        fig_map = choropleth_map(df, id_col, iso_col, cluster_names=cluster_names)
        st.plotly_chart(fig_map, width="stretch")
        st.caption(
            f"{selected} appartient au Cluster {cluster_id} ({cluster_name}). "
            "Passez la souris sur les pays pour voir leur nom et leur cluster."
        )

    # ── ONGLET 2 : Comparaison deux pays ─────────────────────────────────────
    with tab_compare:
        st.caption(
            "Selectionnez deux pays et un modele pour comparer leurs profils "
            "variable par variable et visualiser leur ecart au centroide."
        )

        d_cmp         = _model_selector("compare")
        df_c          = d_cmp["df"]
        id_col_c      = d_cmp["id_col"]
        feat_cols_c   = d_cmp["feat_cols"]
        labels_c      = d_cmp["labels"]
        X_scaled_c    = d_cmp["X_scaled"]
        cluster_names_c = d_cmp["cluster_names"]

        countries_c = sorted(df_c[id_col_c].tolist())

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            idx_a = countries_c.index("France") if "France" in countries_c else 0
            pays_a = st.selectbox("Pays A", countries_c, index=idx_a, key="cmp_a")
        with col_p2:
            idx_b = countries_c.index("Senegal") if "Senegal" in countries_c else 1
            pays_b = st.selectbox("Pays B", countries_c, index=idx_b, key="cmp_b")

        if pays_a == pays_b:
            st.warning("Veuillez selectionner deux pays differents.")
            return

        def _get(df, id_col, pays, feat_cols, labels, X_scaled, cluster_names):
            row_idx      = int(df[df[id_col] == pays].index[0])
            row          = df.loc[row_idx]
            cluster_id   = int(row["cluster"])
            cluster_name = cluster_names.get(cluster_id, f"Cluster {cluster_id}")
            color        = CLUSTER_COLORS[cluster_id % len(CLUSTER_COLORS)]
            vals         = row[feat_cols].values.astype(float)
            cluster_df   = df[df["cluster"] == cluster_id]
            centroid     = cluster_df[feat_cols].mean().values
            x_sc         = X_scaled[row_idx]
            return dict(row_idx=row_idx, cluster_id=cluster_id,
                        cluster_name=cluster_name, color=color,
                        vals=vals, centroid=centroid, x_sc=x_sc,
                        cluster_df=cluster_df)

        ga = _get(df_c, id_col_c, pays_a, feat_cols_c, labels_c, X_scaled_c, cluster_names_c)
        gb = _get(df_c, id_col_c, pays_b, feat_cols_c, labels_c, X_scaled_c, cluster_names_c)

        # ── Badges ───────────────────────────────────────────────────────────
        col_ba, col_bb = st.columns(2)
        with col_ba:
            st.markdown(_badge(pays_a, ga["cluster_id"], ga["cluster_name"], ga["color"]),
                        unsafe_allow_html=True)
        with col_bb:
            st.markdown(_badge(pays_b, gb["cluster_id"], gb["cluster_name"], gb["color"]),
                        unsafe_allow_html=True)

        # ── KPI comparatifs ───────────────────────────────────────────────────
        kpi_targets_c = [
            ("gdpp_log",       "PIB/hab. (log)"),
            ("life_expec",     "Esperance de vie"),
            ("child_mort_log", "Mortalite infantile"),
        ]
        available_c = [(f, l) for f, l in kpi_targets_c if f in feat_cols_c]

        if available_c:
            st.markdown(f"<p class='section-header'>Indicateurs cles</p>",
                        unsafe_allow_html=True)
            kpi_cols_c = st.columns(len(available_c))
            feat_idx_map = {f: i for i, f in enumerate(feat_cols_c)}
            for col_k, (feat, label) in zip(kpi_cols_c, available_c):
                fi   = feat_idx_map[feat]
                va   = float(ga["vals"][fi])
                vb   = float(gb["vals"][fi])
                diff = va - vb
                with col_k:
                    st.metric(
                        label,
                        f"{pays_a}: {va:.2f}  |  {pays_b}: {vb:.2f}",
                        delta=f"{diff:+.2f} (A − B)",
                        delta_color="normal",
                    )

        st.divider()

        # ── Graphique profil comparatif ───────────────────────────────────────
        st.markdown(f"<p class='section-header'>Profil comparatif variable par variable</p>",
                    unsafe_allow_html=True)

        import plotly.graph_objects as go_cmp
        fig_cmp = go_cmp.Figure()
        fig_cmp.add_trace(go_cmp.Bar(
            name=pays_a,
            x=feat_cols_c,
            y=ga["vals"],
            marker_color=ga["color"],
            opacity=0.85,
            hovertemplate=f"<b>{pays_a}</b><br>%{{x}}: %{{y:.3f}}<extra></extra>",
        ))
        fig_cmp.add_trace(go_cmp.Bar(
            name=pays_b,
            x=feat_cols_c,
            y=gb["vals"],
            marker_color=gb["color"],
            opacity=0.85,
            hovertemplate=f"<b>{pays_b}</b><br>%{{x}}: %{{y:.3f}}<extra></extra>",
        ))
        fig_cmp.update_layout(
            barmode="group",
            plot_bgcolor="white",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(tickangle=-30, tickfont=dict(size=10)),
            yaxis=dict(title="Valeur", gridcolor="#f3f4f6"),
            legend=dict(bgcolor="rgba(255,255,255,0.95)", bordercolor="#e5e7eb",
                        borderwidth=1, font=dict(size=11)),
            font=dict(color="#374151"),
            height=420,
        )
        st.plotly_chart(fig_cmp, width="stretch")
        st.caption(
            "Valeurs dans l'espace original (log-transforme pour les variables asymetriques). "
            "Chaque barre represente la valeur brute du pays sur la variable indiquee."
        )

        # ── Positions dans l'espace standardise (dumbbell) ───────────────────
        st.markdown(
            f"<p class='section-header'>Position de chaque pays par variable (espace du modele)</p>",
            unsafe_allow_html=True,
        )

        import plotly.graph_objects as go_db
        feat_labels_c = [
            f.replace("_log", "").replace("social_", "").replace("_", " ")
            for f in feat_cols_c
        ]

        fig_db = go_db.Figure()

        for j in range(len(feat_cols_c)):
            xa = float(ga["x_sc"][j])
            xb = float(gb["x_sc"][j])
            fig_db.add_trace(go_db.Scatter(
                x=[xa, xb], y=[feat_labels_c[j], feat_labels_c[j]],
                mode="lines",
                line=dict(color="#D1D5DB", width=2),
                showlegend=False, hoverinfo="skip",
            ))

        fig_db.add_trace(go_db.Scatter(
            x=ga["x_sc"].tolist(), y=feat_labels_c,
            mode="markers", name=pays_a,
            marker=dict(size=13, color=ga["color"], symbol="circle",
                        line=dict(width=1.5, color="white")),
            hovertemplate=f"<b>{pays_a}</b><br>%{{y}}: %{{x:.3f}}<extra></extra>",
        ))
        fig_db.add_trace(go_db.Scatter(
            x=gb["x_sc"].tolist(), y=feat_labels_c,
            mode="markers", name=pays_b,
            marker=dict(size=13, color=gb["color"], symbol="diamond",
                        line=dict(width=1.5, color="white")),
            hovertemplate=f"<b>{pays_b}</b><br>%{{y}}: %{{x:.3f}}<extra></extra>",
        ))

        fig_db.add_vline(x=0, line_color="#9CA3AF", line_width=1, line_dash="dot")

        fig_db.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(
                title="Valeur standardisee (RobustScaler — 0 = mediane mondiale)",
                gridcolor="#F3F4F6", zeroline=False,
                tickfont=dict(size=10, color="#9CA3AF"),
            ),
            yaxis=dict(tickfont=dict(size=10, color="#374151"), autorange="reversed"),
            legend=dict(bgcolor="rgba(255,255,255,0.95)", bordercolor="#E5E7EB",
                        borderwidth=1, font=dict(size=11)),
            font=dict(color="#374151"),
            height=max(340, len(feat_cols_c) * 34 + 80),
            margin=dict(l=10, r=10, t=20, b=10),
        )
        st.plotly_chart(fig_db, width="stretch")
        st.caption(
            "L'axe horizontal represente la valeur standardisee apres RobustScaler : "
            "0 correspond a la mediane mondiale, les valeurs positives signifient "
            "au-dessus de la mediane, les negatives en dessous. "
            "La ligne pointillee marque cette mediane. "
            "L'ecart horizontal entre les deux points mesure exactement la difference "
            "percue par le modele KMeans entre les deux pays sur chaque dimension."
        )

        # ── Distance entre les deux pays ──────────────────────────────────────
        st.divider()
        dist_ab = float(np.sqrt(((ga["x_sc"] - gb["x_sc"]) ** 2).sum()))
        dist_a_centroid = float(np.sqrt(((ga["x_sc"] - ga["centroid"]) ** 2).sum()))
        dist_b_centroid = float(np.sqrt(((gb["x_sc"] - gb["centroid"]) ** 2).sum()))

        col_d1, col_d2, col_d3 = st.columns(3)
        col_d1.metric("Distance A — B (espace normalise)", f"{dist_ab:.3f}")
        col_d2.metric(f"Distance {pays_a} — centroide C{ga['cluster_id']}",
                      f"{dist_a_centroid:.3f}")
        col_d3.metric(f"Distance {pays_b} — centroide C{gb['cluster_id']}",
                      f"{dist_b_centroid:.3f}")

        st.caption(
            "Distances euclidiennes dans l'espace normalise (RobustScaler). "
            "Une distance A-B proche de 0 indique des profils quasi-identiques, "
            "independamment de leur cluster d'appartenance."
        )

        # ── Tableau des ecarts ────────────────────────────────────────────────
        st.markdown(f"<p class='section-header'>Ecart variable par variable</p>",
                    unsafe_allow_html=True)
        df_diff = pd.DataFrame({
            "Variable":  feat_cols_c,
            pays_a:      np.round(ga["vals"], 3),
            pays_b:      np.round(gb["vals"], 3),
            "Ecart (A-B)": np.round(ga["vals"] - gb["vals"], 3),
        })
        df_diff["Avantage"] = df_diff["Ecart (A-B)"].apply(
            lambda d: pays_a if d > 0 else (pays_b if d < 0 else "=")
        )
        st.dataframe(df_diff.set_index("Variable"), width="stretch", height=380)
