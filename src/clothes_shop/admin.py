from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
from .models import (
    Size, Target, ClothesType, Brand, Product, User, 
    Favorite, WishList, CartItem, Order, OrderItem, Payment, Shipping, Rating
)

# register models for admin screen
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(ClothesType)
class ClothesTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_quantity', 'created_at', 'updated_at')
    search_fields = ('name', 'category')
    list_filter = ('brand', 'clothes_type', 'target', 'size')

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'role','is_active', 'created_at', 'updated_at')
    search_fields = ('email', 'username')
    list_filter = ('role', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'role')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at', 'updated_at')
    search_fields = ('user__name', 'product__name')

@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'is_public', 'created_at', 'updated_at')
    search_fields = ('user__name', 'product__name')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at', 'updated_at')
    search_fields = ('user__name', 'product__name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_date', 'order_status', 'total_price', 'created_at', 'updated_at')
    search_fields = ('user__name', 'order_status')
    list_filter = ('order_status',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'unit_price', 'created_at', 'updated_at')
    search_fields = ('order__id', 'product__name')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_date', 'payment_option', 'payment_status', 'created_at', 'updated_at')
    search_fields = ('order__id', 'payment_status')
    list_filter = ('payment_status', 'payment_option')

@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ('order', 'shipping_tracking_number', 'shipping_date', 'shipping_address', 'created_at', 'updated_at')
    search_fields = ('shipping_tracking_number', 'order__id')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at', 'updated_at')
    search_fields = ('user__name', 'product__name')
    list_filter = ('rating',)