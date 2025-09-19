from django.urls import path
from django.http import JsonResponse

def tickets_status(request):
    return JsonResponse({"app": "tickets", "status": "ready"})

urlpatterns = [
    path('status/', tickets_status, name='tickets_status'),
]