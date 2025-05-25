from django.contrib import admin
from .models import SearchHistory


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ("user_email", "query", "timestamp")  # Показываем email пользователя
    list_filter = ("user", "timestamp")
    search_fields = ("query", "user__email")  # Поиск по городу и email пользователя

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = "Email пользователя"
    user_email.admin_order_field = "user__email"
