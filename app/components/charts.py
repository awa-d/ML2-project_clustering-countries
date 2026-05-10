import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler

from config import CLUSTER_COLORS, PRIMARY, SECONDARY, ACCENT, DANGER

# Constantes de style communes aux graphiques
_GRID  = "#f3f4f6"
_BORDER = "#e5e7eb"
_TEXT  = "#374151"
_MUTED = "#9ca3af"
_BG    = "rgba(0,0,0,0)"


# ── Helpers couleurs ──────────────────────────────────────────────────────────

def _label(cluster_id: int, cluster_names: dict | None) -> str:
    if cluster_names and cluster_id in cluster_names:
        return cluster_names[cluster_id]
    return f"Cluster {cluster_id}"


def _color_map_ids(ids, cluster_names=None) -> dict:
    return {i: CLUSTER_COLORS[i % len(CLUSTER_COLORS)] for i in sorted(set(ids))}


def _color_map_labels(ids, cluster_names=None) -> dict:
    return {_label(i, cluster_names): CLUSTER_COLORS[i % len(CLUSTER_COLORS)]
            for i in sorted(set(ids))}


# ── Carte choroplèthe ─────────────────────────────────────────────────────────

def choropleth_map(df: pd.DataFrame, id_col: str, iso_col: str,
                   cluster_col: str = "cluster",
                   cluster_names: dict | None = None) -> go.Figure:
    df_m = df[[id_col, iso_col, cluster_col]].dropna(subset=[iso_col]).copy()
    df_m["_label"] = df_m[cluster_col].apply(lambda c: _label(int(c), cluster_names))

    unique_ids = sorted(df_m[cluster_col].unique())
    cmap  = {_label(i, cluster_names): CLUSTER_COLORS[i % len(CLUSTER_COLORS)] for i in unique_ids}
    order = [_label(i, cluster_names) for i in unique_ids]

    fig = px.choropleth(
        df_m,
        locations=iso_col,
        locationmode="ISO-3",
        color="_label",
        hover_name=id_col,
        hover_data={"_label": True, iso_col: False},
        color_discrete_map=cmap,
        category_orders={"_label": order},
        labels={"_label": "Cluster"},
    )
    fig.update_geos(
        showframe=False,
        showcoastlines=True, coastlinecolor=_BORDER,
        showland=True,       landcolor="#f9fafb",
        showocean=True,      oceancolor="#eff6ff",
        showlakes=True,      lakecolor="#eff6ff",
        projection_type="natural earth",
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        legend_title_text="",
        legend=dict(
            orientation="h",
            yanchor="bottom", y=0.02,
            xanchor="left",   x=0.01,
            bgcolor="rgba(255,255,255,0.92)",
            bordercolor=_BORDER, borderwidth=1,
            font=dict(size=11, color=_TEXT),
        ),
        paper_bgcolor=_BG,
        geo_bgcolor=_BG,
        height=460,
    )
    return fig


# ── Projection ACP ────────────────────────────────────────────────────────────

def pca_scatter(X_scaled: np.ndarray, labels: np.ndarray,
                country_names: list | None = None,
                cluster_names: dict | None = None,
                title: str = "Projection ACP — 2D") -> go.Figure:
    pca    = PCA(n_components=2, random_state=42)
    coords = pca.fit_transform(X_scaled)
    ve     = pca.explained_variance_ratio_

    df_p = pd.DataFrame({
        "PC1":     coords[:, 0],
        "PC2":     coords[:, 1],
        "_label":  [_label(int(l), cluster_names) for l in labels],
        "_cid":    labels,
    })
    if country_names is not None:
        df_p["Pays"] = country_names

    unique_ids = sorted(set(labels))
    cmap  = {_label(i, cluster_names): CLUSTER_COLORS[i % len(CLUSTER_COLORS)] for i in unique_ids}
    order = [_label(i, cluster_names) for i in unique_ids]

    fig = px.scatter(
        df_p, x="PC1", y="PC2", color="_label",
        color_discrete_map=cmap,
        category_orders={"_label": order},
        hover_name="Pays" if country_names is not None else None,
        labels={
            "PC1":    f"PC1 ({ve[0]*100:.1f} %)",
            "PC2":    f"PC2 ({ve[1]*100:.1f} %)",
            "_label": "Cluster",
        },
        title=title,
    )
    fig.update_traces(marker=dict(size=7, opacity=0.80, line=dict(width=0.5, color="white")))
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor=_BG,
        legend_title_text="",
        legend=dict(bgcolor="rgba(255,255,255,0.95)", bordercolor=_BORDER, borderwidth=1,
                    font=dict(size=11, color=_TEXT)),
        height=400,
        title_font=dict(color=PRIMARY, size=13),
        font=dict(color=_TEXT),
        xaxis=dict(gridcolor=_GRID, zeroline=False, tickfont=dict(size=11, color=_MUTED)),
        yaxis=dict(gridcolor=_GRID, zeroline=False, tickfont=dict(size=11, color=_MUTED)),
    )
    return fig


