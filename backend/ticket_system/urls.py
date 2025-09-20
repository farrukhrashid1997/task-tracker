from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import redis
from django.db import connection
from django.conf import settings
from django.core.cache import cache
import json


def health_check():
    status = {
        "status": "OK", 
        "services": {}, 
        "django": True
    }
    
    #testing the database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        status['services']['database'] = "connected"
    except Exception as e:
        status["services"]["database"] = f"error: {str(e)}"
        status["status"] = "ERROR"
    
    # testing redis
    try:
        r = redis.from_url(settings.REDIS_URL)
        r.ping()
        status['services']['redis'] = "connected"
    
    except Exception as e:
        status["services"]["redis"] = f"error: {str(e)}"
        status["status"] = "ERROR"
    
    
    #testing cache
    try:
        cache.set('health_test', 'ok', 10)
        cache_result = cache.get('health_test')
        status["services"]["cache"] = "working" if cache_result == 'ok' else "error"
    except Exception as e:
        status["services"]["cache"] = f"error: {str(e)}"
        status["status"] = "ERROR"
    
    return JsonResponse(status, json_dumps_params={'indent': 2})

    
urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),
    path('api/auth/', include('accounts.urls')),
    path('api/tickets/', include('tickets.urls')),
    path('api/dashboard/', include('dashboard.urls')),
]
    
    
    