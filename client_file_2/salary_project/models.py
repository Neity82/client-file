from django.db import models


class SalaryProject(models.Model):
    """Модель зарплатных проектов"""

    inn = models.IntegerField(
        verbose_name='ИНН организации'
    )

    class Meta:
        db_table = 'salary_projects'
        verbose_name = 'инн организации'
        verbose_name_plural = 'инн организаций'

    def __str__(self) -> str:
        return f'{self.inn}'
