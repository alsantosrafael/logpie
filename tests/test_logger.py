import json
import logging
from logpie.logger import log


def test_logger_outputs_json(caplog):
    """Logger should output valid JSON with correct structure."""
    with caplog.at_level(logging.INFO):
        log.info("Test message", extra={"user": "alice"})

    record = caplog.records[0]
    parsed = json.loads(record.getMessage())
    assert parsed["level"] == "INFO"
    assert parsed["message"] == "Test message"
    assert parsed["user"] == "alice"
    assert "timestamp" in parsed


def test_logger_handles_utf8(caplog):
    """Should handle UTF-8 characters like accents."""
    with caplog.at_level(logging.INFO):
        log.info("Usuário logou")

    parsed = json.loads(caplog.records[0].getMessage())
    assert parsed["message"] == "Usuário logou"
    assert parsed["level"] == "INFO"


def test_logger_includes_request_id(caplog):
    """Extra fields should be at root level, not nested under 'extra'."""
    with caplog.at_level(logging.INFO):
        log.info("Processing request", extra={"request_id": "abc123"})

    parsed = json.loads(caplog.records[0].getMessage())
    assert parsed["request_id"] == "abc123"
    assert parsed["message"] == "Processing request"
    assert "extra" not in parsed


def test_logger_native_kwargs(caplog):
    """Should accept kwargs directly (structlog style)."""
    with caplog.at_level(logging.INFO):
        log.info("User login", user="bob", session_id="xyz789")

    parsed = json.loads(caplog.records[0].getMessage())
    assert parsed["message"] == "User login"
    assert parsed["user"] == "bob"
    assert parsed["session_id"] == "xyz789"


def test_logger_masks_sensitive_data(caplog):
    """Sensitive data should be masked automatically."""
    with caplog.at_level(logging.INFO):
        log.info("User registered", email="test@example.com", cpf="123.456.789-00")

    parsed = json.loads(caplog.records[0].getMessage())
    assert parsed["email"] == "[EMAIL_MASKED]"
    assert parsed["cpf"] == "[CPF_MASKED]"


def test_logger_different_levels(caplog, monkeypatch):
    """Should log at all levels when LOG_LEVEL=DEBUG is set."""
    import os, importlib
    from logpie import logger as logmod

    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    importlib.reload(logmod)
    _log = logmod.log

    with caplog.at_level(logging.DEBUG):
        _log.debug("Debug message")
        _log.info("Info message")
        _log.warning("Warning message")
        _log.error("Error message")

    levels = [json.loads(r.getMessage())["level"] for r in caplog.records]
    assert levels == ["DEBUG", "INFO", "WARNING", "ERROR"]
