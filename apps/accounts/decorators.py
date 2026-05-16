from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    """Faqat admin yoki staff foydalanuvchilar uchun."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/auth/login/?next={request.path}')
        if request.user.user_type == 'admin' or request.user.is_staff:
            return view_func(request, *args, **kwargs)
        messages.error(request, "Bu sahifaga kirishga ruxsatingiz yo'q.")
        return redirect('home')
    return wrapper


def customer_required(view_func):
    """Login qilgan har qanday foydalanuvchi uchun."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/auth/login/?next={request.path}')
        return view_func(request, *args, **kwargs)
    return wrapper


def seller_required(view_func):
    """Seller yoki Admin foydalanuvchilar uchun."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/auth/login/?next={request.path}')
        if request.user.user_type in ('seller', 'admin') or request.user.is_staff:
            return view_func(request, *args, **kwargs)
        messages.error(request, "Bu sahifaga kirishga ruxsatingiz yo'q.")
        return redirect('home')
    return wrapper
