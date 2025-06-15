import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from companies.models import Company
from companies.tests.factories import CompanyFactory


@pytest.mark.django_db
class TestCompanyRegistrationView:
    
    def setup_method(self):
        """Set up test client for each test"""
        self.client = APIClient()
        self.url = '/api/companies/register/'
    
    def test_successful_company_registration(self):
        """Test successful company registration"""
        data = {'company_name': 'NewTestCompany'}
        response = self.client.post(self.url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'company_name' in response.data
        assert 'password' in response.data
        assert 'created_at' in response.data
        assert 'message' in response.data
        assert response.data['company_name'] == 'NewTestCompany'
        assert len(response.data['password']) > 0
        assert 'successfully' in response.data['message']
        company = Company.objects.get(name='NewTestCompany')
        assert company.active is True
        assert company.check_password(response.data['password']) is True

    def test_duplicate_company_name_rejected(self):
        """Test that duplicate company names are rejected"""
        existing_company = CompanyFactory(name="ExistingCompany")
        data = {'company_name': 'ExistingCompany'}
        response = self.client.post(self.url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'company_name' in response.data
        assert 'already exists' in str(response.data['company_name'][0])

    def test_empty_company_name_rejected(self):
        """Test that empty company name is rejected"""
        data = {'company_name': ''}
        response = self.client.post(self.url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'company_name' in response.data

    def test_missing_company_name_rejected(self):
        """Test that missing company name is rejected"""
        data = {}
        response = self.client.post(self.url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'company_name' in response.data

    def test_long_company_name_rejected(self):
        """Test that overly long company names are rejected"""
        long_name = 'x' * 256  # Exceeds max_length=255
        data = {'company_name': long_name}
        response = self.client.post(self.url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'company_name' in response.data

    def test_only_post_method_allowed(self):
        """Test that only POST method is allowed"""
        data = {'company_name': 'TestCompany'}

        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        response = self.client.put(self.url, data, format='json')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        response = self.client.delete(self.url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_invalid_json_format_rejected(self):
        """Test that invalid JSON format is handled properly"""
        response = self.client.post(
            self.url, 
            'invalid json', 
            content_type='application/json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
