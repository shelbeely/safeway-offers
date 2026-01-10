# Safeway API - Python Edition

A Python-based client for interacting with Safeway's unofficial mobile API, with support for:
- **CLI tool** for command-line usage
- **Web interface** using Flask
- **MCP Server** for AI assistant integration (Claude, etc.)
- **🍳 Complete Cooking Assistant** - Recipe recommendations, meal planning, budget tracking

## What's New - Python Rewrite with Cooking Features

This project has been rewritten in Python with comprehensive cooking and recipe features:

✨ **Core Features:**
- 🐍 Python-based for easier understanding and modification
- 🌐 Web interface with Flask
- 🤖 Model Context Protocol (MCP) server for AI assistants

✨ **Cooking & Recipe Features:**
- 🍳 **Recipe recommendations from current sales** - Get inspired by what's on sale!
- 💰 **Budget meal planning** - Plan meals within your budget
- 🛒 **Smart shopping lists** - With price estimates and sale indicators
- 📅 **Weekly meal plans** - Automated 7-day plans based on sales
- 💵 **Price comparison** - Find cheapest options for ingredients
- 📊 **Cost tracking** - Per-serving and total meal costs

## 🎯 Perfect For

- **AI-Generated Recipes**: "Generate a recipe using sale items at my Safeway"
- **Budget Cooking**: "Plan dinners for $15/day using current sales"
- **Meal Planning**: "Create a week of meals with my $100 budget"
- **Price Shopping**: "Find the cheapest ingredients for lasagna"

👉 **[Complete Cooking Guide](COOKING_GUIDE.md)** - Everything you need to know!

## 🍳 Using for AI-Generated Recipes & Meal Planning

**New!** Complete cooking assistant with budget tracking and recipe recommendations.

```bash
# Get recipe recommendations from current sales
python safeway_api.py --recommend-recipes

# Find cheapest ingredients
python safeway_api.py --find-cheapest "chicken breast"

# Plan a budget meal
python safeway_api.py --budget-plan chicken rice vegetables --max-budget 20.00

# Build shopping list with prices
python safeway_api.py --build-shopping-list milk eggs flour butter \
    --recipe-name "Pancakes" --servings 4

# Generate weekly meal plan
python safeway_api.py --weekly-meal-plan --days 7 --budget-per-day 15.00
```

**With AI Assistants (Claude):**
- "Recommend recipes using items on sale at my Safeway"
- "Plan a week of dinners for $100 total"
- "Find the cheapest way to make lasagna"
- "Build a shopping list for chicken stir fry with prices"

👉 **[Complete Cooking Guide](COOKING_GUIDE.md)** | **[Recipe Basics](RECIPE_GUIDE.md)**

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

# Search for products (NEW - great for recipes!)
python safeway_api.py --search-product "chicken breast"
python safeway_api.py --search-product "organic tomatoes"

# Find recipe ingredients (NEW)
python safeway_api.py --find-ingredients milk eggs flour butter
python safeway_api.py --find-ingredients "ground beef" "taco shells" cheese lettuce
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
- **`safeway_search_products`** - Search for products at your local store (NEW)
- **`safeway_find_recipe_ingredients`** - Check recipe ingredient availability (NEW)

**Example Prompts for Claude:**

```
"Check what Safeway offers are available for me"
"Load all my Safeway offers"
"Search for milk offers at Safeway"
"Explore what other data the Safeway API provides"
"Check if the Safeway API is working"

NEW - Recipe Support:
"Search for chicken breast at my local Safeway"
"Check if these ingredients are available: milk, eggs, flour, butter, sugar"
"Generate a dinner recipe using ingredients on sale at Safeway"
"Find all ingredients for chocolate chip cookies at my store"
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
pantrypilot/
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
./pantrypilot -u "email" -p "pass" -id "2948"
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
- 🐛 [Issue Tracker](https://github.com/shelbeely/pantrypilot/issues)
- 💬 [Discussions](https://github.com/shelbeely/pantrypilot/discussions)
