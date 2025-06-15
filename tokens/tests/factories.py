import factory
from tokens.models import Token
from companies.tests.factories import CompanyFactory


class TokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Token
        skip_postgeneration_save = True

    company = factory.SubFactory(CompanyFactory)
    active = True

    @factory.post_generation
    def token(self, create, extracted, **kwargs):
        """Set a token for the token object"""
        if not create:
            return
        
        raw_token = extracted or Token.generate_token()
        self.set_token(raw_token)
        self.save()


class InactiveTokenFactory(TokenFactory):
    """Factory for inactive tokens"""
    active = False
