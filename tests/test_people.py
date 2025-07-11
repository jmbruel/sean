import pytest

@pytest.mark.parametrize("person", [
    {
        "title": "Jean-Michel Bruel",
        "role": "Professor of Software Engineering",
        "organizations": [
            {"name": "University of Toulouse", "url": "http://www.univ-toulouse.fr/"},
            {"name": "IRIT Laboratory", "url": "http://www.irit.fr/"}
        ],
        "interests": [
            "Model-Based Systems Engineering",
            "Requirements Engineering"
        ],
        "social": [
            {"icon": "envelope", "icon_pack": "fas", "link": "mailto:bruel@irit.fr"},
            {"icon": "x-twitter", "icon_pack": "fab", "link": "https://twitter.com/jmbruel"}
        ]
    }
])
def test_person_valid(person):
    """Test valid person entries"""
    # Check required fields
    assert "title" in person
    assert "role" in person
    assert "organizations" in person
    
    # Validate organizations format
    for org in person["organizations"]:
        assert "name" in org
        assert "url" in org
        assert org["url"].startswith("http")
    
    # Validate social links format
    if "social" in person:
        for link in person["social"]:
            assert "icon" in link
            assert "icon_pack" in link
            assert "link" in link
            assert link["link"].startswith("http") or link["link"].startswith("mailto:")

def test_person_invalid():
    """Test invalid person entries"""
    invalid_person = {
        "title": "Missing required fields",
        "role": "Professor"
    }
    with pytest.raises(AssertionError):
        test_person_valid(invalid_person)

    invalid_org_person = {
        "title": "Invalid organization",
        "role": "Professor",
        "organizations": [{"name": "Test Org"}]
    }
    with pytest.raises(AssertionError):
        test_person_valid(invalid_org_person)

    invalid_social_person = {
        "title": "Invalid social links",
        "role": "Professor",
        "organizations": [{"name": "Test Org", "url": "http://test.org"}],
        "social": [{"icon": "twitter", "link": "invalid_url"}]
    }
    with pytest.raises(AssertionError):
        test_person_valid(invalid_social_person)