# ── Radar chart ───────────────────────────────────────────────────────────────

def radar_chart(df: pd.DataFrame, num_cols: list,
                cluster_col: str = "cluster",
                cluster_names: dict | None = None,
                title: str = "Profil des clusters") -> go.Figure:
    scaler  = MinMaxScaler()
    df_norm = pd.DataFrame(scaler.fit_transform(df[num_cols]), columns=num_cols)
    df_norm[cluster_col] = df[cluster_col].values

    cats = num_cols + [num_cols[0]]
    fig  = go.Figure()

    for cid in sorted(df[cluster_col].unique()):
        vals  = df_norm[df_norm[cluster_col] == cid][num_cols].mean().tolist()
        vals += [vals[0]]
        color = CLUSTER_COLORS[cid % len(CLUSTER_COLORS)]
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=cats,
            fill="toself",
            name=_label(int(cid), cluster_names),
            line_color=color,
            fillcolor=color,
            opacity=0.30,
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1], showticklabels=False,
                            gridcolor=_BORDER),
            angularaxis=dict(tickfont=dict(size=10, color=_MUTED)),
            bgcolor="rgba(249,250,251,0.5)",
        ),
        showlegend=True,
        title=dict(text=title, font=dict(color=PRIMARY, size=13)),
        paper_bgcolor=_BG,
        height=440,
        legend_title_text="",
        font=dict(color=_TEXT),
        legend=dict(bgcolor="rgba(255,255,255,0.95)", bordercolor=_BORDER, borderwidth=1,
                    font=dict(size=11)),
    )
    return fig


# ── Distribution clusters ─────────────────────────────────────────────────────

def cluster_bar(df: pd.DataFrame, cluster_col: str = "cluster",
                cluster_names: dict | None = None) -> go.Figure:
    counts = df[cluster_col].value_counts().sort_index().reset_index()
    counts.columns = ["cid", "Pays"]
    counts["Cluster"] = counts["cid"].apply(lambda c: _label(int(c), cluster_names))
    counts["color"]   = counts["cid"].apply(lambda c: CLUSTER_COLORS[c % len(CLUSTER_COLORS)])

    fig = go.Figure(go.Bar(
        x=counts["Cluster"], y=counts["Pays"],
        marker_color=counts["color"],
        text=counts["Pays"],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>%{y} pays<extra></extra>",
    ))
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor=_BG,
        showlegend=False,
        xaxis=dict(title="", tickangle=-15, tickfont=dict(size=11, color=_TEXT)),
        yaxis=dict(title="Pays", gridcolor=_GRID, tickfont=dict(size=11, color=_MUTED)),
        font=dict(color=_TEXT),
        height=300,
    )
    return fig


