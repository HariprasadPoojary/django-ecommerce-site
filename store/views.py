from itertools import product
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import data_cart, guest_order

# Create your views here.
def store_page(request):

    data = data_cart(request)
    cart_items = data["cart_items"]

    # Get all products
    products = Product.objects.all()

    context = {
        "products": products,
        "cart_items": cart_items,
    }
    return render(request, "store/store.html", context)


def cart_page(request):

    data = data_cart(request)
    items = data["items"]
    order = data["order"]
    cart_items = data["cart_items"]

    context = {
        "items": items,
        "order": order,
        "cart_items": cart_items,
    }
    return render(request, "store/cart.html", context)


def checkout_page(request):
    # Get dictionary returned from utils.py
    context = data_cart(request)
    return render(request, "store/checkout.html", context)


def update_item(request):
    data = json.loads(request.body)
    #! print(data)
    # Get Product ID and Action
    product_id = data["productid"]
    action = data["action"]
    print(f"Prod ID: {product_id}, Action: {action}")
    # Get Customer
    customer = request.user.customer
    # Get Product
    product = Product.objects.get(id=product_id)
    # Get or Create Order
    order, order_created = Order.objects.get_or_create(
        customer=customer, completed=False
    )
    # Get or Create OrderItem
    orderItem, orderItem_created = OrderItem.objects.get_or_create(
        order=order, product=product
    )
    # Change quantity based on action
    if action == "add":
        orderItem.quantity += 1
    elif action == "remove":
        orderItem.quantity -= 1

    if orderItem.quantity <= 0:
        orderItem.delete()  # Delete item
        return JsonResponse("Item was deleted..", safe=False)

    orderItem.save()
    return JsonResponse("Item quantity changed..", safe=False)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, order_created = Order.objects.get_or_create(
            customer=customer, completed=False
        )

    else:  # Anonymous User
        customer, order = guest_order(request, data)

    total = float(data["form"]["total"])
    # Set value of transaction id
    order.transaction_id = transaction_id
    # validate total form fronted with backend
    if total == order.get_total_cart_price:
        order.completed = True
    # Save the order
    order.save()

    # Create shipping data
    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data["shipping"]["address"],
        city=data["shipping"]["city"],
        state=data["shipping"]["state"],
        pincode=data["shipping"]["pincode"],
    )

    return JsonResponse("Payment Submitted!", safe=False)
