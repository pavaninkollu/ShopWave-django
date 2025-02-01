from .views import get_cart_item_count

def cart_item_count_processor(request):
    """Makes the cart item count accessible globally in templates."""
    return {
        'cart_item_count': get_cart_item_count(request.user)
    }
