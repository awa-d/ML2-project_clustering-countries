
from src.config.paths import DATA_DIR

import pandas as pd
import pycountry

contry = DATA_DIR / "Country-data.csv"

# --------------------------------------------------------------------------------------

def list_country():
    """
    Retourne la liste des pays.
    """
    df = pd.read_csv(contry)

    countries = df["country"].tolist()
    
    return countries


# --------------------------------------------------------------------------------------

def country_to_iso3(country_name):
    try:
        country = pycountry.countries.lookup(country_name)
        return country.alpha_3
    except LookupError:
        return None