from django.urls import path
from . import views

urlpatterns = [
    path("", views.store_page, name="store"),
    path("cart/", views.cart_page, name="cart"),
    path("checkout/", views.checkout_page, name="checkout"),
]