import pytest
from rest_framework.test import APIRequestFactory
from reports.api.views import DashboardView


def test_dashboard_view_get(monkeypatch):
    expected_data = {
        "products": 10,
        "low_stock": 3,
        "out_of_stock": 1,
    }

    def mock_get_summary():
        return expected_data

    class FakeSerializer:
        def __init__(self, data):
            self.data = {
                "products": data["products"],
                "low_stock": data["low_stock"],
                "out_of_stock": data["out_of_stock"],
            }

    monkeypatch.setattr(
        "reports.api.views.DashboardService.get_summary",
        mock_get_summary,
    )

    monkeypatch.setattr(
        "reports.api.views.DashboardSerializer",
        FakeSerializer,
    )

    factory = APIRequestFactory()
    request = factory.get("/api/reports/dashboard/")

    view = DashboardView()
    response = view.get(request)

    assert response.status_code == 200
    assert response.data == expected_data