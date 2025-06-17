from rest_framework import serializers

from companies.models import Company
from tokens.models import Token


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
    company_name = serializers.CharField(max_length=255)
    
    def validate(self, data):
        """Validate token exists, is active, and belongs to the company"""
        token_hash = Token.hash_token(data['token'])
        
        try:
            token = Token.objects.get(token_hash=token_hash, company__name=data['company_name'])
        except Token.DoesNotExist:
            token_exists = Token.objects.filter(token_hash=token_hash).exists()
            if not token_exists:
                raise serializers.ValidationError({
                    'token': 'Token does not exist'
                })
            else:
                raise serializers.ValidationError({
                    'company_name': 'Token does not belong to this company'
                })
                
        if not token.is_valid():
            if not token.active:
                raise serializers.ValidationError({
                    'token': 'Token is inactive'
                })
            elif not token.company.active:
                raise serializers.ValidationError({
                    'company_name': 'Company is inactive'
                })
                
        return data


class TokenResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    company_name = serializers.CharField()
    created_at = serializers.DateTimeField()
