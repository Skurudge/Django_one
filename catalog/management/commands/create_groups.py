from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product
from blog.models import BlogPost


class Command(BaseCommand):
    help = "Создает группы пользователей и назначает им соответствующие права доступа"

    def handle(self, *args, **options):
        # 1. Настройка группы Модератор продуктов
        moderator_group, created = Group.objects.get_or_create(name="Модератор продуктов")

        # Получаем необходимые разрешения для модератора
        product_content_type = ContentType.objects.get_for_model(Product)
        can_unpublish = Permission.objects.get(
            codename="can_unpublish_product",
            content_type=product_content_type
        )
        can_delete_product = Permission.objects.get(
            codename="delete_product",
            content_type=product_content_type
        )

        # Назначаем права группе модераторов
        moderator_group.permissions.set([can_unpublish, can_delete_product])
        self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" успешно настроена.'))

        # 2. Настройка группы Контент-менеджер (Дополнительное задание)
        content_manager_group, created = Group.objects.get_or_create(name="Контент-менеджер")

        # Получаем все разрешения для модели блога
        blog_content_type = ContentType.objects.get_for_model(BlogPost)
        blog_permissions = Permission.objects.filter(content_type=blog_content_type)

        # Назначаем контент-менеджерам все права на CRUD блога
        content_manager_group.permissions.set(blog_permissions)
        self.stdout.write(self.style.SUCCESS('Группа "Контент-менеджер" успешно настроена.'))
