from django.contrib import admin
from .models import Endpoint, TestArea, ApiKey, DrinkRound

class EndpointAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'url_suffix', 'llm_model', 'created_at')
    list_filter = ('llm_model', 'user')
    search_fields = ('name', 'url_suffix')

class TestAreaAdmin(admin.ModelAdmin):
    list_display = ('endpoint', 'created_at')
    list_filter = ('endpoint',)

class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'key_type', 'created_at')
    list_filter = ('key_type', 'user')

class DrinkRoundAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'endpoint', 'is_active', 'usage_count', 'usage_limit', 'expires_at')
    list_filter = ('is_active', 'creator')
    search_fields = ('name', 'description', 'access_token')
    readonly_fields = ('access_token', 'usage_count')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(creator=request.user)

admin.site.register(Endpoint, EndpointAdmin)
admin.site.register(TestArea, TestAreaAdmin)
admin.site.register(ApiKey, ApiKeyAdmin)
admin.site.register(DrinkRound, DrinkRoundAdmin)