def cluster_pie(df: pd.DataFrame, cluster_col: str = "cluster",
                cluster_names: dict | None = None) -> go.Figure:
    counts = df[cluster_col].value_counts().sort_index()
    colors = [CLUSTER_COLORS[i % len(CLUSTER_COLORS)] for i in counts.index]
    labels = [_label(int(i), cluster_names) for i in counts.index]

    fig = go.Figure(go.Pie(
        labels=labels,
        values=counts.values,
        marker_colors=colors,
        hole=0.45,
        textinfo="label+percent",
        hoverinfo="label+value+percent",
        textfont=dict(size=11),
    ))
    fig.update_layout(
        paper_bgcolor=_BG,
        showlegend=True,
        legend_title_text="",
        legend=dict(bgcolor="rgba(255,255,255,0.95)", bordercolor=_BORDER, borderwidth=1,
                    font=dict(size=11, color=_TEXT)),
        font=dict(color=_TEXT),
        height=300,
    )
    return fig


# ── Boxplot variable ──────────────────────────────────────────────────────────

def boxplot_variable(df: pd.DataFrame, variable: str,
                     cluster_col: str = "cluster",
                     cluster_names: dict | None = None) -> go.Figure:
    df_b = df.copy()
    df_b["_label"] = df_b[cluster_col].apply(lambda c: _label(int(c), cluster_names))
    unique_ids = sorted(df[cluster_col].unique())
    order = [_label(i, cluster_names) for i in unique_ids]

    fig = px.box(
        df_b, x="_label", y=variable,
        color="_label",
        color_discrete_map={_label(i, cluster_names): CLUSTER_COLORS[i % len(CLUSTER_COLORS)]
                            for i in unique_ids},
        category_orders={"_label": order},
        points="outliers",
        labels={"_label": "Cluster"},
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor=_BG,
        showlegend=False,
        xaxis=dict(title="", tickangle=-15, tickfont=dict(size=11, color=_TEXT)),
        yaxis=dict(gridcolor=_GRID, tickfont=dict(size=11, color=_MUTED)),
        font=dict(color=_TEXT),
        height=360,
    )
    return fig


# ── Heatmap profils moyens ────────────────────────────────────────────────────

def heatmap_cluster_profiles(df: pd.DataFrame, num_cols: list,
                              cluster_col: str = "cluster",
                              cluster_names: dict | None = None) -> go.Figure:
    profile = df.groupby(cluster_col)[num_cols].mean()
    scaler  = MinMaxScaler()
    norm    = pd.DataFrame(
        scaler.fit_transform(profile),
        index=profile.index, columns=profile.columns,
    )
    ylabels = [_label(int(i), cluster_names) for i in norm.index]

    fig = go.Figure(go.Heatmap(
        z=norm.values,
        x=norm.columns.tolist(),
        y=ylabels,
        colorscale="RdYlGn",
        zmin=0, zmax=1,
        text=np.round(profile.values, 2),
        texttemplate="%{text}",
        hovertemplate="Variable: %{x}<br>Cluster: %{y}<br>Valeur brute: %{text}<extra></extra>",
        colorbar=dict(thickness=12, title="Norm."),
    ))
    fig.update_layout(
        xaxis=dict(tickangle=-35, tickfont=dict(size=10, color=_MUTED)),
        yaxis=dict(tickfont=dict(size=11, color=_TEXT)),
        paper_bgcolor=_BG,
        plot_bgcolor=_BG,
        font=dict(color=_TEXT),
        height=max(200, len(profile) * 52 + 50),
        margin=dict(l=0, r=10, t=10, b=0),
    )
    return fig


# ── Feature importance bar ────────────────────────────────────────────────────

def feature_importance_bar(feature_names: list, importances: np.ndarray,
                            title: str = "Importance des variables") -> go.Figure:
    df_fi = pd.DataFrame({"Feature": feature_names, "Importance": importances})
    df_fi = df_fi.sort_values("Importance")

    fig = px.bar(
        df_fi, x="Importance", y="Feature",
        orientation="h",
        color="Importance",
        color_continuous_scale=["#e0f2f1", SECONDARY, PRIMARY],
        title=title,
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor=_BG,
        coloraxis_showscale=False,
        yaxis_title="",
        title_font=dict(color=PRIMARY, size=13),
        font=dict(color=_TEXT),
        xaxis=dict(gridcolor=_GRID, tickfont=dict(size=11, color=_MUTED)),
        yaxis=dict(tickfont=dict(size=11, color=_TEXT)),
        height=max(320, len(feature_names) * 28),
    )
    return fig


