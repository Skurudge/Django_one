from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home, contacts, my_contact, product_detail, add_product

# Настройка пространства имен на основе конфигурации приложения
app_name = CatalogConfig.name

urlpatterns = [
    # Главная страница каталога товаров
    path("", home, name="home"),

    # Страницы контактов (разделенные пути во избежание конфликтов)
    path("contacts_info/", contacts, name="contacts"),
    path("contacts/", my_contact, name="my_contact"),

    # Страница подробной информации о товаре
    path("products/<int:pk>/", product_detail, name="product_detail"),

    # Страница добавления нового товара
    path("products/add/", add_product, name="add_product"),
]
