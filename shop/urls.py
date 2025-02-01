from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . import views
from .views import wishlist_view, add_to_wishlist, delete_from_wishlist, delete_cart_item, add_to_cart, home

urlpatterns = [
    path('', home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('wishlist/', wishlist_view, name='wishlist'),  # Consolidate wishlist URL
    path('checkout/', views.checkout, name='checkout'),
     path("payment/verify/", views.verify_payment, name="verify_payment"),
    path('orders/', views.order_history, name='order_history'),
    path('cart/', views.cart_view, name='cart'),
    path('delete-cart-item/<int:item_id>/', delete_cart_item, name='delete_cart_item'),
    path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),
    path('add-to-wishlist/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),  # Add to wishlist
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('delete-from-wishlist/<int:product_id>/', delete_from_wishlist, name='delete_from_wishlist'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('login/', views.sign_in, name='login'),  # Login page
    path('logout/', views.sign_out, name='logout'),  # Logout action
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    

    
    
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)