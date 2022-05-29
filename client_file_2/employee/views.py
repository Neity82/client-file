from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views.generic import DetailView

from employee.forms import LoginUserForm
from employee.models import Employee


class LoginEmployee(LoginView):
    """Представление страницы для авторизации пользователя"""

    form_class = LoginUserForm
    template_name = 'employee/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Авторизация'
        return context


class ProfileEmployee(DetailView):
    """Представление страницы профиль сотрудника"""

    model = Employee
    template_name = 'employee/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Профиль'
        return context


def password_change_done(request):
    """Изменение пароля"""

    logout(request)
    return redirect('login')
