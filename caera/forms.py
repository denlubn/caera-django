from django import forms
from django.contrib.auth.forms import UserCreationForm

from caera.models import Proposal, Tag, User, City, Project, Comment


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        labels = {
            'name': 'Назва',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'Текст',
        }


class ProposalForm(forms.ModelForm):
    image = forms.ImageField(
        label="Зображення",
        required=False,
    )

    class Meta:
        model = Proposal
        fields = "__all__"
        exclude = ['author']
        labels = {
            "title": "Заголовок",
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
        widget=forms.TextInput(attrs={"placeholder": "Пошук за назвою"})
    )

    tags = forms.ModelChoiceField(
        queryset=Tag.objects.none(),
        required=False,
        label="",
        empty_label="Усі теги",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    city = forms.ModelChoiceField(
        queryset=City.objects.none(),
        required=False,
        label="",
        empty_label="Усі міста",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tags"].queryset = Tag.objects.all()
        self.fields["city"].queryset = City.objects.all()


class ProjectForm(forms.ModelForm):
    image = forms.ImageField(
        label="Зображення",
        required=True,
    )

    class Meta:
        model = Project
        fields = "__all__"
        exclude = ['author', 'proposal']
        labels = {
            "title": "Заголовок",
            "proposal": "Пропозиція",
            "description": "Опис",
            "city": "Місто",
            "tags": "Теги",
            "author": "Автор",
            "created_at": "Дата створення",
        }


class ProfileCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "email",
        )
        labels = {
            "username": "Псевдонім",
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


class ProfileUpdateForm(forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            "username": "Псевдонім",
            "first_name": "Ім’я",
            "last_name": "Прізвище",
            "email": "Електронна пошта",
        }
        help_texts = {
            "username": "Обов’язково. Не більше 150 символів. Літери, цифри та символи @/./+/-/_",}

