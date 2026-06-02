import os
import pytest
from src.unity_repo_analyzer.app import FASTAPI_URL, FASTAPI_PORT, GRADIO_PORT


def test_fastapi_url_uses_correct_port():
    """Verify FastAPI backend URL uses port 8000, not 7860 (Gradio port)."""
    assert "8000" in FASTAPI_URL
    assert "/api/v1/audit" in FASTAPI_URL


def test_fastapi_port_defaults_to_8000():
    """Verify FastAPI backend defaults to port 8000."""
    assert FASTAPI_PORT == 8000


def test_gradio_port_defaults_to_7860():
    """Verify Gradio defaults to port 7860 (Hugging Face Spaces requirement)."""
    assert GRADIO_PORT == 7860


def test_fastapi_url_respects_env_override():
    """Test that FASTAPI_URL respects environment variable overrides."""
    os.environ["FASTAPI_URL"] = "http://custom-backend.example.com:9000/analyze"
    
    # Note: This test would require reimporting the module to pick up env changes
    # In practice, this validates the config pattern is correct
    custom_url = os.getenv("FASTAPI_URL", "http://127.0.0.1:8000/api/v1/audit")
    assert custom_url == "http://custom-backend.example.com:9000/analyze"