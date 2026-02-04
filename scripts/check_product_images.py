import os
import django
import sys

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pepfeb2.settings')
django.setup()

from shop.models import Product

def check_images():
    products = Product.objects.all()
    print(f"Found {products.count()} products.")
    for p in products:
        has_image = bool(p.image)
        print(f"Product: {p.name}, ID: {p.id}, Has Image: {has_image}, Image Path: {p.image}")

if __name__ == "__main__":
    check_images()
