from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from employee.forms import UserCreationForm, UserChangeForm
from employee.models import Employee, Office


@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    """Представление модели сотрудника в интерфейсе администратора"""

    form = UserChangeForm
    add_form = UserCreationForm
    save_on_top = True

    list_display = [
        'id',
        'last_name',
        'first_name',
        'middle_name',
        'office',
        'get_groups'
    ]
    list_display_links = ['id', 'last_name']
    list_filter = ['office']

    fieldsets = (
        (None, {'fields': ('username',
                           'password',
                           'office')}
         ),
        ('Персональная информация', {'fields': ('last_name',
                                                'first_name',
                                                'middle_name',)}
         ),
        ('Права доступа', {'fields': ('is_staff',
                                      'is_active',
                                      'is_superuser',
                                      'groups',
                                      'user_permissions')}
         ),
        ('Важные даты', {'fields': ('last_login',
                                    'date_joined',)}
         ),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username',
                       'last_name',
                       'first_name',
                       'middle_name',
                       'office',
                       'password1',
                       'password2')
        }
         ),
    )

    def get_groups(self, obj) -> str:
        """
        Получаем перечень групп, в которые входит сотрудник

        :param obj: Сотрудник
        :type obj: Employee
        :return: Перечень групп
        :rtype: str
        """

        groups = obj.groups.all()
        groups_list = []
        if groups:
            for i in groups:
                groups_list.append(str(i))
            groups_str = ', '.join(groups_list)
            return groups_str

    get_groups.short_description = 'группа'


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    """Представление модели офиса в интерфейсе администратора"""

    list_display = ['code_office', 'name']
