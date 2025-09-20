from django.urls import path
from . import views

urlpatterns = [
    path('status-stats/', views.ticket_status_stats, name='ticket_status_stats'),
    path('priority-stats/', views.ticket_priority_stats, name='ticket_priority_stats'),
    path('summary/', views.dashboard_summary, name='dashboard_summary'),               
]