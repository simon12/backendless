from rest_framework import serializers
from .models import Endpoint, TestArea, ApiKey

class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        fields = [
            'id', 'user', 'name', 'url_suffix', 'api_payload_format', 'prompt',
            'llm_model', 'api_payload_injection', 'post_llm_processing_rules',
            'response_typing', 'created_at', 'updated_at'
        ]

class TestAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestArea
        fields = ['id', 'endpoint', 'test_case', 'created_at', 'updated_at']

class ApiKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiKey
        fields = ['id', 'user', 'key', 'encrypted_key', 'key_type', 'created_at', 'updated_at']
        read_only_fields = ['key', 'encrypted_key']
