import pytest
from rest_framework.exceptions import ValidationError
from products.tests.factories import CategoryFactory, UserFactory
from products.services import ProductService, CategoryService


#este test verifica que se pueda crear un producto correctamente
@pytest.mark.django_db
def test_create_product():

    category = CategoryFactory()

    user = UserFactory(
        role="ADMIN"
    )

    data = {
        "sku": "ABC123",
        "name": "Notebook",
        "description": "",
        "category": category,
        "price": 1000,
        "stock": 5,
        "minimum_stock": 1,
    }

    product = ProductService.create_product(
        data,
        user
    )

    assert product.id is not None
    assert product.sku == "ABC123"
    assert product.created_by == user
    
#este test verifica que no se pueda crear un producto con un SKU duplicado
@pytest.mark.django_db
def test_create_product_rejects_duplicate_sku():

    category = CategoryFactory()

    user = UserFactory(
        role="ADMIN"
    )

    data = {
        "sku": "ABC123",
        "name": "Notebook",
        "description": "",
        "category": category,
        "price": 1000,
        "stock": 5,
        "minimum_stock": 1,
    }

    ProductService.create_product(
        data,
        user
    )

    with pytest.raises(ValidationError):
        ProductService.create_product(
            data,
            user
        )


@pytest.mark.django_db
def test_create_product_rejects_invalid_price():

    category = CategoryFactory()

    user = UserFactory(
        role="ADMIN"
    )

    data = {
        "sku": "PRICE-001",
        "name": "Producto precio inválido",
        "description": "",
        "category": category,
        "price": -100,
        "stock": 5,
        "minimum_stock": 1,
    }

    with pytest.raises(ValidationError):
        ProductService.create_product(
            data,
            user
        )

@pytest.mark.django_db
def test_create_product_rejects_invalid_stock():

    category = CategoryFactory()

    user = UserFactory(
        role="ADMIN"
    )

    data = {
        "sku": "STOCK-001",
        "name": "Producto stock inválido",
        "description": "",
        "category": category,
        "price": 1000,
        "stock": -5,
        "minimum_stock": 1,
    }

    with pytest.raises(ValidationError):
        ProductService.create_product(
            data,
            user
        )
        
        
@pytest.mark.django_db
def test_create_product_rejects_invalid_price():
    category = CategoryFactory()
    user = UserFactory()

    data = {
        "sku": "PRICE-001",
        "name": "Producto inválido",
        "description": "",
        "category": category,
        "price": -100,
        "stock": 5,
        "minimum_stock": 1,
    }

    with pytest.raises(ValidationError):
        ProductService.create_product(data, user)
        

@pytest.mark.django_db
def test_create_product_rejects_duplicate_sku():
    category = CategoryFactory()
    user = UserFactory()

    data = {
        "sku": "DUP-001",
        "name": "Primer producto",
        "description": "",
        "category": category,
        "price": 1000,
        "stock": 5,
        "minimum_stock": 1,
    }

    ProductService.create_product(data, user)

    duplicate_data = {
        "sku": "DUP-001",
        "name": "Segundo producto",
        "description": "",
        "category": category,
        "price": 2000,
        "stock": 10,
        "minimum_stock": 2,
    }

    with pytest.raises(ValidationError):
        ProductService.create_product(duplicate_data, user)
        
    
@pytest.mark.django_db
def test_update_product():
    category = CategoryFactory()
    user = UserFactory()

    data = {
        "sku": "UPD-001",
        "name": "Producto original",
        "description": "",
        "category": category,
        "price": 1000,
        "stock": 5,
        "minimum_stock": 1,
    }

    product = ProductService.create_product(data, user)

    update_data = {
        "name": "Producto actualizado",
        "price": 1500,
        "stock": 10,
    }

    updated_product = ProductService.update_product(
        product,
        update_data,
        user,
    )

    assert updated_product.name == "Producto actualizado"
    assert updated_product.price == 1500
    assert updated_product.stock == 10
    

