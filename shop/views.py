from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, CartItem, Category, Order, OrderItem
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def _get_cart(request):
    """Helper to get or create a cart based on session."""
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

def product_list(request):
    category_id = request.GET.get('category')
    categories = Category.objects.all()
    
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
        
    cart = _get_cart(request) # To show cart count if needed
    return render(request, 'shop/product_list.html', {
        'products': products, 
        'cart': cart,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')

def remove_from_cart(request, item_id):
    cart = _get_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart_detail')

def cart_detail(request):
    cart = _get_cart(request)
    return render(request, 'shop/cart.html', {'cart': cart})

def checkout(request):
    cart = _get_cart(request)
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        
        if not (full_name and address and phone_number):
             messages.error(request, 'Please fill in all fields.')
             return render(request, 'shop/checkout.html', {'cart': cart})

        # Create Order
        user = request.user if request.user.is_authenticated else None
        order = Order.objects.create(
            user=user,
            full_name=full_name,
            address=address,
            phone_number=phone_number,
            total_price=cart.total_price
        )

        # Create OrderItems
        for item in cart.cartitem_set.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Clear cart
        cart.cartitem_set.all().delete()
        messages.success(request, 'Payment successful! Your order has been placed.')
        return redirect('product_list')
    
    return render(request, 'shop/checkout.html', {'cart': cart})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('product_list')

def order_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/order_list.html', {'orders': orders})
