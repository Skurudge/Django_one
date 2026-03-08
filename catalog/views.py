from django.shortcuts import render
from django.http import HttpResponse
from catalog.models import Product


def home(request):
    latest_products = Product.objects.order_by('-created_at')[:5]
    for product in latest_products:
        print(f"Продукт: {product.name}, создан: {product.created_at}")

    context = {"latest_products": latest_products}
    return render(request, "home.html", context)


def contacts(request):
    return render(request, "contacts.html")


def my_contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение {message} и телефон {phone} получены.")
    return render(request, "contacts.html")
