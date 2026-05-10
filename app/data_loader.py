import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd
import numpy as np
import joblib
import streamlit as st

from config import (
    CLUSTERS_K3_PATH, CLUSTERS_K4_PATH,
    SCALER_K3_PATH, SCALER_K4_PATH,
    FEAT_K3, FEAT_K4, CLUSTER_COLORS,
)

# ── Noms ISO3 connus pour les pays du dataset classique qui echouent pycountry ──

_ISO3_OVERRIDES = {
    "Brunei":                         "BRN",
    "Cape Verde":                     "CPV",
    "Congo, Dem. Rep.":               "COD",
    "Congo, Rep.":                    "COG",
    "Cote d'Ivoire":                  "CIV",
    "Macedonia, FYR":                 "MKD",
    "Micronesia, Fed. Sts.":          "FSM",
    "Russia":                         "RUS",
    "St. Vincent and the Grenadines": "VCT",
    "Turkey":                         "TUR",
}


def _name_to_iso3(name: str) -> str | None:
    if name in _ISO3_OVERRIDES:
        return _ISO3_OVERRIDES[name]
    try:
        import pycountry
        return pycountry.countries.lookup(name).alpha_3
    except Exception:
        pass
    try:
        import pycountry
        results = pycountry.countries.search_fuzzy(name)
        return results[0].alpha_3 if results else None
    except Exception:
        return None


# ── Nommage automatique des clusters ─────────────────────────────────────────

def _auto_names_k3(df: pd.DataFrame) -> dict:
    profile = df.groupby("cluster")[FEAT_K3].mean()
    dev = int(profile["gdpp_log"].idxmax())
    pri = int(profile["child_mort_log"].idxmax())
    mid = [k for k in profile.index.tolist() if k not in [dev, pri]][0]
    return {dev: "Developpes", mid: "Intermediaires", pri: "Prioritaires"}


def _auto_names_k4(df: pd.DataFrame) -> dict:
    profile = df.groupby("cluster")[FEAT_K4].mean()
    hiv  = int(profile["hiv_prevalence_log"].idxmax())
    sec  = int(profile["security_apparatus"].idxmax())
    dev  = int(profile["gdpp_log"].idxmax())
    vuln = [k for k in profile.index.tolist() if k not in [hiv, sec, dev]][0]
    return {
        dev:  "Developpes stables",
        hiv:  "Crise VIH",
        sec:  "Etats fragiles",
        vuln: "Intermediaires vulnerables",
    }


# ── API principale ────────────────────────────────────────────────────────────

@st.cache_data
def get_labeled_data(model_key: str) -> dict:
    """
    Charge les donnees et le scaler depuis les fichiers precomputes.
    Retourne un dict pret a l'emploi pour toutes les pages.
    """
    if model_key == "Modele enrichi":
        df        = pd.read_csv(CLUSTERS_K4_PATH)
        scaler    = joblib.load(SCALER_K4_PATH)
        feat_cols = FEAT_K4
        iso_col   = "iso_code" if "iso_code" in df.columns else None
        cluster_names = _auto_names_k4(df)
    else:
        df        = pd.read_csv(CLUSTERS_K3_PATH)
        scaler    = joblib.load(SCALER_K3_PATH)
        feat_cols = FEAT_K3
        iso_col   = None
        cluster_names = _auto_names_k3(df)

    df = df.copy()
    labels   = df["cluster"].values.astype(int)
    X_scaled = scaler.transform(df[feat_cols])

    df["cluster_name"]  = df["cluster"].map(cluster_names)
    df["cluster_color"] = [CLUSTER_COLORS[int(c) % len(CLUSTER_COLORS)] for c in labels]

    if iso_col is None or iso_col not in df.columns:
        df["iso3"] = df["country"].apply(_name_to_iso3)
        iso_col = "iso3"

    return {
        "df":            df,
        "id_col":        "country",
        "iso_col":       iso_col,
        "num_cols":      feat_cols,
        "feat_cols":     feat_cols,
        "labels":        labels,
        "X_scaled":      X_scaled,
        "k":             int(labels.max()) + 1,
        "cluster_names": cluster_names,
    }


def get_both_labeled() -> tuple:
    return get_labeled_data("Modele classique"), get_labeled_data("Modele enrichi")


# ── Metriques de qualite ──────────────────────────────────────────────────────

def compute_metrics(X_scaled: np.ndarray, labels: np.ndarray) -> dict:
    from sklearn.metrics import (
        silhouette_score, davies_bouldin_score, calinski_harabasz_score,
    )
    counts = np.bincount(labels)
    return {
        "Silhouette":          round(float(silhouette_score(X_scaled, labels)), 4),
        "Davies-Bouldin":      round(float(davies_bouldin_score(X_scaled, labels)), 4),
        "Calinski-Harabasz":   round(float(calinski_harabasz_score(X_scaled, labels)), 1),
        "Equilibre (min/max)": round(float(counts.min() / counts.max()), 3),
    }


# ── Description textuelle automatique ────────────────────────────────────────

def auto_describe_cluster(df: pd.DataFrame, cluster_id: int,
                           id_col: str, num_cols: list) -> str:
    c_df   = df[df["cluster"] == cluster_id][num_cols]
    g_df   = df[num_cols]
    means  = c_df.mean()
    g_mean = g_df.mean()
    g_std  = g_df.std().replace(0, 1)

    high = [c for c in num_cols if means[c] > g_mean[c] + 0.6 * g_std[c]]
    low  = [c for c in num_cols if means[c] < g_mean[c] - 0.6 * g_std[c]]

    size  = int((df["cluster"] == cluster_id).sum())
    parts = []
    if high:
        parts.append("valeurs elevees : " + ", ".join(high[:4]))
    if low:
        parts.append("valeurs basses : " + ", ".join(low[:4]))

    desc = f"{size} pays. "
    desc += ("Caracterise par " + " — ".join(parts)) if parts else "Profil proche de la moyenne globale."
    return desc
