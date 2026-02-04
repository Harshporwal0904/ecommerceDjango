import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pepfeb2.settings')
django.setup()

from shop.models import Product

def list_products():
    products = Product.objects.all()
    with open('products_list.txt', 'w') as f:
        for p in products:
            f.write(f"{p.name}|{p.image}\n")

if __name__ == "__main__":
    list_products()
