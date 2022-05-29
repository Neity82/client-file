from django.db import models

from employee.models import Employee

BANK_CHOICES = [
    ('ВТБ', 'ВТБ'),
    ('Сбербанк', 'Сбербанк'),
    ('СГБ', 'СГБ'),
    ('ПочтаБанк', 'ПочтаБанк'),
    ('Тинькофф', 'Тинькофф'),
    ('Альфа', 'Альфа'),
    ('Наличка', 'Наличка'),
    ('Другой', 'Другой'),
    ('Нет', 'Нет'),
]

PRODUCT_CHOICES = [
    ('Кредит наличными', 'Кредит наличными'),
    ('Кредитная карта', 'Кредитная карта'),
    ('Депозит', 'Депозит'),
    ('Зарплатная карта', 'Зарплатная карта'),
    ('Пакет услуг', 'Пакет услуг'),
    ('Сервис', 'Сервис'),
]

RESULT_CHOICES = [
    ('Оформлено', 'Оформлено'),
    ('Думает', 'Думает'),
    ('Отказ', 'Отказ'),
    ('Уже есть', 'Уже есть'),
    ('Планирует оформить', 'Планирует оформить'),
    ('', ''),
]

TYPE_NEXT_CONTACT_CHOICES = [
    ('Звонок', 'Звонок'),
    ('Визит', 'Визит'),
]

TYPE_PACKAGE_CHOICES = [
    ('Мультикарта', 'Мультикарта'),
    ('Привилегия', 'Привилегия'),
]


class SalaryProject(models.Model):
    """Модель зарплатных проектов"""

    inn = models.IntegerField(verbose_name='ИНН')

    objects = models.Manager()

    class Meta:
        db_table = 'salary_project'
        verbose_name = 'зарплатный проект'
        verbose_name_plural = 'зарплатные проекты'

    def __str__(self) -> str:
        return str(self.inn)


class ClientVisit(models.Model):
    """Модель визит клиента"""

    employee = models.ForeignKey(
        Employee,
        models.CASCADE,
        related_name='client_visit',
        verbose_name='сотрудник'
    )

    date_visit = models.DateField(
        auto_now_add=True,
        verbose_name='дата создания'
    )

    first_name_client = models.CharField(
        max_length=150,
        verbose_name='имя клиента'
    )

    middle_name_client = models.CharField(
        max_length=150,
        verbose_name='отчество клиента'
    )

    last_name_client = models.CharField(
        max_length=150,
        verbose_name='фамилия клиента'
    )

    date_of_birth = models.CharField(
        max_length=10,
        verbose_name='дата рождения клиента'
    )

    inn_employer = models.IntegerField(
        verbose_name='инн работодателя',
        blank=True,
        default=0
    )

    salary_bank = models.CharField(
        max_length=50,
        verbose_name='зарплатный банк',
        choices=BANK_CHOICES,
        default='Другой'
    )

    pension_bank = models.CharField(
        max_length=50,
        verbose_name='пенсионный банк',
        choices=BANK_CHOICES,
        default='Нет'
    )

    main_product = models.CharField(
        max_length=50,
        verbose_name='продукт',
        choices=PRODUCT_CHOICES
    )

    credit_result = models.CharField(
        max_length=50,
        verbose_name='кн результат',
        choices=RESULT_CHOICES,
        blank=True
    )

    credit_sum = models.IntegerField(
        verbose_name='кн сумма',
        default=0
    )

    credit_comment = models.TextField(
        verbose_name='кн комментарии',
        blank=True
    )

    credit_insurance_result = models.CharField(
        max_length=50,
        verbose_name='фз кн результат',
        choices=RESULT_CHOICES,
        blank=True
    )

    credit_insurance_sum = models.IntegerField(
        verbose_name='фз кн сумма',
        default=0
    )

    credit_insurance_comment = models.TextField(
        verbose_name='фз кн комментарии',
        blank=True
    )

    credit_card_result = models.CharField(
        max_length=50,
        verbose_name='кк результат',
        choices=RESULT_CHOICES,
        blank=True
    )

    credit_card_comment = models.TextField(
        verbose_name='кк комментарии',
        blank=True
    )

    credit_card_insurance_result = models.CharField(
        max_length=50,
        verbose_name='фз кк результат',
        choices=RESULT_CHOICES,
        blank=True
    )

    credit_card_insurance_comment = models.TextField(
        verbose_name='фз кк комментарии',
        blank=True
    )

    deposit_result = models.CharField(
        max_length=50,
        verbose_name='депозит результат',
        choices=RESULT_CHOICES,
        blank=True
    )

    deposit_sum = models.IntegerField(
        verbose_name='депозит сумма',
        default=0
    )

    deposit_comment = models.TextField(
        verbose_name='депозит комментарии',
        blank=True
    )

    service_package_result = models.CharField(
        max_length=50,
        verbose_name='пу результат',
        choices=RESULT_CHOICES,
        blank=True
    )

    service_package_type = models.CharField(
        max_length=50,
        verbose_name='тип пу',
        choices=TYPE_PACKAGE_CHOICES,
        blank=True
    )

    service_package_comment = models.TextField(
        verbose_name='пу комментарии',
        blank=True
    )

    izp_result = models.CharField(
        max_length=50,
        verbose_name='изп результат',
        choices=RESULT_CHOICES,
        blank=True
    )

    izp_comment = models.TextField(
        verbose_name='изп комментарии',
        blank=True
    )

    pension_result = models.CharField(
        max_length=50,
        verbose_name='перевод пенсии результат',
        choices=RESULT_CHOICES,
        blank=True
    )

    pension_comment = models.TextField(
        verbose_name='перевод пенсии комментарии',
        blank=True
    )

    ksp_result = models.CharField(
        max_length=50,
        verbose_name='ксп результат',
        choices=RESULT_CHOICES,
        blank=True
    )

    ksp_sum = models.IntegerField(
        verbose_name='ксп сумма',
        default=0
    )

    ksp_comment = models.TextField(
        verbose_name='ксп комментарии',
        blank=True
    )

    broker_navigate_result = models.CharField(
        max_length=50,
        verbose_name='лиды БО',
        choices=RESULT_CHOICES,
        blank=True
    )

    broker_navigate_comment = models.TextField(
        verbose_name='лиды БО комментарии',
        blank=True
    )

    nsg_result = models.CharField(
        max_length=50,
        verbose_name='нсж результат',
        choices=RESULT_CHOICES,
        blank=True
    )

    nsg_sum = models.IntegerField(
        verbose_name='нсж сумма',
        default=0
    )

    nsg_comment = models.TextField(
        verbose_name='нсж комментарии',
        blank=True
    )

    isg_result = models.CharField(
        max_length=50,
        verbose_name='исж результат',
        choices=RESULT_CHOICES,
        blank=True
    )

    isg_sum = models.IntegerField(
        verbose_name='исж сумма',
        default=0
    )

    isg_comment = models.TextField(
        verbose_name='исж комментарии',
        blank=True
    )

    npo_result = models.CharField(
        max_length=50,
        verbose_name='нпо результат',
        choices=RESULT_CHOICES,
        blank=True
    )

    npo_sum = models.IntegerField(
        verbose_name='нпо сумма',
        default=0
    )

    npo_comment = models.TextField(
        verbose_name='нпо комментарии',
        blank=True
    )

    date_next_contact = models.DateField(
        verbose_name='дата следующего контакта',
        blank=True,
        null=True
    )

    type_next_contact = models.CharField(
        max_length=50,
        verbose_name='тип следующего контакта',
        choices=TYPE_NEXT_CONTACT_CHOICES,
        blank=True
    )

    total_comment = models.TextField(
        verbose_name='итоговые комментарии',
        blank=True
    )

    objects = models.Manager()

    class Meta:
        db_table = 'client_visit'
        verbose_name = 'визит клиента'
        verbose_name_plural = 'визиты клиентов'
        ordering = ['-date_visit']

    def __str__(self) -> str:
        return f'{self.date_visit} - ' \
               f'{self.employee} - ' \
               f'{self.last_name_client} - ' \
               f'{self.main_product}'


