from django.contrib import admin
from .models import Endpoint, TestArea, ApiKey

@admin.register(Endpoint)
class EndpointAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'url_suffix', 'llm_model', 'created_at', 'updated_at')
    search_fields = ('name', 'url_suffix')
    list_filter = ('llm_model', 'created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(TestArea)
class TestAreaAdmin(admin.ModelAdmin):
    list_display = ('endpoint', 'test_case', 'created_at', 'updated_at')
    search_fields = ('endpoint__name',)
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'created_at', 'updated_at')
    search_fields = ('user__username', 'key')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
