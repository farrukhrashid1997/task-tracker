from django.urls import path
from django.http import JsonResponse
from . import views

def accounts_status(request):
    return JsonResponse({"app": "accounts", "status": "ready"})

urlpatterns = [
    path('status/', views.status_view, name='accounts_status'),
    path('login/', views.login, name='login'),
    path('register/', views.register_user, name='register'),
    path('profile/', views.profile, name='profile'),
]