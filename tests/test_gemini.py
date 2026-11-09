
from types import SimpleNamespace

import pytest

from ai import gemini_service


def test_generate_ai_response(monkeypatch):
    """Test Gemini response without making an API request."""

    def mock_generate_content(**kwargs):
        assert kwargs["model"] == gemini_service.MODEL
        assert kwargs["input"] == "Explain MCP"

        return SimpleNamespace(
            output_text="MCP connects AI applications with external tools."
        )

    monkeypatch.setattr(
        gemini_service.client.interactions,
        "create",
        mock_generate_content
    )

    result = gemini_service.generate_ai_response("Explain MCP")

    assert "MCP connects AI applications" in result


def test_empty_prompt():
    """Verify empty prompts are rejected."""

    with pytest.raises(ValueError):
        gemini_service.generate_ai_response("   ")


def test_oversized_prompt():
    """Verify oversized prompts are rejected."""

    with pytest.raises(ValueError):
        gemini_service.generate_ai_response("A" * 30001)
