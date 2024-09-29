from django.contrib import admin
from .models import ChatRoom


# Register your models here.
@admin.register(ChatRoom)
class MessageAdmin(admin.ModelAdmin):
    pass
