from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .models import Product, Cart, Wishlist, Order, OrderItem, CartItem, UserProfile, Category
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.conf import settings




# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


# Sign In View
def sign_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You are now logged in.")
                return redirect('home')  # Redirect to homepage or dashboard
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'shop/sign_in.html', {'form': form})

# Sign Out View
def sign_out(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')  # Redirect to homepage after logging out

def home(request):
    # Fetch featured products, here assuming `is_featured` is a boolean field on the Product model
    featured_products = Product.objects.filter(is_featured=True)
    return render(request, 'shop/home.html', {'featured_products': featured_products})

def product_list(request):
    products = Product.objects.all()
   
    # Optionally, filter by category if a category is selected
    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        # Otherwise, show all products (can be left empty if you don't want it)
        products = Product.objects.all()

    categories = Category.objects.all()  # Fetch all categories to display in the filter
    return render(request, 'shop/product_list.html', {'products': products, 'categories': categories, 'selected_category': category_id})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # AJAX response for adding to cart without page reload
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({"message": "Added to cart successfully", "quantity": cart_item.quantity})
    
    return redirect('product_detail', product_id=product_id)

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    if product in wishlist.products.all():
        wishlist.products.remove(product)
        added = False
    else:
        wishlist.products.add(product)
        added = True
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'added': added})
    
    return redirect('product_detail', product_id=product_id)
@login_required
def wishlist(request):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    wishlist_items = wishlist.products.all()
    return render(request, 'shop/wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.cartitem_set.all()

    # Calculate total price for each item and overall total price
    cart_items_with_totals = []
    for item in cart_items:
        item_total = float(item.product.price * item.quantity)  # Calculate item total
        cart_items_with_totals.append({
            'product': item.product,
            'quantity': item.quantity,
            'item_total': item_total,
            'price_per_item': float(item.product.price)  # Add price per item for display
        })
    
    total_price = float(sum(item['item_total'] for item in cart_items_with_totals) * 100)  # Razorpay expects price in paise

    if request.method == 'POST':
        # Create Razorpay order
        razorpay_order = razorpay_client.order.create({
            "amount": total_price,
            "currency": "INR",
            "payment_capture": "1"
        })

        # Save Razorpay order ID for later verification
        order = Order.objects.create(
            user=request.user,
            total_price=total_price / 100,  # Convert to original amount for record
            status='Pending',
            razorpay_order_id=razorpay_order['id']
        )

        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

        # Clear the cart
        cart.cartitem_set.all().delete()

        # Pass payment details to template
        context = {
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
            'amount': total_price,
            'currency': 'INR',
            'callback_url': "/payment/verify/"
        }
        return render(request, 'shop/payment.html', context)

    return render(request, 'shop/checkout.html', {
        'cart_items': cart_items_with_totals,
        'total_price': total_price / 100  # Convert to original amount for display
    })
    
    
@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        order = Order.objects.get(razorpay_order_id=razorpay_order_id)

        # Verify payment signature
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
            # If verification is successful, mark order as paid
            order.status = 'Paid'
            order.save()
            return JsonResponse({'status': 'Payment successful'})
        except razorpay.errors.SignatureVerificationError:
            order.status = 'Failed'
            order.save()
            return JsonResponse({'status': 'Payment verification failed'})
    return HttpResponse(status=400)

    
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('order_items__product')
    return render(request, 'shop/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/order_detail.html', {'order': order})

@login_required
def delete_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item has been removed from your cart.")
    return redirect('cart')

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    # Calculate total price per item and overall total
    cart_items_with_totals = []
    for item in cart_items:
        item_total = item.product.price * item.quantity
        cart_items_with_totals.append({
            'product': item.product,
            'quantity': item.quantity,
            'item_total': item_total,
            'id': item.id,
        })
    
    total_price = sum(item['item_total'] for item in cart_items_with_totals)
    
    if request.method == 'POST':
        for item in cart_items:
            quantity = request.POST.get(f'quantity_{item.id}')
            if quantity:
                item.quantity = int(quantity)
                item.save()
        return redirect('cart')

    return render(request, 'shop/cart.html', {'cart_items': cart_items_with_totals, 'total_price': total_price})

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Create a new cart or get the existing one
    cart, created = Cart.objects.get_or_create(user=request.user)
    CartItem.objects.create(cart=cart, product=product, quantity=1)  # Add item to cart with quantity of 1 by default
    
    return redirect('checkout')  # Redirect directly to checkout page

def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'shop/search_results.html', {'products': products, 'query': query})

@login_required
def wishlist_view(request):
    wishlist = Wishlist.objects.filter(user=request.user).first()
    wishlist_items = wishlist.products.all() if wishlist else []
    return render(request, 'shop/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def delete_from_wishlist(request, product_id):
    wishlist = Wishlist.objects.filter(user=request.user).first()
    if wishlist:
        product = get_object_or_404(Product, id=product_id)
        if product in wishlist.products.all():
            wishlist.products.remove(product)
            messages.success(request, f'{product.name} has been removed from your wishlist.')
        else:
            messages.info(request, f'{product.name} is not in your wishlist.')

    return redirect('wishlist')

def get_cart_item_count(user):
    if user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=user)
        return CartItem.objects.filter(cart=cart).aggregate(Sum('quantity'))['quantity__sum'] or 0
    return 0

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another one.')
            return redirect('register')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered. Please use a different email.')
            return redirect('register')

        # Create a new user
        user = User.objects.create_user(username=username, password=password, email=email)

        # Ensure the user doesn't already have a UserProfile
        if not hasattr(user, 'userprofile'):
            # Create UserProfile for the new user
            UserProfile.objects.create(
                user=user,
                phone_number=phone_number,
                address=address,
            )

        messages.success(request, 'Registration successful! You can now log in.')
        return redirect('login')

    return render(request, 'shop/register.html')