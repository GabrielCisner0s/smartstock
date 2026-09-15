import pytest
from rest_framework import status
from core.handlers import custom_exception_handler


def test_custom_exception_handler_internal_server_error(monkeypatch):
    class DummyException(Exception):
        pass

    def mock_exception_handler(exc, context):
        return None

    monkeypatch.setattr(
        "core.handlers.exception_handler",
        mock_exception_handler,
    )

    exc = DummyException("Error interno de prueba")

    response = custom_exception_handler(exc, {})

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.data["success"] is False
    assert response.data["message"] == "Internal server error"
    assert response.data["detail"] == "Error interno de prueba"