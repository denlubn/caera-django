from django import forms
from django.contrib.auth.forms import UserCreationForm

from caera.models import Proposal, Tag, User


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        labels = {
            'name': 'Назва',
        }


class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = "__all__"
        labels = {
            "title": "Заголовок",
            "image_url": "Посилання на зображення",
            "description": "Опис",
            "city": "Місто",
            "tags": "Теги",
            "author": "Автор",
            "created_at": "Дата створення",
        }


class ProposalSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Пошук по назві"})
    )


# image = forms.ImageField(
#         label="Select image for car",
#         required=False,
#     )

class ProfileCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "email",
        )
        labels = {
            "username": "Ім’я користувача",
            "first_name": "Ім’я",
            "last_name": "Прізвище",
            "email": "Електронна пошта",
            "password1": "Пароль",
            "password2": "Підтвердження пароля",
        }
        help_texts = {
            "username": "Обов’язково. Не більше 150 символів. Літери, цифри та символи @/./+/-/_",
            "password1": (
                "<ul>"
                "<li>Ваш пароль не повинен бути надто схожим на іншу особисту інформацію.</li>"
                "<li>Ваш пароль має містити щонайменше 8 символів.</li>"
                "<li>Пароль не повинен бути занадто поширеним.</li>"
                "<li>Пароль не повинен складатися лише з цифр.</li>"
                "</ul>"
            ),
            "password2": "Введіть той самий пароль ще раз для перевірки.",
        }
