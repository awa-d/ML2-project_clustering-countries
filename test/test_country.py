from src.utils.country import list_country

def test_list_country_returns_list():
    countries = list_country()

    assert len(countries) ==167
    assert "Afghanistan" in countries
