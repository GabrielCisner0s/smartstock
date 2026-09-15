import factory

from users.models import CustomUser
from products.models import Category, Product

#clase para crear usuarios de prueba, se puede usar en los tests para crear productos con usuarios asociados
class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = CustomUser
        skip_postgeneration_save = True

    email = factory.Sequence(lambda n: f"user{n}@test.com")
    username = factory.Sequence(lambda n: f"user{n}")

    first_name = "Gabriel"
    last_name = "Cisneros"

    role = CustomUser.Role.ADMIN

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        password = extracted or "Password123!"
        self.set_password(password)
        if create:
            self.save()

#esta clase es para crear categorias de prueba, se puede usar en los tests para crear productos con categorias asociadas
class CategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Categoría {n}")
    description = "Categoría de prueba"


class ProductFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Product

    sku = factory.Sequence(lambda n: f"SKU-{n}")
    name = factory.Sequence(lambda n: f"Producto {n}")

    description = "Producto de prueba"

    category = factory.SubFactory(CategoryFactory)

    price = 100

    stock = 10

    minimum_stock = 2