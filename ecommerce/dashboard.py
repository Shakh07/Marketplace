from django.utils.translation import gettext_lazy as _

def dashboard_callback(request, context):
    """
    Callback to provide custom context data to Unfold's dashboard.
    """
    from apps.orders.models import Order
    from apps.accounts.models import CustomUser
    from django.db.models import Sum
    from datetime import timedelta
    from django.utils import timezone

    now = timezone.now()
    thirty_days_ago = now - timedelta(days=30)
    
    # Calculate simple stats
    total_revenue = Order.objects.filter(order_status='delivered').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    recent_orders_count = Order.objects.filter(created_at__gte=thirty_days_ago).count()
    total_users = CustomUser.objects.filter(user_type='customer').count()
    
    context.update({
        "navigation": [
            {
                "title": _("Moliya va Sotuvlar (Oxirgi 30 kun)"),
                "items": [
                    {
                        "title": _("Umumiy Sof Foyda"),
                        "link": "#",
                        "metric": f"{total_revenue:,.0f} so'm",
                    },
                    {
                        "title": _("Yangi Buyurtmalar"),
                        "link": "#",
                        "metric": f"{recent_orders_count} ta",
                    },
                    {
                        "title": _("Aktiv Mijozlar"),
                        "link": "#",
                        "metric": f"{total_users} ta",
                    },
                ],
            },
        ],
    })
    
    return context
