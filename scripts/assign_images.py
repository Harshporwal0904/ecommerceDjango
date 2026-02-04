import os
import django
import sys
from django.core.files import File

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pepfeb2.settings')
django.setup()

from shop.models import Product

def assign_images():
    # Map product names (or parts of them) to filenames
    # filenames are in media/products/
    # format: name_timestamp.png. 
    # Since I don't know the exact timestamps, I will list files in media/products and match them.
    
    media_products_dir = os.path.join(settings.MEDIA_ROOT, 'products')
    if not os.path.exists(media_products_dir):
        print(f"Directory not found: {media_products_dir}")
        return

    files = os.listdir(media_products_dir)
    print(f"Found {len(files)} files in {media_products_dir}")

    products = Product.objects.all()
    
    mapping = {
        'classic leather watch': 'classic_leather_watch',
        'wireless noise-canceling headphones': 'wireless_headphones',
        'minimalist backpack': 'minimalist_backpack',
        'smart home speaker': 'smart_home_speaker',
        'premium coffee maker': 'premium_coffee_maker',
        'smartphone': 'smartphone',
        't-shirt': 't_shirt'
    }

    for product in products:
        p_name_lower = product.name.lower()
        matched_key = None
        for key in mapping:
            if key in p_name_lower:
                matched_key = key
                break
        
        if matched_key:
            # Find the file that starts with the mapped value
            prefix = mapping[matched_key]
            matching_files = [f for f in files if f.startswith(prefix)]
            
            if matching_files:
                # Use the first match (most likely the one we generated)
                filename = matching_files[0]
                # We need to set the image field. 
                # Since the file is already in media/products, we can set the relative path.
                # However, ImageField usually expects to verify the file.
                # If we just set `product.image = 'products/' + filename`, it should work if the file exists there.
                
                print(f"Assigning {filename} to {product.name}")
                product.image = f'products/{filename}'
                product.save()
            else:
                print(f"No file found for prefix {prefix} (Product: {product.name})")
        else:
            print(f"No mapping found for product: {product.name}")

from django.conf import settings

if __name__ == "__main__":
    assign_images()
