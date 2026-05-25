from django import forms
from django.core.exceptions import ValidationError
from catalog.models import Product

# Константа со списком запрещенных слов согласно критериям оценки
FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name", "description", "image", "category", "price", "is_published")

    def __init__(self, *args, **kwargs):
        """Стилизация всех полей формы под Bootstrap."""
        # Извлекаем кастомный флаг, переданный из контроллера
        is_moderator = kwargs.pop("is_moderator", False)
        super().__init__(*args, **kwargs)

        # Если пользователь не модератор/суперпользователь, скрываем поле публикации
        if not is_moderator:
            self.fields["is_published"].widget = forms.HiddenInput()
            self.fields["is_published"].required = False

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            elif not isinstance(field.widget, forms.HiddenInput):
                field.widget.attrs["class"] = "form-control"

    def clean_name(self):
        """Валидация названия на отсутствие запрещенных слов и автоматическое приведение к нижнему регистру."""
        name = self.cleaned_data.get("name")
        if name:
            name_lower = name.lower()
            for word in FORBIDDEN_WORDS:
                if word in name_lower:
                    raise ValidationError(
                        f"Название товара не может содержать запрещенное слово: '{word}'."
                    )
            return name_lower
        return name

    def clean_description(self):
        """Валидация описания на отсутствие запрещенных слов (без учета регистра)."""
        description = self.cleaned_data.get("description")
        if description:
            lower_description = description.lower()
            for word in FORBIDDEN_WORDS:
                if word in lower_description:
                    raise ValidationError(
                        f"Описание товара не может содержать запрещенное слово: '{word}'."
                    )
        return description

    def clean_price(self):
        """Валидация цены на отсутствие отрицательных значений."""
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise ValidationError(
                "Цена продукта не может быть отрицательной. Укажите корректную стоимость."
            )
        return price

    def clean_image(self):
        """Валидация формата (JPEG/PNG) и размера изображения (до 5 МБ)."""
        image = self.cleaned_data.get("image")
        if image:
            max_size = 5 * 1024 * 1024
            if image.size > max_size:
                raise ValidationError("Размер изображения не должен превышать 5 МБ.")

            valid_extensions = ["image/jpeg", "image/png", "image/jpg"]
            content_type = getattr(image, "content_type", "")
            if content_type not in valid_extensions:
                raise ValidationError("Допускаются только изображения в формате JPEG или PNG.")
        return image
