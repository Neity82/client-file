import re

from django import forms
from django.core.exceptions import ValidationError

from client_visit.models import ClientVisit, ClientCall


def inn_valid(inn: int) -> bool:
    """
    Проверка ИНН организации на корректность (количество знаков 10 или 12)

    :param inn: ИНН организации
    :type inn: int
    :return: Булевое значение
    :rtype: bool
    """

    if len(str(inn)) != 10 and len(str(inn)) != 12 and inn != 0:
        raise ValidationError('ИНН должен содержать 10 или 12 цифр, или равен 0')
    return True


def date_of_birth_valid(date: str) -> bool:
    """
    Проверка даты рождения на корректность

    :param date: Дата рождения
    :type date: str
    :return: Булевое значение
    :rtype: bool
    """

    date_pattern: str = r'(?<!\d)(?:0?[1-9]|[12][0-9]|3[01])\.' \
                        r'(?:0?[1-9]|1[0-2])\.' \
                        r'(?:19[0-9][0-9]|20[012][0-9])(?!\d)'
    if not re.findall(date_pattern, date):
        raise ValidationError('Неверный формат даты')
    return True


def typy_next_contact_valid(type_contact: str, date: str) -> bool:
    """
    Проверяем заполнено поле type_contact или нет

    :param type_contact: Тип контакта
    :type type_contact: str
    :param date: Дата
    :type date: str
    :return: Булевое значение
    :rtype: bool
    """

    if date:
        if not type_contact:
            raise ValidationError('Заполните тип следующего контакта')
    return True


class VisitNameForm(forms.ModelForm):
    """Форма для начальных данных при визите клиента"""

    name_client = forms.CharField(
        label='ФИО клиента',
        widget=forms.TextInput(attrs={'class': 'visit__form_control-name'}))

    class Meta:
        model = ClientVisit
        fields = ['name_client', 'date_of_birth', 'inn_employer', 'main_product']
        widgets = {
            'date_of_birth': forms.TextInput(attrs={'placeholder': 'ДД.ММ.ГГГГ'}),
        }

    def clean_date_of_birth(self) -> str:
        """Проверка корректности поля date_of_birth"""

        date_of_birth: str = self.cleaned_data['date_of_birth']
        date_of_birth_valid(date_of_birth)
        return date_of_birth

    def clean_inn_employer(self) -> int:
        """Проверка корректности поля inn_employer"""

        inn: int = self.cleaned_data['inn_employer']

        inn_valid(inn)
        return inn


