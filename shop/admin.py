from django.contrib import admin
from .models import Product, Cart, CartItem, Wishlist, Order, OrderItem, ProductImage, Category
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.utils.html import format_html

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    
class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())  # Use CKEditorWidget

    class Meta:
        model = Product
        fields = '__all__'
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category',  'colored_rating')
    search_fields = ('name', 'description')
    inlines = [ProductImageInline]
    
    
    def colored_rating(self, obj):
        color = "green" if obj.rating >= 4 else "orange" if obj.rating >= 3 else "red"
        return format_html('<span style="color: {};">{}</span>', color, obj.rating)

    colored_rating.short_description = 'Rating'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    list_filter = ('cart',)

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    list_filter = ('order',)


# Register the Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display category name in list
    search_fields = ('name',)  # Allow searching by category name