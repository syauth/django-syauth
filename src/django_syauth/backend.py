from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class SyauthBackend(ModelBackend):
    def authenticate(self, request, token_info=None, **kwargs):
        """
        Authenticates a user based on the token information from Syauth.
        expected token_info: dict containing 'sub', 'email', 'given_name', 'family_name'
        """
        if not token_info:
            return None
            
        User = get_user_model()
        user_id = token_info.get('sub')
        email = token_info.get('email')
        
        if not user_id or not email:
            return None
            
        # Try to find user by username (using syauth_id) or email
        try:
            user = User.objects.get(username=user_id)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Create a new user
                user = User(username=user_id, email=email)
                user.set_unusable_password()
        
        # Update user details
        user.first_name = token_info.get('given_name', '')
        user.last_name = token_info.get('family_name', '')
        user.save()
        
        return user

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
