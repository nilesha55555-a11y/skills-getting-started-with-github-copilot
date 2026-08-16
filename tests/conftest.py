from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activity store before each test."""
    original_activities = deepcopy(activities)

    activities.clear()
    activities.update(deepcopy(original_activities))

    yield

    activities.clear()
    activities.update(deepcopy(original_activities))


@pytest.fixture
def client():
    """Provide a test client for FastAPI requests."""
    return TestClient(app)
