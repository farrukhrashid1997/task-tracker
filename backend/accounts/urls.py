from django.urls import path
from django.http import JsonResponse

def accounts_status(request):
    return JsonResponse({"app": "accounts", "status": "ready"})

urlpatterns = [
    path('status/', accounts_status, name='accounts_status'),
]