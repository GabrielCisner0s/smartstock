from reports.services import DashboardService


def test_get_summary(monkeypatch):
    class FakeQuerySet:
        def __init__(self, count):
            self._count = count

        def count(self):
            return self._count

    class FakeManager:
        def __init__(self, counts):
            self.counts = counts
            self.calls = []

        def filter(self, **kwargs):
            self.calls.append(kwargs)
            return FakeQuerySet(self.counts[len(self.calls) - 1])

    product_manager = FakeManager(
        [
            10,  # total_products
            3,   # low_stock_products
            7,   # active_products
        ]
    )

    movement_manager = FakeManager(
        [
            5,  # entries_today
            2,  # exits_today
        ]
    )

    monkeypatch.setattr(
        "reports.services.Product.objects",
        product_manager,
    )

    monkeypatch.setattr(
        "reports.services.StockMovement.objects",
        movement_manager,
    )

    result = DashboardService.get_summary()

    assert result == {
        "total_products": 10,
        "low_stock_products": 3,
        "active_products": 7,
        "entries_today": 5,
        "exits_today": 2,
    }

    assert product_manager.calls[0] == {
        "is_deleted": False,
    }

    assert product_manager.calls[1] == {
        "stock__lte": 0,
    }

    assert product_manager.calls[2] == {
        "is_deleted": False,
        "status": "ACTIVE",
    }

    assert movement_manager.calls[0]["movement_type"] == "ENTRY"
    assert movement_manager.calls[1]["movement_type"] == "EXIT"