from django.contrib import admin

from .models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['model', 'color', 'plate_number']
    list_filter = ['color', 'model']
