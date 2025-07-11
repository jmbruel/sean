import pytest
from datetime import datetime

@pytest.mark.parametrize("event", [
    {
        "title": "Journées des correspondantes et correspondants Europe",
        "event": "INS2I",
        "location": "Paris, France",
        "date": "2025-04-16T09:00:00Z",
        "date_end": "2025-04-17T17:00:00Z",
        "all_day": True,
        "url_pdf": "programme.pdf"
    }
])
def test_event_valid(event):
    """Test valid event entries"""
    # Check required fields
    assert "title" in event
    assert "event" in event
    assert "date" in event
    
    # Validate date format
    try:
        datetime.fromisoformat(event["date"])
        if "date_end" in event:
            datetime.fromisoformat(event["date_end"])
    except ValueError:
        pytest.fail(f"Invalid date format in event: {event}")

def test_event_invalid():
    """Test invalid event entries"""
    invalid_event = {
        "title": "Missing required fields",
        "date": "2025-04-16T09:00:00Z"
    }
    with pytest.raises(AssertionError):
        test_event_valid(invalid_event)

    invalid_date_event = {
        "title": "Invalid date format",
        "event": "Test Event",
        "date": "2025/04/16 09:00:00"
    }
    with pytest.raises(ValueError):
        test_event_valid(invalid_date_event)
