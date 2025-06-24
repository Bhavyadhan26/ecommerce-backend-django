from django.contrib import admin
from .models import Product, Cart, Order, OrderItem

admin.site.register(Product)
admin.site.register(Cart)


class OrderItemInline(admin.TabularInline):  
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price'] 

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']
    inlines = [OrderItemInline]  
    search_fields = ['user__username']
    list_filter = ['created_at']
