from django.conf import settings
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
from django.http import JsonResponse




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
    
    if user is not None and user.is_active:
        tokens = get_tokens_for_user(user)
        
        # Create response with user data (NO TOKENS in body)
        response_data = {
            'message': 'Login Successful',
            'user': {
                'id': user.id,  # Add ID here
                'username': user.username, 
                'email': user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.profile.role,
            }
        }
        
        response = JsonResponse(response_data)
        
        response.set_cookie(
            'access_token',
            tokens['access'],
            max_age=60 * 60,
            httponly=True, 
            samesite='Strict'
        )
        
        response.set_cookie(
            'refresh_token',
            tokens['refresh'],
            max_age=60 * 60 * 24 * 7,  # 7 days
            httponly=True,
            samesite='Strict'
        )
        
        return response
    
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
        response_data = {
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.profile.role,
            }
        }
        
        response = JsonResponse(response_data, status=201)

        
        
        response.set_cookie(
            'access_token',
            tokens['access'],
            max_age=60 * 60,
            httponly=True, 
            samesite='Strict'
        )
        
        response.set_cookie(
            'refresh_token',
            tokens['refresh'],
            max_age=60 * 60 * 24 * 7,
            httponly=True,
            samesite='Strict'
        )
        
        return response
    
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
    

def verify_google_token(id_token_str):
    try:
        idinfo = id_token.verify_oauth2_token(
            id_token_str,
            google_requests.Request(),
            "33046009397-91mkm5pdv4febp6pg867p5e90ifichjb.apps.googleusercontent.com"
        )
        return idinfo
    except Exception as e:
        print("Invalid token:", e)
        return None

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def google_auth_view(request):
    try:
        google_access_token = request.data.get('credential')
        if not google_access_token:
            return Response({
                'error': 'Google access token is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        google_id_token = request.data.get('credential')
        idinfo = verify_google_token(google_id_token)
        if not idinfo:
            return Response({'error': 'Invalid Google ID token'}, status=400)


        email = idinfo.get('email')
        first_name = idinfo.get('given_name', '')
        last_name = idinfo.get('family_name')
        
        try:
            user = User.objects.get(email=email)
        
        except User.DoesNotExist:
            username = email.split('@')[0]
            original_username = username
            counter = 1
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
        response_data = {
            'message': 'Google authentication successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.profile.role,
            }
        }

        response = JsonResponse(response_data, status=200)

        response.set_cookie(
            'access_token',
            tokens['access'],
            max_age=60 * 60,
            httponly=True, 
            samesite='Strict'
        )

        response.set_cookie(
            'refresh_token',
            tokens['refresh'],
            max_age=60 * 60 * 24 * 7,
            httponly=True,
            samesite='Strict'
        )

        return response
            

        
    except ImportError:
        return Response({
            'error': 'Google OAuth not properly configured'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({
            'error': f'Google authentication failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    response = JsonResponse({'message': 'Logged out successfully'})
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response
        
@api_view(['GET'])
def status_view(request):
    return Response({'status': 'Accounts app is running'})