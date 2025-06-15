import pytest
from rest_framework.exceptions import ValidationError
from companies.serializers import CompanyRegistrationSerializer
from companies.tests.factories import CompanyFactory
from companies.models import Company


@pytest.mark.django_db
class TestCompanyRegistrationSerializer:
    
    def test_valid_company_registration(self):
        """Test valid company registration"""
        data = {'company_name': 'NewTestCompany'}
        serializer = CompanyRegistrationSerializer(data=data)
        
        assert serializer.is_valid()
        result = serializer.save()
        
        assert 'company' in result
        assert 'password' in result
        assert isinstance(result['password'], str)
        assert len(result['password']) > 0
        
        company = result['company']
        assert company.name == 'NewTestCompany'
        assert company.active is True
        assert company.password_hash is not None

    def test_duplicate_company_name_validation(self):
        """Test that duplicate company names are rejected"""
        existing_company = CompanyFactory(name="ExistingCompany")
        data = {'company_name': 'ExistingCompany'}
        serializer = CompanyRegistrationSerializer(data=data)
        
        assert not serializer.is_valid()
        assert 'company_name' in serializer.errors
        assert 'already exists' in str(serializer.errors['company_name'][0])

    def test_empty_company_name_validation(self):
        """Test that empty company name is rejected"""
        data = {'company_name': ''}
        serializer = CompanyRegistrationSerializer(data=data)
        
        assert not serializer.is_valid()
        assert 'company_name' in serializer.errors

    def test_missing_company_name_validation(self):
        """Test that missing company name is rejected"""
        data = {}
        serializer = CompanyRegistrationSerializer(data=data)
        
        assert not serializer.is_valid()
        assert 'company_name' in serializer.errors

    def test_company_name_max_length_validation(self):
        """Test that very long company names are rejected"""
        long_name = 'x' * 256  # Exceeds max_length=255
        data = {'company_name': long_name}
        serializer = CompanyRegistrationSerializer(data=data)
        
        assert not serializer.is_valid()
        assert 'company_name' in serializer.errors

    def test_password_is_not_exposed_in_validated_data(self):
        """Test that password is not in the validated data (security check)"""
        data = {'company_name': 'TestCompany'}
        serializer = CompanyRegistrationSerializer(data=data)
        
        assert serializer.is_valid()
        assert 'password' not in serializer.validated_data

    def test_created_company_can_authenticate(self):
        """Test that the created company can authenticate with returned password"""
        data = {'company_name': 'AuthTestCompany'}
        serializer = CompanyRegistrationSerializer(data=data)
        
        assert serializer.is_valid()
        result = serializer.save()
        
        company = result['company']
        password = result['password']
        
        assert company.check_password(password) is True
        assert company.check_password('wrong_password') is False
