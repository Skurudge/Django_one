from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from users.models import User


class UserRegisterForm(forms.ModelForm):
    """Форма для регистрации нового пользователя с подтверждением пароля."""
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password_confirm = forms.CharField(
        label="Подтвердите пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["class"] = "form-control"

    def clean_password_confirm(self):
        """Проверка совпадения двух введенных паролей."""
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Пароли не совпадают. Повторите ввод.")
        return password_confirm

    def save(self, commit=True):
        """Хеширование пароля перед сохранением пользователя в базу."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """Форма авторизации по электронной почте (email)."""
    username = forms.EmailField(
        label="Электронная почта",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "email@example.com"})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class UserProfileForm(forms.ModelForm):
    """Форма для редактирования профиля пользователя (Дополнительное задание)."""
    class Meta:
        model = User
        fields = ("avatar", "phone", "country", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.FileInput):
                field.widget.attrs["class"] = "form-control"
