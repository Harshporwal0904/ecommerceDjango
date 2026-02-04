import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pepfeb2.settings')
django.setup()

from shop.models import Product, Category

def populate():
    # Create Categories
    electronics, created = Category.objects.get_or_create(name='Electronics')
    clothing, created = Category.objects.get_or_create(name='Clothing')
    
    print(f"Categories: {electronics}, {clothing}")

    # Create Products
    p1, created = Product.objects.get_or_create(
        name='Smartphone',
        defaults={
            'category': electronics,
            'price': 699.99,
            'description': 'Latest model smartphone'
        }
    )
    
    p2, created = Product.objects.get_or_create(
        name='T-Shirt',
        defaults={
            'category': clothing,
            'price': 19.99,
            'description': 'Cotton crew neck t-shirt'
        }
    )

    print(f"Products created: {p1}, {p2}")

if __name__ == '__main__':
    populate()
