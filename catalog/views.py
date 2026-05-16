from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, TemplateView, View
from catalog.models import Product, Category
from datetime import date


class ProductListView(ListView):
    """CBV для главной страницы со списком товаров и пагинацией."""
    model = Product
    template_name = "home.html"
    context_object_name = "page_obj"
    paginate_by = 6

    def get_queryset(self):
        # Лаконичный запрос ко всем продуктам согласно чек-листу
        queryset = super().get_queryset()

        # Сохраняем вашу оригинальную логику вывода в консоль
        for product in queryset:
            print(f"Продукт: {product.name}, создан: {product.created_at}")

        return queryset


class ProductDetailView(DetailView):
    """CBV для детальной страницы товара."""
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    """CBV для создания нового товара с ручной валидацией полей."""
    model = Product
    template_name = "add_product.html"
    fields = ["name", "description", "price", "category", "image"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["errors"] = {}
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        price = request.POST.get("price", "").strip()
        category_id = request.POST.get("category", "").strip()
        image = request.FILES.get("image")

        errors = {}
        if not name: errors["name"] = "Название обязательно"
        if not description: errors["description"] = "Описание обязательно"
        if not price: errors["price"] = "Цена обязательна"

        if errors:
            return self.render_to_response(
                self.get_context_data(errors=errors, categories=Category.objects.all())
            )

        category = Category.objects.get(pk=category_id) if category_id else None

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


class ContactsTemplateView(TemplateView):
    """CBV для отображения статической информации на странице контактов."""
    template_name = "contacts.html"


class MyContactView(View):
    """CBV для обработки POST-запроса формы обратной связи."""

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение {message} и телефон {phone} получены.")

    def get(self, request, *args, **kwargs):
        # Если случайно зашли GET-запросом, перенаправляем на информационную страницу
        return redirect("catalog:contacts")

