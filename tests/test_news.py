import pytest
from datetime import datetime

@pytest.mark.parametrize("news", [
    {
        "title": "SEAN project accepted for 5 years!",
        "date": "2025-01-01",
        "image": {"focal_point": "top"},
        "content": "I am happy to share that the IRN submission has been accepted.\nThis project will run now for the next 5 years, starting on January 1st, 2025."
    },
    {
        "title": "Informatics Europe calls for more Software Engineering projects",
        "date": "2025-03-11",
        "image": {"focal_point": "top"},
        "publication": ["informaticsEurope2025"]
    }
])
def test_news_valid(news):
    """Test valid news entries"""
    # Check required fields
    assert "title" in news
    assert "date" in news
    assert "content" in news
    
    # Validate date format
    try:
        datetime.strptime(news["date"], "%Y-%m-%d")
    except ValueError:
        pytest.fail(f"Invalid date format: {news['date']}")

def test_news_invalid():
    """Test invalid news entries"""
    invalid_news = {
        "title": "Missing date",
        "content": "This news is missing a date"
    }
    with pytest.raises(AssertionError):
        test_news_valid(invalid_news)

    invalid_date_news = {
        "title": "Invalid date format",
        "date": "2025/01/01",
        "content": "This news has an invalid date format"
    }
    with pytest.raises(ValueError):
        test_news_valid(invalid_date_news)
