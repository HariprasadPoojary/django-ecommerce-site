from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json

# Create your views here.
def store_page(request):
    # Get Customer Info from logged in User
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        # items = order.orderitem_set.all()
        cart_items = order.get_total_cart_items
    else:  # If Users is not logged in
        # # Empty items
        items = []
        # # Empty order dict
        order = {
            "get_total_cart_price": 0,
            "get_total_cart_items": 0,
        }
        cart_items = order["get_total_cart_items"]
    # Get all products
    products = Product.objects.all()

    context = {
        "products": products,
        "cart_items": cart_items,
    }
    return render(request, "store/store.html", context)


def cart_page(request):
    # Get Customer Info from logged in User
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cart_items = order.get_total_cart_items
    else:  # If Users is not logged in
        # Empty items
        items = []
        # Empty order dict
        order = {
            "get_total_cart_price": 0,
            "get_total_cart_items": 0,
        }
        cart_items = order["get_total_cart_items"]

    context = {
        "items": items,
        "order": order,
        "cart_items": cart_items,
    }
    return render(request, "store/cart.html", context)


def checkout_page(request):
    # Get Customer Info from logged in User
    if request.user.is_authenticated:
        logged_in = True
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cart_items = order.get_total_cart_items
    else:  # If Users is not logged in
        # Empty items
        items = []
        # Empty order dict
        order = {
            "get_total_cart_price": 0,
            "get_total_cart_items": 0,
            "need_shipping": False,
        }
        cart_items = order["get_total_cart_items"]
        customer = []
        logged_in = False

    context = {
        "items": items,
        "order": order,
        "cart_items": cart_items,
        "customer": customer,
        "logged_in": logged_in,
    }
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
    return JsonResponse("Item was added..", safe=False)
