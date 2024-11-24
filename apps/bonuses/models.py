from django.db import models

# Create your models here.
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


# Модель для отзывов
class Feedback(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    wb_username = models.CharField(max_length=255, verbose_name="Имя пользователя WB")
    wb_id = models.CharField(max_length=255, unique=True, verbose_name="ID отзыва WB")
    text = models.TextField(verbose_name="Текст отзыва")
    review_date = models.DateField(verbose_name="Дата отзыва")

    def __str__(self):
        return f"Отзыв {self.wb_username} на {self.product}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


# Модель для заявок на бонус
class BonusRequest(models.Model):
    class StatusChoices(models.TextChoices):
        # CREATED = 'created', 'Заявка соз'
        SUBMITTED = 'submitted', 'Подал заявку'
        SELECTED_ARTICLE = 'selected_article', 'Выбрал артикул'
        SELECTED_FEEDBACK = 'selected_feedback', 'Выбрал отзыв'
        SENT_PHONE = 'sent_phone', 'Отправил телефон'
        BONUS_RECEIVED = 'bonus_received', 'Получил бонус на телефон'

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заявки")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения заявки")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    feedback = models.OneToOneField(
        Feedback,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Отзыв"
    )
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Телефон")
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.SUBMITTED,
        verbose_name="Статус"
    )

    def __str__(self):
        return f"Заявка #{self.id} от {self.user}"

    class Meta:
        verbose_name = "Заявка на бонус"
        verbose_name_plural = "Заявки на бонус"
        ordering = ['-created_at']
