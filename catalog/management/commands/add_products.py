from django.core.management.base import BaseCommand
from catalog.models import Category, Product

class Command(BaseCommand):
    help = "Кастомная команда для добавления тестовых продуктов."

    def handle(self, *args, **kwargs):
        # Полная очистка таблиц перед наполнением
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создание тестовых категорий
        category1, _ = Category.objects.get_or_create(name="ручки", description="различные пишущие ручки")
        category2, _ = Category.objects.get_or_create(name="карандаши", description="грифельные карандаши")

        # Список тестовых продуктов
        products = [
            {
                "name": "красная ручка",
                "description": "красная гелевая ручка",
                "category": category1,
                "price": 350.0,
                "created_at": "2025-12-24",
                "updated_at": "2025-12-30",
            },
            {
                "name": "синяя ручка",
                "description": "синяя шариковая ручка",
                "category": category1,
                "price": 150.0,
                "created_at": "2025-12-31",
                "updated_at": "2026-02-11",
            },
            {
                "name": "черная ручка",
                "description": "черная гелевая ручка",
                "category": category1,
                "price": 300.0,
                "created_at": "2025-12-27",
                "updated_at": "2025-12-30",
            },
            {
                "name": "черный карандаш",
                "description": "карандаш кохинор",
                "category": category2,
                "price": 500.0,
                "created_at": "2026-01-15",
                "updated_at": "2026-02-11",
            },
            {
                "name": "красный карандаш",
                "description": "красный грифельный карандаш",
                "category": category2,
                "price": 350.0,
                "created_at": "2025-12-27",
                "updated_at": "2026-02-11",
            },
        ]

        # Сохранение продуктов в базу данных
        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Успешно добавлен продукт {product.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Продукт уже существует: {product.name}"))
