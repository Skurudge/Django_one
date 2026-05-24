from django.urls import path
from users.apps import UsersConfig
from users.views import RegisterView, UserLoginView, UserLogoutView, ProfileView

app_name = UsersConfig.name

urlpatterns = [
    # Вход на сайт
    path("login/", UserLoginView.as_view(), name="login"),

    # Выход с сайта
    path("logout/", UserLogoutView.as_view(), name="logout"),

    # Регистрация
    path("register/", RegisterView.as_view(), name="register"),

    # Редактирование профиля (Дополнительное задание)
    path("profile/", ProfileView.as_view(), name="profile"),
]
