from django.urls import path
from django.http import JsonResponse

def dashboard_status(request):
    return JsonResponse({"app": "dashboard", "status": "ready"})

urlpatterns = [
    path('status/', dashboard_status, name='dashboard_status'),
]