from django.db import models

# Create your models here.


class Client(models.Model):
    # Уникальный идентификатор пользователя
    user_id = models.BigIntegerField(unique=True)
    # Имя пользователя (может быть пустым)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    # Юзернейм пользователя в Telegram (может быть пустым)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    # Юзернейм пользователя в Telegram (может быть пустым)
    username = models.CharField(max_length=100, blank=True, null=True)
    # Код языка пользователя (например, 'ru' для русского, 'en' для английского)
    wb_username = models.CharField(max_length=100, blank=True, null=True)
    language_code = models.CharField(max_length=10, blank=True, null=True)
    # Дата и время, когда запись была создана. Заполняется автоматически.
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания
    # Дата и время последнего обновления записи. Обновляется автоматически при изменении записи.
    updated_at = models.DateTimeField(auto_now=True)  # Дата и время последнего обновления
    # Телефонный номер клиента
    phone_number = models.CharField(max_length=15, blank=True,
                                    null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.username})'

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"