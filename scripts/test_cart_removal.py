import os
import django
import sys
from django.test import RequestFactory, Client
from django.contrib.sessions.middleware import SessionMiddleware

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pepfeb2.settings')
django.setup()

from shop.models import Product, Cart, CartItem
from shop.views import add_to_cart, remove_from_cart

def test_cart_removal():
    # Setup
    print("Setting up test...")
    factory = RequestFactory()
    
    # Get a product
    product = Product.objects.first()
    if not product:
        print("No products found to test with.")
        return

    # Create a request to add to cart
    print(f"Adding '{product.name}' to cart...")
    request = factory.get(f'/add-to-cart/{product.id}/')
    
    # Add session middleware to handle sessions
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session.save()
    
    # Add message middleware
    from django.contrib.messages.middleware import MessageMiddleware
    msg_middleware = MessageMiddleware(lambda x: None)
    msg_middleware.process_request(request)
    
    # Call add_to_cart view
    add_to_cart(request, product.id)
    
    # Verify item is in cart
    session_key = request.session.session_key
    cart = Cart.objects.get(session_key=session_key)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    print(f"Item verified in cart: {cart_item}")
    
    # Create request to remove from cart
    print(f"Removing item {cart_item.id} from cart...")
    remove_request = factory.get(f'/remove-from-cart/{cart_item.id}/')
    remove_request.session = request.session # Use same session
    
    # Call remove_from_cart view
    remove_from_cart(remove_request, cart_item.id)
    
    # Verify item is gone
    item_exists = CartItem.objects.filter(id=cart_item.id).exists()
    if not item_exists:
        print("Success: Item was removed from cart.")
    else:
        print("Failure: Item still exists in cart.")

if __name__ == "__main__":
    test_cart_removal()
