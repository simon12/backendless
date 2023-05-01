from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django_cryptography.fields import encrypt

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
