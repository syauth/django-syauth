import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django_syauth.decorators import syauth_login_required
from django.conf import settings
from urllib.parse import urlencode

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    config = settings.SYAUTH
    base_url = config['API_URL'].rstrip('/')
    
    # Construct register/forgot urls just like in Next.js example
    params = {
        'client_id': config['CLIENT_ID'],
        'redirect_uri': config['REDIRECT_URI'],
    }
    encoded_params = urlencode(params)
    
    context = {
        'syauth_register_url': f"{base_url}/auth/register/?{encoded_params}",
        'syauth_forgot_password_url': f"{base_url}/auth/forgot-password/?{encoded_params}",
    }
    return render(request, 'home.html', context)

@syauth_login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@syauth_login_required
def profile(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        access_token = request.session.get('syauth_access_token')
        
        if not access_token:
            messages.error(request, 'Session expired or invalid token. Please login again.')
            return redirect('profile')
            
        base_url = settings.SYAUTH['API_URL'].rstrip('/')
        headers = {'Authorization': f'Bearer {access_token}'}
        
        if action == 'update_profile':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            
            try:
                response = requests.patch(
                    f"{base_url}/user/profile/", 
                    json={'first_name': first_name, 'last_name': last_name},
                    headers=headers
                )
                
                if response.status_code == 200:
                    request.user.first_name = first_name
                    request.user.last_name = last_name
                    request.user.save()
                    messages.success(request, 'Profile updated successfully!')
                else:
                    messages.error(request, f"Failed to update profile: {response.text}")
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
                
        elif action == 'change_password':
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if new_password != confirm_password:
                messages.error(request, "New passwords do not match")
            else:
                try:
                    response = requests.post(
                        f"{base_url}/user/password/update/",
                        json={
                            'current_password': current_password, 
                            'new_password': new_password,
                            'confirm_password': confirm_password
                        },
                        headers=headers
                    )
                    
                    if response.status_code == 200:
                        messages.success(request, 'Password changed successfully!')
                    else:
                        messages.error(request, f"Failed to change password: {response.text}")
                except Exception as e:
                    messages.error(request, f"Error: {str(e)}")
        
        return redirect('profile')

    return render(request, 'profile.html')
