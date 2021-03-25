import json
from .models import *


def cookie_cart(request):
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
        "need_shipping": False,
    }
    cart_items = order["get_total_cart_items"]
    customer = []
    logged_in = False

    for item in cart:
        try:
            item_quantity = cart[item]["quantity"]
            # Calculate total item quantity
            cart_items += item_quantity
            # Get product
            product = Product.objects.get(id=item)  # key is the Product id
            # Calculate total price of product i.e. prod * quantity
            total = product.price * item_quantity
            # update order dict
            order["get_total_cart_price"] += total
            order["get_total_cart_items"] += item_quantity
            # create item dict and append to items list
            item_dict = {
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "imageURL": product.imageURL,
                },
                "quantity": item_quantity,
                "get_total": total,
            }
            items.append(item_dict)

            # Set shpping info
            if product.digital == False:
                order["need_shipping"] = True
        except:
            pass

    return {
        "items": items,
        "order": order,
        "cart_items": cart_items,
        "customer": customer,
        "logged_in": logged_in,
    }


def data_cart(request):
    # Get Customer Info from logged in User
    if request.user.is_authenticated:
        logged_in = True
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cart_items = order.get_total_cart_items
    else:  # If Users is not logged in
        cookie_info = cookie_cart(request)  # from utils
        cart_items = cookie_info["cart_items"]
        items = cookie_info["items"]
        order = cookie_info["order"]
        customer = cookie_info["customer"]
        logged_in = cookie_info["logged_in"]

    return {
        "items": items,
        "order": order,
        "cart_items": cart_items,
        "customer": customer,
        "logged_in": logged_in,
    }


def guest_order(request, data):
    print("User is not logged in...")
    print(f"Cookies: {request.COOKIES}")
    name = data["form"]["name"]
    email = data["form"]["email"]
    cookie_cart_info = cookie_cart(request)
    items = cookie_cart_info["items"]
    # check if a anonymous user exists with same email id
    # we will store the email id and create a customer, in case the anonymous user shops again; we don't have to create a new customer for the same email id
    customer, customer_created = Customer.objects.get_or_create(email=email)
    # assign the name to the customer. We don't assign name above because what if customer decides to change his name but uses same email id?
    customer.name = name
    # save customer
    customer.save()

    # create order
    order = Order.objects.create(
        customer=customer,
        completed=False,
    )

    for item in items:
        product_id = item["product"]["id"]
        product = Product.objects.get(id=product_id)
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item["quantity"],
        )

    return customer, order