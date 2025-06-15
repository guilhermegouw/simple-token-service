from django.db import models
import hashlib
import secrets


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    password_hash = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def set_password(self, raw_password):
        """Hash and set the password"""
        self.password_hash = hashlib.sha256(raw_password.encode()).hexdigest()

    def check_password(self, raw_password):
        """Check if the provided password matches the stored hash"""
        return self.password_hash == hashlib.sha256(raw_password.encode()).hexdigest()

    @classmethod
    def generate_password(cls):
        """Generate a random password for the company"""
        return secrets.token_urlsafe(16)

    class Meta:
        verbose_name_plural = "companies"
