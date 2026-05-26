from django.db import models
from django.conf import settings


class Category(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.CharField(max_length=150, verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["name"]


class Product(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.CharField(max_length=150, verbose_name="Описание")
    image = models.ImageField(upload_to="static/products/images", blank=True, null=True, verbose_name="Изображение")
    category = models.ForeignKey(
        to="Category",
        on_delete=models.SET_NULL,
        max_length=100,
        verbose_name="Категория",
        blank=True,
        null=True,
        related_name="products",
    )
    price = models.DecimalField(verbose_name="Цена за покупку", max_digits=8, decimal_places=2)
    created_at = models.DateField(verbose_name="Дата создания")
    updated_at = models.DateField(verbose_name="Дата последнего изменения")

    # Новые поля для Задания 1 и Задания 2
    is_published = models.BooleanField(default=False, verbose_name="Признак публикации")
    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Владелец",
        related_name="products"
    )

    def __str__(self):
        return f"продукт '{self.name}' из категории '{self.category}'"

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ["category", "name"]

        # Кастомные права доступа согласно ТЗ Задания 1
        permissions = [
            ("can_unpublish_product", "Can unpublish product"),
        ]
