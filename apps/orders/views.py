from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order, OrderItem, ShoppingCart, PaymentTransaction
from .serializers import OrderSerializer, ShoppingCartSerializer
from apps.catalog.models import Product, ProductVariant


# ═══════════════════════════════════════
# API Views
# ═══════════════════════════════════════

class OrderListAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailAPIView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class CartListAPIView(generics.ListCreateAPIView):
    serializer_class = ShoppingCartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ═══════════════════════════════════════
# Template Views
# ═══════════════════════════════════════

@login_required
def cart_view(request):
    cart_items = ShoppingCart.objects.filter(user=request.user).select_related('product', 'variant')
    total = sum(item.item_total for item in cart_items)
    return render(request, 'orders/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


@login_required
def add_to_cart(request, product_id):
    import json as _json
    from django.http import JsonResponse

    # If reached via GET (e.g. after login redirect with ?ajax=1),
    # just redirect cleanly to the product page or product list
    if request.method != 'POST':
        referer = request.META.get('HTTP_REFERER', '')
        product = get_object_or_404(Product, id=product_id)
        if referer and not 'ajax' in referer:
            return redirect(referer)
        try:
            return redirect('product_detail', slug=product.slug)
        except Exception:
            return redirect('product_list')

    product = get_object_or_404(Product, id=product_id)
    variant_id = request.POST.get('variant_id')
    raw_qty = int(request.POST.get('quantity', 1))
    
    # Validation: Cap the quantity to total_stock
    available_stock = product.total_stock
    
    cart_item, created = ShoppingCart.objects.get_or_create(
        user=request.user,
        product=product,
        variant_id=variant_id if variant_id else None,
        defaults={'quantity': min(max(1, raw_qty), available_stock)}
    )

    if not created:
        new_qty = cart_item.quantity + raw_qty
        if new_qty <= 0:
            cart_item.delete()
            msg = f"Mahsulot savatchadan olib tashlandi."
        else:
            cart_item.quantity = min(new_qty, available_stock)
            cart_item.save()
            msg = f"{product.product_name} savatchaga qo'shildi!" if raw_qty > 0 else ""
    else:
        msg = f"{product.product_name} savatchaga qo'shildi!"

    # AJAX request → JSON response
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.GET.get('ajax') == '1'
    if is_ajax:
        remaining = ShoppingCart.objects.filter(user=request.user, product=product, variant_id=variant_id if variant_id else None).first()
        cart_count = ShoppingCart.objects.filter(user=request.user).count()
        return JsonResponse({
            'success': True,
            'cart_count': cart_count,
            'message': msg,
            'item_id': remaining.id if remaining else None,
            'quantity': remaining.quantity if remaining else 0
        })

    # Normal form submit → redirect back
    if msg:
        messages.success(request, msg)
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'product_list'
    if next_url.startswith('/'):
        return redirect(next_url)
    return redirect('product_list')


@login_required
def remove_from_cart(request, item_id):
    from django.http import JsonResponse
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST required'}, status=405)
    
    item = get_object_or_404(ShoppingCart, id=item_id, user=request.user)
    item.delete()

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.GET.get('ajax') == '1'
    if is_ajax:
        cart_count = ShoppingCart.objects.filter(user=request.user).count()
        return JsonResponse({'success': True, 'cart_count': cart_count})

    messages.success(request, "Mahsulot savatchadan olib tashlandi.")
    return redirect('cart')


@login_required
def checkout_view(request):
    cart_items = ShoppingCart.objects.filter(user=request.user).select_related('product')
    if not cart_items.exists():
        messages.warning(request, "Savatchingiz bo'sh!")
        return redirect('cart')

    total = sum(item.item_total for item in cart_items)
    addresses = request.user.addresses.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if action == 'add_address':
            from apps.accounts.models import Address
            full_name = request.POST.get('full_name', '').strip()
            phone = request.POST.get('phone', '').strip()
            city = request.POST.get('city', '').strip()
            region = request.POST.get('region', '').strip()
            street_address = request.POST.get('street_address', '').strip()
            
            if full_name and phone and street_address:
                addr = Address.objects.create(
                    user=request.user,
                    full_name=full_name,
                    phone=phone,
                    city=city,
                    region=region,
                    street_address=street_address,
                )
                if request.user.addresses.count() == 1:
                    addr.is_default = True
                    addr.save()
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'address': {
                            'id': addr.id,
                            'full_name': addr.full_name,
                            'phone': addr.phone,
                            'city': addr.city,
                            'region': addr.region,
                            'street_address': addr.street_address,
                            'is_default': addr.is_default,
                        }
                    })
                messages.success(request, "Manzil muvaffaqiyatli saqlandi!")
            else:
                if is_ajax:
                    return JsonResponse({'success': False, 'error': "Iltimos barcha kerakli maydonlarni to'ldiring."})
                messages.error(request, "Iltimos barcha kerakli manzillarni to'ldiring.")
            return redirect('checkout')

        elif action == 'delete_address':
            address_id = request.POST.get('address_id')
            if address_id:
                from apps.accounts.models import Address
                try:
                    addr = Address.objects.get(id=address_id, user=request.user)
                    addr.delete()
                    if is_ajax:
                        return JsonResponse({'success': True, 'deleted_id': int(address_id)})
                    messages.success(request, "Manzil muvaffaqiyatli o'chirildi.")
                except Address.DoesNotExist:
                    if is_ajax:
                        return JsonResponse({'success': False, 'error': 'Manzil topilmadi.'})
                    messages.error(request, "Manzil topilmadi.")
            elif is_ajax:
                return JsonResponse({'success': False, 'error': 'address_id yo\'q.'})
            return redirect('checkout')

        # Normal checkout submission
        payment_method = request.POST.get('payment_method', 'cash')
        address_id = request.POST.get('address_id')

        if not address_id:
            messages.error(request, "Iltimos, yetkazib berish manzilini tanlang. Agar manzil qo'shilmagan bo'lsa, 'Yangi manzil' tugmasi orqali qo'shing.")
            return redirect('checkout')

        # Resolve selected address
        delivery_data = {}
        from apps.accounts.models import Address
        try:
            addr = Address.objects.get(id=address_id, user=request.user)
            delivery_data = {
                'delivery_full_name': addr.full_name,
                'delivery_phone':     addr.phone,
                'delivery_street':    addr.street_address,
                'delivery_city':      addr.city,
                'delivery_region':    getattr(addr, 'region', ''),
            }
        except Address.DoesNotExist:
            messages.error(request, "Tanlangan manzil topilmadi yoki sizga tegishli emas.")
            return redirect('checkout')

        # Create order
        order = Order.objects.create(
            user=request.user,
            subtotal=total,
            total_amount=total,
            payment_method=payment_method,
            **delivery_data,
        )

        # Create order items
        from apps.warehouse.models import Warehouse, Inventory, InventoryMovement
        main_warehouse = Warehouse.objects.filter(warehouse_name="Asosiy Ombor").first()

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                variant=item.variant,
                quantity=item.quantity,
                unit_price=item.product.current_price,
                subtotal=item.item_total,
            )
            
            # Inventory Deductions
            if main_warehouse:
                inventory = Inventory.objects.filter(product=item.product, warehouse=main_warehouse).first()
                if inventory and inventory.quantity_available > 0:
                    deduct = min(item.quantity, inventory.quantity_available)
                    inventory.quantity_available -= deduct
                    inventory.save()
                    
                    InventoryMovement.objects.create(
                        inventory=inventory,
                        movement_type='out',
                        quantity=deduct,
                        created_by=request.user,
                        reference_type=f'Order #{order.order_number}'
                    )
                    
                    if inventory.quantity_available <= 0:
                        item.product.product_status = 'out_of_stock'
                        item.product.save()

        # Clear cart
        cart_items.delete()

        # Create payment transaction
        PaymentTransaction.objects.create(
            order=order,
            payment_method=payment_method,
            amount=total,
            status='pending',
        )

        messages.success(request, f"Buyurtma #{order.order_number} muvaffaqiyatli yaratildi!")
        return redirect('order_detail', order_id=order.id)

    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'addresses': addresses,
    })


@login_required
def order_list_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'cancel_order' and order.order_status == 'pending':
            order.order_status = 'cancelled'
            order.save()
            messages.success(request, f"Buyurtma #{order.order_number} bekor qilindi.")
            return redirect('order_detail', order_id=order.id)
            
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_receipt_print(request, order_id):
    """Render a print-optimised receipt page that auto-triggers the browser
    Save-as-PDF dialog — no third-party libraries required."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    from apps.accounts.models import SiteSettings
    settings = SiteSettings.get_settings()
    return render(request, 'orders/receipt_print.html', {
        'order': order,
        'site_settings': settings,
    })
