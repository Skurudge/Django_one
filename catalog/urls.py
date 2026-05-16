from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import (
    ProductListView,
    ContactsTemplateView,
    MyContactView,
    ProductDetailView,
    ProductCreateView
)

# Настройка пространства имен на основе конфигурации приложения
app_name = CatalogConfig.name

urlpatterns = [
    # Главная страница каталога товаров (CBV)
    path("", ProductListView.as_view(), name="home"),

    # Страницы контактов (CBV, разделенные пути во избежание конфликтов)
    path("contacts_info/", ContactsTemplateView.as_view(), name="contacts"),
    path("contacts/", MyContactView.as_view(), name="my_contact"),

    # Страница подробной информации о товаре (CBV)
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),

    # Страница добавления нового товара (CBV)
    path("products/add/", ProductCreateView.as_view(), name="add_product"),
]
