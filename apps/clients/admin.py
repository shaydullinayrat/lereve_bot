from django.contrib import admin

# Register your models here.
from apps.clients.models import Client


class ClientAdmin(admin.ModelAdmin):
    # Указываем все поля модели, которые должны отображаться в таблице
    list_display = [field.name for field in Client._meta.fields]


# Регистрируем модель с настройками админки
admin.site.register(Client, ClientAdmin)
