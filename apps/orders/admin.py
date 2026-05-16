from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from .models import Order, OrderItem, ShoppingCart, PaymentTransaction, PendingOrder, DeliveredOrder


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal',)


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ('order_number', 'user', 'order_status', 'payment_status', 'total_amount', 'created_at')
    list_filter = ('order_status', 'payment_status', 'payment_method')
    search_fields = ('order_number', 'user__username', 'user__email')
    readonly_fields = ('order_number', 'order_type', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    exclude = ('order_type',)


@admin.register(PendingOrder)
class PendingOrderAdmin(OrderAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(order_status='pending')


@admin.register(DeliveredOrder)
class DeliveredOrderAdmin(OrderAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(order_status='delivered')


@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    list_display = ('order', 'product', 'variant', 'quantity', 'unit_price', 'subtotal')
    readonly_fields = ('subtotal',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(ModelAdmin):
    list_display = ('user', 'product', 'variant', 'quantity', 'added_at')
    readonly_fields = ('added_at',)


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(ModelAdmin):
    list_display = ('order', 'payment_method', 'transaction_reference', 'amount', 'status', 'created_at')
    list_filter = ('status', 'payment_method')
    search_fields = ('transaction_reference',)
    readonly_fields = ('created_at',)
