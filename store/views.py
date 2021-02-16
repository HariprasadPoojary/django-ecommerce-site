from django.shortcuts import render

# Create your views here.
def main_page(request):
    return render(request, "store/main.html")


def store_page(request):
    return render(request, "store/store.html")


def cart_page(request):
    return render(request, "store/cart.html")


def checkout_page(request):
    return render(request, "store/checkout.html")
