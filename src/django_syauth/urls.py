from django.urls import path
from . import views

app_name = 'django_syauth'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('callback/', views.CallbackView.as_view(), name='callback'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
