from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from .models import Supplier, PurchaseOrder, PurchaseOrderItem


class PurchaseOrderItemInline(TabularInline):
    model = PurchaseOrderItem
    extra = 1


@admin.register(Supplier)
class SupplierAdmin(ModelAdmin):
    list_display = ('supplier_name', 'contact_person', 'email', 'phone', 'rating', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('supplier_name', 'contact_person', 'email')


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(ModelAdmin):
    list_display = ('po_number', 'supplier', 'warehouse', 'order_date', 'status', 'total_amount')
    list_filter = ('status',)
    search_fields = ('po_number', 'supplier__supplier_name')
    readonly_fields = ('created_at',)
    inlines = [PurchaseOrderItemInline]


@admin.register(PurchaseOrderItem)
class PurchaseOrderItemAdmin(ModelAdmin):
    list_display = ('purchase_order', 'product', 'variant', 'quantity_ordered', 'quantity_received', 'unit_price')
