import pytest
from rest_framework.exceptions import ValidationError

from companies.tests.factories import CompanyFactory, InactiveCompanyFactory
from tokens.models import Token
from tokens.serializers import (TokenGenerationSerializer,
                                TokenValidationSerializer)
from tokens.tests.factories import InactiveTokenFactory, TokenFactory


@pytest.mark.django_db
class TestTokenGenerationSerializer:
    
    def test_valid_token_generation(self):
        """Test valid token generation for active company"""
        company = CompanyFactory(password="test123")
        data = {
            'company_name': company.name,
            'password': 'test123'
        }
        
        serializer = TokenGenerationSerializer(data=data)
        assert serializer.is_valid()
        
        result = serializer.create(serializer.validated_data)
        assert 'token' in result
        assert 'token_obj' in result
        assert len(result['token']) > 0
        assert result['token_obj'].company == company

    def test_invalid_company_name(self):
        """Test token generation with non-existent company"""
        data = {
            'company_name': 'NonExistentCompany',
            'password': 'test123'
        }
        
        serializer = TokenGenerationSerializer(data=data)
        assert not serializer.is_valid()
        assert 'non_field_errors' in serializer.errors

    def test_inactive_company_rejected(self):
        """Test token generation rejected for inactive company"""
        company = InactiveCompanyFactory(password="test123")
        data = {
            'company_name': company.name,
            'password': 'test123'
        }
        
        serializer = TokenGenerationSerializer(data=data)
        assert not serializer.is_valid()

    def test_wrong_password_rejected(self):
        """Test token generation rejected for wrong password"""
        company = CompanyFactory(password="correct123")
        data = {
            'company_name': company.name,
            'password': 'wrong123'
        }
        
        serializer = TokenGenerationSerializer(data=data)
        assert not serializer.is_valid()


@pytest.mark.django_db
class TestTokenValidationSerializer:
    
    def test_valid_token_validation(self):
        """Test validation of valid, active token"""
        token = TokenFactory(token="test-token-123")
        data = {'token': 'test-token-123', 'company_name': token.company.name}
        
        serializer = TokenValidationSerializer(data=data)
        assert serializer.is_valid()

    def test_invalid_token_rejected(self):
        """Test validation of non-existent token"""
        company = CompanyFactory()
        data = {'token': 'non-existent-token', 'company_name': company.name}
        
        serializer = TokenValidationSerializer(data=data)
        assert not serializer.is_valid()
        assert 'token' in serializer.errors
        assert 'Token does not exist' in str(serializer.errors['token'])

    def test_wrong_company_rejected(self):
        """Test validation of token with wrong company"""
        token = TokenFactory(token="test-token-123")
        other_company = CompanyFactory()
        data = {'token': 'test-token-123', 'company_name': other_company.name}
        
        serializer = TokenValidationSerializer(data=data)
        assert not serializer.is_valid()
        assert 'company_name' in serializer.errors
        assert 'Token does not belong to this company' in str(serializer.errors['company_name'])
