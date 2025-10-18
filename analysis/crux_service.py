"""
CrUX API Service

Handles CrUX API communication.
Perfect for analysis and display of CrUX data.
"""

import requests
import logging
from datetime import datetime
from typing import Dict, Any, List
from django.conf import settings


logger = logging.getLogger(__name__)


class CrUXAPIError(Exception):
    """Custom exception for CrUX API related errors."""
    pass


class CrUXService:
    """
    Service for fetching CrUX data.
    
    This service focuses on API communication and data formatting for analysis
    for analysis and display of CrUX data.
    """
    
    def __init__(self):
        self.api_key = settings.CRUX_API_KEY
        self.api_url = settings.CRUX_API_URL
        self.timeout = 10  # seconds
        
        if not self.api_key:
            raise CrUXAPIError("CrUX API key not configured")
    
    def analyze_urls(self, urls: List[str]) -> Dict[str, Any]:
        """
        Analyze multiple URLs and return results for analysis and display.
        
        Args:
            urls: List of URLs to analyze
            
        Returns:
            Dictionary with results, summary, and errors for analysis and display.
        """
        results = []
        errors = []
        
        # Process each URL
        for url in urls:
            try:
                crux_data = self.fetch_crux_data(url)
                results.append(crux_data)
            except CrUXAPIError as e:
                errors.append({'url': url, 'error': str(e)})
                logger.warning(f"CrUX API error for {url}: {str(e)}")
            except Exception as e:
                error_msg = f"Unexpected error: {str(e)}"
                errors.append({'url': url, 'error': error_msg})
                logger.error(f"Unexpected error analyzing {url}: {str(e)}")
        
        # Generate summary statistics
        summary = self._generate_summary(results)
        
        return {
            'results': results,
            'summary': summary,
            'errors': errors,
            'totalUrls': len(urls),
            'successCount': len(results),
            'timestamp': datetime.now().isoformat()
        }
    
    def fetch_crux_data(self, url: str) -> Dict[str, Any]:
        """
        Fetch CrUX data for a single URL.
        
        Args:
            url: The URL to analyze
            
        Returns:
            Formatted CrUX data
        """
        try:
            response = self._make_api_request(url)
            return self._parse_crux_response(response, url)
        except requests.RequestException as e:
            logger.error(f"Error fetching CrUX data for {url}: {str(e)}")
            raise CrUXAPIError(f"Failed to fetch CrUX data: {str(e)}")
    
    def _make_api_request(self, url: str) -> Dict[str, Any]:
        """Make HTTP request to CrUX API."""
        request_url = f"{self.api_url}?key={self.api_key}"
        payload = {"url": url}
        
        response = requests.post(
            request_url,
            json=payload,
            timeout=self.timeout,
            headers={'Content-Type': 'application/json'}
        )
        
        response.raise_for_status()
        return response.json()
    
    def _parse_crux_response(self, data: Dict[str, Any], url: str) -> Dict[str, Any]:
        """Parse CrUX API response into display format."""
        metrics = data.get('record', {}).get('metrics', {})
        
        return {
            'url': url,
            'fetchTime': datetime.now().isoformat(),
            'metrics': {
                'lcp': self._parse_metric(metrics.get('largest_contentful_paint')),
                'cls': self._parse_metric(metrics.get('cumulative_layout_shift')),
                'fcp': self._parse_metric(metrics.get('first_contentful_paint')),
            },
            'collectionPeriod': data.get('record', {}).get('collectionPeriod', {}),
        }
    
    def _parse_metric(self, metric: Dict[str, Any]) -> Dict[str, Any]:
        """Parse individual metric data."""
        if not metric or not metric.get('percentiles'):
            return {
                'p75': None,
                'p90': None,
                'p99': None,
                'status': 'unavailable'
            }
        
        percentiles = metric.get('percentiles', {})
        return {
            'p75': percentiles.get('p75'),
            'p90': percentiles.get('p90'),
            'p99': percentiles.get('p99'),
            'distribution': metric.get('distribution', []),
            'status': 'available',
        }
    
    def _generate_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
        """Generate summary statistics for display."""
        metrics = ['lcp', 'cls', 'fcp']
        summary = {}
        
        for metric in metrics:
            values = []
            for result in results:
                metric_data = result.get('metrics', {}).get(metric, {})
                p75_value = metric_data.get('p75')
                if p75_value is not None:
                    values.append(float(p75_value))
            
            if values:
                summary[metric] = {
                    'avg': round(sum(values) / len(values), 2),
                    'min': min(values),
                    'max': max(values),
                    'count': len(values)
                }
            else:
                summary[metric] = {
                    'avg': 0,
                    'min': 0,
                    'max': 0,
                    'count': 0
                }
        
        return summary
