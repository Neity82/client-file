from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from employee.manager import EmployeeManager


class Employee(AbstractUser):
    """Модель сотрудника"""

    middle_name = models.CharField(
        max_length=50,
        verbose_name='отчество',
        blank=True
    )

    office = models.ForeignKey(
        'Office',
        verbose_name='офис',
        on_delete=models.CASCADE,
        related_name='office'
    )

    objects = EmployeeManager()

    class Meta:
        db_table = 'employee'
        verbose_name = 'сотрудник'
        verbose_name_plural = 'сотрудники'

    def __str__(self) -> str:
        """Метод возвращает строковое представление объекта"""

        return f'{self.first_name} {self.last_name} ({self.office.code_office})'


class Office(models.Model):
    """Модель офиса"""

    name = models.CharField(
        max_length=150,
        verbose_name='название'
    )

    code_office = models.IntegerField(
        verbose_name='код подразделения'
    )

    objects = models.Manager()

    class Meta:
        db_table = 'offices'
        verbose_name = 'офис'
        verbose_name_plural = 'офисы'

    def __str__(self) ->str:
        return f'{self.name}({self.code_office})'
