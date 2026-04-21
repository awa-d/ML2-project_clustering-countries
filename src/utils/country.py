
from src.config.paths import DATA_DIR

import pandas as pd

contry = DATA_DIR / "Country-data.csv"

def list_country():
    """
    Retourne la liste des pays.
    """
    df = pd.read_csv(contry)

    countries = df["country"].tolist()
    
    return countries

