from django.shortcuts import render, redirect, resolve_url
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser, Address
from .serializers import UserRegistrationSerializer, UserProfileSerializer, AddressSerializer


# ═══════════════════════════════════════
# API Views
# ═══════════════════════════════════════

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class AddressListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AddressDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


# ═══════════════════════════════════════
# Template Views
# ═══════════════════════════════════════

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')

        if password != password_confirm:
            messages.error(request, "Parollar mos kelmadi!")
            return render(request, 'accounts/register.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Bu username allaqachon band!")
            return render(request, 'accounts/register.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Bu email allaqachon ro'yxatdan o'tgan!")
            return render(request, 'accounts/register.html')

        user = CustomUser.objects.create_user(
            username=username, email=email, password=password,
            first_name=first_name, last_name=last_name
        )
        login(request, user)
        messages.success(request, "Muvaffaqiyatli ro'yxatdan o'tdingiz!")
        return redirect('home')

    return render(request, 'accounts/register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.first_name or user.username}!")
            next_url = request.GET.get('next')
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect('home')
        else:
            messages.error(request, "Username yoki parol noto'g'ri!")

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Tizimdan chiqdingiz.")
    return redirect('home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        # ── Edit profile info ──────────────────────────────────────────────
        if action == 'edit_profile':
            first_name = request.POST.get('first_name', '').strip()
            last_name  = request.POST.get('last_name', '').strip()
            email      = request.POST.get('email', '').strip()
            phone      = request.POST.get('phone', '').strip()
            u = request.user
            u.first_name = first_name
            u.last_name  = last_name
            u.email      = email
            u.phone      = phone
            u.save(update_fields=['first_name', 'last_name', 'email', 'phone', 'updated_at'])
            if is_ajax:
                return JsonResponse({'success': True,
                                     'first_name': first_name,
                                     'last_name': last_name,
                                     'full_name': u.get_full_name() or u.username,
                                     'phone': phone})
            messages.success(request, "Profil yangilandi!")
            return redirect('profile')

        # ── Add address ────────────────────────────────────────────────────
        elif action == 'add_address':
            full_name      = request.POST.get('full_name', '').strip()
            phone          = request.POST.get('phone', '').strip()
            city           = request.POST.get('city', '').strip()
            region         = request.POST.get('region', '').strip()
            street_address = request.POST.get('street_address', '').strip()
            set_default    = request.POST.get('is_default') == '1'

            if full_name and phone and street_address:
                if set_default:
                    request.user.addresses.all().update(is_default=False)
                addr = Address.objects.create(
                    user=request.user,
                    full_name=full_name,
                    phone=phone,
                    city=city,
                    region=region,
                    street_address=street_address,
                    is_default=set_default or (request.user.addresses.count() == 0),
                )
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
                messages.success(request, "Yangi manzil saqlandi!")
            else:
                if is_ajax:
                    return JsonResponse({'success': False, 'error': "Iltimos barcha kerakli maydonlarni to'ldiring."})
                messages.error(request, "Iltimos barcha kerakli maydonlarni to'ldiring.")
            return redirect('profile')

        # ── Delete address ─────────────────────────────────────────────────
        elif action == 'delete_address':
            address_id = request.POST.get('address_id')
            if address_id:
                try:
                    addr = Address.objects.get(id=address_id, user=request.user)
                    was_default = addr.is_default
                    addr.delete()
                    # Reassign default if needed
                    if was_default:
                        first = request.user.addresses.first()
                        if first:
                            first.is_default = True
                            first.save()
                    if is_ajax:
                        return JsonResponse({'success': True, 'deleted_id': int(address_id)})
                    messages.success(request, "Manzil o'chirildi.")
                except Address.DoesNotExist:
                    if is_ajax:
                        return JsonResponse({'success': False, 'error': 'Manzil topilmadi.'})
                    messages.error(request, "Manzil topilmadi.")
            return redirect('profile')

        # ── Set default address ────────────────────────────────────────────
        elif action == 'set_default_address':
            address_id = request.POST.get('address_id')
            if address_id:
                try:
                    request.user.addresses.all().update(is_default=False)
                    addr = Address.objects.get(id=address_id, user=request.user)
                    addr.is_default = True
                    addr.save()
                    if is_ajax:
                        return JsonResponse({'success': True, 'default_id': int(address_id)})
                except Address.DoesNotExist:
                    if is_ajax:
                        return JsonResponse({'success': False})
            return redirect('profile')

    addresses = Address.objects.filter(user=request.user).order_by('-is_default', '-id')
    orders    = request.user.orders.all()[:10]
    # Compute real total spent from delivered/confirmed/processing orders
    from django.db.models import Sum
    total_spent = request.user.orders.filter(
        order_status__in=['delivered', 'confirmed', 'processing', 'shipped']
    ).aggregate(t=Sum('total_amount'))['t'] or 0

    return render(request, 'accounts/profile.html', {
        'addresses':   addresses,
        'orders':      orders,
        'total_spent': total_spent,
    })


def subscribe_newsletter(request):
    """AJAX view to subscribe email to newsletter."""
    from django.http import JsonResponse
    from .models import NewsletterSubscriber

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if not email:
            return JsonResponse({'success': False, 'message': "Emailni kiriting!"})

        # Basic verification and add to db
        subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
        if created:
            return JsonResponse({'success': True, 'message': "Obuna bo'ldingiz!"})
        else:
            return JsonResponse({'success': True, 'message': "Siz allaqachon obuna bo'lgansiz!"})
            
    return JsonResponse({'success': False, 'message': "Not allowed."})
