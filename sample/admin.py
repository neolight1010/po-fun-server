from .models import Sample
from django.contrib import admin


@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    list_display = ("name", "author")
