from django.db import models

# Create your models here.


class Bonus(models.Model):
    is_active = models.BooleanField(default=True, verbose_name="Активный бонус")
    title = models.CharField(max_length=255, verbose_name="Название бонуса")
    description = models.TextField(blank=True, null=True, verbose_name="Описание бонуса")
    amount = models.PositiveIntegerField(default=0, verbose_name="Сумма бонуса")

    class Meta:
        verbose_name = "Бонус"
        verbose_name_plural = "Бонусы"
        ordering = ["-is_active", "title"]

    def __str__(self):
        return self.title