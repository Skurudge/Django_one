from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.mail import send_mail
from django.conf import settings
from blog.models import BlogPost


class BlogPostListView(ListView):
    """CBV для вывода списка статей блога."""
    model = BlogPost
    template_name = "blog/blogpost_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        """Фильтрация: выводим только те статьи, у которых флаг публикации True."""
        queryset = super().get_queryset()
        return queryset.filter(is_published=True)


class BlogPostDetailView(DetailView):
    """CBV для отображения отдельной статьи блога."""
    model = BlogPost
    template_name = "blog/blogpost_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        """Увеличение счетчика просмотров при каждом открытии статьи."""
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()

        # Дополнительное задание: отправка поздравления при 100 просмотрах
        if obj.views_count == 100:
            send_mail(
                subject="Поздравляем с достижением!",
                message=f"Статья '{obj.title}' набрала 100 просмотров!",
                from_email=getattr(settings, "EMAIL_HOST_USER", "admin@skystore.local"),
                recipient_list=["my_email@example.com"],
                fail_silently=True,
            )

        return obj


class BlogPostCreateView(CreateView):
    """CBV для создания новой статьи."""
    model = BlogPost
    fields = ["title", "content", "image", "is_published"]
    template_name = "blog/blogpost_form.html"
    success_url = reverse_lazy("blog:list")


class BlogPostUpdateView(UpdateView):
    """CBV для редактирования существующей статьи."""
    model = BlogPost
    fields = ["title", "content", "image", "is_published"]
    template_name = "blog/blogpost_form.html"

    def get_success_url(self):
        """Перенаправление на страницу этой же статьи после её редактирования."""
        return reverse("blog:detail", kwargs={"pk": self.object.pk})


class BlogPostDeleteView(DeleteView):
    """CBV для удаления статьи."""
    model = BlogPost
    template_name = "blog/blogpost_confirm_delete.html"
    success_url = reverse_lazy("blog:list")
