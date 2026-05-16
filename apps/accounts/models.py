import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

_img_validator = [FileExtensionValidator(allowed_extensions=['jpg','jpeg','png','webp'])]


class CustomUser(AbstractUser):
    """Custom User model — extends AbstractUser with e-commerce fields."""

    class Gender(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'
        OTHER = 'other', 'Other'

    class AccountStatus(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        SUSPENDED = 'suspended', 'Suspended'
        DELETED = 'deleted', 'Deleted'

    class UserType(models.TextChoices):
        CUSTOMER = 'customer', 'Customer'
        SELLER = 'seller', 'Seller'
        ADMIN = 'admin', 'Admin'

    phone = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True)
    profile_image_url = models.ImageField(upload_to='profiles/', blank=True, null=True, validators=_img_validator)
    account_status = models.CharField(max_length=15, choices=AccountStatus.choices, default=AccountStatus.ACTIVE)
    user_type = models.CharField(max_length=10, choices=UserType.choices, default=UserType.CUSTOMER)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    customer_segment = models.CharField(max_length=50, blank=True)
    lifetime_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    loyalty_points = models.IntegerField(default=0)
    preferred_language = models.CharField(max_length=10, default='uz')
    timezone = models.CharField(max_length=50, default='Asia/Tashkent')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class Address(models.Model):
    """User addresses for shipping and billing."""

    class AddressType(models.TextChoices):
        SHIPPING = 'shipping', 'Shipping'
        BILLING = 'billing', 'Billing'
        BOTH = 'both', 'Both'

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=10, choices=AddressType.choices, default=AddressType.BOTH)
    is_default = models.BooleanField(default=False)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=50, default='Uzbekistan')
    region = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    district = models.CharField(max_length=50, blank=True)
    street_address = models.TextField(blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'addresses'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f"{self.full_name} — {self.city}, {self.street_address}"


class PasswordResetToken(models.Model):
    """Tokens for password reset functionality."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'password_reset_tokens'

    def __str__(self):
        return f"Reset token for {self.user.username}"


class EmailVerificationToken(models.Model):
    """Tokens for email verification."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='email_verification_tokens')
    token = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    expires_at = models.DateTimeField()
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'email_verification_tokens'

    def __str__(self):
        return f"Email verification for {self.user.username}"


class UserSession(models.Model):
    """Tracks user login sessions."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_sessions')
    session_token = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    device_type = models.CharField(max_length=20, blank=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_sessions'

    def __str__(self):
        return f"Session for {self.user.username} ({self.device_type})"


class SiteSettings(models.Model):
    """Singleton model for site-wide configurable settings — editable via admin panel."""
    site_name        = models.CharField(max_length=100, default='NEXUS', verbose_name='Sayt nomi')
    site_domain      = models.CharField(max_length=200, default='nexus.uz', verbose_name='Domen / URL')
    contact_email    = models.EmailField(default='support@nexus.uz', verbose_name='Aloqa email')
    contact_phone    = models.CharField(max_length=50, blank=True, default='+998 71 200 00 00', verbose_name='Telefon raqam')
    address          = models.TextField(blank=True, default="Toshkent, O'zbekiston", verbose_name='Manzil')
    receipt_footer   = models.TextField(blank=True, default="Xarid uchun rahmat! Savol yoki muammo bo'lsa bizga murojaat qiling.",
                                        verbose_name="Chek pastki matni")
    social_instagram = models.CharField(max_length=200, blank=True, verbose_name='Instagram URL')
    social_telegram  = models.CharField(max_length=200, blank=True, verbose_name='Telegram URL')

    class Meta:
        db_table = 'site_settings'
        verbose_name = 'Sayt Sozlamalari'
        verbose_name_plural = 'Sayt Sozlamalari'

    def save(self, *args, **kwargs):
        # Singleton: always use pk=1
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return f"Sayt Sozlamalari — {self.site_name}"


class NewsletterSubscriber(models.Model):
    """Model to store emails of users who subscribe to the newsletter."""
    email = models.EmailField(unique=True, verbose_name="Email manzili")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'newsletter_subscribers'
        verbose_name = 'Obunachi'
        verbose_name_plural = 'Obunachilar'
        ordering = ['-created_at']

    def __str__(self):
        return self.email
