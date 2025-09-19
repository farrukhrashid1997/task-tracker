from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.models import SocialAccount
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import requests
from .models import UserProfile




def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh), 
        'access': str(refresh.access_token)
    }


@api_view(['POST'])
@permission_classes([])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'Username and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    
    if user is not None:
        if user.is_active:
            tokens = get_tokens_for_user(user)
            return Response({
                'message': 'Login Successful', 
                "tokens": tokens, 
                "user": {
                    'username': user.username, 
                    'email': user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.profile.role,
                    
                }
            })
    
    else: 
        return Response({
            'error': "Invalid username or password"
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')
    role = request.data.get('role', 'customer')
    
    if not username or not password or not email:
        return Response({
            'error': 'Username, password and email are required'
        }, status=status.HTTP_400_BAD_REQUEST)
        
    if User.objects.filter(username=username).exists():
        return Response({
            'error': 'Username already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(email=email).exists():
        return Response({
            'error': 'Email already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    valid_roles = [choice[0] for choice in UserProfile.ROLE_CHOICES]
    if role not in valid_roles:
        role = 'customer'
        
    
    try:
        user = User.objects.create_user(
            username=username, 
            password=password, 
            email=email, 
            first_name=first_name, 
            last_name=last_name
        )
        user.profile.role = role
        user.profile.save()
        
        tokens = get_tokens_for_user(user)
        
        
        return Response({
            'message': 'User registered successfully',
            'tokens': tokens,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.profile.role,
            }
        }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({
            'error': f'Registration failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile(request):
    user = request.user
    return Response({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.profile.role,
            'date_joined': user.date_joined,
            'last_login': user.last_login,
        }
    }, status=status.HTTP_200_OK)
    

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def google_auth_view(request):
    try:
        google_access_token = request.data.get('access_token')
        
        if not google_access_token:
            return Response({
                'error': 'Google access token is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        google_user_info_url = f"https://www.googleapis.com/oauth2/v2/userinfo?access_token={google_access_token}"
        response = requests.get(google_user_info_url)
        
        if response.status_code != 200:
            return Response({
                'error': 'Invalud Google Access token'
            }, status=status.HTTP_400_BAD_REQUEST)

        google_user_data = response.json()
        email = google_user_data.get('email')
        first_name = google_user_data.get('given_name', '')
        last_name = google_user_data.get('id')
        
        try:
            user = User.objects.get(email=email)
        
        except User.DoesNotExist:
            username = email.split('@')[0]
            original_username = username
            counter = 1
            ## TODO: Give the user an option to choose a username for themselves, for now we will just add a counter in front
            while User.objects.filter(username=username).exists():
                username = f"{original_username}{counter}"
                counter += 1
            
            user = User.objects.create_user(
                username=username, 
                email=email, 
                first_name=first_name, 
                last_name=last_name
            )
            
            user.profile.role = 'customer'
            user.profile.save()
            
        tokens = get_tokens_for_user(user)
            
        return Response({
            'message': 'Google authentication successful',
            'tokens': tokens,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.profile.role,
            }
        }, status=status.HTTP_200_OK)
        
    except ImportError:
        return Response({
            'error': 'Google OAuth not properly configured'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({
            'error': f'Google authentication failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
@api_view(['GET'])
def status_view(request):
    return Response({'status': 'Accounts app is running'})