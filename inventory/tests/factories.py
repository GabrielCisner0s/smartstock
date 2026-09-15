import factory

from inventory.models import StockMovement
from products.tests.factories import ProductFactory
from users.tests.factories import UserFactory


class StockMovementFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = StockMovement
        skip_postgeneration_save = True


    product = factory.SubFactory(
        ProductFactory
    )

    movement_type = (
        StockMovement.MovementType.ENTRY
    )

    quantity = 10

    created_by = factory.SubFactory(
        UserFactory
    )

    reason = "Carga inicial"