from datetime import datetime, timezone
import pytest
from src.app import remaining_sla


def test_timezone_required():
    with pytest.raises(ValueError, match="timezone"):
        remaining_sla({"priority": "P1", "opened_at": "2026-01-01T10:00:00"}, datetime(2026, 1, 1, 11, tzinfo=timezone.utc))


def test_unknown_priority():
    with pytest.raises(ValueError, match="priority"):
        remaining_sla({"priority": "P9", "opened_at": "2026-01-01T10:00:00+00:00"}, datetime(2026, 1, 1, 11, tzinfo=timezone.utc))
