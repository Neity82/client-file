from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.urls import path

from employee.views import LoginEmployee, ProfileEmployee, password_change_done

urlpatterns = [
    path('login/', LoginEmployee.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>', ProfileEmployee.as_view(), name='profile'),
    path('password-change/', PasswordChangeView.as_view(template_name='employee/password_change.html'),
         name='password_change'),
    path('password-change/done/', password_change_done, name='password_change_done'),
]
