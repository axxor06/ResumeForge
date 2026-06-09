from django.contrib import admin
from .models import Resume

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'template', 'created_at', 'updated_at']
    list_filter = ['template', 'is_draft']
    search_fields = ['title', 'user__email', 'full_name']
