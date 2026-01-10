# Safeway API - Python Edition

A Python-based client for interacting with Safeway's unofficial mobile API, with support for:
- **CLI tool** for command-line usage
- **Web interface** using Flask
- **MCP Server** for AI assistant integration (Claude, etc.)

## What's New - Python Rewrite

This project has been rewritten in Python with web technologies for better accessibility:

✨ **New Features:**
- 🐍 Python-based for easier understanding and modification
- 🌐 Web interface with Flask
- 🤖 Model Context Protocol (MCP) server for AI assistants
- 🔍 Enhanced API exploration capabilities
- 🔐 Environment variable support for credentials
- 📦 Simple pip installation

## Quick Start

### Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Or install specific components:
pip install requests  # For CLI only
pip install requests flask  # For CLI + Web interface
pip install requests mcp  # For CLI + MCP server
```

### CLI Usage

```bash
# Set credentials as environment variables
export SAFEWAY_USERNAME="your-email@example.com"
export SAFEWAY_PASSWORD="your-password"
export SAFEWAY_STORE_ID="2948"

# Load all offers
python safeway_api.py

# Or pass credentials as arguments
python safeway_api.py -u "email@example.com" -p "password" -id "2948"

# Check API status
python safeway_api.py --check-api

# Explore API endpoints
python safeway_api.py --explore --endpoint=all
python safeway_api.py --explore --endpoint=offers
python safeway_api.py --explore --endpoint=products
```

### Web Interface

```bash
# Set credentials
export SAFEWAY_USERNAME="your-email@example.com"
export SAFEWAY_PASSWORD="your-password"
export SAFEWAY_STORE_ID="2948"
export SECRET_KEY="your-secret-key-for-sessions"

# Start the web server
python app.py

# Open browser to http://localhost:5000
```

The web interface provides:
- 📊 Dashboard showing available offers
- 🔘 One-click to load all offers
- 🔍 API explorer to see what data is available
- 📈 Real-time API status checking

### MCP Server for AI Assistants

The MCP server allows AI assistants like Claude to interact with your Safeway account.

**Setup:**

1. Install MCP SDK:
```bash
pip install mcp
```

2. Configure Claude Desktop (or other MCP client):

Edit your MCP settings file:
- **MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add this configuration:

```json
{
  "mcpServers": {
    "safeway": {
      "command": "python",
      "args": ["/path/to/safeway_mcp_server.py"],
      "env": {
        "SAFEWAY_USERNAME": "your-email@example.com",
        "SAFEWAY_PASSWORD": "your-password",
        "SAFEWAY_STORE_ID": "2948"
      }
    }
  }
}
```

3. Restart Claude Desktop

**Available MCP Tools:**

Once configured, Claude can:
- `safeway_get_offers` - View all available offers and coupons
- `safeway_load_offers` - Automatically load all offers to your account
- `safeway_add_offer` - Add specific offers by ID
- `safeway_explore_api` - Explore what data is available in the API
- `safeway_check_api_status` - Check if API endpoints are working
- `safeway_search_offers` - Search offers by keyword

**Example Prompts for Claude:**

```
"Check what Safeway offers are available for me"
"Load all my Safeway offers"
"Search for milk offers at Safeway"
"Explore what other data the Safeway API provides"
"Check if the Safeway API is working"
```

## GitHub Actions (Automated Offer Loading)

You can set up a GitHub Action to automatically load offers weekly:

1. Fork this repository
2. Go to Settings → Secrets → Actions
3. Add these secrets:
   - `SAFEWAY_USERNAME`
   - `SAFEWAY_PASSWORD`
   - `SAFEWAY_STORE_ID`
4. The workflow will run weekly on Sundays at 8 AM

See `.github/workflows/load-offers.yml` for details.

## API Features

### Core Functionality
- ✅ Manufacturer coupons
- ✅ Personalized offers
- ✅ Shopping list (already loaded offers)
- ✅ Add offers to account

### Additional API Endpoints (Exploration)
The API provides access to more features (may require additional parameters):
- 🔍 Product search
- 🏪 Store information
- 👤 Account details
- 🛒 Shopping cart
- 📰 Weekly ads
- 📦 Order history

Use the `--explore` flag or web interface to discover what's available.

## Architecture

```
safeway-offers/
├── safeway_api.py          # Core API client (CLI)
├── app.py                  # Flask web interface
├── safeway_mcp_server.py   # MCP server for AI assistants
├── requirements.txt        # Python dependencies
├── templates/              # HTML templates for web UI
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   └── explore.html
├── static/                 # CSS, JS for web UI
│   └── style.css
└── .github/
    └── workflows/
        └── load-offers.yml # GitHub Action workflow
```

## API Status (January 2026)

✅ **The Safeway API is still operational** as of January 2026.

**Important Notes:**
- ⚠️ This is an **unofficial API** - not documented or supported by Safeway
- 🔒 Uses Okta OAuth 2.0 for authentication
- 🔄 API may change without notice
- ⚖️ Use at your own risk - may violate terms of service

For detailed API status information, see [API_STATUS.md](API_STATUS.md)

## Finding Your Store ID

1. Go to https://local.safeway.com/safeway.html
2. Search for your local store
3. Hover over the "Weekly Ad" link
4. The URL will show something like: `https://www.safeway.com/set-store.html?storeId=2948&target=weeklyad`
5. The store ID is the number after `storeId=` (e.g., `2948`)

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
# Format code
black safeway_api.py app.py safeway_mcp_server.py

# Lint code
flake8 safeway_api.py app.py safeway_mcp_server.py

# Type checking
mypy safeway_api.py
```

## Migrating from Go Version

If you were using the Go version:

**Old (Go):**
```bash
./safeway-offers -u "email" -p "pass" -id "2948"
```

**New (Python):**
```bash
python safeway_api.py -u "email" -p "pass" -id "2948"
```

The Python version offers the same functionality plus:
- Web interface
- MCP server for AI integration
- Better error messages
- Easier to modify and extend

## Troubleshooting

### Authentication Issues

```bash
# Test authentication
python safeway_api.py -u "email" -p "pass" -id "2948" --explore --endpoint=offers
```

If authentication fails:
- Verify credentials are correct
- Try logging into the Safeway website/app
- Check if your account is locked

### API Not Working

```bash
# Check API status
python safeway_api.py --check-api
```

If endpoints are not accessible:
- The API may have changed
- Network connectivity issues
- Safeway may have updated their infrastructure

See [API_STATUS.md](API_STATUS.md) for detailed troubleshooting.

## Security Notes

- 🔐 Never commit credentials to Git
- 🔑 Use environment variables for sensitive data
- 🛡️ The web interface requires a SECRET_KEY for sessions
- ⚠️ MCP server credentials are stored in Claude's config file (secure location)

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes. Use at your own risk.

## Credits

- Original Go version by @giwty
- Python rewrite with web/MCP support
- MCP integration for AI assistant compatibility

## Support

- 📖 [API Documentation](API_STATUS.md)
- 🐛 [Issue Tracker](https://github.com/shelbeely/safeway-offers/issues)
- 💬 [Discussions](https://github.com/shelbeely/safeway-offers/discussions)
