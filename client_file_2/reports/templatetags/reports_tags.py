import datetime
from typing import Dict, Union

from django import template
from django.db.models import QuerySet

from client_visit.models import ClientVisit
from employee.models import Office, Employee
from reports.utils import get_dict_date, get_quarter

register = template.Library()


@register.simple_tag
def get_offices(user: Employee) -> QuerySet[Office]:
    """
    Получаем список офисов

    :param user: Сотрудник
    :type user: Employee
    :return: Список офисов
    :rtype: QuerySet[Office]
    """

    result = None
    if user.groups.filter(name__in=['Фронт', 'Директор']).exists():
        result = Office.objects.filter(
            code_office=user.office.code_office
        )
    elif user.groups.filter(name='Управляющий').exists():
        result = Office.objects.exclude(
            code_office=0
        )
    return result


@register.simple_tag
def get_employees(office: Office) -> QuerySet[Employee]:
    """
    Получаем список сотрудников офиса

    :param office: Объект офиса
    :type office: Office
    :return: Список сотрудников
    :rtype: QuerySet[Employee]
    """
    return Employee.objects.filter(
        groups__name='Фронт',
        office=office
    )


@register.simple_tag
def get_data_today() -> Dict[Union[str, Employee], Dict[str, int]]:
    """
    Формируем словарь с данными о продажах за день

    :return: Словарь с данными по продажам
    :rtype: Dict[Union[str, Employee], Dict[str, int]]
    """

    data_dict: Dict = {}
    employee: QuerySet[Employee] = Employee.objects.all()
    data_today: QuerySet[ClientVisit] = ClientVisit.objects.filter(
        date_visit=datetime.date.today()
    )
    data_dict['total'] = {}
    data_dict = get_dict_date(data_dict=data_dict, key='total', list_object=data_today)

    for emp in employee:
        employee_data = data_today.filter(employee=emp)
        data_dict[emp] = {}
        data_dict = get_dict_date(data_dict=data_dict, key=emp, list_object=employee_data)

    return data_dict


@register.simple_tag
def get_data_month() -> Dict[Union[str, Employee], Dict[str, int]]:
    """
    Формируем словарь с данными о продажах за месяц

    :return: Словарь с данными по продажам
    :rtype: Dict[Union[str, Employee], Dict[str, int]]
    """

    data_dict: Dict = {}
    employee: QuerySet[Employee] = Employee.objects.all()
    end = datetime.date.today()
    start = datetime.datetime.strptime(f'{end.year}-{end.month}-01', '%Y-%m-%d')
    data_month: QuerySet[ClientVisit] = ClientVisit.objects.filter(
        date_visit__range=[start, end]
    )
    data_dict['total'] = {}
    data_dict = get_dict_date(data_dict=data_dict, key='total', list_object=data_month)

    for emp in employee:
        employee_data = data_month.filter(employee=emp)
        data_dict[emp] = dict()

        data_dict = get_dict_date(data_dict=data_dict, key=emp, list_object=employee_data)

    return data_dict


@register.simple_tag
def get_data_quarter() -> Dict[Union[str, Employee], Dict[str, int]]:
    """
    Формируем словарь с данными о продажах за квартал

    :return: Словарь с данными по продажам
    :rtype: Dict[Union[str, Employee], Dict[str, int]]
    """

    data_dict: Dict = {}
    employee: QuerySet[Employee] = Employee.objects.all()

    end = datetime.date.today()
    quarter = get_quarter(end.month)
    if quarter == 1:
        start = datetime.datetime.strptime(f'{end.year}-01-01', '%Y-%m-%d')
    elif quarter == 2:
        start = datetime.datetime.strptime(f'{end.year}-04-01', '%Y-%m-%d')
    elif quarter == 3:
        start = datetime.datetime.strptime(f'{end.year}-07-01', '%Y-%m-%d')
    else:
        start = datetime.datetime.strptime(f'{end.year}-10-01', '%Y-%m-%d')

    data_quarter = ClientVisit.objects.filter(
        date_visit__range=[start, end]
    )
    data_dict['total'] = dict()
    data_dict = get_dict_date(data_dict=data_dict, key='total', list_object=data_quarter)

    for emp in employee:
        employee_data = data_quarter.filter(employee=emp)
        data_dict[emp] = dict()

        data_dict = get_dict_date(data_dict=data_dict, key=emp, list_object=employee_data)

    return data_dict


