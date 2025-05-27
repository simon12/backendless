from rest_framework import serializers
from .models import Endpoint, TestArea, ApiKey, DrinkRound
from django.utils import timezone

class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

class TestAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestArea
        fields = '__all__'
        read_only_fields = ['endpoint', 'created_at', 'updated_at']

class ApiKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiKey
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

class DrinkRoundSerializer(serializers.ModelSerializer):
    expires_in_hours = serializers.IntegerField(write_only=True, required=False, default=24)
    status = serializers.SerializerMethodField()
    share_url = serializers.SerializerMethodField()
    
    class Meta:
        model = DrinkRound
        fields = ['id', 'endpoint', 'name', 'description', 'expires_at', 'expires_in_hours', 
                  'usage_limit', 'usage_count', 'is_active', 'created_at', 'updated_at', 
                  'status', 'share_url']
        read_only_fields = ['creator', 'access_token', 'created_at', 'updated_at', 
                           'usage_count', 'is_active']
    
    def get_status(self, obj):
        if not obj.is_active:
            return "Revoked"
        if obj.is_expired():
            return "Expired"
        if obj.is_usage_limit_reached():
            return "Usage limit reached"
        return "Active"
    
    def get_share_url(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(f'/shared/{obj.access_token}/')
        return f'/shared/{obj.access_token}/'
    
    def create(self, validated_data):
        expires_in_hours = validated_data.pop('expires_in_hours', 24)
        validated_data['expires_at'] = timezone.now() + timezone.timedelta(hours=expires_in_hours)
        return super().create(validated_data)
