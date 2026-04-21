from src.utils.country import list_country
from src.utils.country import country_to_iso3



# --------------------------------------------------------------------------------------

def test_list_country_returns_list():
    countries = list_country()

    assert len(countries) ==167
    assert "Afghanistan" in countries


# --------------------------------------------------------------------------------------

def test_country_to_iso3():
    assert country_to_iso3("Afghanistan") == "AFG"
