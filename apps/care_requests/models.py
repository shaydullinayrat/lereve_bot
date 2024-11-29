from django.db import models

# Подставьте вашу модель пользователя, если она кастомная
from apps.clients.models import Client
from apps.shops.models import Product
from PIL import Image
import os


class CareRequest(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создан'),
        ('answered', 'Отвечен'),
        ('completed', 'Завершен'),
    ]

    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='care_requests',
        verbose_name='Клиент'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    answered_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата ответа'
    )
    # question = models.TextField(
    #     verbose_name='Вопрос', null=True, blank=True
    # )
    product = models.ForeignKey(Product,  # Замените 'Product' на вашу реальную модель продукта
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True,
                                related_name='care_requests',
                                verbose_name='Продукт'
                                )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='created',
        verbose_name='Статус'
    )

    class Meta:
        verbose_name = 'Запрос в службу заботы'
        verbose_name_plural = 'Запросы в службу заботы'
        ordering = ['-created_at']

    def __str__(self):
        return f"Запрос от {self.client} - {self.get_status_display()}"


class CareRequestDetail(models.Model):
    class MediaType(models.TextChoices):
        TEXT = "text", "Текст"
        VIDEO = "video", "Видео"
        AUDIO = "audio", "Аудио"
        VOICE = "voice", "Голосовое сообщение"
        PHOTO = "photo", "Фото"

    care_request = models.ForeignKey(CareRequest, on_delete=models.CASCADE, related_name="details")
    media_type = models.CharField(max_length=50, choices=MediaType.choices)  # Тип медиа: photo, video, audio, voice
    file_id = models.CharField(max_length=255, blank=True, null=True)  # Telegram file_id
    file_url = models.TextField(blank=True, null=True)  # Telegram file_url
    text = models.TextField(blank=True, null=True)  # Доп. описание
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Деталь запроса'
        verbose_name_plural = 'Деталь запроса'
        ordering = ['id']

    def __str__(self):
        return f"Деталь для запроса {self.care_request.id}"

# class CareRequestPhoto(models.Model):
#     care_request = models.ForeignKey(
#         'CareRequest',
#         on_delete=models.CASCADE,
#         related_name='photos',
#         verbose_name='Запрос в службу заботы'
#     )
#     photo = models.ImageField(
#         upload_to='media/care_request_photos/',
#         verbose_name='Фото запроса'
#     )
#     description = models.TextField(
#         blank=True,
#         null=True,
#         verbose_name='Описание'
#     )
#     uploaded_at = models.DateTimeField(
#         auto_now_add=True,
#         verbose_name='Дата загрузки'
#     )
#
#     class Meta:
#         verbose_name = 'Фото запроса'
#         verbose_name_plural = 'Фото запросов'
#         ordering = ['-uploaded_at']
#
#     def save(self, *args, **kwargs):
#         # Сохраняем объект перед обработкой фото, чтобы получить путь
#         super().save(*args, **kwargs)
#
#         # Открываем загруженное изображение
#         img_path = self.photo.path
#         img = Image.open(img_path)
#
#         # Проверяем, нужно ли сжимать (например, если ширина > 1024)
#         max_width = 1024
#         if img.width > max_width:
#             # Вычисляем пропорции для уменьшения размера
#             ratio = max_width / float(img.width)
#             new_height = int(float(img.height) * ratio)
#
#             # Сжимаем изображение
#             img = img.resize((max_width, new_height), Image.ANTIALIAS)
#
#             # Перезаписываем сжатое изображение
#             img.save(img_path, quality=85, optimize=True)
#
#     def __str__(self):
#         return f"Фото для {self.care_request} (загружено {self.uploaded_at})"
