from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from companies.serializers import CompanyRegistrationSerializer


@api_view(['POST'])
def register_company(request):
    """
    Register a new company and return credentials
    """
    serializer = CompanyRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        result = serializer.create(serializer.validated_data)
        company = result['company']
        password = result['password']
        
        response_data = {
            'company_name': company.name,
            'password': password,
            'created_at': company.created_at,
            'message': 'Company registered successfully. Please save your password - it will not be shown again.'
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
