# backend/accounts/tests/test_models.py
import pytest
from django.contrib.auth.models import User
from accounts.models import UserProfile


@pytest.mark.django_db
class TestUserProfileModel:
    """Test cases for the UserProfile model"""
    
    def test_user_profile_created_automatically(self):
        """Test that UserProfile is created automatically when User is created"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Profile should be created automatically via signal
        assert hasattr(user, 'profile')
        assert user.profile.user == user
        assert user.profile.role == 'customer'  # Default role

    def test_user_profile_with_custom_role(self):
        """Test creating user profile with custom role"""
        user = User.objects.create_user(
            username='admin_user',
            email='admin@example.com',
            password='testpass123'
        )
        
        # Change role after creation
        user.profile.role = 'admin'
        user.profile.save()
        
        assert user.profile.role == 'admin'

    def test_user_profile_role_choices(self):
        """Test that profile role accepts only valid choices"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Valid roles
        for role in ['admin', 'agent', 'customer']:
            user.profile.role = role
            user.profile.save()
            user.profile.refresh_from_db()
            assert user.profile.role == role

    def test_user_profile_str_method(self):
        """Test the string representation of UserProfile"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        user.profile.role = 'agent'
        user.profile.save()
        
        expected = "testuser - agent"
        assert str(user.profile) == expected

    def test_user_profile_cascade_delete(self):
        """Test that UserProfile is deleted when User is deleted"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        profile_id = user.profile.id
        assert UserProfile.objects.filter(id=profile_id).exists()
        
        # Delete user
        user.delete()
        
        # Profile should be deleted due to CASCADE
        assert not UserProfile.objects.filter(id=profile_id).exists()

    def test_user_profile_timestamps(self):
        """Test that created_at and updated_at are set correctly"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        profile = user.profile
        assert profile.created_at is not None
        assert profile.updated_at is not None
        
        # Update profile and check updated_at changes
        original_updated_at = profile.updated_at
        profile.role = 'admin'
        profile.save()
        
        profile.refresh_from_db()
        assert profile.updated_at > original_updated_at

    def test_multiple_users_have_separate_profiles(self):
        """Test that multiple users each get their own profile"""
        user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='testpass123'
        )
        
        user2 = User.objects.create_user(
            username='user2', 
            email='user2@example.com',
            password='testpass123'
        )
        
        # Each user should have their own profile
        assert user1.profile != user2.profile
        assert user1.profile.user == user1
        assert user2.profile.user == user2
        
        # Profiles should have default role
        assert user1.profile.role == 'customer'
        assert user2.profile.role == 'customer'