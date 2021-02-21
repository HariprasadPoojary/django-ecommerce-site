from django.shortcuts import render
from .models import *

# Create your views here.
def store_page(request):
    # Get all products
    products = Product.objects.all()

    context = {"products": products}
    return render(request, "store/store.html", context)


def cart_page(request):
    # Get Customer Info from logged in User
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
    else:  # If Users is not logged in
        items = []

    context = {"items": items, "order":order}
    return render(request, "store/cart.html", context)


def checkout_page(request):
    return render(request, "store/checkout.html")
