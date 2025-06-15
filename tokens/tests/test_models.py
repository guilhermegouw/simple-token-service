import pytest
from tokens.models import Token
from tokens.tests.factories import TokenFactory, InactiveTokenFactory
from companies.tests.factories import CompanyFactory, InactiveCompanyFactory


@pytest.mark.django_db
class TestTokenModel:
    
    def test_token_creation(self):
        """Test basic token creation"""
        token = TokenFactory()
        assert token.token_hash is not None
        assert token.active is True
        assert token.company is not None

    def test_token_generation(self):
        """Test token generation method"""
        raw_token = Token.generate_token()
        assert len(raw_token) > 0
        assert isinstance(raw_token, str)
        assert '-' in raw_token  # UUID format has dashes

    def test_token_hashing(self):
        """Test token hashing functionality"""
        raw_token = "test-token-123"
        hashed = Token.hash_token(raw_token)
        
        # Create token with this raw token
        token = TokenFactory.build()
        token.set_token(raw_token)
        
        assert token.token_hash == hashed

    def test_token_validation_active_company_active_token(self):
        """Test token is valid when both company and token are active"""
        company = CompanyFactory(active=True)
        token = TokenFactory(company=company, active=True)
        assert token.is_valid() is True

    def test_token_validation_inactive_company(self):
        """Test token is invalid when company is inactive"""
        company = InactiveCompanyFactory()
        token = TokenFactory(company=company, active=True)
        assert token.is_valid() is False

    def test_token_validation_inactive_token(self):
        """Test token is invalid when token is inactive"""
        company = CompanyFactory(active=True)
        token = InactiveTokenFactory(company=company)
        assert token.is_valid() is False

    def test_token_validation_both_inactive(self):
        """Test token is invalid when both company and token are inactive"""
        company = InactiveCompanyFactory()
        token = InactiveTokenFactory(company=company)
        assert token.is_valid() is False
