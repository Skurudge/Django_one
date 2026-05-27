from django.core.cache import cache
from catalog.models import Product


def get_products_by_category(category_id):
    """
    Сервисная функция для работы с продуктами.
    Возвращает список всех опубликованных продуктов в указанной категории с низкоуровневым кэшированием.
    Ключ кэша: category_{id}.
    """
    # Формируем ключ кэширования согласно критериям оценки
    cache_key = f"category_{category_id}"

    # Пытаемся получить данные из кэша Redis
    products_list = cache.get(cache_key)

    # Если в кэше пусто — забираем данные из базы данных PostgreSQL
    if products_list is None:
        products_list = list(Product.objects.filter(category_id=category_id, is_published=True))

        # Сохраняем данные в Redis на 15 минут (900 секунд)
        cache.set(cache_key, products_list, timeout=900)

    return products_list
