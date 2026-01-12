"""Unit tests for Safeway API Client"""
import pytest
from unittest.mock import Mock, patch, MagicMock

def test_client_initialization(mock_credentials):
    """Test client initializes with correct credentials"""
    from safeway_api import SafewayAPIClient
    client = SafewayAPIClient(
        mock_credentials['username'],
        mock_credentials['password'],
        mock_credentials['store_id']
    )
    assert client.username == mock_credentials['username']
    assert client.password == mock_credentials['password']
    assert client.store_id == mock_credentials['store_id']

def test_endpoints_are_https():
    """Test all API endpoints use HTTPS"""
    from safeway_api import SafewayEndpoints
    endpoints = [
        SafewayEndpoints.OAUTH_TOKEN,
        SafewayEndpoints.MANUFACTURER_COUPONS,
        SafewayEndpoints.PERSONALIZED_OFFERS,
        SafewayEndpoints.PRODUCT_SEARCH
    ]
    for endpoint in endpoints:
        assert endpoint.startswith('https://'), f"Endpoint {endpoint} is not HTTPS"

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
