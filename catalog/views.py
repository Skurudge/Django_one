from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db import models  # Добавили импорт для работы с models.Q

from catalog.models import Product, Category
from catalog.forms import ProductForm
from catalog.services import get_products_by_category


class ProductListView(ListView):
    """CBV для главной страницы со списком товаров и пагинацией."""
    model = Product
    template_name = "home.html"
    context_object_name = "page_obj"
    paginate_by = 6

    def get_queryset(self):
        """Фильтрация товаров в зависимости от прав доступа пользователя."""
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_authenticated and (user.is_superuser or user.groups.filter(name="Модератор продуктов").exists()):
            return queryset

        if user.is_authenticated:
            return queryset.filter(models.Q(is_published=True) | models.Q(owner=user))

        return queryset.filter(is_published=True)


# Задание 2: Кэширование страницы одного продукта на 15 минут (900 секунд)
@method_decorator(cache_page(900), name="dispatch")
class ProductDetailView(LoginRequiredMixin, DetailView):
    """CBV для детальной страницы товара с защитой доступа и кэшированием."""
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"

    def get_object(self, queryset=None):
        """Запрещаем просмотр неопубликованного чужого товара анонимам и обычным пользователям."""
        obj = super().get_object(queryset)
        user = self.request.user

        if user.is_superuser or user.groups.filter(name="Модератор продуктов").exists():
            return obj

        if obj.is_published or obj.owner == user:
            return obj

        raise Http404("Товар находится на модерации и недоступен для просмотра.")


class CategoryProductListView(ListView):
    """Задание 3: Представление для отображения продуктов в конкретной категории."""
    model = Product
    template_name = "category_products.html"
    context_object_name = "products"

    def get_queryset(self):
        """Получаем список продуктов из сервисной функции (с низкоуровневым кэшированием)."""
        self.category = get_object_or_404(Category, pk=self.kwargs.get("pk"))
        return get_products_by_category(self.category.pk)

    def get_context_data(self, **kwargs):
        """Добавляем категорию в контекст для отображения заголовка."""
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    """CBV для создания нового товара с автоматической привязкой владельца."""
    model = Product
    form_class = ProductForm
    template_name = "add_product.html"
    success_url = reverse_lazy("catalog:home")

    def get_form_kwargs(self):
        """Передаем флаг модератора в форму для управления полем публикации."""
        kwargs = super().get_form_kwargs()
        user = self.request.user
        kwargs["is_moderator"] = user.is_superuser or user.has_perm("catalog.can_unpublish_product")
        return kwargs

    def form_valid(self, form):
        """Автоматически привязываем создателя товара к текущему пользователю."""
        from datetime import date
        product = form.save(commit=False)
        product.created_at = date.today()
        product.updated_at = date.today()
        product.owner = self.request.user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """CBV для редактирования существующего товара (доступно владельцу или модератору)."""
    model = Product
    form_class = ProductForm
    template_name = "add_product.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = self.request.user
        kwargs["is_moderator"] = user.is_superuser or user.has_perm("catalog.can_unpublish_product")
        return kwargs

    def get_object(self, queryset=None):
        """Проверяем, что редактировать товар может только его владелец или модератор."""
        obj = super().get_object(queryset)
        user = self.request.user

        if obj.owner == user or user.is_superuser or user.has_perm("catalog.can_unpublish_product"):
            return obj

        raise Http404("У вас нет прав для редактирования этого товара.")

    def get_success_url(self):
        return reverse("catalog:product_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        from datetime import date
        product = form.save(commit=False)
        product.updated_at = date.today()
        product.save()
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """CBV для удаления товара (доступно владельцу или модератору с правами)."""
    model = Product
    template_name = "product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")

    def get_object(self, queryset=None):
        """Удалять продукты может создатель или модератор."""
        obj = super().get_object(queryset)
        user = self.request.user

        if obj.owner == user or user.is_superuser or user.has_perm("catalog.delete_product"):
            return obj

        raise Http404("У вас нет прав на удаление этого товара.")


class ContactsTemplateView(TemplateView):
    template_name = "contacts.html"


class MyContactView(View):
    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение {message} и телефон {phone} получены.")

    def get(self, request, *args, **kwargs):
        return redirect("catalog:contacts")
