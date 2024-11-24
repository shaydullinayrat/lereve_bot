from django.db import models

# Create your models here.

from django.db import models

class Shop(models.Model):
    url = models.URLField(max_length=200, unique=True, verbose_name="URL магазина")
    photo = models.ImageField(upload_to='media/shops/', null=True, blank=True, verbose_name="Фото магазина")
    title = models.CharField(max_length=255, verbose_name="Название магазина")
    is_active = models.BooleanField(default=True, verbose_name="Активен ли магазин")
    description = models.TextField(null=True, blank=True, verbose_name="Описание магазина")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"


class Product(models.Model):
    article = models.PositiveIntegerField(unique=True, default=0, verbose_name="Артикул")
    url = models.URLField(max_length=200, unique=True, verbose_name="URL продукта")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="products", verbose_name="Магазин")
    photo = models.ImageField(upload_to='media/products/', null=True, blank=True, verbose_name="Фото продукта")
    title = models.CharField(max_length=255, verbose_name="Название продукта")
    is_active = models.BooleanField(default=True, verbose_name="Активен ли продукт")
    description = models.TextField(null=True, blank=True, verbose_name="Описание продукта")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

