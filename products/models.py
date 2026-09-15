from django.core.validators import MinValueValidator
from decimal import Decimal

from django.db import models
from django.conf import settings

class Category(models.Model):
    
    name = models.CharField(max_length=100, unique=True)
    
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        
        verbose_name = "Categoría"
        
        verbose_name_plural = "Categorías"

        ordering = ["name"]

        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name





class Product(models.Model):

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Activo"
        INACTIVE = "INACTIVE", "Inactivo"
    
    sku = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    is_deleted = models.BooleanField(default=False)
    
    
    
    
    
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
        MinValueValidator(Decimal("0.01"))
    ],
    )

    stock = models.PositiveIntegerField(default=0)

    minimum_stock = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    # Auditoría
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_products"
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="updated_products"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
