"""
Views for CrUX Analysis API for analysis and display of CrUX data.
"""

import logging
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone
from django.conf import settings

from .serializers import URLListSerializer, HealthCheckSerializer
from .crux_service import CrUXService, CrUXAPIError


logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([AllowAny])
def analyze_url(request):
    """
    Analyze URLs for CrUX performance data.
    
    POST /api/analyze-url/
    Body: {"urls": ["https://example.com", "https://google.com"]}
    
    Returns analysis results for analysis and display of CrUX data with filtering/sorting support.
    """
    try:
        # Validate input
        serializer = URLListSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Invalid input', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        urls = serializer.validated_data['urls']
        logger.info(f"Analyzing {len(urls)} URLs")
        
        # Perform analysis
        service = CrUXService()
        results = service.analyze_urls(urls)
        
        logger.info(f"Analysis completed: {results['successCount']}/{results['totalUrls']} successful")
        return Response(results, status=status.HTTP_200_OK)
    
    except CrUXAPIError as e:
        logger.error(f"CrUX API error: {str(e)}")
        return Response(
            {'error': 'CrUX API error', 'message': str(e)},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except Exception as e:
        logger.error(f"Unexpected error in analyze_url: {str(e)}")
        return Response(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint for analysis and display of CrUX data and health check.
    
    GET /api/health/
    
    Returns server status and API configuration for analysis and display of CrUX data and health check.
    """
    try:
        health_data = {
            'status': 'ok',
            'apiConfigured': bool(settings.CRUX_API_KEY),
            'timestamp': timezone.now(),
            'version': '1.0.0'
        }
        
        serializer = HealthCheckSerializer(health_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return Response(
            {'status': 'error', 'message': 'Health check failed'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )