# Project Summary - Safeway API Tool

## What We've Built

This project now provides **three ways** to interact with the Safeway API:

### 1. 🐍 Python CLI Tool (`safeway_api.py`)
A command-line interface for:
- Loading all offers automatically
- Exploring API endpoints
- Checking API status
- Searching through offers

**Usage:**
```bash
python safeway_api.py -u email@example.com -p password -id 2948
python safeway_api.py --explore --endpoint=all
python safeway_api.py --check-api
```

### 2. 🌐 Web Interface (`app.py`)
A Flask-based web application providing:
- User-friendly dashboard
- Visual offer management
- Real-time API exploration
- Status monitoring

**Usage:**
```bash
export SAFEWAY_USERNAME="email@example.com"
export SAFEWAY_PASSWORD="password"
export SAFEWAY_STORE_ID="2948"
python app.py
# Visit http://localhost:5000
```

### 3. 🤖 MCP Server (`safeway_mcp_server.py`)
Model Context Protocol server for AI assistants (Claude, etc.):
- Direct API access from AI chat
- Natural language interface
- Automated offer management
- API exploration through conversation

**Setup:** Add to Claude Desktop config:
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

**Then ask Claude:**
- "What Safeway offers are available?"
- "Load all my Safeway offers"
- "Search for milk coupons at Safeway"

## API Capabilities

### ✅ Confirmed Working (January 2026)
- **Manufacturer Coupons** - Generic coupons from brands
- **Personalized Offers** - Deals based on shopping history
- **Shopping List** - View already loaded offers
- **Add Offers** - Clip coupons/deals to account

### 🔍 Exploratory Features
The API may also provide (requires testing):
- Product search and catalog
- Store information (hours, location, services)
- Account details
- Shopping cart
- Weekly ad items
- Order history

Use `--explore` to discover what's available!

## GitHub Actions Integration

Automate offer loading with GitHub Actions:
1. Fork the repository
2. Add secrets: `SAFEWAY_USERNAME`, `SAFEWAY_PASSWORD`, `SAFEWAY_STORE_ID`
3. Workflow runs weekly on Sundays at 8 AM UTC

## Technical Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Safeway API                           │
│  (nimbus.safeway.com + albertsons.okta.com)             │
└──────────────────┬──────────────────────────────────────┘
                   │
                   │ OAuth 2.0
                   │
    ┌──────────────┴───────────────┐
    │                              │
┌───▼────────┐  ┌─────────────┐  ┌▼──────────────┐
│  CLI Tool  │  │ Web Interface│  │  MCP Server   │
│  (Python)  │  │   (Flask)    │  │  (for AI)     │
└────────────┘  └──────────────┘  └───────────────┘
     │                │                    │
     │                │                    │
     └────────────────┴────────────────────┘
                      │
              ┌───────▼────────┐
              │   End Users     │
              │  - CLI users    │
              │  - Web users    │
              │  - AI assistants│
              └─────────────────┘
```

## Security Best Practices

✅ Environment variables for credentials
✅ No credentials in code
✅ Secret management via GitHub Secrets
✅ Session-based auth for web interface
✅ Secure config file for MCP server

## Migration Guide

### From Go to Python

**Before (Go):**
```bash
./pantrypilot -u "email" -p "pass" -id "2948"
```

**After (Python):**
```bash
python safeway_api.py -u "email" -p "pass" -id "2948"
```

**Advantages of Python version:**
- More accessible to web developers
- Easier to modify and extend
- Web interface included
- AI assistant integration
- Better error messages
- Native async support

## What's New

### vs Original Go Version:
✨ Python rewrite for accessibility
✨ Web interface with Flask
✨ MCP server for AI integration
✨ Enhanced API exploration
✨ GitHub Actions workflow
✨ Environment variable support
✨ Comprehensive documentation
✨ Better error handling

## API Status

✅ **Still Working** as of January 2026

⚠️ **Important Notes:**
- Unofficial API (not documented by Safeway)
- May change without notice
- Use at your own risk
- May violate terms of service

See [API_STATUS.md](API_STATUS.md) for detailed information.

## Next Steps

### For Users:
1. Choose your preferred interface (CLI, Web, or MCP)
2. Install Python dependencies: `pip install -r requirements.txt`
3. Set up credentials
4. Start using!

### For Developers:
1. Fork the repository
2. Explore the code (`safeway_api.py` is the core)
3. Extend with new features
4. Submit pull requests

### For AI Enthusiasts:
1. Install MCP SDK: `pip install mcp`
2. Configure Claude Desktop
3. Start chatting with your Safeway account!

## Files Overview

```
pantrypilot/
├── safeway_api.py              # Core Python API client + CLI
├── app.py                      # Flask web interface
├── safeway_mcp_server.py       # MCP server for AI assistants
├── requirements.txt            # Python dependencies
├── mcp_config_example.json     # Example MCP configuration
├── README.md                   # Main documentation (both versions)
├── README_PYTHON.md            # Python-specific documentation
├── API_STATUS.md               # Detailed API status report
├── .github/workflows/
│   └── load-offers.yml         # GitHub Actions workflow
├── main.go                     # Original Go version (legacy)
├── check_api.go                # Go API checker (legacy)
├── api_types.go                # Go type definitions (legacy)
└── explore_api.go              # Go API explorer (legacy)
```

## Community & Support

- 📖 [Full Documentation](README_PYTHON.md)
- 🔍 [API Status](API_STATUS.md)
- 🐛 [Report Issues](https://github.com/shelbeely/pantrypilot/issues)
- 💬 [Discussions](https://github.com/shelbeely/pantrypilot/discussions)

## Credits

- **Original Go version:** @giwty
- **Python rewrite + Web/MCP:** This PR
- **API research:** Community contributors
- **Inspiration:** Automating tedious coupon clipping!

## License

Educational purposes only. Use at your own risk.

---

**Built with ❤️ for the Safeway coupon clipping community**
