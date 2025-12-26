import jwt
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from .utils import get_config

class SyauthRemoteUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Check for Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return

        token = auth_header.split(' ')[1]
        try:
            # Decode token (verify signature in production)
            payload = jwt.decode(token, options={"verify_signature": False})
            
            user_id = payload.get('sub')
            email = payload.get('email')
            
            if user_id:
                User = get_user_model()
                # Get or create user (stateless auth)
                try:
                    user = User.objects.get(username=user_id)
                except User.DoesNotExist:
                    if email:
                        user = User(username=user_id, email=email)
                        user.set_unusable_password()
                        user.save()
                    else:
                        return
                
                request.user = user

        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)
