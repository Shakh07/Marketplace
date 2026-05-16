from rest_framework import serializers
from .models import Order, OrderItem, ShoppingCart, PaymentTransaction


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_name', 'variant', 'quantity', 'unit_price', 'subtotal')
        read_only_fields = ('subtotal',)


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'order_number', 'order_status', 'payment_status',
                  'subtotal', 'total_amount', 'payment_method', 'items', 'created_at')
        read_only_fields = ('order_number', 'created_at')


class ShoppingCartSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name', read_only=True)
    product_price = serializers.DecimalField(source='product.current_price', max_digits=12, decimal_places=2, read_only=True)
    item_total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ('id', 'product', 'product_name', 'product_price', 'variant', 'quantity', 'item_total', 'added_at')
        read_only_fields = ('user',)


class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = '__all__'
