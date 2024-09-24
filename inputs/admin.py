from django.contrib import admin
from .models import Input


@admin.register(Input)
class InputAdmin(admin.ModelAdmin):
    pass