# ── Comparaison metriques ─────────────────────────────────────────────────────

def metrics_comparison_bar(metrics_a: dict, metrics_b: dict,
                            label_a: str, label_b: str) -> go.Figure:
    metrics = list(metrics_a.keys())
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name=label_a, x=metrics, y=list(metrics_a.values()),
        marker_color=SECONDARY,
        text=[f"{v:.3f}" for v in metrics_a.values()],
        textposition="outside",
    ))
    fig.add_trace(go.Bar(
        name=label_b, x=metrics, y=list(metrics_b.values()),
        marker_color=DANGER,
        text=[f"{v:.3f}" for v in metrics_b.values()],
        textposition="outside",
    ))
    fig.update_layout(
        barmode="group",
        plot_bgcolor="white",
        paper_bgcolor=_BG,
        legend_title_text="",
        legend=dict(bgcolor="rgba(255,255,255,0.95)", bordercolor=_BORDER, borderwidth=1,
                    font=dict(size=11)),
        yaxis=dict(gridcolor=_GRID, tickfont=dict(size=11, color=_MUTED)),
        xaxis=dict(tickfont=dict(size=11, color=_TEXT)),
        font=dict(color=_TEXT),
        height=360,
    )
    return fig


# ── Profil pays vs cluster ────────────────────────────────────────────────────

def country_profile_chart(country_vals: np.ndarray, cluster_mean: np.ndarray,
                           feat_cols: list, country_name: str,
                           cluster_name: str) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name=country_name,
        x=feat_cols, y=country_vals,
        marker_color=PRIMARY,
        opacity=0.85,
        hovertemplate="<b>" + country_name + "</b><br>%{x}: %{y:.3f}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name=f"Moyenne — {cluster_name}",
        x=feat_cols, y=cluster_mean,
        marker_color=SECONDARY,
        opacity=0.75,
        hovertemplate="<b>Moyenne cluster</b><br>%{x}: %{y:.3f}<extra></extra>",
    ))
    fig.update_layout(
        barmode="group",
        plot_bgcolor="white",
        paper_bgcolor=_BG,
        xaxis=dict(tickangle=-30, tickfont=dict(size=10, color=_MUTED), title=""),
        yaxis=dict(title="Valeur", gridcolor=_GRID, tickfont=dict(size=11, color=_MUTED)),
        legend=dict(bgcolor="rgba(255,255,255,0.95)", bordercolor=_BORDER, borderwidth=1,
                    font=dict(size=11, color=_TEXT)),
        font=dict(color=_TEXT),
        height=400,
    )
    return fig


# ── Radar pays vs cluster ─────────────────────────────────────────────────────

def country_radar_chart(country_vals: np.ndarray, cluster_mean: np.ndarray,
                        feat_cols: list, country_name: str,
                        cluster_name: str) -> go.Figure:
    scaler = MinMaxScaler()
    data   = np.vstack([country_vals, cluster_mean])
    norm   = scaler.fit_transform(data)
    c_norm = norm[0].tolist()
    m_norm = norm[1].tolist()

    cats = feat_cols + [feat_cols[0]]
    c_norm += [c_norm[0]]
    m_norm += [m_norm[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=c_norm, theta=cats, fill="toself",
        name=country_name,
        line_color=PRIMARY, fillcolor=PRIMARY, opacity=0.25,
    ))
    fig.add_trace(go.Scatterpolar(
        r=m_norm, theta=cats, fill="toself",
        name=f"Moyenne — {cluster_name}",
        line_color=SECONDARY, fillcolor=SECONDARY, opacity=0.20,
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1], showticklabels=False,
                            gridcolor=_BORDER),
            angularaxis=dict(tickfont=dict(size=9, color=_MUTED)),
            bgcolor="rgba(249,250,251,0.5)",
        ),
        showlegend=True,
        paper_bgcolor=_BG,
        font=dict(color=_TEXT),
        height=380,
        legend=dict(bgcolor="rgba(255,255,255,0.95)", bordercolor=_BORDER, borderwidth=1,
                    font=dict(size=11)),
    )
    return fig