@pytest.mark.django_db
def test_update_product_rejects_invalid_price():
    category = CategoryFactory()
    user = UserFactory()

    data = {
        "sku": "UPD-PRICE-001",
        "name": "Producto original",
        "description": "",
        "category": category,
        "price": 1000,
        "stock": 5,
        "minimum_stock": 1,
    }

    product = ProductService.create_product(data, user)

    update_data = {
        "price": -500,
    }

    with pytest.raises(ValidationError):
        ProductService.update_product(
            product,
            update_data,
            user,
        )

@pytest.mark.django_db
def test_update_product_rejects_invalid_stock():
    category = CategoryFactory()
    user = UserFactory()

    data = {
        "sku": "UPD-STOCK-001",
        "name": "Producto original",
        "description": "",
        "category": category,
        "price": 1000,
        "stock": 5,
        "minimum_stock": 1,
    }

    product = ProductService.create_product(data, user)

    update_data = {
        "stock": -10,
    }

    with pytest.raises(ValidationError):
        ProductService.update_product(
            product,
            update_data,
            user,
        )

@pytest.mark.django_db
def test_update_product_rejects_duplicate_sku():
    category = CategoryFactory()
    user = UserFactory()

    first_data = {
        "sku": "SKU-001",
        "name": "Primer producto",
        "description": "",
        "category": category,
        "price": 1000,
        "stock": 5,
        "minimum_stock": 1,
    }

    second_data = {
        "sku": "SKU-002",
        "name": "Segundo producto",
        "description": "",
        "category": category,
        "price": 2000,
        "stock": 10,
        "minimum_stock": 2,
    }

    first_product = ProductService.create_product(first_data, user)
    second_product = ProductService.create_product(second_data, user)

    update_data = {
        "sku": first_product.sku,
    }

    with pytest.raises(ValidationError):
        ProductService.update_product(
            second_product,
            update_data,
            user,
        )

@pytest.mark.django_db
def test_update_product_sets_updated_by():
    category = CategoryFactory()
    creator = UserFactory()
    updater = UserFactory()

    data = {
        "sku": "AUDIT-001",
        "name": "Producto original",
        "description": "",
        "category": category,
        "price": 1000,
        "stock": 5,
        "minimum_stock": 1,
    }

    product = ProductService.create_product(data, creator)

    update_data = {
        "name": "Producto actualizado",
    }

    updated_product = ProductService.update_product(
        product,
        update_data,
        updater,
    )

    assert updated_product.updated_by == updater
    

@pytest.mark.django_db
def test_update_product_does_not_change_created_by():
    category = CategoryFactory()
    creator = UserFactory()
    updater = UserFactory()

    data = {
        "sku": "AUDIT-002",
        "name": "Producto original",
        "description": "",
        "category": category,
        "price": 1000,
        "stock": 5,
        "minimum_stock": 1,
    }

    product = ProductService.create_product(data, creator)

    update_data = {
        "name": "Producto actualizado",
        "created_by": updater,
    }

    updated_product = ProductService.update_product(
        product,
        update_data,
        updater,
    )

    assert updated_product.created_by == creator
    
    
@pytest.mark.django_db
def test_delete_product_soft_deletes():
    category = CategoryFactory()
    user = UserFactory()

    data = {
        "sku": "DEL-001",
        "name": "Producto a eliminar",
        "description": "",
        "category": category,
        "price": 1000,
        "stock": 5,
        "minimum_stock": 1,
    }

    product = ProductService.create_product(data, user)

    ProductService.delete_product(product, user)

    product.refresh_from_db()

    assert product.is_deleted is True
    

@pytest.mark.django_db
def test_delete_product_sets_updated_by():
    category = CategoryFactory()
    creator = UserFactory()
    deleter = UserFactory()

    data = {
        "sku": "DEL-AUDIT-001",
        "name": "Producto a eliminar",
        "description": "",
        "category": category,
        "price": 1000,
        "stock": 5,
        "minimum_stock": 1,
    }

    product = ProductService.create_product(data, creator)

    ProductService.delete_product(product, deleter)

    product.refresh_from_db()

    assert product.is_deleted is True
    assert product.updated_by == deleter
    

