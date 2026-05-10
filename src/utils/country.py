
from src.config.paths import DATA_DIR

import pandas as pd

try:
    import pycountry as _pycountry
except ImportError:
    _pycountry = None

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
    if _pycountry is None:
        raise ImportError("pycountry is required for this function")
    try:
        country = _pycountry.countries.lookup(country_name)
        return country.alpha_3
    except LookupError:
        return None


# --------------------------------------------------------------------------------------
# Mappings vers les noms ADMIN du fond de carte Natural Earth 110m (pour visualisation)
# Les petits États insulaires sans polygone NE (Antigua, Bahrain, Barbados, Cabo Verde,
# Comoros, Grenada, Kiribati, Maldives, Malta, Mauritius, Micronesia, Samoa, Seychelles,
# Singapore, St. Vincent, Tonga) restent absents du fond de carte — c'est attendu.
# --------------------------------------------------------------------------------------

# Dataset classique (noms issus du fichier Country-data.csv original)
COUNTRY_MAP_CLASSIC = {
    'United States':                         'United States of America',
    'Bahamas':                               'The Bahamas',
    'Czech Republic':                        'Czechia',
    'Congo, Dem. Rep.':                      'Democratic Republic of the Congo',
    'Congo, Rep.':                           'Republic of the Congo',
    'Tanzania':                              'United Republic of Tanzania',
    'Timor-Leste':                           'East Timor',
    "Cote d'Ivoire":                         'Ivory Coast',
    'Serbia':                                'Republic of Serbia',
    'Kyrgyz Republic':                       'Kyrgyzstan',
    'Lao':                                   'Laos',
    'Macedonia, FYR':                        'North Macedonia',
    'Slovak Republic':                       'Slovakia',
}

# Dataset enrichi (noms normalisés via pycountry dans P0)
COUNTRY_MAP_ENRICHED = {
    'United States':                         'United States of America',
    'Bahamas':                               'The Bahamas',
    'Czech Republic':                        'Czechia',
    'Congo, The Democratic Republic of the': 'Democratic Republic of the Congo',
    'Congo':                                 'Republic of the Congo',
    'Tanzania':                              'United Republic of Tanzania',
    'Timor-Leste':                           'East Timor',
    "Côte d'Ivoire":                         'Ivory Coast',
    'Serbia':                                'Republic of Serbia',
    'Kyrgyz Republic':                       'Kyrgyzstan',
    'Lao':                                   'Laos',
    'North Macedonia':                       'North Macedonia',
    'Slovak Republic':                       'Slovakia',
    'Russian Federation':                    'Russia',
    'South Korea':                           'South Korea',
    'Saint Vincent and the Grenadines':      'Saint Vincent and the Grenadines',
    'Türkiye':                               'Turkey',
    'Brunei Darussalam':                     'Brunei',
    'Cabo Verde':                            'Cape Verde',
    'Micronesia, Federated States of':       'Micronesia',
    'Iran':                                  'Iran',
    'Bolivia':                               'Bolivia',
    'Venezuela':                             'Venezuela',
    'Vietnam':                               'Vietnam',
    'Yemen':                                 'Yemen',
}


def apply_ne_mapping(country_series: pd.Series, dataset: str = 'classic') -> pd.Series:
    """
    Applique le mapping vers les noms du fond Natural Earth 110m.
    dataset: 'classic' ou 'enriched'
    """
    mapping = COUNTRY_MAP_CLASSIC if dataset == 'classic' else COUNTRY_MAP_ENRICHED
    return country_series.astype(str).str.strip().replace(mapping)
