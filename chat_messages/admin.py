from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("short_question", "formatted_created_at")
    list_filter = ("created_at", "chat_room")
    readonly_fields = ("created_at",)

    def short_question(self, obj):
        return obj.question[:30]

    short_question.short_description = "Question"

    def formatted_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")

    formatted_created_at.short_description = "Created At"
