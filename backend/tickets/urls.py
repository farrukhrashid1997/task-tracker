from django.urls import path
from django.http import JsonResponse
from . import views

def tickets_status(request):
    return JsonResponse({"app": "tickets", "status": "ready"})

urlpatterns = [
    path('', views.get_tickets, name='get_tickets'),          
    path('create/', views.create_ticket, name='create_ticket'),       
    path('<int:ticket_id>/', views.get_ticket, name='get_ticket'),      
    path('<int:ticket_id>/update/', views.update_ticket, name='update_ticket'), 
    path('<int:ticket_id>/delete/', views.delete_ticket, name='delete_ticket'),
    path('<int:ticket_id>/comments/', views.create_comment, name='create_comment'),
    path('users/', views.get_users, name='get_users'),
    path('status/', tickets_status, name='tickets_status'),
]