@pytest.mark.django_db
def test_restore_product():
    category = CategoryFactory()
    user = UserFactory()

    data = {
        "sku": "RESTORE-001",
        "name": "Producto restaurable",
        "description": "",
        "category": category,
        "price": 1000,
        "stock": 5,
        "minimum_stock": 1,
    }

    product = ProductService.create_product(data, user)

    ProductService.delete_product(product, user)

    product.refresh_from_db()
    assert product.is_deleted is True

    ProductService.restore_product(product, user)

    product.refresh_from_db()

    assert product.is_deleted is False
    
@pytest.mark.django_db
def test_restore_product_sets_updated_by():
    category = CategoryFactory()
    creator = UserFactory()
    restorer = UserFactory()

    data = {
        "sku": "RESTORE-AUDIT-001",
        "name": "Producto restaurable",
        "description": "",
        "category": category,
        "price": 1000,
        "stock": 5,
        "minimum_stock": 1,
    }

    product = ProductService.create_product(data, creator)

    ProductService.delete_product(product, creator)

    product.refresh_from_db()

    assert product.is_deleted is True

    ProductService.restore_product(product, restorer)

    product.refresh_from_db()

    assert product.is_deleted is False
    assert product.updated_by == restorer
    
@pytest.mark.django_db
def test_restore_active_product():
    category = CategoryFactory()
    user = UserFactory()

    data = {
        "sku": "RESTORE-ACTIVE-001",
        "name": "Producto activo",
        "description": "",
        "category": category,
        "price": 1000,
        "stock": 5,
        "minimum_stock": 1,
    }

    product = ProductService.create_product(data, user)

    assert product.is_deleted is False

    restored_product = ProductService.restore_product(product, user)

    restored_product.refresh_from_db()

    assert restored_product.is_deleted is False
    assert restored_product.updated_by == user

@pytest.mark.django_db
def test_create_category():
    data = {
        "name": "Electrónica",
    }

    category = CategoryService.create_category(data)

    assert category.id is not None
    assert category.name == "Electrónica"
    

@pytest.mark.django_db
def test_create_category_rejects_duplicate_name():
    data = {
        "name": "Electrónica",
    }

    CategoryService.create_category(data)

    with pytest.raises(ValidationError):
        CategoryService.create_category(data)
        
        
        
@pytest.mark.django_db
def test_update_product_with_same_sku():
    category = CategoryFactory()
    user = UserFactory()

    data = {
        "sku": "SAME-SKU-001",
        "name": "Producto original",
        "description": "",
        "category": category,
        "price": 1000,
        "stock": 5,
        "minimum_stock": 1,
    }

    product = ProductService.create_product(data, user)

    update_data = {
        "sku": "SAME-SKU-001",
        "name": "Producto actualizado",
    }

    updated_product = ProductService.update_product(
        product,
        update_data,
        user,
    )

    assert updated_product.sku == "SAME-SKU-001"
    assert updated_product.name == "Producto actualizado"


@pytest.mark.django_db
def test_update_product_with_new_sku():
    category = CategoryFactory()
    user = UserFactory()

    data = {
        "sku": "OLD-SKU-001",
        "name": "Producto original",
        "description": "",
        "category": category,
        "price": 1000,
        "stock": 5,
        "minimum_stock": 1,
    }

    product = ProductService.create_product(data, user)

    update_data = {
        "sku": "NEW-SKU-001",
    }

    updated_product = ProductService.update_product(
        product,
        update_data,
        user,
    )

    assert updated_product.sku == "NEW-SKU-001"


@pytest.mark.django_db
def test_update_product_without_price_and_stock():
    category = CategoryFactory()
    user = UserFactory()

    data = {
        "sku": "NO-VALIDATION-001",
        "name": "Producto original",
        "description": "",
        "category": category,
        "price": 1000,
        "stock": 5,
        "minimum_stock": 1,
    }

    product = ProductService.create_product(data, user)

    update_data = {
        "name": "Producto actualizado",
    }

    updated_product = ProductService.update_product(
        product,
        update_data,
        user,
    )

    assert updated_product.name == "Producto actualizado"
    assert updated_product.price == 1000
    assert updated_product.stock == 5
    
