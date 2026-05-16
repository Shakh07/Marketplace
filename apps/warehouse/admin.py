from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from .models import Warehouse, Inventory, InventoryMovement


@admin.register(Warehouse)
class WarehouseAdmin(ModelAdmin):
    list_display = ('warehouse_name', 'city', 'region', 'phone', 'is_active')
    list_filter = ('is_active', 'region')
    search_fields = ('warehouse_name', 'city')


@admin.register(Inventory)
class InventoryAdmin(ModelAdmin):
    list_display = ('product', 'variant', 'warehouse', 'quantity_available', 'quantity_reserved', 'quantity_damaged')
    list_filter = ('warehouse',)
    search_fields = ('product__product_name',)


@admin.register(InventoryMovement)
class InventoryMovementAdmin(ModelAdmin):
    list_display = ('inventory', 'movement_type', 'quantity', 'created_by', 'created_at')
    list_filter = ('movement_type',)
    readonly_fields = ('created_at',)
