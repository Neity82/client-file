from django.contrib import admin

from client_visit.models import ClientVisit, ClientCall


@admin.register(ClientVisit)
class ClientVisitAdmin(admin.ModelAdmin):
    """Представление модели визит клиента в интерфейсе администратора"""

    list_display = [
        'date_visit',
        'employee',
        'last_name_client',
        'main_product',
        'date_next_contact'
    ]

    list_display_links = ['date_visit']
    list_filter = ['employee', 'main_product']
    save_on_top = True


@admin.register(ClientCall)
class ClientVisitAdmin(admin.ModelAdmin):
    """Представление модели звонок клиенту в интерфейсе администратора"""

    list_display = [
        'date_call',
        'employee',
        'last_name_client',
        'main_product',
        'date_next_contact'
    ]

    list_display_links = ['date_call']
    list_filter = ['employee', 'main_product']
    save_on_top = True

