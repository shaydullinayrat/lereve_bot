from django.contrib import admin

# Register your models here.
from apps.bonuses.models import Bonus


class BonusAdmin(admin.ModelAdmin):
    # Указываем все поля модели, которые должны отображаться в таблице
    list_display = [field.name for field in Bonus._meta.fields]


# Регистрируем модель с настройками админки
admin.site.register(Bonus, BonusAdmin)