from django.contrib import admin
from .models import Product, Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Строковое обозначение "id" вместо встроенной функции Python
    list_display = ("id", "name", "price", "category")
    list_filter = ("category",)
    search_fields = (
        "name",
        "description",
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Строковое обозначение "id" вместо встроенной функции Python
    list_display = ("id", "name")
