import pytest
from rest_framework.test import APIClient
from rest_framework import status
from companies.tests.factories import CompanyFactory, InactiveCompanyFactory
from tokens.tests.factories import TokenFactory, InactiveTokenFactory


@pytest.mark.django_db
class TestTokenGenerationView:
    
    def setup_method(self):
        """Set up test client for each test"""
        self.client = APIClient()
        self.url = '/api/tokens/'
    
    def test_successful_token_generation(self):
        """Test successful token generation for valid company"""
        company = CompanyFactory(password="test123")
        data = {
            'company_name': company.name,
            'password': 'test123'
        }
        
        response = self.client.post(self.url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'token' in response.data
        assert 'company_name' in response.data
        assert 'created_at' in response.data
        assert 'message' in response.data
        assert response.data['company_name'] == company.name
        assert len(response.data['token']) > 0
        assert 'successfully' in response.data['message']

    def test_invalid_company_credentials(self):
        """Test token generation with invalid credentials"""
        company = CompanyFactory(password="correct123")
        data = {
            'company_name': company.name,
            'password': 'wrong123'
        }
        
        response = self.client.post(self.url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'non_field_errors' in response.data

    def test_nonexistent_company(self):
        """Test token generation for nonexistent company"""
        data = {
            'company_name': 'NonExistentCompany',
            'password': 'test123'
        }
        
        response = self.client.post(self.url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'non_field_errors' in response.data

    def test_inactive_company_rejected(self):
        """Test token generation rejected for inactive company"""
        company = InactiveCompanyFactory(password="test123")
        data = {
            'company_name': company.name,
            'password': 'test123'
        }
        
        response = self.client.post(self.url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_missing_credentials(self):
        """Test token generation with missing credentials"""
        data = {'company_name': 'TestCompany'}
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        data = {'password': 'test123'}
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_only_post_method_allowed(self):
        """Test that only POST method is allowed"""
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
class TestTokenValidationView:
    
    def setup_method(self):
        """Set up test client for each test"""
        self.client = APIClient()
        self.url = '/api/tokens/validate/'
    
    def test_valid_token_validation(self):
        """Test validation of valid, active token"""
        token = TokenFactory(token="test-token-123")
        data = {'token': 'test-token-123'}
        
        response = self.client.post(self.url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['valid'] is True
        assert 'valid' in response.data['message']

    def test_invalid_token_validation(self):
        """Test validation of nonexistent token"""
        data = {'token': 'nonexistent-token'}
        
        response = self.client.post(self.url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['valid'] is False
        assert 'invalid' in response.data['message']

    def test_inactive_token_validation(self):
        """Test validation of inactive token"""
        token = InactiveTokenFactory(token="inactive-token")
        data = {'token': 'inactive-token'}
        
        response = self.client.post(self.url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['valid'] is False

    def test_token_from_inactive_company(self):
        """Test validation of token from inactive company"""
        company = InactiveCompanyFactory()
        token = TokenFactory(company=company, token="company-inactive-token")
        data = {'token': 'company-inactive-token'}
        
        response = self.client.post(self.url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['valid'] is False

    def test_missing_token(self):
        """Test validation with missing token"""
        data = {}
        response = self.client.post(self.url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['valid'] is False

    def test_only_post_method_allowed(self):
        """Test that only POST method is allowed"""
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
