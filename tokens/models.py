from django.db import models
import hashlib
import uuid
from companies.models import Company


class Token(models.Model):
    token_hash = models.CharField(max_length=255, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='tokens')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token for {self.company.name}"

    def set_token(self, raw_token):
        """Hash and set the token"""
        self.token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

    @classmethod
    def generate_token(cls):
        """Generate a random UUID token"""
        return str(uuid.uuid4())

    @classmethod
    def hash_token(cls, raw_token):
        """Helper method to hash a token for lookups"""
        return hashlib.sha256(raw_token.encode()).hexdigest()

    def is_valid(self):
        """Check if token is active and company is active"""
        return self.active and self.company.active

    class Meta:
        ordering = ['-created_at']
