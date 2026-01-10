"""Pytest configuration and shared fixtures for Safeway MCP Server tests"""
import pytest
import os
from unittest.mock import Mock, MagicMock

@pytest.fixture
def mock_credentials():
    """Provide mock Safeway credentials for testing"""
    return {
        'username': 'test@example.com',
        'password': 'test_password_123',
        'store_id': '2948'
    }

@pytest.fixture
def mock_env_vars(monkeypatch, mock_credentials):
    """Set environment variables for testing"""
    monkeypatch.setenv('SAFEWAY_USERNAME', mock_credentials['username'])
    monkeypatch.setenv('SAFEWAY_PASSWORD', mock_credentials['password'])
    monkeypatch.setenv('SAFEWAY_STORE_ID', mock_credentials['store_id'])
    return mock_credentials

@pytest.fixture
def mock_requests(monkeypatch):
    """Mock requests library for API calls"""
    mock_session = MagicMock()
    
    # Mock authentication
    auth_response = Mock()
    auth_response.status_code = 200
    auth_response.json.return_value = {'access_token': 'mock_token_abc123', 'token_type': 'Bearer', 'expires_in': 3600}
    
    # Mock offers endpoint
    offers_response = Mock()
    offers_response.status_code = 200
    offers_response.json.return_value = {
        'offers': [
            {'offerId': 'OFFER123', 'description': 'Save $2 on Milk', 'offerType': 'PD', 'offerPrice': '$2.99', 'isLoaded': False}
        ]
    }
    
    # Configure session mock
    mock_session.post.return_value = auth_response
    mock_session.get.return_value = offers_response
    
    # Patch requests.Session
    mock_session_class = Mock(return_value=mock_session)
    monkeypatch.setattr('requests.Session', mock_session_class)
    
    return mock_session
