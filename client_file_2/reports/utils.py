from typing import Dict, Union

from django.db.models import Sum, QuerySet
from django.db.models.functions import Coalesce

from client_visit.models import ClientVisit
from employee.models import Employee


def get_month_name(month_num: int) -> str:
    """
    Формируем название месяца

    :param month_num: Порядковый номер месяца
    :type month_num: int
    :return: Название месяца
    :rtype: str
    """

    month_dict: Dict = {
        1: 'январь',
        2: 'февраль',
        3: 'март',
        4: 'апрель',
        5: 'май',
        6: 'июнь',
        7: 'июль',
        8: 'август',
        9: 'сентябрь',
        10: 'октябрь',
        11: 'ноябрь',
        12: 'декабрь',
    }
    return month_dict[month_num]


def get_quarter(month: int) -> int:
    """
    Определяем порядковый номер квартала

    :param month: Порядковый номер месяца
    :type month: int
    :return: Номер квартала
    :rtype: int
    """

    quarter = ''
    if month in [1, 2, 3]:
        quarter = 1
    elif month in [4, 5, 6]:
        quarter = 2
    elif month in [7, 8, 9]:
        quarter = 3
    elif month in [10, 11, 12]:
        quarter = 4
    return quarter


def get_dict_date(
        data_dict: Dict[str, Dict],
        key: Union[str, Employee],
        list_object: QuerySet[ClientVisit]
) -> Dict[Union[str, Employee], Dict[str, int]]:
    """
    Формируем словарь с данными по продажам

    :param data_dict: Словарь
    :type data_dict: Dict[str, Dict]
    :param key: Либо имя сотрудника по которому считаем, либо офис в целом
    :type key: Union[str, Employee]
    :param list_object: Список визитов клиентов за период
    :type list_object: QuerySet[ClientVisit]
    :return: Словарь с данными по продажам
    :rtype: Dict[Union[str, Employee], Dict[str, int]]
    """

    data_dict[key]['kn_quantity'] = list_object.filter(
        credit_result='Оформлено'
    ).count()

    kn_sum = list_object.filter(
        credit_result='Оформлено'
    ).aggregate(
        sum=Coalesce(Sum('credit_sum'), 0)
    )

    data_dict[key]['kn_sum'] = int(kn_sum['sum'] / 1000)

    kn_ins_sum = list_object.filter(
        credit_insurance_result='Оформлено'
    ).aggregate(
        sum=Coalesce(Sum('credit_insurance_sum'), 0)
    )

    data_dict[key]['kn_ins_sum'] = int(kn_ins_sum['sum'] / 1000)

    data_dict[key]['izp_quantity'] = list_object.filter(
        izp_result='Оформлено'
    ).count()

    data_dict[key]['pension_quantity'] = list_object.filter(
        pension_result='Оформлено'
    ).count()

    data_dict[key]['package_vip_quantity'] = list_object.filter(
        service_package_result='Оформлено',
        service_package_type='Привилегия'
    ).count()

    data_dict[key]['kk_quantity'] = list_object.filter(
        credit_card_result='Оформлено'
    ).count()

    data_dict[key]['package_quantity'] = list_object.filter(
        service_package_result='Оформлено',
        service_package_type='Мультикарта'
    ).count()

    npo_sum = list_object.filter(
        npo_result='Оформлено'
    ).aggregate(
        sum=Coalesce(Sum('npo_sum'), 0)
    )

    data_dict[key]['npo_sum'] = int(npo_sum['sum'] / 1000)

    data_dict[key]['broker_nav'] = list_object.filter(
        broker_navigate_result='Оформлено'
    ).count()

    ksp_sum = list_object.filter(
        ksp_result='Оформлено'
    ).aggregate(
        sum=Coalesce(Sum('ksp_sum'), 0)
    )

    data_dict[key]['ksp_sum'] = int(ksp_sum['sum'] / 1000)

    isg_sum = list_object.filter(
        isg_result='Оформлено'
    ).aggregate(
        sum=Coalesce(Sum('isg_sum'), 0)
    )
    data_dict[key]['isg_sum'] = int(isg_sum['sum'] / 1000)

    nsg_sum = list_object.filter(
        nsg_result='Оформлено'
    ).aggregate(
        sum=Coalesce(Sum('nsg_sum'), 0)
    )
    data_dict[key]['nsg_sum'] = int(nsg_sum['sum'] / 1000)

    return data_dict
