from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
from apps.warehouse.models import Inventory

@receiver(post_save, sender=Inventory)
def automate_product_stock_status(sender, instance, **kwargs):
    """
    Kachonki ombordagi qoldiq o'zgarsa (Inventory modeli orqali saqlansa),
    va umumiy qoldiq 0 yoki undan kam bo'lib qolsa, mahsulot statusini 'out_of_stock' ga
    avtomatik o'zgartiradi. Agar yana qayta stok kelsa 'active' ga qaytaradi.
    """
    product = instance.product
    if product:
        total_stock = product.total_stock
        
        if total_stock <= 0:
            if product.product_status != Product.ProductStatus.OUT_OF_STOCK:
                product.product_status = Product.ProductStatus.OUT_OF_STOCK
                product.save(update_fields=['product_status'])
        else:
            # Agar omborga yangi mol kilsa va oldin 'out_of_stock' bo'lsa, aktivga qaytarish orqali avtomatlashtirish
            if product.product_status == Product.ProductStatus.OUT_OF_STOCK:
                product.product_status = Product.ProductStatus.ACTIVE
                product.save(update_fields=['product_status'])
