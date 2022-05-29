from django.contrib import admin

from salary_project.models import SalaryProject


@admin.register(SalaryProject)
class SalaryProjectAdmin(admin.ModelAdmin):
    """Представление модели зарплатных проектов в интерфейсе администратора"""

    list_display = ['inn']
    list_display_links = ['inn']
