from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from .models import CustomUser, Address, PasswordResetToken, EmailVerificationToken, UserSession, SiteSettings, NewsletterSubscriber


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'account_status', 'is_staff')
    list_filter = ('user_type', 'account_status', 'gender', 'email_verified', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('E-commerce Info', {
            'fields': ('phone', 'date_of_birth', 'gender', 'profile_image_url',
                       'account_status', 'user_type', 'email_verified', 'phone_verified',
                       'customer_segment', 'lifetime_value', 'loyalty_points',
                       'preferred_language', 'timezone')
        }),
    )


@admin.register(Address)
class AddressAdmin(ModelAdmin):
    list_display = ('full_name', 'user', 'city', 'region', 'address_type', 'is_default')
    list_filter = ('address_type', 'is_default', 'country', 'region')
    search_fields = ('full_name', 'city', 'street_address')


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(ModelAdmin):
    list_display = ('user', 'token', 'expires_at', 'used', 'created_at')
    list_filter = ('used',)
    readonly_fields = ('token', 'created_at')


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(ModelAdmin):
    list_display = ('user', 'token', 'expires_at', 'verified', 'created_at')
    list_filter = ('verified',)
    readonly_fields = ('token', 'created_at')


@admin.register(UserSession)
class UserSessionAdmin(ModelAdmin):
    list_display = ('user', 'ip_address', 'device_type', 'created_at', 'last_activity')
    list_filter = ('device_type',)
    search_fields = ('user__username', 'ip_address')
    readonly_fields = ('session_token', 'created_at', 'last_activity')


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    """Singleton admin — only 1 record allowed."""
    list_display = ('site_name', 'contact_email', 'contact_phone', 'site_domain')

    fieldsets = (
        ('Asosiy Ma\'lumotlar', {
            'fields': ('site_name', 'site_domain')
        }),
        ('Aloqa', {
            'fields': ('contact_email', 'contact_phone', 'address')
        }),
        ('Chek Sozlamalari', {
            'fields': ('receipt_footer',)
        }),
        ('Ijtimoiy Tarmoqlar', {
            'fields': ('social_instagram', 'social_telegram')
        }),
    )

    def has_add_permission(self, request):
        # Only allow adding if no record exists yet
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False  # Prevent deletion


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(ModelAdmin):
    list_display = ('email', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('email',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
