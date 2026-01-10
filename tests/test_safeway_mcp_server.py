"""Unit tests for PantryPilot"""
import pytest

def test_server_initialization():
    """Test MCP server initializes correctly"""
    import safeway_mcp_server
    assert safeway_mcp_server.app is not None
    assert safeway_mcp_server.app.name == "safeway-api"

def test_environment_variables_required(monkeypatch):
    """Test that environment variables are required"""
    # Remove environment variables
    monkeypatch.delenv('SAFEWAY_USERNAME', raising=False)
    monkeypatch.delenv('SAFEWAY_PASSWORD', raising=False)
    monkeypatch.delenv('SAFEWAY_STORE_ID', raising=False)
    
    import safeway_mcp_server
    safeway_mcp_server._client = None
    
    # Should fail without credentials
    with pytest.raises((ValueError, RuntimeError)):
        safeway_mcp_server.get_client()

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
