import pytest
from rest_framework.exceptions import ValidationError
from tokens.serializers import TokenGenerationSerializer, TokenValidationSerializer
from companies.tests.factories import CompanyFactory, InactiveCompanyFactory
from tokens.tests.factories import TokenFactory, InactiveTokenFactory

from tokens.models import Token


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
        data = {'token': 'test-token-123'}
        
        serializer = TokenValidationSerializer(data=data)
        assert serializer.is_valid()

    def test_invalid_token_rejected(self):
        """Test validation of non-existent token"""
        data = {'token': 'non-existent-token'}
        
        serializer = TokenValidationSerializer(data=data)
        assert not serializer.is_valid()
        assert 'token' in serializer.errors

    def test_inactive_token_rejected(self):
        """Test validation of inactive token"""
        token = InactiveTokenFactory(token="inactive-token")
        data = {'token': 'inactive-token'}
        serializer = TokenValidationSerializer(data=data)

        assert not serializer.is_valid()
