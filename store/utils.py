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
