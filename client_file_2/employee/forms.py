from django.contrib.auth.forms import AuthenticationForm, ReadOnlyPasswordHashField
from django import forms

from employee.models import Employee


class UserCreationForm(forms.ModelForm):
    """Форма для создания нового пользователя."""

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput)

    class Meta:
        model = Employee
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    Форма, используемая в интерфейсе администратора
    для изменения информации о пользователе и его списка прав.
    """
    password = ReadOnlyPasswordHashField(
        label='Пароль',
        help_text='Необработанные пароли не сохраняются, '
                  'поэтому нет возможности увидеть пароль этого пользователя,'
                  ' но вы можете изменить пароль с помощью '
                  '<a href="{}">этой формы</a>.',
    )

    class Meta:
        model = Employee
        fields = ('username', 'last_name', 'first_name', 'middle_name', 'password', 'office')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format('../password/')
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')

    def clean_password(self):
        return self.initial["password"]


class LoginUserForm(AuthenticationForm):
    """Форма для авторизации пользователя"""

    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
