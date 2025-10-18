"""
Main URL configuration for CrUX analyzer project.
"""

from django.urls import path, include

urlpatterns = [
    path("api/", include('analysis.urls')),
]