class VisitForm(forms.ModelForm):
    """Форма для полного заполнения данными при визите клиента"""

    credit_sum = forms.IntegerField(localize=True)
    credit_insurance_sum = forms.IntegerField(localize=True)
    deposit_sum = forms.IntegerField(localize=True)
    ksp_sum = forms.IntegerField(localize=True)
    nsg_sum = forms.IntegerField(localize=True)
    isg_sum = forms.IntegerField(localize=True)
    npo_sum = forms.IntegerField(localize=True)

    class Meta:
        model = ClientVisit
        fields = ['inn_employer', 'pension_bank', 'main_product',
                  'date_next_contact', 'type_next_contact', 'total_comment',
                  'credit_result', 'credit_sum', 'credit_comment',
                  'credit_insurance_result', 'credit_insurance_sum',
                  'credit_insurance_comment',
                  'credit_card_result', 'credit_card_comment',
                  'credit_card_insurance_result', 'credit_card_insurance_comment',
                  'deposit_result', 'deposit_sum', 'deposit_comment',
                  'service_package_result', 'service_package_type',
                  'service_package_comment',
                  'izp_result', 'izp_comment', 'pension_result', 'pension_comment',
                  'ksp_result', 'ksp_sum', 'ksp_comment',
                  'broker_navigate_result', 'broker_navigate_comment',
                  'nsg_result', 'nsg_sum', 'nsg_comment',
                  'isg_result', 'isg_sum', 'isg_comment',
                  'npo_result', 'npo_sum', 'npo_comment']

        widgets = {
            'date_next_contact': forms.TextInput(attrs={'placeholder': 'ДД.ММ.ГГГГ'}),

            'credit_comment': forms.Textarea(attrs={'cols': 100, 'rows': 3}),
            'credit_insurance_comment': forms.Textarea(attrs={'cols': 100, 'rows': 3}),
            'credit_card_comment': forms.Textarea(attrs={'cols': 100, 'rows': 3}),
            'credit_card_insurance_comment': forms.Textarea(
                attrs={'cols': 100, 'rows': 3}),
            'deposit_comment': forms.Textarea(attrs={'cols': 100, 'rows': 3}),
            'service_package_comment': forms.Textarea(attrs={'cols': 100, 'rows': 3}),
            'izp_comment': forms.Textarea(attrs={'cols': 100, 'rows': 3}),
            'pension_comment': forms.Textarea(attrs={'cols': 100, 'rows': 3}),
            'ksp_comment': forms.Textarea(attrs={'cols': 100, 'rows': 3}),
            'broker_navigate_comment': forms.Textarea(attrs={'cols': 100, 'rows': 3}),
            'nsg_comment': forms.Textarea(attrs={'cols': 100, 'rows': 3}),
            'isg_comment': forms.Textarea(attrs={'cols': 100, 'rows': 3}),
            'npo_comment': forms.Textarea(attrs={'cols': 100, 'rows': 3}),
            'total_comment': forms.Textarea(attrs={'cols': 100, 'rows': 5}),
        }

    def clean_inn_employer(self) -> int:
        """Проверка корректности поля inn_employer"""

        inn: int = self.cleaned_data.get('inn_employer')
        inn_valid(inn)
        return inn

    def clean_date_next_contact(self) -> str:
        """Проверка корректности заполнения поля date_next_contact"""

        if self.cleaned_data.get('result') in ['Думает', 'Планирует оформить'] and \
                self.cleaned_data.get('date_next_contact') is None:
            raise ValidationError('Заполните дату следующего контакта')
        return self.cleaned_data.get('date_next_contact')

    def clean_type_next_contact(self) -> str:
        """Проверка корректности заполнения поля type_next_contact"""

        type_contact = self.cleaned_data.get('type_next_contact')
        date = self.cleaned_data.get('date_next_contact')
        typy_next_contact_valid(type_contact, date)
        return type_contact


class CallForm(forms.ModelForm):
    """Форма для начальных данных при звонке клиенту"""

    sum = forms.IntegerField(localize=True, initial=0)

    class Meta:
        model = ClientCall
        fields = ['last_name_client', 'first_name_client', 'middle_name_client',
                  'date_of_birth', 'main_product', 'result', 'date_next_contact',
                  'type_next_contact',
                  'sum', 'comment']
        widgets = {
            'date_of_birth': forms.TextInput(attrs={'placeholder': 'ДД.ММ.ГГГГ'}),
            'date_next_contact': forms.TextInput(attrs={'placeholder': 'ДД.ММ.ГГГГ'}),
            'comment': forms.Textarea(
                attrs={'cols': 100, 'rows': 5, 'placeholder': 'Комментарии'})
        }

    def clean_date_of_birth(self) -> str:
        """Проверка корректности заполнения поля date_of_birth"""

        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth:
            date_of_birth_valid(date_of_birth)
        return date_of_birth

    def clean_date_next_contact(self) -> str:
        """Проверка корректности заполнения поля date_next_contact"""

        if self.cleaned_data.get('result') in ['Думает', 'Планирует оформить'] and \
                self.cleaned_data.get('date_next_contact') is None:
            raise ValidationError('Заполните дату следующего контакта')
        return self.cleaned_data.get('date_next_contact')

    def clean_type_next_contact(self) -> str:
        """Проверка корректности заполнения поля type_next_contact"""

        type_contact = self.cleaned_data.get('type_next_contact')
        date = self.cleaned_data.get('date_next_contact')
        typy_next_contact_valid(type_contact, date)
        return type_contact
