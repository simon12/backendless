from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode, urlsafe_b64decode
import os
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    api_key = models.CharField(_('API Key'), max_length=64, default=get_random_string)
    encrypted_openai_key = models.BinaryField(_('Encrypted OpenAI Key'), blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def generate_api_key(self):
        self.api_key = get_random_string(length=64)
        self.save()

    def set_openai_key(self, openai_key):
        encrypted_key = self.encrypt_openai_key(openai_key)
        self.encrypted_openai_key = encrypted_key
        self.save()

    def get_openai_key(self):
        return self.decrypt_openai_key(self.encrypted_openai_key)

    @staticmethod
    def encrypt_openai_key(openai_key):
        key = urlsafe_b64encode(os.environ['FERNET_KEY'].encode())
        f = Fernet(key)
        encrypted_key = f.encrypt(openai_key.encode())
        return encrypted_key

    @staticmethod
    def decrypt_openai_key(encrypted_key):
        key = urlsafe_b64encode(os.environ['FERNET_KEY'].encode())
        f = Fernet(key)
        decrypted_key = f.decrypt(encrypted_key)
        return decrypted_key.decode()
