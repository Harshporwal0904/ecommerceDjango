from django.contrib import admin
from .models import Product, Category, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'total_price', 'is_delivered', 'created_at']
    list_filter = ['is_delivered', 'created_at']
    list_editable = ['is_delivered']
    inlines = [OrderItemInline]

admin.site.register(Product)
admin.site.register(Category)
