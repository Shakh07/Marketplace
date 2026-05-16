"""ecommerce URL Configuration"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.catalog.urls')),
    path('', include('apps.accounts.urls')),
    path('', include('apps.orders.urls')),
    path('', include('apps.reviews.urls')),
    path('', include('apps.warehouse.urls')),
    path('', include('apps.suppliers.urls')),
    path('', include('apps.returns.urls')),
    path('manager/', include('apps.manager.urls')),

    # Always serve media files (Gunicorn doesn't serve media automatically)
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
