from django.urls import path
from blog.apps import BlogConfig
from blog.views import (
    BlogPostListView,
    BlogPostDetailView,
    BlogPostCreateView,
    BlogPostUpdateView,
    BlogPostDeleteView,
)

app_name = BlogConfig.name

urlpatterns = [
    # Список всех опубликованных статей
    path("blogs/", BlogPostListView.as_view(), name="list"),

    # Детальная страница статьи
    path("blogs/<int:pk>/", BlogPostDetailView.as_view(), name="detail"),

    # Создание статьи
    path("blogs/create/", BlogPostCreateView.as_view(), name="create"),

    # Редактирование статьи
    path("blogs/<int:pk>/update/", BlogPostUpdateView.as_view(), name="update"),

    # Удаление статьи
    path("blogs/<int:pk>/delete/", BlogPostDeleteView.as_view(), name="delete"),
]
