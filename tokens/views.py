from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from tokens.serializers import TokenGenerationSerializer, TokenValidationSerializer


@api_view(['POST'])
def generate_token(request):
    """
    Generate a new token for authenticated company
    """
    serializer = TokenGenerationSerializer(data=request.data)
    
    if serializer.is_valid():
        result = serializer.create(serializer.validated_data)
        token_obj = result['token_obj']
        raw_token = result['token']
        
        response_data = {
            'token': raw_token,
            'company_name': token_obj.company.name,
            'created_at': token_obj.created_at,
            'message': 'Token generated successfully. Please save your token - it will not be shown again.'
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def validate_token(request):
    """
    Validate if a token is active and valid
    """
    serializer = TokenValidationSerializer(data=request.data)
    
    if serializer.is_valid():
        response_data = {
            'valid': True,
            'message': 'Token is valid'
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    response_data = {
        'valid': False,
        'message': 'Token is invalid or inactive'
    }
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
