from django.contrib import admin

# Register your models here.
from apps.shops.models import Product, Shop


class ProductInline(admin.TabularInline):
    model = Product  # Связь с моделью SubInstruction
    extra = 1  # Количество пустых форм для добавления подинструкций
    fields = ('is_active', 'order', 'article', 'title', 'url', 'description', 'photo')  # Поля, которые будут отображаться
    # ordering = ('order',)  # Сортировка подинструкций по полю order


class ShopAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Shop._meta.fields] # Поля, отображаемые в списке инструкций
    list_filter = ('title', 'url', 'description')  # Фильтрация по полю is_active
    search_fields = ('title', 'url', 'description')  # Поиск по полям title и text

    # Включаем отображение подинструкций прямо в форме редактирования инструкции
    inlines = [ProductInline]


# Регистрируем модели в админке
admin.site.register(Shop, ShopAdmin)
admin.site.register(Product)  # Регистрируем модель SubInstruction, если она не зарегистрирована
