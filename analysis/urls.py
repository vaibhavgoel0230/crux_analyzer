"""
URL Configuration for CrUX Analysis API for analysis and display of CrUX data.

Just the essential endpoints for analysis and display of CrUX data and health check.
"""

from django.urls import path
from . import views

app_name = 'analysis'

urlpatterns = [
    # Main analysis endpoint for analysis and display of CrUX data
    path('analyze-url', views.analyze_url, name='analyze_url'),
    
    # Health check endpoint for analysis and display of CrUX data and health check.
    path('health/', views.health_check, name='health_check'),
]