class ClientCall(models.Model):
    """Модель звонок клиенту"""

    employee = models.ForeignKey(
        Employee,
        models.CASCADE,
        related_name='client_call',
        verbose_name='сотрудник'
    )

    date_call = models.DateField(
        auto_now_add=True,
        verbose_name='дата создания'
    )

    first_name_client = models.CharField(
        max_length=150,
        verbose_name='имя клиента'
    )

    middle_name_client = models.CharField(
        max_length=150,
        verbose_name='отчество клиента',
        blank=True
    )

    last_name_client = models.CharField(
        max_length=150,
        verbose_name='фамилия клиента',
        blank=True
    )

    date_of_birth = models.CharField(
        max_length=10,
        verbose_name='дата рождения клиента',
        blank=True
    )

    main_product = models.CharField(
        max_length=50,
        verbose_name='продукт',
        choices=PRODUCT_CHOICES
    )

    result = models.CharField(
        max_length=50,
        verbose_name='результат звонка',
        choices=RESULT_CHOICES
    )

    sum = models.IntegerField(
        verbose_name='сумма',
        default=0
    )

    comment = models.TextField(
        verbose_name='комментарии',
        blank=True
    )

    date_next_contact = models.DateField(
        verbose_name='дата следующего контакта',
        blank=True,
        null=True
    )

    type_next_contact = models.CharField(
        max_length=50,
        verbose_name='тип следующего контакта',
        choices=TYPE_NEXT_CONTACT_CHOICES,
        blank=True
    )

    objects = models.Manager()

    class Meta:
        db_table = 'client_call'
        verbose_name = 'звонок клиенту'
        verbose_name_plural = 'звонки клиентам'
        ordering = ['-date_call']

    def __str__(self) -> str:
        return f'{self.date_call} - ' \
               f'{self.employee} - ' \
               f'{self.last_name_client} - ' \
               f'{self.main_product}'
