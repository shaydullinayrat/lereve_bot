from django.contrib import admin

# Register your models here.

# bot/admin.py
from django.contrib import admin
from .models import Instruction, SubInstruction


class SubInstructionInline(admin.TabularInline):
    model = SubInstruction  # Связь с моделью SubInstruction
    extra = 1  # Количество пустых форм для добавления подинструкций
    fields = ('title', 'order', 'text', 'is_active', 'photo')  # Поля, которые будут отображаться
    ordering = ('order',)  # Сортировка подинструкций по полю order


class InstructionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'photo')  # Поля, отображаемые в списке инструкций
    list_filter = ('is_active',)  # Фильтрация по полю is_active
    search_fields = ('title', 'text')  # Поиск по полям title и text

    # Включаем отображение подинструкций прямо в форме редактирования инструкции
    inlines = [SubInstructionInline]


# Регистрируем модели в админке
admin.site.register(Instruction, InstructionAdmin)
admin.site.register(SubInstruction)  # Регистрируем модель SubInstruction, если она не зарегистрирована
