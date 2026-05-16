import os
import glob

files = glob.glob('apps/*/admin.py')

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if "from unfold.admin import" in content:
        continue

    # Replacements
    content = content.replace("from django.contrib import admin", "from django.contrib import admin\nfrom unfold.admin import ModelAdmin, TabularInline, StackedInline")
    content = content.replace("(admin.ModelAdmin)", "(ModelAdmin)")
    content = content.replace("(admin.TabularInline)", "(TabularInline)")
    content = content.replace("(admin.StackedInline)", "(StackedInline)")

    if "accounts" in f:
        # Accounts has special UserAdmin setup
        content = content.replace("from django.contrib.auth.admin import UserAdmin", 
            "from django.contrib.auth.admin import UserAdmin as BaseUserAdmin\n"
            "from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm"
        )
        content = content.replace("class CustomUserAdmin(UserAdmin):", 
            "class CustomUserAdmin(BaseUserAdmin, ModelAdmin):\n"
            "    form = UserChangeForm\n"
            "    add_form = UserCreationForm\n"
            "    change_password_form = AdminPasswordChangeForm"
        )
        content = content.replace("UserAdmin.fieldsets", "BaseUserAdmin.fieldsets")
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("Updated all admin files for Unfold")
