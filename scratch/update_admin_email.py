import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from apps.accounts.models import CustomUser

# Update the admin email
updated = CustomUser.objects.filter(username='admin').update(email='admin@nexus.uz')
print(f"Updated {updated} user(s).")
