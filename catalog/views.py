from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from catalog.models import Product, Category
from datetime import date


def home(request):
    # Лаконичный запрос ко всем продуктам согласно чек-листу
    products_list = Product.objects.all()

    # Постраничный вывод: по 6 товаров на страницу
    paginator = Paginator(products_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Сохраняем вашу оригинальную логику вывода в консоль
    for product in page_obj:
        print(f"Продукт: {product.name}, создан: {product.created_at}")

    context = {"page_obj": page_obj}
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


def product_detail(request, pk):
    # Извлечение объекта через ORM по pk согласно чек-листу
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {"product": product})


def add_product(request):
    categories = Category.objects.all()
    errors = {}

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        price = request.POST.get("price", "").strip()
        category_id = request.POST.get("category", "").strip()
        image = request.FILES.get("image")

        # Валидация: обязательные поля и защита от ошибок
        if not name: errors["name"] = "Название обязательно"
        if not description: errors["description"] = "Описание обязательно"
        if not price: errors["price"] = "Цена обязательна"

        if not errors:
            category = Category.objects.get(pk=category_id) if category_id else None

            # Сохранение нового товара в базу данных
            Product.objects.create(
                name=name,
                description=description,
                price=price,
                category=category,
                image=image,
                created_at=date.today(),
                updated_at=date.today()
            )
            return redirect("catalog:home")

    return render(request, "add_product.html", {"categories": categories, "errors": errors})
