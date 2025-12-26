import os
import secrets
from django.shortcuts import redirect
from django.conf import settings
from django.views import View
from django.contrib.auth import login, logout
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse
from .utils import generate_pkce_pair, get_authorization_url, exchange_code_for_token, decode_id_token, get_config
from .backend import SyauthBackend

class LoginView(View):
    def get(self, request):
        code_verifier, code_challenge = generate_pkce_pair()
        state = secrets.token_urlsafe(16)
        
        # Store verifier and state in session
        request.session['syauth_code_verifier'] = code_verifier
        request.session['syauth_state'] = state
        
        # Redirect to Syauth
        auth_url = get_authorization_url(state, code_challenge)
        return redirect(auth_url)

class CallbackView(View):
    def get(self, request):
        error = request.GET.get('error')
        if error:
            return HttpResponseBadRequest(f"Login failed: {error}")
            
        code = request.GET.get('code')
        state = request.GET.get('state')
        stored_state = request.session.get('syauth_state')
        code_verifier = request.session.get('syauth_code_verifier')
        
        if not code or not state or not stored_state or not code_verifier:
            return HttpResponseBadRequest("Missing required parameters or session expired")
            
        if state != stored_state:
            return HttpResponseBadRequest("Invalid state parameter")
            
        try:
            tokens = exchange_code_for_token(code, code_verifier)
            id_token = tokens.get('id_token')
            
            if not id_token:
                return HttpResponseBadRequest("No ID token received")
                
            user_info = decode_id_token(id_token)
            
            # Authenticate user
            backend = SyauthBackend()
            user = backend.authenticate(request, token_info=user_info)
            
            if user:
                login(request, user, backend='django_syauth.backend.SyauthBackend')
                
                # Store access token in session for API calls
                access_token = tokens.get('access_token')
                if access_token:
                    request.session['syauth_access_token'] = access_token
                
                # Cleanup session
                del request.session['syauth_code_verifier']
                del request.session['syauth_state']
                
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                return HttpResponseBadRequest("Authentication failed")
                
        except Exception as e:
            return HttpResponseBadRequest(f"Authentication error: {str(e)}")

class LogoutView(View):
    def get(self, request):
        logout(request)
        config = get_config()
        # Optional: Redirect to Syauth logout if supported, otherwise home
        # For now, just redirect to home
        return redirect('/')
