from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django_cryptography.fields import encrypt
import uuid
from django.utils import timezone
import datetime

class LLM(models.TextChoices):
    GPT_3 = 'GPT-3'
    GPT_4 = 'GPT-4'

class Endpoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    url_suffix = models.CharField(max_length=100, unique=True)
    api_payload_format = models.JSONField()
    prompt = models.TextField()
    llm_model = models.CharField(max_length=10, choices=LLM.choices, default=LLM.GPT_3)
    api_payload_injection = models.TextField()
    post_llm_processing_rules = models.JSONField()
    response_typing = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class TestArea(models.Model):
    endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE)
    test_case = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Test Area for {self.endpoint.name}'

class ApiKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, unique=True, validators=[MinLengthValidator(32), MaxLengthValidator(32)], editable=False)
    encrypted_key = encrypt(models.CharField(max_length=100, unique=True))
    key_type = models.CharField(max_length=10, choices=[('Internal', 'Internal'), ('External', 'External')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'API Key for {self.user.username}'

class DrinkRound(models.Model):
    endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE, related_name='drink_rounds')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_drink_rounds')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    access_token = models.CharField(max_length=64, unique=True, editable=False)
    expires_at = models.DateTimeField()
    usage_limit = models.PositiveIntegerField(default=10)
    usage_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Generate access token if not provided
        if not self.access_token:
            self.access_token = uuid.uuid4().hex
        
        # Set default expiration time if not provided (24 hours from now)
        if not self.expires_at:
            self.expires_at = timezone.now() + datetime.timedelta(hours=24)
            
        super().save(*args, **kwargs)
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def is_usage_limit_reached(self):
        return self.usage_count >= self.usage_limit
    
    def is_available(self):
        return self.is_active and not self.is_expired() and not self.is_usage_limit_reached()
    
    def increment_usage(self):
        self.usage_count += 1
        self.save(update_fields=['usage_count', 'updated_at'])
    
    def __str__(self):
        return f'Round of Drinks: {self.name} by {self.creator.username}'
