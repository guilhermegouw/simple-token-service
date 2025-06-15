from rest_framework import serializers
from tokens.models import Token
from companies.models import Company


class TokenGenerationSerializer(serializers.Serializer):
    company_name = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)

    def validate(self, data):
        """Validate company credentials"""
        try:
            company = Company.objects.get(
                name=data['company_name'],
                active=True
            )
        except Company.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")

        if not company.check_password(data['password']):
            raise serializers.ValidationError("Invalid credentials")

        data['company'] = company
        return data

    def create(self, validated_data):
        """Create a new token for the authenticated company"""
        company = validated_data['company']
        raw_token = Token.generate_token()
        
        token = Token(company=company)
        token.set_token(raw_token)
        token.save()
        
        return {
            'token': raw_token,
            'token_obj': token
        }


class TokenValidationSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)

    def validate_token(self, value):
        """Validate token exists and is active"""
        token_hash = Token.hash_token(value)
        
        try:
            token = Token.objects.get(token_hash=token_hash)
        except Token.DoesNotExist:
            raise serializers.ValidationError("Invalid token")

        if not token.is_valid():
            raise serializers.ValidationError("Token is not active")

        return value


class TokenResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    company_name = serializers.CharField()
    created_at = serializers.DateTimeField()
