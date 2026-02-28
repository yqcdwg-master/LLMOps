from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response"""
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(content="Hello, how can I help you?")
        )
    ]
    return mock_response


@pytest.fixture
def app(mock_openai_response):
    """Create Flask test app"""
    # Mock OpenAI
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_openai_response

    with patch("internal.handler.app_handler.OpenAI", return_value=mock_client):
        from app.http.app import app as test_app
        test_app.config["TESTING"] = True
        yield test_app


@pytest.fixture
def client(app):
    """Create Flask test client"""
    with app.test_client() as client:
        yield client
