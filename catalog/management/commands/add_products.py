from django.core.management.base import BaseCommand
from catalog.models import Product, Category
from django.contrib.auth import get_user_model
from datetime import date


class Command(BaseCommand):
    help = "Наполняет базу данных тестовыми категориями и продуктами с привязкой владельца"

    def handle(self, *args, **options):
        # 1. Сначала очищаем старые продукты и категории, чтобы не было дублей
        Product.objects.all().delete()
        Category.objects.all().delete()

        # 2. Получаем или создаем системного пользователя для назначения владельцем
        User = get_user_model()
        system_user = User.objects.first()

        if not system_user:
            # Если в базе совсем нет пользователей, создаем технического администратора
            system_user = User.objects.create_superuser(
                email="admin@skystore.local",
                password="adminpassword"
            )
            self.stdout.write(self.style.WARNING("Создан суперпользователь admin@skystore.local"))

        # 3. Создаем тестовые категории
        cat_pens = Category.objects.create(name="ручки", description="различные шариковые ручки")
        cat_pencils = Category.objects.create(name="карандаши", description="различные грифельные карандаши")

        # 4. Наполняем базу продуктами (ставим is_published=True, чтобы их было видно всем)
        products_to_create = [
            Product(
                name="красная ручка",
                description="красная шариковая ручка",
                category=cat_pens,
                price=32.20,
                created_at=date(2026, 2, 12),
                updated_at=date(2026, 2, 15),
                is_published=True,
                owner=system_user
            ),
            Product(
                name="черный карандаш",
                description="черный кохинор",
                category=cat_pencils,
                price=35.00,
                created_at=date(2026, 3, 2),
                updated_at=date(2026, 3, 2),
                is_published=True,
                owner=system_user
            ),
            Product(
                name="черная ручка",
                description="различные шариковые ручки",
                category=cat_pens,
                price=500.00,
                created_at=date(2026, 1, 13),
                updated_at=date(2026, 3, 3),
                is_published=True,
                owner=system_user
            ),
        ]

        Product.objects.bulk_create(products_to_create)
        self.stdout.write(self.style.SUCCESS("База данных успешно наполнена тестовыми продуктами!"))

