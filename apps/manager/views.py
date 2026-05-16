from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta

from apps.accounts.decorators import admin_required
from apps.orders.models import Order, OrderItem
from apps.catalog.models import Product, Category, Brand
from apps.accounts.models import CustomUser


# ─────────────────────────────────────────
#  Dashboard
# ─────────────────────────────────────────

@admin_required
def dashboard(request):
    import json
    from django.db.models.functions import TruncDay, TruncMonth

    now = timezone.now()
    ninety_days_ago = now - timedelta(days=90)
    thirty_days_ago  = now - timedelta(days=30)
    seven_days_ago   = now - timedelta(days=7)

    # ── Core Stats ──
    total_orders     = Order.objects.count()
    pending_orders   = Order.objects.filter(order_status='pending').count()
    processing_orders = Order.objects.filter(order_status__in=['confirmed','processing','shipped']).count()
    delivered_orders = Order.objects.filter(order_status='delivered').count()
    cancelled_orders = Order.objects.filter(order_status='cancelled').count()

    total_revenue = Order.objects.filter(
        order_status='delivered'
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    monthly_revenue = Order.objects.filter(
        order_status='delivered',
        created_at__gte=thirty_days_ago
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    total_customers = CustomUser.objects.filter(user_type='customer').count()
    new_customers   = CustomUser.objects.filter(
        user_type='customer', date_joined__gte=thirty_days_ago
    ).count()
    total_products  = Product.objects.filter(product_status='active').count()

    # ── Build 90-day chart data (pure Python, no pandas timezone issues) ──
    from django.db.models.functions import TruncDay
    from django.utils import timezone as tz_mod
    local_now = now.astimezone(tz_mod.get_current_timezone())

    def _day_key(dt):
        """Convert any datetime (tz-aware or naive) to local date."""
        if hasattr(dt, 'astimezone'):
            dt = dt.astimezone(tz_mod.get_current_timezone())
        return dt.date() if hasattr(dt, 'date') else dt

    # Revenue per day (delivered orders only)
    rev_by_day = {}
    for row in (Order.objects
                .filter(order_status='delivered', created_at__gte=ninety_days_ago)
                .annotate(day=TruncDay('created_at'))
                .values('day')
                .annotate(revenue=Sum('total_amount'))
                .order_by('day')):
        rev_by_day[_day_key(row['day'])] = float(row['revenue'] or 0)

    # Order count per day (all statuses)
    ord_by_day = {}
    for row in (Order.objects
                .filter(created_at__gte=ninety_days_ago)
                .annotate(day=TruncDay('created_at'))
                .values('day')
                .annotate(count=Count('id'))
                .order_by('day')):
        ord_by_day[_day_key(row['day'])] = int(row['count'] or 0)

    # Per-status order counts per day
    per_status_data = {}
    for st in ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled']:
        st_by_day = {}
        for row in (Order.objects
                    .filter(order_status=st, created_at__gte=ninety_days_ago)
                    .annotate(day=TruncDay('created_at'))
                    .values('day')
                    .annotate(count=Count('id'))
                    .order_by('day')):
            st_by_day[_day_key(row['day'])] = int(row['count'] or 0)
        per_status_data[st] = []
        for i in range(90):
            d = (local_now - timedelta(days=89 - i)).date()
            per_status_data[st].append(st_by_day.get(d, 0))

    # Build label/revenue/orders arrays for last 90 days
    chart_labels  = []
    chart_revenue = []
    chart_orders  = []
    for i in range(90):
        d = (local_now - timedelta(days=89 - i)).date()
        chart_labels.append(d.strftime('%d %b'))
        chart_revenue.append(rev_by_day.get(d, 0))
        chart_orders.append(ord_by_day.get(d, 0))




    # ── Weekly order count trend (last 8 weeks) via pandas ──
    weekly_qs = (
        Order.objects
        .filter(created_at__gte=now - timedelta(weeks=8))
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(cnt=Count('id'))
        .order_by('month')
    )
    weekly_data = {str(r['month'].date()): r['cnt'] for r in weekly_qs} if weekly_qs else {}

    # ── Order Status Breakdown (for donut chart) ──
    status_data = {
        'Kutayotgan':    pending_orders,
        'Jarayonda':     processing_orders,
        'Yetkazildi':    delivered_orders,
        'Bekor qilindi': cancelled_orders,
    }

    # ── Top Products by revenue ──
    top_products_qs = list(
        OrderItem.objects
        .values('product__product_name')
        .annotate(total=Sum('subtotal'), qty=Sum('quantity'))
        .order_by('-total')[:6]
    )
    top_product_names = [r['product__product_name'] or "Noma'lum" for r in top_products_qs]
    top_product_sales = [float(r['total'] or 0) for r in top_products_qs]

    # ── Revenue change % (vs previous 30 days) ──
    prev_revenue = Order.objects.filter(
        order_status='delivered',
        created_at__gte=thirty_days_ago - timedelta(days=30),
        created_at__lt=thirty_days_ago
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    if prev_revenue > 0:
        revenue_change = round(((monthly_revenue - prev_revenue) / prev_revenue) * 100, 1)
    else:
        revenue_change = 100.0 if monthly_revenue > 0 else 0.0

    # ── Financial Stats (Tan narxi / Sotilgan narxi / Foyda) ──
    from decimal import Decimal

    # Delivered buyurtmalar bo'yicha statistika
    delivered_items = OrderItem.objects.filter(
        order__order_status='delivered'
    ).select_related('product')

    total_selling_price = Decimal('0')  # Sotilgan narx (daromad)
    total_cost_price    = Decimal('0')  # Tan narxi (xarid narxi)

    for item in delivered_items:
        total_selling_price += Decimal(str(item.subtotal or 0))
        if item.product and item.product.cost_price:
            total_cost_price += item.product.cost_price * item.quantity

    total_profit = total_selling_price - total_cost_price

    # Oylik (so'ngi 30 kun) moliyaviy statistika
    monthly_items = OrderItem.objects.filter(
        order__order_status='delivered',
        order__created_at__gte=thirty_days_ago
    ).select_related('product')

    monthly_selling = Decimal('0')
    monthly_cost    = Decimal('0')

    for item in monthly_items:
        monthly_selling += Decimal(str(item.subtotal or 0))
        if item.product and item.product.cost_price:
            monthly_cost += item.product.cost_price * item.quantity

    monthly_profit = monthly_selling - monthly_cost
    profit_margin = round((float(monthly_profit) / float(monthly_selling) * 100), 1) if monthly_selling > 0 else 0

    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:8]

    context = {
        'today':             now,
        'total_orders':      total_orders,
        'pending_orders':    pending_orders,
        'processing_orders': processing_orders,
        'delivered_orders':  delivered_orders,
        'cancelled_orders':  cancelled_orders,
        'total_revenue':     total_revenue,
        'monthly_revenue':   monthly_revenue,
        'revenue_change':    revenue_change,
        'total_customers':   total_customers,
        'new_customers':     new_customers,
        'total_products':    total_products,
        'recent_orders':     recent_orders,
        # Financial stats
        'total_selling_price': total_selling_price,
        'total_cost_price':    total_cost_price,
        'total_profit':        total_profit,
        'monthly_selling':     monthly_selling,
        'monthly_cost':        monthly_cost,
        'monthly_profit':      monthly_profit,
        'profit_margin':       profit_margin,
        # Chart data (JSON)
        'chart_labels':       json.dumps(chart_labels),
        'chart_revenue':      json.dumps(chart_revenue),
        'chart_orders':       json.dumps(chart_orders),
        'status_data_labels': json.dumps(list(status_data.keys())),
        'status_data_values': json.dumps(list(status_data.values())),
        'top_product_names':  json.dumps(top_product_names),
        'top_product_sales':  json.dumps(top_product_sales),
        'per_status_data':    json.dumps(per_status_data),
    }
    return render(request, 'manager/dashboard.html', context)



# ─────────────────────────────────────────
#  Orders
# ─────────────────────────────────────────

@admin_required
def order_list(request):
    status_filter = request.GET.get('status', '')
    query = request.GET.get('q', '').strip()
    orders = Order.objects.filter(order_type='retail').select_related('user').order_by('-created_at')

    if status_filter:
        orders = orders.filter(order_status=status_filter)
        
    if query:
        orders = orders.filter(
            Q(order_number__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__phone__icontains=query) |
            Q(delivery_phone__icontains=query) |
            Q(delivery_full_name__icontains=query)
        ).distinct()

    retail_orders = Order.objects.filter(order_type='retail')
    status_counts = {
        'all': retail_orders.count(),
        'pending': retail_orders.filter(order_status='pending').count(),
        'confirmed': retail_orders.filter(order_status='confirmed').count(),
        'processing': retail_orders.filter(order_status='processing').count(),
        'shipped': retail_orders.filter(order_status='shipped').count(),
        'delivered': retail_orders.filter(order_status='delivered').count(),
        'cancelled': retail_orders.filter(order_status='cancelled').count(),
    }

    context = {
        'orders': orders,
        'status_filter': status_filter,
        'status_counts': status_counts,
        'search_query': query,
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        from django.template.loader import render_to_string
        from django.http import JsonResponse
        html = render_to_string('manager/order_list_partial.html', context, request=request)
        return JsonResponse({'html': html, 'status_filter': status_filter})

    return render(request, 'manager/order_list.html', context)


@admin_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_statuses = [
        ('pending',    'Kutayotgan'),
        ('confirmed',  'Tasdiqlangan'),
        ('processing', 'Tayyorlanmoqda'),
        ('shipped',    'Yo\'lga chiqdi'),
        ('delivered',  'Yetkazildi'),
        ('cancelled',  'Bekor qilingan'),
        ('refunded',   'Qaytarildi'),
    ]

    return render(request, 'manager/order_detail.html', {
        'order': order,
        'order_statuses': order_statuses,
    })


@admin_required
def order_update_status(request, order_id):
    if request.method != 'POST':
        return redirect('manager_order_detail', order_id=order_id)

    from django.http import JsonResponse

    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')

    STATUS_LABELS = {
        'pending':    'Kutayotgan',
        'confirmed':  'Tasdiqlangan',
        'processing': 'Tayyorlanmoqda',
        'shipped':    "Yo'lga chiqdi",
        'delivered':  'Yetkazildi',
        'cancelled':  'Bekor qilingan',
        'refunded':   'Qaytarildi',
    }

    valid_statuses = list(STATUS_LABELS.keys())
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if new_status in valid_statuses:
        old_status = order.order_status
        order.order_status = new_status

        # Auto-update timestamps — always set to current time
        now = timezone.now()
        if new_status == 'confirmed':   order.confirmed_at  = now
        if new_status == 'processing':  order.processing_at = now
        if new_status == 'shipped':     order.shipped_at    = now
        if new_status == 'delivered':   order.delivered_at  = now
        if new_status == 'cancelled':   order.cancelled_at  = now
        if new_status == 'refunded':    order.cancelled_at  = now

        # Auto-update payment status when delivered
        if new_status == 'delivered' and order.payment_method == 'cash':
            order.payment_status = 'paid'

        order.save()

        if is_ajax:
            from django.template.loader import render_to_string
            order_statuses = [
                ('pending',    'Kutayotgan'),
                ('confirmed',  'Tasdiqlangan'),
                ('processing', 'Tayyorlanmoqda'),
                ('shipped',    "Yo'lga chiqdi"),
                ('delivered',  'Yetkazildi'),
                ('cancelled',  'Bekor qilingan'),
                ('refunded',   'Qaytarildi'),
            ]
            stepper_html = render_to_string('manager/order_stepper_partial.html', {'order': order, 'order_statuses': order_statuses}, request=request)
            return JsonResponse({
                'success': True,
                'new_status': new_status,
                'new_status_label': STATUS_LABELS[new_status],
                'old_status': old_status,
                'stepper_html': stepper_html,
            })

        messages.success(request, f"Buyurtma #{order.order_number}: {STATUS_LABELS.get(old_status, old_status)} → {STATUS_LABELS[new_status]}")
    else:
        if is_ajax:
            return JsonResponse({'success': False, 'error': "Noto'g'ri status."})
        messages.error(request, "Noto'g'ri status.")

    return redirect('manager_order_detail', order_id=order_id)




@admin_required
def order_update_address(request, order_id):
    if request.method != 'POST':
        return redirect('manager_order_detail', order_id=order_id)

    from django.http import JsonResponse
    order = get_object_or_404(Order, id=order_id)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    # Update fields
    order.delivery_full_name = request.POST.get('full_name', order.delivery_full_name)
    order.delivery_phone = request.POST.get('phone', order.delivery_phone)
    order.delivery_street = request.POST.get('street', order.delivery_street)
    order.delivery_city = request.POST.get('city', order.delivery_city)
    order.delivery_region = request.POST.get('region', order.delivery_region)
    order.delivery_notes = request.POST.get('notes', order.delivery_notes)

    order.save()

    if is_ajax:
        return JsonResponse({
            'success': True,
            'full_name': order.delivery_full_name,
            'phone': order.delivery_phone,
            'street': order.delivery_street,
            'city': order.delivery_city,
            'region': order.delivery_region,
            'notes': order.delivery_notes,
        })

    messages.success(request, "Manzil ma'lumotlari yangilandi.")
    return redirect('manager_order_detail', order_id=order_id)


# ─────────────────────────────────────────
#  Products
# ─────────────────────────────────────────

@admin_required
def product_list(request):
    query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')

    products = Product.objects.select_related('brand', 'category').order_by('-product_status', '-created_at')

    if query:
        products = products.filter(product_name__icontains=query)
    if category_filter:
        products = products.filter(category__slug=category_filter)

    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'category_filter': category_filter,
        'total_products': products.count(),
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        from django.template.loader import render_to_string
        from django.http import JsonResponse
        html = render_to_string('manager/product_list_partial.html', context, request=request)
        return JsonResponse({'html': html, 'total_products': context['total_products']})
        
    return render(request, 'manager/product_list.html', context)


@admin_required
def product_toggle_active(request, product_id):
    from django.http import JsonResponse
    product = get_object_or_404(Product, id=product_id)
    if product.product_status == 'active':
        product.product_status = 'discontinued'
        new_label = 'Nofaol'
        btn_label = 'Faollashtirish'
        btn_color = '#34c759'
        pill_bg = 'rgba(0,0,0,0.06)'
        pill_color = '#48484a'
    else:
        product.product_status = 'active'
        new_label = 'Faol'
        btn_label = "O'chirish"
        btn_color = '#ff3b30'
        pill_bg = 'rgba(52,199,89,0.12)'
        pill_color = '#15803d'
    product.save()

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        return JsonResponse({
            'success': True,
            'new_status': product.product_status,
            'new_label': new_label,
            'btn_label': btn_label,
            'btn_color': btn_color,
            'pill_bg': pill_bg,
            'pill_color': pill_color,
        })

    messages.success(request, f"'{product.product_name}' {new_label.lower()} qilindi.")
    return redirect('manager_product_list')

from .forms import ProductForm
from apps.catalog.models import ProductImage, ProductVariant
from apps.warehouse.models import Warehouse, Inventory, InventoryMovement
from django.utils.text import slugify

@admin_required
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            if not product.slug:
                product.slug = slugify(product.product_name)
            product.save()
            
            image_file = request.FILES.get('image')
            if image_file:
                ProductImage.objects.create(
                    product=product,
                    image_url=image_file,
                    is_primary=True
                )
                
            gallery_images = request.FILES.getlist('gallery_images')
            for g_img in gallery_images:
                ProductImage.objects.create(
                    product=product,
                    image_url=g_img,
                    is_primary=False
                )
                
            # Handle Variants
            v_names = request.POST.getlist('variant_name[]')
            v_prices = request.POST.getlist('variant_price[]')
            v_stocks = request.POST.getlist('variant_stock[]')
            for i, (name, price, stock) in enumerate(zip(v_names, v_prices, v_stocks)):
                if name.strip():
                    variant = ProductVariant.objects.create(
                        product=product,
                        variant_name=name.strip(),
                        price_adjustment=price if price else 0,
                        stock_quantity=stock if stock else 0
                    )
                    
                    # Save variant-specific images
                    v_images = request.FILES.getlist(f'variant_images_{i}')
                    for v_img in v_images:
                        ProductImage.objects.create(
                            product=product,
                            variant=variant,
                            image_url=v_img,
                            is_primary=False
                        )
                
            # Handle Inventory
            stock_qty = form.cleaned_data.get('initial_stock', 0)
            if stock_qty > 0:
                warehouse, _ = Warehouse.objects.get_or_create(
                    warehouse_name="Asosiy Ombor",
                    defaults={'is_active': True}
                )
                inventory = Inventory.objects.create(
                    product=product,
                    warehouse=warehouse,
                    quantity_available=stock_qty
                )
                InventoryMovement.objects.create(
                    inventory=inventory,
                    movement_type='in',
                    quantity=stock_qty,
                    created_by=request.user,
                    reference_type='Initial Stock'
                )

            messages.success(request, f"'{product.product_name}' muvaffaqiyatli markazga qo'shildi.")
            return redirect('manager_product_list')
    else:
        form = ProductForm()
    
    return render(request, 'manager/product_form.html', {
        'form': form,
        'title': 'Yangi Mahsulot',
        'is_edit': False
    })

@admin_required
def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Pre-fill stock if it exists
    main_warehouse = Warehouse.objects.filter(warehouse_name="Asosiy Ombor").first()
    inventory = Inventory.objects.filter(product=product, warehouse=main_warehouse).first() if main_warehouse else None
    current_stock = inventory.quantity_available if inventory else 0

    gallery_images = product.images.filter(is_primary=False, variant__isnull=True)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            
            image_file = request.FILES.get('image')
            if image_file:
                old_img = product.images.filter(is_primary=True).first()
                if old_img:
                    old_img.delete()
                
                ProductImage.objects.create(
                    product=product,
                    image_url=image_file,
                    is_primary=True
                )
            
            # Delete selected gallery images
            deleted_ids = request.POST.getlist('delete_gallery_images')
            if deleted_ids:
                product.images.filter(id__in=deleted_ids).delete()
                
            # Add new gallery images
            new_gallery_images = request.FILES.getlist('gallery_images')
            for g_img in new_gallery_images:
                ProductImage.objects.create(
                    product=product,
                    image_url=g_img,
                    is_primary=False
                )
            
            # Delete selected variant images
            deleted_v_ids = request.POST.getlist('delete_variant_image[]')
            if deleted_v_ids:
                ProductImage.objects.filter(id__in=deleted_v_ids).delete()

            # Handle Variants Updates
            v_ids = request.POST.getlist('variant_id[]')
            v_names = request.POST.getlist('variant_name[]')
            v_prices = request.POST.getlist('variant_price[]')
            v_stocks = request.POST.getlist('variant_stock[]')
            
            kept_variant_ids = set()
            for i, (vid, name, price, stock) in enumerate(zip(v_ids, v_names, v_prices, v_stocks)):
                name = name.strip()
                if not name: continue
                p_adj = price if price else 0
                s_qty = stock if stock else 0
                
                variant = None
                if vid and vid != 'new':
                    try:
                        variant = ProductVariant.objects.get(id=vid, product=product)
                        variant.variant_name = name
                        variant.price_adjustment = p_adj
                        variant.stock_quantity = s_qty
                        variant.save()
                        kept_variant_ids.add(variant.id)
                    except ProductVariant.DoesNotExist:
                        pass
                else:
                    variant = ProductVariant.objects.create(
                        product=product,
                        variant_name=name,
                        price_adjustment=p_adj,
                        stock_quantity=s_qty
                    )
                    kept_variant_ids.add(variant.id)
                
                # Handle new images for this variant (both for existing and new variants)
                if variant:
                    v_images = request.FILES.getlist(f'variant_images_{i}')
                    for v_img in v_images:
                        ProductImage.objects.create(
                            product=product,
                            variant=variant,
                            image_url=v_img,
                            is_primary=False
                        )
            
            # Delete removed variants
            product.variants.exclude(id__in=kept_variant_ids).delete()
                
            # Handle Inventory Updates
            new_stock = form.cleaned_data.get('initial_stock', 0)
            if new_stock != current_stock:
                if not main_warehouse:
                    main_warehouse, _ = Warehouse.objects.get_or_create(warehouse_name="Asosiy Ombor", defaults={'is_active': True})
                
                if not inventory:
                    inventory = Inventory.objects.create(product=product, warehouse=main_warehouse, quantity_available=0)
                
                difference = new_stock - inventory.quantity_available
                inventory.quantity_available = new_stock
                inventory.save()
                
                movement_type = 'in' if difference > 0 else 'out'
                if current_stock > 0 and difference != current_stock:
                    movement_type = 'adjustment'
                    
                InventoryMovement.objects.create(
                    inventory=inventory,
                    movement_type=movement_type,
                    quantity=abs(difference),
                    created_by=request.user,
                    reference_type='Manual Edit'
                )

            messages.success(request, f"'{product.product_name}' haqida ma'lumotlar saqlandi.")
            return redirect('manager_product_list')
    else:
        form = ProductForm(instance=product, initial={'initial_stock': current_stock})
    
    primary_image = product.images.filter(is_primary=True).first()
    
    return render(request, 'manager/product_form.html', {
        'form': form,
        'product': product,
        'primary_image': primary_image,
        'gallery_images': gallery_images,
        'variants': product.variants.all(),
        'title': f"{product.product_name} tahrirlash",
        'is_edit': True
    })


# ─────────────────────────────────────────
#  Users
# ─────────────────────────────────────────

@admin_required
def user_list(request):
    user_type_filter = request.GET.get('type', '')
    query = request.GET.get('q', '')

    users = CustomUser.objects.order_by('-date_joined')

    if user_type_filter:
        users = users.filter(user_type=user_type_filter)
    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )

    # Counts (Dynamic based on search)
    count_qs = CustomUser.objects.all()
    if query:
        count_qs = count_qs.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )

    user_counts = {
        'all': count_qs.count(),
        'customer': count_qs.filter(user_type='customer').count(),
        'seller': count_qs.filter(user_type='seller').count(),
        'admin': count_qs.filter(user_type='admin').count(),
    }

    context = {
        'users': users,
        'user_type_filter': user_type_filter,
        'query': query,
        'user_counts': user_counts,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        from django.template.loader import render_to_string
        from django.http import JsonResponse
        html = render_to_string('manager/user_list_rows.html', context, request=request)
        return JsonResponse({
            'html': html,
            'user_counts': user_counts
        })

    return render(request, 'manager/user_list.html', context)


@admin_required
def user_detail(request, user_id):
    from django.db.models import Sum, Count
    from apps.orders.models import Order
    
    user = get_object_or_404(CustomUser, id=user_id)
    addresses = user.addresses.all()
    
    # User's orders
    user_orders = Order.objects.filter(user=user).order_by('-created_at')
    
    # Quick statistics
    total_orders = user_orders.count()
    completed_orders = user_orders.filter(order_status='delivered').count()
    total_spent = user_orders.filter(order_status='delivered').aggregate(total=Sum('total_amount'))['total'] or 0
    cancelled_orders = user_orders.filter(order_status__in=['cancelled', 'refunded']).count()
    
    context = {
        'target_user': user,
        'addresses': addresses,
        'user_orders': user_orders[:10], # Show up to 10 recent orders
        'total_orders': total_orders,
        'completed_orders': completed_orders,
        'total_spent': total_spent,
        'cancelled_orders': cancelled_orders,
    }
    
    return render(request, 'manager/user_detail.html', context)


@admin_required
def user_toggle_status(request, user_id):
    from django.http import JsonResponse
    user = get_object_or_404(CustomUser, id=user_id)
    if user.account_status == 'active':
        user.account_status = 'suspended'
        msg = f"'{user.username}' bloklandi."
        pill_txt = 'Bloklangan'
        pill_bg = 'rgba(255,59,48,0.1)'
        pill_color = '#ff3b30'
        btn_txt = 'Faollash'
        btn_bg = 'rgba(52,199,89,0.12)'
        btn_color = '#15803d'
    else:
        user.account_status = 'active'
        msg = f"'{user.username}' faollashtirildi."
        pill_txt = 'Faol'
        pill_bg = 'rgba(52,199,89,0.12)'
        pill_color = '#15803d'
        btn_txt = 'Bloklash'
        btn_bg = 'rgba(255,59,48,0.1)'
        btn_color = '#ff3b30'
    user.save()

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        return JsonResponse({
            'success': True,
            'message': msg,
            'pill_txt': pill_txt,
            'pill_bg': pill_bg,
            'pill_color': pill_color,
            'btn_txt': btn_txt,
            'btn_bg': btn_bg,
            'btn_color': btn_color,
        })

    messages.success(request, msg)
    return redirect('manager_user_list')


# ─────────────────────────────────────────
#  Warehouse & Inventory
# ─────────────────────────────────────────

@admin_required
def inventory_list(request):
    query = request.GET.get('q', '').strip()
    stock_status = request.GET.get('status', 'all')
    inventory_items = Inventory.objects.select_related('product', 'warehouse', 'variant', 'product__category').order_by('product__product_name')
    
    if query:
        inventory_items = inventory_items.filter(
            Q(product__product_name__icontains=query) |
            Q(product__sku__icontains=query) |
            Q(variant__sku__icontains=query) |
            Q(variant__variant_name__icontains=query)
        ).distinct()

    if stock_status == 'low':
        inventory_items = inventory_items.filter(quantity_available__gt=0, quantity_available__lte=5)
    elif stock_status == 'out':
        inventory_items = inventory_items.filter(quantity_available__lte=0)

    # Calculate filtered stats for the top cards
    current_out_of_stock = inventory_items.filter(quantity_available__lte=0).count()
    current_low_stock = inventory_items.filter(quantity_available__gt=0, quantity_available__lte=5).count()
    current_products_count = inventory_items.values('product').distinct().count()
    
    # Calculate Total Inventory Value and individual item totals
    total_inventory_value = 0
    for item in inventory_items:
        price = item.product.base_price
        if item.variant:
            price += item.variant.price_adjustment
        
        item.current_price = price
        item.row_total = price * item.quantity_available if item.quantity_available > 0 else 0
        
        # Formatted versions for template
        item.current_price_formatted = f"{int(price):,}".replace(",", " ")
        item.row_total_formatted = f"{int(item.row_total):,}".replace(",", " ")
        
        if item.quantity_available > 0:
            total_inventory_value += item.row_total

    # Format values for display (e.g. 1 125 330 000)
    total_inventory_value_formatted = f"{int(total_inventory_value):,}".replace(",", " ")
    
    context = {
        'inventory_items': inventory_items,
        'total_products': current_products_count,
        'out_of_stock_count': current_out_of_stock,
        'low_stock_count': current_low_stock,
        'total_inventory_value': total_inventory_value,
        'total_inventory_value_formatted': total_inventory_value_formatted,
        'search_query': query,
        'current_status': stock_status,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        from django.template.loader import render_to_string
        from django.http import JsonResponse
        html = render_to_string('manager/inventory_list_partial.html', context, request=request)
        return JsonResponse({
            'html': html,
            'metrics': {
                'total_products': current_products_count,
                'total_value': total_inventory_value_formatted,
                'low_stock': current_low_stock,
                'out_stock': current_out_of_stock
            }
        })

    return render(request, 'manager/inventory_list.html', context)


# ─────────────────────────────────────────
#  Storefront & CMS (Hero and Categories)
# ─────────────────────────────────────────

@admin_required
def storefront_settings(request):
    import logging, traceback
    logger = logging.getLogger(__name__)
    from apps.catalog.models import HeroSection
    from apps.accounts.models import SiteSettings
    from .forms import HeroSectionForm, SiteSettingsForm

    hero = HeroSection.get_instance()
    site_settings = SiteSettings.get_settings()

    if request.method == 'POST':
        hero_form = HeroSectionForm(request.POST, request.FILES, instance=hero, prefix='hero')
        site_form = SiteSettingsForm(request.POST, instance=site_settings, prefix='site')

        try:
            if hero_form.is_valid() and site_form.is_valid():
                hero_form.save()
                site_form.save()
                messages.success(request, "Sayt sozlamalari muvaffaqiyatli saqlandi.")
                return redirect('manager_storefront')
            else:
                logger.error(f"Storefront form errors - hero: {hero_form.errors}, site: {site_form.errors}")
        except Exception as e:
            logger.error(f"Storefront POST error: {e}\n{traceback.format_exc()}")
            messages.error(request, f"Xatolik: {str(e)}")
    else:
        hero_form = HeroSectionForm(instance=hero, prefix='hero')
        site_form = SiteSettingsForm(instance=site_settings, prefix='site')

    return render(request, 'manager/storefront_settings.html', {
        'hero_form': hero_form,
        'site_form': site_form,
        'hero': hero,
        'site_settings': site_settings
    })


@admin_required
def category_list(request):
    from apps.catalog.models import Category
    categories = Category.objects.all().order_by('category_name')
    return render(request, 'manager/category_list.html', {'categories': categories})


@admin_required
def category_add(request):
    from .forms import CategoryForm
    from django.utils.text import slugify
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            cat = form.save(commit=False)
            if not cat.slug:
                cat.slug = slugify(cat.category_name)
            cat.save()
            messages.success(request, "Yangi kategoriya qo'shildi.")
            return redirect('manager_category_list')
    else:
        form = CategoryForm()
        
    return render(request, 'manager/category_form.html', {'form': form, 'is_edit': False})


@admin_required
def category_edit(request, category_id):
    from apps.catalog.models import Category
    from .forms import CategoryForm
    
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Kategoriya ma'lumotlari yangilandi.")
            return redirect('manager_category_list')
    else:
        form = CategoryForm(instance=category)
        
    return render(request, 'manager/category_form.html', {'form': form, 'category': category, 'is_edit': True})

@admin_required
def brand_list(request):
    from apps.catalog.models import Brand
    brands = Brand.objects.all().order_by('brand_name')
    return render(request, 'manager/brand_list.html', {'brands': brands})

@admin_required
def brand_add(request):
    from .forms import BrandForm
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Yangi brend qo'shildi.")
            return redirect('manager_brand_list')
    else:
        form = BrandForm()
    return render(request, 'manager/brand_form.html', {'form': form, 'is_edit': False})

@admin_required
def brand_edit(request, brand_id):
    from apps.catalog.models import Brand
    from .forms import BrandForm
    brand = get_object_or_404(Brand, id=brand_id)
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES, instance=brand)
        if form.is_valid():
            form.save()
            messages.success(request, "Brend ma'lumotlari yangilandi.")
            return redirect('manager_brand_list')
    else:
        form = BrandForm(instance=brand)
        for item in order.items.all():
            if item.variant:
                inventory_obj = item.variant.inventory.first()
            else:
                inventory_obj = item.product.inventory.first()
                
            if inventory_obj:
                inventory_obj.quantity_available += item.quantity
                inventory_obj.save()
                InventoryMovement.objects.create(
                    inventory=inventory_obj,
                    movement_type='return',
                    quantity=item.quantity,
                    reference_type='order_delete',
                    reference_id=order.id,
                    created_by=request.user,
                    notes="Nasiya o'chirildi, tovar zaxiraga qaytdi"
                )
        
        order.delete()
        messages.success(request, "Nasiya muvaffaqiyatli o'chirildi (Tovar zaxiraga qaytdi).")
        
    return redirect('manager_credit_list')
