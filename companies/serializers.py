from rest_framework import serializers
from companies.models import Company


class CompanyRegistrationSerializer(serializers.Serializer):
    company_name = serializers.CharField(max_length=255)
    
    def validate_company_name(self, value):
        """Check if company name is already taken"""
        if Company.objects.filter(name=value).exists():
            raise serializers.ValidationError("Company name already exists")
        return value

    def create(self, validated_data):
        """Create a new company with generated password"""
        password = Company.generate_password()
        company = Company(name=validated_data['company_name'])
        company.set_password(password)
        company.save()
        
        return {
            'company': company,
            'password': password
        }


class CompanyRegistrationResponseSerializer(serializers.Serializer):
    company_name = serializers.CharField()
    password = serializers.CharField()
    created_at = serializers.DateTimeField()
    message = serializers.CharField()
