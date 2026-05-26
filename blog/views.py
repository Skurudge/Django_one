from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.conf import settings
from blog.models import BlogPost


class BlogPostListView(ListView):
    """CBV для вывода списка статей блога (доступно всем)."""
    model = BlogPost
    template_name = "blog/blogpost_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        """Фильтрация: выводим только те статьи, у которых флаг публикации True."""
        queryset = super().get_queryset()
        return queryset.filter(is_published=True)


class BlogPostDetailView(DetailView):
    """CBV для отображения отдельной статьи блога (доступно всем)."""
    model = BlogPost
    template_name = "blog/blogpost_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        """Увеличение счетчика просмотров при каждом открытии статьи."""
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()

        # Отправка поздравления при 100 просмотрах
        if obj.views_count == 100:
            send_mail(
                subject="Поздравляем с достижением!",
                message=f"Статья '{obj.title}' набрала 100 просмотров!",
                from_email=getattr(settings, "EMAIL_HOST_USER", "admin@skystore.local"),
                recipient_list=["my_email@example.com"],
                fail_silently=True,
            )

        return obj


class BlogPostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """CBV для создания новой статьи (только для Контент-менеджеров)."""
    model = BlogPost
    fields = ["title", "content", "image", "is_published"]
    template_name = "blog/blogpost_form.html"
    success_url = reverse_lazy("blog:list")
    # Проверка системного разрешения на добавление записи блога
    permission_required = "blog.add_blogpost"


class BlogPostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """CBV для редактирования существующей статьи (только для Контент-менеджеров)."""
    model = BlogPost
    fields = ["title", "content", "image", "is_published"]
    template_name = "blog/blogpost_form.html"
    permission_required = "blog.change_blogpost"

    def get_success_url(self):
        return reverse("blog:detail", kwargs={"pk": self.object.pk})


class BlogPostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """CBV для удаления статьи (только для Контент-менеджеров)."""
    model = BlogPost
    template_name = "blog/blogpost_confirm_delete.html"
    success_url = reverse_lazy("blog:list")
    permission_required = "blog.delete_blogpost"
