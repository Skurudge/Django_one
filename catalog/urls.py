from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import (
    ProductListView,
    ContactsTemplateView,
    MyContactView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    CategoryProductListView,  # Добавили новый контроллер
)

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="home"),

    # Новый маршрут для просмотра продуктов по категориям (Задание 3)
    path("category/<int:pk>/", CategoryProductListView.as_view(), name="category_products"),

    path("contacts_info/", ContactsTemplateView.as_view(), name="contacts"),
    path("contacts/", MyContactView.as_view(), name="my_contact"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/add/", ProductCreateView.as_view(), name="add_product"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
]
