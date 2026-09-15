from urllib import response

import pytest


from rest_framework.test import APIClient
from users.tests.factories import UserFactory


from products.tests.factories import (
    ProductFactory
)


@pytest.mark.django_db
def test_get_products():
   
    ProductFactory.create_batch(5)

    user = UserFactory()

    client = APIClient()

    client.force_authenticate(user=user)

    response = client.get("/api/products/")

    assert response.status_code == 200

    assert response.data["count"] == 5
    assert len(response.data["results"]) == 5


#este test verifica que la api de productos con bajo stock funciona correctamente, se crean dos productos uno con bajo stock y otro con stock suficiente, luego se hace una peticion a la api y se verifica que solo se devuelva el producto con bajo stock
@pytest.mark.django_db
def test_low_stock_products():

    
    ProductFactory(
        stock=2,
        minimum_stock=5,
    )

    ProductFactory(
        stock=20,
        minimum_stock=5,
    )

    user = UserFactory()

    client = APIClient()

    client.force_authenticate(user=user)

    response = client.get(
        "/api/products/low-stock/"
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1
    

@pytest.mark.django_db
def test_search_products_by_name():

    ProductFactory(name="Mouse Logitech")
    ProductFactory(name="Teclado Redragon")

    user = UserFactory()

    client = APIClient()

    client.force_authenticate(
        user=user
    )

    response = client.get(
        "/api/products/?search=Mouse"
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
    
    

@pytest.mark.django_db
def test_search_products_by_sku():

    ProductFactory(
        sku="MOU-001"
    )

    ProductFactory(
        sku="TEC-001"
    )

    user = UserFactory()

    client = APIClient()

    client.force_authenticate(
        user=user
    )

    response = client.get(
        "/api/products/?search=MOU-001"
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
    


@pytest.mark.django_db
def test_filter_products_by_price():

    ProductFactory(price=1000)
    ProductFactory(price=5000)
    ProductFactory(price=10000)

    user = UserFactory()

    client = APIClient()

    client.force_authenticate(
        user=user
    )

    response = client.get(
        "/api/products/?price_min=2000&price_max=6000"
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
    
    
#este test verifica que se pueden combinar los filtros de busqueda y precio, se crean tres productos, dos de ellos con el nombre "Mouse" y uno con el nombre "Teclado", luego se hace una peticion a la api filtrando por el nombre "Mouse" y un precio maximo de 5000, se espera que solo se devuelva un producto
@pytest.mark.django_db
def test_combine_search_and_price_filter():

    ProductFactory(
        name="Mouse Logitech",
        price=3000,
    )

    ProductFactory(
        name="Mouse Gamer",
        price=15000,
    )

    ProductFactory(
        name="Teclado Logitech",
        price=3000,
    )

    user = UserFactory()

    client = APIClient()

    client.force_authenticate(
        user=user
    )

    response = client.get(
        "/api/products/"
        "?search=Mouse"
        "&price_max=5000"
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
    
def test_category_list_create_perform_create(monkeypatch):
    from products.api.views import CategoryListCreateView

    serializer = type("Serializer", (), {})()
    serializer.validated_data = {
        "name": "Electrónica",
        "description": "Productos electrónicos",
    }

    called_data = {}

    def mock_create_category(**data):
        called_data.update(data)

    monkeypatch.setattr(
        "products.api.views.CategoryService.create_category",
        mock_create_category,
    )

    view = CategoryListCreateView()
    view.perform_create(serializer)

    assert called_data == {
        "name": "Electrónica",
        "description": "Productos electrónicos",
    }