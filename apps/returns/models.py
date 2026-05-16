from django.db import models
from django.conf import settings


class Return(models.Model):
    """Product returns from customers."""

    class ReturnStatus(models.TextChoices):
        REQUESTED = 'requested', 'Requested'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        RECEIVED = 'received', 'Received'
        REFUNDED = 'refunded', 'Refunded'

    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='returns')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='returns')
    return_status = models.CharField(max_length=15, choices=ReturnStatus.choices, default=ReturnStatus.REQUESTED)
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'returns'
        ordering = ['-created_at']

    def __str__(self):
        return f"Return #{self.id} — Order {self.order.order_number}"


class ReturnItem(models.Model):
    """Individual items within a return."""
    return_request = models.ForeignKey(Return, on_delete=models.CASCADE, related_name='items')
    order_item = models.ForeignKey('orders.OrderItem', on_delete=models.CASCADE, related_name='return_items')
    quantity = models.IntegerField(default=1)
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        db_table = 'return_items'

    def __str__(self):
        return f"Return item — {self.order_item} x{self.quantity}"
