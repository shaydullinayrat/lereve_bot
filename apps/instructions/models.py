from django.core.validators import MaxLengthValidator
from django.db import models

# Create your models here.
# bot/models.py
from django.db import models


class Instruction(models.Model):
    # Флаг активности инструкции
    is_active = models.BooleanField(default=True)

    # Название инструкции
    title = models.CharField(max_length=255)

    # Текст инструкции
    text = models.TextField(validators=[MaxLengthValidator(760)])

    # Фото, связанное с инструкцией
    photo = models.ImageField(upload_to='media/instructions/', blank=True, null=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']
        verbose_name = "Инструкция"
        verbose_name_plural = "Инструкции"


class SubInstruction(models.Model):
    # Связь с основной инструкцией
    instruction = models.ForeignKey(Instruction, related_name='subinstructions', on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    # Текст подинструкции
    title = models.CharField(max_length=255)
    text = models.TextField(validators=[MaxLengthValidator(760)])  # Текст подинструкции
    photo = models.ImageField(upload_to='media/subinstructions/', blank=True, null=True)  # Фото подинструкции

    is_active = models.BooleanField(default=True)  # Флаг активности подинструкции

    def __str__(self):
        return self.title

    class Meta:
        # Сортируем подинструкции по полю order
        ordering = ['order']
        verbose_name = "Подинструкция"
        verbose_name_plural = "Подинструкции"
