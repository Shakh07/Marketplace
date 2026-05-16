from .models import SiteSettings


def site_settings(request):
    """Inject site-wide settings into every template context."""
    from apps.catalog.models import Category
    try:
        categories = Category.objects.filter(is_active=True, parent_category__isnull=True)[:6]
    except Exception:
        categories = []
        
    return {
        'site_settings': SiteSettings.get_settings(),
        'global_categories': categories,
    }
