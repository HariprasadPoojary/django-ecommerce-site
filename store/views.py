from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime

# Create your views here.
def store_page(request):
    # Get Customer Info from logged in User
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        # items = order.orderitem_set.all()
        cart_items = order.get_total_cart_items
    else:  # If Users is not logged in
        # Get total number of items from browser cookies & convert to python object
        try:
            cart = json.loads(request.COOKIES["cart"])
        except:
            cart = {}
        print(f"Cart from Cookie: {cart}")
        cart_items = 0
        # Calculate total item quantity
        for item in cart:
            cart_items += cart[item]["quantity"]

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
        # Get total number of items from browser cookies & convert to python object
        try:
            cart = json.loads(request.COOKIES["cart"])
        except:
            cart = {}
        # Empty items
        items = []
        # Empty order dict
        order = {
            "get_total_cart_price": 0,
            "get_total_cart_items": 0,
        }
        cart_items = order["get_total_cart_items"]
        # Calculate total item quantity
        for item in cart:
            cart_items += cart[item]["quantity"]

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
    return JsonResponse("Item quantity changed..", safe=False)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, order_created = Order.objects.get_or_create(
            customer=customer, completed=False
        )
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
    else:
        print("User is not logged in...")

    return JsonResponse("Payment Submitted!", safe=False)
