from django.shortcuts import render
from store.models import Collection, Product, Cart, CartItem
import time


def say_hello(request):
    cart = Cart()
    cart.save()
    item1 = CartItem()
    item1.cart = cart
    item1.quantity = 1
    item1.product = Product(pk=23)
    item1.save()
    return render(request, "hello.html", {"name": "Mosh"})
