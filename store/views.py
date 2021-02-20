from django.shortcuts import render
from .models import *

# Create your views here.
def store_page(request):
    # Get all products
    products = Product.objects.all()

    context = {"products": products}
    return render(request, "store/store.html", context)


def cart_page(request):
    return render(request, "store/cart.html")


def checkout_page(request):
    return render(request, "store/checkout.html")
