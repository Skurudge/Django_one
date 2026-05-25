from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.conf import settings
from users.models import User
from users.forms import UserRegisterForm, UserLoginForm, UserProfileForm


class RegisterView(CreateView):
    """CBV для регистрации пользователей с отправкой приветственного письма."""
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        # Сохраняем пользователя в базу данных
        response = super().form_valid(form)
        user = self.object

        # Логика отправки приветственного письма согласно ТЗ
        send_mail(
            subject="Добро пожаловать в Skystore!",
            message=(
                f"Здравствуйте, {user.email}!\n\n"
                f"Вы успешно зарегистрировались на платформе Skystore.\n"
                f"Теперь вам доступны все возможности управления каталогом товаров.\n\n"
                f"С уважением,\nКоманда Skystore"
            ),
            from_email=getattr(settings, "EMAIL_HOST_USER", "admin@skystore.local"),
            recipient_list=[user.email],
            fail_silently=True,
        )
        return response


class UserLoginView(LoginView):
    """CBV для авторизации пользователей по email."""
    form_class = UserLoginForm
    template_name = "users/login.html"


class UserLogoutView(LogoutView):
    """CBV для выхода из учетной записи."""
    next_page = reverse_lazy("catalog:home")


class ProfileView(LoginRequiredMixin, UpdateView):
    """CBV для редактирования профиля пользователя (Дополнительное задание)."""
    model = User
    form_class = UserProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        # Возвращаем текущего авторизованного пользователя
        return self.request.user
