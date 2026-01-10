"""Integration tests for PantryPilot"""
import pytest

@pytest.mark.integration
def test_full_workflow_mock(mock_env_vars, mock_requests):
    """Test complete workflow with mocked APIs"""
    from safeway_api import SafewayAPIClient
    
    client = SafewayAPIClient(
        mock_env_vars['username'],
        mock_env_vars['password'],
        mock_env_vars['store_id']
    )
    
    # Test authentication
    assert client.authenticate() is True
    
    # Test getting offers
    offers = client.get_manufacturer_coupons()
    assert isinstance(offers, (list, type(None)))

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
