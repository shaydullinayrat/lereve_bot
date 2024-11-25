from django.contrib import admin

# Register your models here.
from apps.bonuses.models import Bonus, BonusRequest, Feedback


class BonusAdmin(admin.ModelAdmin):
    # Указываем все поля модели, которые должны отображаться в таблице
    list_display = [field.name for field in Bonus._meta.fields]

# Регистрируем модель с настройками админки
admin.site.register(Bonus, BonusAdmin)

class FeedbackInline(admin.StackedInline):
    model = Feedback
    readonly_fields = [field.name for field in Feedback._meta.fields]  # Все поля только для чтения
    can_delete = False
    verbose_name_plural = "Отзыв"
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False  # Запрет добавления нового отзыва из инлайна

    def has_change_permission(self, request, obj=None):
        return False  # Запрет редактирования отзыва из инлайна
class BonusRequestAdmin(admin.ModelAdmin):
    # Указываем все поля модели, которые должны отображаться в таблице
    inlines = [FeedbackInline]
    list_display = [field.name for field in BonusRequest._meta.fields]
    # readonly_fields = (
    #     'feedback_product',
    #     'feedback_wb_username',
    #     'feedback_wb_id',
    #     'feedback_text',
    #     'feedback_review_date',
    # )
    #
    # def feedback_product(self, obj):
    #     return obj.feedback.product if obj.feedback else None
    #
    # feedback_product.short_description = "Продукт отзыва"
    #
    # def feedback_wb_username(self, obj):
    #     return obj.feedback.wb_username if obj.feedback else None
    #
    # feedback_wb_username.short_description = "Имя пользователя WB"
    #
    # def feedback_wb_id(self, obj):
    #     return obj.feedback.wb_id if obj.feedback else None
    #
    # feedback_wb_id.short_description = "ID отзыва WB"
    #
    # def feedback_text(self, obj):
    #     return obj.feedback.text if obj.feedback else None
    #
    # feedback_text.short_description = "Текст отзыва"
    #
    # def feedback_review_date(self, obj):
    #     return obj.feedback.review_date if obj.feedback else None
    #
    # feedback_review_date.short_description = "Дата отзыва"

# Регистрируем модель с настройками админки
admin.site.register(BonusRequest, BonusRequestAdmin)

class FeedbackAdmin(admin.ModelAdmin):
    # Указываем все поля модели, которые должны отображаться в таблице
    list_display = [field.name for field in Feedback._meta.fields]



# Регистрируем модель с настройками админки
admin.site.register(Feedback, FeedbackAdmin)

