from django.db import models
from django.conf import settings


class Warehouse(models.Model):
    """Physical warehouses for inventory storage."""
    warehouse_name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    region = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'warehouses'

    def __str__(self):
        return self.warehouse_name


class Inventory(models.Model):
    """Inventory tracking per product/variant/warehouse."""
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, related_name='inventory')
    variant = models.ForeignKey('catalog.ProductVariant', on_delete=models.SET_NULL, null=True, blank=True, related_name='inventory')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='inventory')
    quantity_available = models.IntegerField(default=0)
    quantity_reserved = models.IntegerField(default=0)
    quantity_damaged = models.IntegerField(default=0)
    last_restock_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'inventory'
        verbose_name_plural = 'Inventory'

    def __str__(self):
        return f"{self.product.product_name} @ {self.warehouse.warehouse_name} — {self.quantity_available}"


class InventoryMovement(models.Model):
    """Tracks inventory movements (in, out, adjustment, return, damage)."""

    class MovementType(models.TextChoices):
        IN = 'in', 'In'
        OUT = 'out', 'Out'
        ADJUSTMENT = 'adjustment', 'Adjustment'
        RETURN = 'return', 'Return'
        DAMAGE = 'damage', 'Damage'

    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=15, choices=MovementType.choices)
    quantity = models.IntegerField()
    reference_type = models.CharField(max_length=50, blank=True)
    reference_id = models.IntegerField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='inventory_movements')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inventory_movements'

    def __str__(self):
        return f"{self.movement_type} — {self.quantity} units"
