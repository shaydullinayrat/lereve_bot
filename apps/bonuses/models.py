from django.db import models

# Create your models here.
from apps.clients.models import Client
from apps.shops.models import Product
from django.db import models
from django.contrib.auth.models import User


class Bonus(models.Model):
    is_active = models.BooleanField(default=True, verbose_name="Активный бонус")
    title = models.CharField(max_length=255, verbose_name="Название бонуса")
    description = models.TextField(blank=True, null=True, verbose_name="Описание бонуса")
    amount = models.PositiveIntegerField(default=0, verbose_name="Сумма бонуса")
    photo = models.ImageField(upload_to='media/bonuses/', null=True, blank=True, verbose_name="Постер бонуса")

    class Meta:
        verbose_name = "Бонус"
        verbose_name_plural = "Бонусы"
        ordering = ["-is_active", "title"]

    def __str__(self):
        return self.title




# Модель для заявок на бонус
class BonusRequest(models.Model):
    class StatusChoices(models.TextChoices):
        SUBMITTED = 'submitted', 'Подал заявку'
        SELECTED_ARTICLE = 'selected_article', 'Выбрал артикул'
        SELECTED_FEEDBACK = 'selected_feedback', 'Выбрал отзыв'
        SENT_PHONE = 'sent_phone', 'Отправил телефон'
        BONUS_RECEIVED = 'bonus_received', 'Получил бонус на телефон'

    # user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, verbose_name="Клиент", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заявки")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения заявки")
    bonus = models.ForeignKey(Bonus, on_delete=models.SET_NULL, verbose_name="Бонусная программа", null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, verbose_name="Продукт", null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Телефон")
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.SUBMITTED,
        verbose_name="Статус"
    )

    def __str__(self):
        return f"Заявка #{self.id} от {self.client}"

    class Meta:
        verbose_name = "Заявка на бонус"
        verbose_name_plural = "Заявки на бонус"
        ordering = ['-created_at']



# Модель для отзывов
class Feedback(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    wb_username = models.CharField(max_length=255, verbose_name="Имя пользователя WB")
    wb_feedback_id = models.CharField(max_length=255, unique=True, verbose_name="ID отзыва WB")
    text = models.TextField(verbose_name="Впечатления", default=None, null=True, blank=True)
    pros = models.TextField(verbose_name="Текст отзыва", default=None, null=True, blank=True)
    review_date = models.DateTimeField(verbose_name="Дата отзыва")
    bonus_request = models.OneToOneField(
        BonusRequest,
        on_delete=models.CASCADE,
        # null=True,
        # blank=True,
        verbose_name="Отзыв"
    )
    def __str__(self):
        return f"Отзыв {self.wb_username} на {self.product}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"