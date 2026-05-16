import uuid
from django.db import models
from django.conf import settings


class Order(models.Model):
    """Customer orders."""

    class OrderStatus(models.TextChoices):
        PENDING    = 'pending',    "Kutilmoqda"
        CONFIRMED  = 'confirmed',  "Tasdiqlandi"
        PROCESSING = 'processing', "Tayyorlanmoqda"
        SHIPPED    = 'shipped',    "Yo'lda"
        DELIVERED  = 'delivered',  "Yetkazildi"
        CANCELLED  = 'cancelled',  "Bekor qilindi"
        REFUNDED   = 'refunded',   "Qaytarildi"

    class PaymentStatus(models.TextChoices):
        PENDING  = 'pending',  "To'lanmagan"
        PAID     = 'paid',     "To'langan"
        FAILED   = 'failed',   "Xatolik"
        REFUNDED = 'refunded', "Qaytarildi"

    class OrderType(models.TextChoices):
        RETAIL = 'retail', 'Chakana'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=50, unique=True, editable=False)
    order_type = models.CharField(max_length=15, choices=OrderType.choices, default=OrderType.RETAIL)
    order_status = models.CharField(max_length=15, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    payment_status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=50, blank=True)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Delivery address snapshot (real e-commerce style — address saved at order time)
    delivery_full_name   = models.CharField(max_length=150, blank=True)
    delivery_phone       = models.CharField(max_length=30, blank=True)
    delivery_street      = models.CharField(max_length=255, blank=True)
    delivery_city        = models.CharField(max_length=100, blank=True)
    delivery_region      = models.CharField(max_length=100, blank=True)
    delivery_notes       = models.TextField(blank=True)

    # Delivery address snapshot

    # Status Timestamps
    confirmed_at = models.DateTimeField(null=True, blank=True)
    processing_at = models.DateTimeField(null=True, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"ORD-{uuid.uuid4().hex[:10].upper()}"
                    
        super().save(*args, **kwargs)


    def recalculate_paid(self):
        """Recalculate paid_amount from all completed transactions."""
        from django.db.models import Sum
        total_paid = self.transactions.filter(status='completed').aggregate(s=Sum('amount'))['s'] or 0
        self.paid_amount = total_paid
        if self.paid_amount >= self.total_amount:
            self.payment_status = 'paid'
        elif self.paid_amount > 0:
            self.payment_status = 'pending'
        self.save()

    def __str__(self):
        return f"Order {self.order_number} — {self.user.username}"


class OrderItem(models.Model):
    """Items within an order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('catalog.Product', on_delete=models.SET_NULL, null=True, related_name='order_items')
    variant = models.ForeignKey('catalog.ProductVariant', on_delete=models.SET_NULL, null=True, blank=True, related_name='order_items')
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'order_items'

    def save(self, *args, **kwargs):
        self.subtotal = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.product_name} x{self.quantity}"


class ShoppingCart(models.Model):
    """Shopping cart items."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, related_name='in_carts')
    variant = models.ForeignKey('catalog.ProductVariant', on_delete=models.SET_NULL, null=True, blank=True, related_name='in_carts')
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'shopping_cart'

    def __str__(self):
        return f"{self.user.username} — {self.product.product_name} x{self.quantity}"

    @property
    def item_total(self):
        price = self.product.current_price
        return price * self.quantity


class PaymentTransaction(models.Model):
    """Payment transaction records."""

    class TransactionStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'
        REFUNDED = 'refunded', 'Refunded'

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='transactions')
    payment_method = models.CharField(max_length=50)
    transaction_reference = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=TransactionStatus.choices, default=TransactionStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payment_transactions'

    def __str__(self):
        return f"Transaction {self.transaction_reference} — {self.amount}"


# Proxy Models for Admin Dashboard Sections
class PendingOrder(Order):
    class Meta:
        proxy = True
        verbose_name = 'Kutayotgan Buyurtma'
        verbose_name_plural = 'Kutayotgan Buyurtmalar'


class DeliveredOrder(Order):
    class Meta:
        proxy = True
        verbose_name = 'Yetkazib berilgan Buyurtma'
        verbose_name_plural = 'Yetkazib berilganlar'
