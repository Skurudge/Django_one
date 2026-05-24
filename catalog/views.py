from django.shortcuts import redirect
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from catalog.models import Product, Category
from catalog.forms import ProductForm


class ProductListView(ListView):
    """CBV для главной страницы со списком товаров и пагинацией (доступна всем)."""
    model = Product
    template_name = "home.html"
    context_object_name = "page_obj"
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        # Сохраняем вашу оригинальную логику вывода в консоль
        for product in queryset:
            print(f"Продукт: {product.name}, создан: {product.created_at}")
        return queryset


class ProductDetailView(LoginRequiredMixin, DetailView):
    """CBV для детальной страницы товара (только для авторизованных)."""
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    """CBV для создания нового товара с использованием ProductForm (только для авторизованных)."""
    model = Product
    form_class = ProductForm
    template_name = "add_product.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        """Автоматическое заполнение дат перед сохранением."""
        from datetime import date
        product = form.save(commit=False)
        product.created_at = date.today()
        product.updated_at = date.today()
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """CBV для редактирования существующего товара с использованием ProductForm (только для авторизованных)."""
    model = Product
    form_class = ProductForm
    template_name = "add_product.html"

    def get_success_url(self):
        """Перенаправление на страницу этого же товара после успешного редактирования."""
        return reverse("catalog:product_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        """Обновление даты изменения товара."""
        from datetime import date
        product = form.save(commit=False)
        product.updated_at = date.today()
        product.save()
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """CBV для удаления товара с использованием собственного шаблона (только для авторизованных)."""
    model = Product
    template_name = "product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")


class ContactsTemplateView(TemplateView):
    """CBV для отображения статической информации на странице контактов (доступна всем)."""
    template_name = "contacts.html"


class MyContactView(View):
    """CBV для обработки POST-запроса формы обратной связи (доступна всем)."""
    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение {message} и телефон {phone} получены.")

    def get(self, request, *args, **kwargs):
        return redirect("catalog:contacts")
