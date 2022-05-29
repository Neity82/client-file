from django import forms


# PRODUCT_CHOICES = [
#     ('КН', 'КН'),
#     ('КК', 'КК'),
#     ('ПУ', 'ПУ'),
#     ('ИЗП', 'ИЗП'),
#     ('Пенсия', 'Пенсия'),
#     ('Депозит', 'Депозит'),
#     ('КСП', 'КСП'),
#     ('НПО', 'НПО'),
#     ('ИСЖ', 'ИСЖ'),
#     ('НСЖ', 'НСЖ'),
# ]

RESULT_CHOICES = [
    ('Оформлено', 'Оформлено'),
    ('Думает', 'Думает'),
    ('Планирует оформить', 'Планирует оформить'),
    ('Отказ', 'Отказ'),
]


class FilterInReports(forms.Form):
    # product = forms.ChoiceField(choices=PRODUCT_CHOICES)
    result = forms.ChoiceField(choices=RESULT_CHOICES)
