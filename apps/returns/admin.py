from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from .models import Return, ReturnItem


class ReturnItemInline(TabularInline):
    model = ReturnItem
    extra = 0


@admin.register(Return)
class ReturnAdmin(ModelAdmin):
    list_display = ('id', 'order', 'user', 'return_status', 'refund_amount', 'created_at')
    list_filter = ('return_status',)
    search_fields = ('order__order_number', 'user__username')
    readonly_fields = ('created_at',)
    inlines = [ReturnItemInline]


@admin.register(ReturnItem)
class ReturnItemAdmin(ModelAdmin):
    list_display = ('return_request', 'order_item', 'quantity', 'refund_amount')
