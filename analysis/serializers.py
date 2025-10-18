"""
Serializers for CrUX Analysis API

Basic validation and serialization for analysis and display of CrUX data.
"""

from rest_framework import serializers
from typing import List
import re


class FlexibleURLField(serializers.URLField):
    """URL field that automatically adds protocol if missing."""
    
    def to_internal_value(self, data):
        """Convert input to internal value, adding protocol if needed."""
        if not data:
            return data
            
        # Convert to string if not already
        url = str(data).strip()
        
        # If no protocol is specified, add https://
        if not re.match(r'^https?://', url, re.IGNORECASE):
            # Handle special cases
            if url.startswith('//'):
                url = 'https:' + url
            else:
                url = 'https://' + url
        
        # Use parent validation with the protocol-corrected URL
        return super().to_internal_value(url)


class URLListSerializer(serializers.Serializer):
    """Serializer for validating list of URLs for analysis and display of CrUX data."""
    
    urls = serializers.ListField(
        child=FlexibleURLField(max_length=2048),
        min_length=1,
        max_length=20,  # Reasonable limit for analysis and display of CrUX data
        help_text="List of URLs to analyze (max 20 URLs). Protocol (http/https) will be added automatically if missing."
    )
    
    def validate_urls(self, value: List[str]) -> List[str]:
        """Remove duplicates while preserving order for analysis and display of CrUX data."""
        # The FlexibleURLField already handles URL validation and protocol addition
        # We just need to remove duplicates
        seen = set()
        unique_urls = []
        for url in value:
            if url not in seen:
                seen.add(url)
                unique_urls.append(url)
        
        return unique_urls


class HealthCheckSerializer(serializers.Serializer):
    """Serializer for health check response for analysis and display of CrUX data."""
    
    status = serializers.CharField(default='ok')
    apiConfigured = serializers.BooleanField()
    timestamp = serializers.DateTimeField()
    version = serializers.CharField(default='1.0.0')
