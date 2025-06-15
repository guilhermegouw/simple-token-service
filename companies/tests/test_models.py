import pytest
from companies.models import Company
from companies.tests.factories import CompanyFactory, InactiveCompanyFactory


@pytest.mark.django_db
class TestCompanyModel:
    
    def test_company_creation(self):
        """Test basic company creation"""
        company = CompanyFactory()
        assert company.name.startswith("TestCompany")
        assert company.active is True
        assert company.password_hash is not None

    def test_password_generation(self):
        """Test password generation method"""
        password = Company.generate_password()
        assert len(password) > 0
        assert isinstance(password, str)

    def test_password_setting_and_checking(self):
        """Test password hashing and validation"""
        company = CompanyFactory.build()
        raw_password = "my_secret_password"
        
        company.set_password(raw_password)
        assert company.check_password(raw_password) is True
        assert company.check_password("wrong_password") is False

    def test_inactive_company(self):
        """Test inactive company creation"""
        company = InactiveCompanyFactory()
        assert company.active is False
