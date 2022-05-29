import datetime
from typing import List

from django import template

from salary_project.models import SalaryProject

register = template.Library()


@register.simple_tag
def get_salary_project(inn: int) -> str:
    """
    Проверяем по ИНН принадлежность организации к зарплатным проектам

    :param inn: ИНН организации
    :type inn: int
    :return: Строка с ответом 'Да' или 'Нет'
    :rtype: str
    """
    if SalaryProject.objects.filter(inn=inn).first():
        return 'Да'
    else:
        return 'Нет'


@register.simple_tag
def is_pension(middle_name: str, date_of_birth: str) -> str:
    """Проверяем является ли пенсионером

    :param middle_name: Отчество
    :type middle_name: str
    :param date_of_birth: Дата рождения
    :type date_of_birth: str
    :return: Строка с ответом 'Пенсионер' или 'Не пенсионер'
    :type: str
    """
    date_now: datetime = datetime.date.today()
    date_of_birth = '-'.join(reversed(date_of_birth.split('.')))
    date_of_birth = datetime.datetime.strptime(date_of_birth, '%Y-%m-%d')
    age = date_now.year - date_of_birth.year
    if middle_name.endswith('a'):
        if age >= 55:
            return 'Пенсионер'
        else:
            return 'Не пенсионер'
    else:
        if age >= 60:
            return 'Пенсионер'
        else:
            return 'Не пенсионер'


@register.simple_tag
def get_date_list():
    """
    Получаем список ближайших 10 рабочих дней (с субботами)

    :return: Список дат
    :rtype: List[datetime]
    """

    date_now: datetime = datetime.date.today()
    date_list = list()
    for i in range(14):
        if len(date_list) == 10:
            break
        date = date_now + datetime.timedelta(days=i)
        if date.weekday() != 6:
            date_list.append(date)
    return date_list


