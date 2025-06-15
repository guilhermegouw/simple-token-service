import factory
from companies.models import Company


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company
        skip_postgeneration_save = True

    name = factory.Sequence(lambda n: f"TestCompany{n}")
    active = True

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        """Set a password for the company"""
        if not create:
            return
        
        password = extracted or "test_password_123"
        self.set_password(password)
        self.save()


class InactiveCompanyFactory(CompanyFactory):
    """Factory for inactive companies"""
    active = False
