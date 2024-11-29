from django.contrib import admin

from apps.care_requests.models import CareRequestDetail, CareRequest


class CareRequestDetailInline(admin.TabularInline):
    model = CareRequestDetail
    extra = 1  # Количество пустых строк для добавления новых объектов в админке
    fields = ('media_type', 'file_url', 'text', 'created_at')
    readonly_fields = ('media_type', 'file_url', 'text', 'created_at')
    # readonly_fields = ('created_at',)
    show_change_link = True


@admin.register(CareRequest)
class CareRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'product', 'created_at', 'answered_at')
    readonly_fields = ('id', 'client', 'product', 'created_at', 'answered_at')
    list_filter = ('created_at', 'answered_at', 'product')
    search_fields = ('client', 'question')
    inlines = [CareRequestDetailInline]  # Подключаем Inline
    ordering = ('-created_at',)


@admin.register(CareRequestDetail)
class CareRequestDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'care_request', 'media_type', 'file_url', 'text', 'created_at')
    readonly_fields = ('id', 'care_request', 'media_type', 'file_url', 'text', 'created_at')
    list_filter = ('media_type', 'created_at')
    search_fields = ('text', 'file_url')
    ordering = ('-created_at',)
