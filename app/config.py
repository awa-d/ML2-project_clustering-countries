from pathlib import Path
import sys

APP_DIR  = Path(__file__).resolve().parent
ROOT_DIR = APP_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config.paths import DATA_DIR, ROOT_DIR as PROJ_ROOT

MODEL_DIR = PROJ_ROOT / "models"

MODEL_K3_PATH    = MODEL_DIR / "kmeans_k3_classique.joblib"
SCALER_K3_PATH   = MODEL_DIR / "scaler_classique.joblib"
CLUSTERS_K3_PATH = MODEL_DIR / "clusters_classique_k3.csv"
MODEL_K4_PATH    = MODEL_DIR / "kmeans_k4_enrichi.joblib"
SCALER_K4_PATH   = MODEL_DIR / "scaler_enrichi.joblib"
CLUSTERS_K4_PATH = MODEL_DIR / "clusters_enrichi_k4.csv"

FEAT_K3 = [
    "life_expec", "child_mort_log", "total_fer", "gdpp_log",
    "health", "inflation_log", "exports_log", "imports_log",
]
FEAT_K4 = [
    "physicians_per_1000", "hiv_prevalence_log", "life_expec", "child_mort_log",
    "vaccination_dpt_log", "gdpp_log", "inflation_log", "social_undernourishment_log",
    "social_poverty_2_15_log", "social_schooling_log",
    "security_apparatus", "group_grievance", "refugees_idps", "external_intervention",
]
FSI_COLS = ["security_apparatus", "group_grievance", "refugees_idps", "external_intervention"]

MODELS_META = {
    "Modele classique": {
        "label":       "Modele classique",
        "description": "Clustering sur 8 indicateurs socio-economiques et sanitaires.",
        "features":    8,
        "k":           3,
        "feat_cols":   FEAT_K3,
    },
    "Modele enrichi": {
        "label":       "Modele enrichi",
        "description": "Clustering sur 14 variables incluant 4 indicateurs FSI de fragilite etatique.",
        "features":    14,
        "k":           4,
        "feat_cols":   FEAT_K4,
    },
}

APP_TITLE    = "SigmaPulse"
APP_SUBTITLE = "Calculated compassion: where Data Science meets human dignity."

TEAM = [
    {"name": "Awa Diaw",                      "role": "Team work",            "github": ""},
    {"name": "Moussa Dieme",                  "role": "Team work",            "github": ""},
    {"name": "Ndeye Ramatoulaye Ndoye Fall",  "role": "Team work",  "github": ""},
    {"name": "Hildegarde Edima Biyenda",      "role": "Team work",            "github": ""},
]
SUPERVISOR = "Mously Diaw — Senior Machine Learning & Data Science Supervisor"

# Palette : indigo profond comme accent unique, clusters contrastes clairs
CLUSTER_COLORS = ["#4F46E5", "#059669", "#DC2626", "#D97706", "#7C3AED"]

PRIMARY   = "#0F172A"   # slate-900
SECONDARY = "#4338CA"   # indigo-700  (accent principal)
ACCENT    = "#6366F1"   # indigo-500
DANGER    = "#DC2626"   # red-600
