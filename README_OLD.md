# PantryPilot

**PantryPilot - AI-Powered Grocery Assistant**

The **PantryPilot** is an AI-powered tool that connects Claude (and other AI assistants) directly to your Safeway account for intelligent grocery shopping, meal planning, and budget management.

> **⚡ The MCP Server is the primary and recommended way to use this tool.**

## Quick Start

1. **Install:** `pip install -r requirements.txt`
2. **Configure Claude Desktop** with your Safeway credentials
3. **Start chatting:** "What's on sale at my Safeway?"

👉 **[5-Minute Setup Guide](MCP_QUICKSTART.md)**

## What It Does

Talk to Claude in natural language to:

- 🛒 **"Load all my Safeway offers"** - Automatically clip all coupons
- 🍳 **"Recommend dinner recipes using sale items"** - Get recipe ideas based on current sales
- 💰 **"Plan a week of meals for $100"** - Budget-conscious meal planning
- 📋 **"Build a shopping list for lasagna with prices"** - Complete lists with cost estimates
- 💵 **"Find the cheapest chicken breast"** - Price comparison across products

**No commands to memorize. No syntax to learn. Just talk.**

## Why Use the MCP Server?

### Traditional CLI:
```bash
# Multiple commands needed
python safeway_api.py --search-product "milk"
python safeway_api.py --find-cheapest "milk"  
python safeway_api.py --recommend-recipes
python safeway_api.py --budget-plan milk eggs bread
python safeway_api.py --build-shopping-list ...
```

### MCP Server:
```
You: "Find the cheapest milk and recommend recipes I can make with it"
Claude: [Automatically handles everything]
```

**The AI assistant:**
- Understands context and conversation flow
- Handles complex multi-step workflows
- Makes intelligent recommendations
- Tracks your budget automatically
- Suggests alternatives when needed

## Documentation

### MCP Server (Primary Interface)
- **[Quick Start](MCP_QUICKSTART.md)** - 5-minute setup ⭐ START HERE
- **[Complete Guide](MCP_SERVER_GUIDE.md)** - 30,000-word comprehensive documentation
- **[Cooking Workflows](COOKING_GUIDE.md)** - Recipe and meal planning examples

### Additional Resources
- **[Python CLI](README_PYTHON.md)** - Command-line usage (alternative to MCP)
- **[Recipe Guide](RECIPE_GUIDE.md)** - Recipe-specific features
- **[API Status](API_STATUS.md)** - API availability information

## Features

### 13 AI-Powered Tools

1. **Offer Management** - View, search, and load coupons
2. **Product Search** - Find items at your local store
3. **Price Comparison** - Find cheapest options
4. **Recipe Recommendations** - Ideas based on current sales
5. **Shopping Lists** - With price estimates and sale indicators
6. **Budget Planning** - Track spending, cost per serving
7. **Weekly Meal Plans** - Automated multi-day planning
8. **Ingredient Checking** - Verify availability before shopping
9. **API Exploration** - Discover available data
10. **Status Monitoring** - Check API health
11. **Offer Search** - Find specific deals
12. **Budget Meal Planning** - Stay within spending limits
13. **Complete Workflows** - End-to-end grocery automation

## Example Conversations

### Weekly Meal Planning
```
You: "I have $120 for groceries this week. Plan 7 dinners."

Claude: 
- Checks current sales at your store
- Generates 7 different recipes
- Builds complete shopping list
- Calculates total cost: $117.50
- Shows savings: $32 with sale items
- Loads available coupons
```

### Quick Dinner Ideas
```
You: "What can I make for dinner with items on sale?"

Claude:
- Analyzes current sales
- Suggests 3 recipes
- Shows estimated costs
- Builds shopping list if you choose one
```

### Budget Shopping
```
You: "Find cheapest ingredients for chicken stir fry under $15"

Claude:
- Searches for each ingredient
- Finds lowest prices
- Calculates total: $13.50
- Shows you're under budget
- Creates shopping list
```

## Installation

### Prerequisites
- Python 3.8+
- Safeway account
- Claude Desktop (or MCP-compatible AI)

### Setup

```bash
# 1. Clone repository
git clone https://github.com/shelbeely/pantrypilot
cd pantrypilot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure Claude Desktop
# See MCP_QUICKSTART.md for detailed steps

# 4. Add your credentials to Claude's config file
```

**Full setup instructions:** [MCP_QUICKSTART.md](MCP_QUICKSTART.md)

## About the API

This tool uses Safeway's unofficial mobile API:
- ✅ Currently operational (January 2026)
- ⚠️ Unofficial - not documented by Safeway
- 🔒 Uses OAuth 2.0 authentication
- 📱 Same API used by Safeway mobile app
- ⚡ May change without notice

**Learn more:** [API_STATUS.md](API_STATUS.md)

## Architecture

```
You (natural language)
    ↓
Claude Desktop (AI Assistant)
    ↓
MCP Server (this tool - runs locally)
    ↓
Safeway API
    ↓
Your Local Store Data
```

**Privacy:** All processing happens locally. Your credentials stay on your computer.

## Alternative Interfaces

While the **MCP Server is recommended**, you can also use:

### Python CLI
```bash
python safeway_api.py --recommend-recipes
python safeway_api.py --weekly-meal-plan --budget-per-day 15
```
[See Python CLI Guide](README_PYTHON.md)

### Flask Web Interface
```bash
python app.py
# Visit http://localhost:5000
```

### Go Version (Original)
```bash
./pantrypilot -u email -p pass -id 2948
```

## Use Cases

- **Busy Families** - Automate weekly meal planning
- **Budget Conscious** - Track spending, find deals
- **Meal Preppers** - Plan bulk cooking sessions
- **Recipe Enthusiasts** - Discover new dishes from sales
- **Students** - Cheap meals within budget
- **Health Focused** - Meal plans with dietary restrictions
- **Learning to Cook** - Simple recipes with guidance

## Contributing

Contributions welcome! The MCP server is Python-based and easy to extend.

## License

Educational purposes. Use at your own risk. Unofficial API.

## Credits

- Original Go version: @giwty
- Python/MCP rewrite: @copilot
- Community contributions

---

**Ready to get started?**

👉 **[5-Minute Setup Guide](MCP_QUICKSTART.md)** ⭐

**Questions?**

- [Complete MCP Guide](MCP_SERVER_GUIDE.md) - Everything you need to know
- [Troubleshooting](MCP_SERVER_GUIDE.md#troubleshooting) - Common issues
- [Examples](MCP_SERVER_GUIDE.md#usage-examples) - Real conversations

**The MCP Server is the future of grocery automation.** 🚀

---

## Finding Your Safeway Store ID

Your store ID is a 4-digit number that identifies your local Safeway store.

**Easy method:**
1. Go to https://local.safeway.com/safeway.html
2. Search for your local store
3. Hover over "Weekly Ad" link
4. The URL shows: `storeId=2948` (your number may differ)

**Example Store IDs:**
- San Francisco area: 2948, 0534, 1614
- Seattle area: 1024, 1574, 3132
- Denver area: 3124, 1520, 0354

---

## API Status (Updated January 2026)

**The Safeway API is operational as of January 2026**, though it's an unofficial/undocumented API used by the Safeway mobile app.

- ✅ Currently working: `nimbus.safeway.com` and `albertsons.okta.com`
- 🔒 Uses OAuth 2.0 authentication via Okta
- ⚠️ **Unofficial API** - Safeway/Albertsons may change or discontinue it without notice
- 🔄 The mobile app uses the same API, so as long as the app works, this should work

📋 **For detailed information:** [API_STATUS.md](API_STATUS.md)

---

## Appendix: Alternative Interfaces

### Go Version (Original Command-Line Tool)

The original Go version is still available for users who prefer a simple command-line binary.

**Usage:**
```bash
# Check API status
./pantrypilot -check-api

# Load offers
./pantrypilot -u "email" -p "password" -id "2948"
```

**Windows:**
```
pantrypilot.exe -u "email" -p "password" -id "2948"
```

**Finding the binary:**
- Download from releases page
- Or build from source: `go build`

**Note:** The Go version only loads offers. For recipe recommendations, meal planning, and budget features, use the MCP Server.

### Direct Python CLI

For users who prefer command-line over AI chat:

```bash
python safeway_api.py --recommend-recipes
python safeway_api.py --weekly-meal-plan --budget-per-day 15
python safeway_api.py --build-shopping-list milk eggs flour --recipe-name "Pancakes"
```

See [README_PYTHON.md](README_PYTHON.md) for full CLI documentation.

### Flask Web Interface

For users who prefer a web browser:

```bash
python app.py
# Visit http://localhost:5000
```

**Note:** Web interface is basic. MCP Server with Claude provides better experience.

---

## Security & Privacy

- **Credentials:** Stored locally in Claude's config file (secure location)
- **Data:** MCP server runs on your computer, communicates directly with Safeway
- **Privacy:** Claude only sees tool results, not your credentials
- **Network:** All API calls go directly from your computer to Safeway

---

**The recommended way to use this tool is the MCP Server with Claude Desktop.**

---

## Troubleshooting

### MCP Server Issues

**Problem:** Claude doesn't see Safeway tools

**Solution:**
1. Completely restart Claude Desktop (quit, don't just close)
2. Verify config file path is correct and absolute
3. Check JSON syntax at jsonlint.com
4. See [MCP_SERVER_GUIDE.md#troubleshooting](MCP_SERVER_GUIDE.md#troubleshooting)

**Problem:** Authentication errors

**Solution:**
1. Test login at safeway.com with same credentials
2. Check for typos in config file
3. Verify store ID is a 4-digit number as a string
4. Reset password if needed

**Problem:** API not working

**Solution:**
1. Check if Safeway mobile app works
2. Try again in a few minutes (API can be slow)
3. See [API_STATUS.md](API_STATUS.md) for current status

### Complete Troubleshooting Guide

See [MCP_SERVER_GUIDE.md](MCP_SERVER_GUIDE.md#troubleshooting) for:
- Detailed error messages and solutions
- Network and connectivity issues
- Configuration problems
- Performance optimization

---

## Development & Contributing

The MCP server is Python-based and easy to extend:

```python
# Add a new tool in safeway_mcp_server.py

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="safeway_my_custom_tool",
            description="What it does",
            inputSchema={...}
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any):
    if name == "safeway_my_custom_tool":
        # Your logic here
        return [TextContent(type="text", text=result)]
```

**Contributions welcome!**

---

## License

This project is for educational purposes. Use at your own risk.

**Important:**
- Uses unofficial/undocumented Safeway API
- May violate Safeway's terms of service
- Safeway could block access at any time
- No warranty or support provided

---

## Credits & Acknowledgments

- **Original Go version:** @giwty - Created the first Safeway offers loader
- **Python/MCP rewrite:** @copilot - Added AI integration and cooking features
- **Community:** Thank you to all contributors and testers!

**Special thanks to:**
- Safeway/Albertsons for (unintentionally) providing API access
- Claude/Anthropic for MCP protocol
- The open-source community

---

## Additional Resources

### Documentation
- **[MCP_QUICKSTART.md](MCP_QUICKSTART.md)** - 5-minute setup ⭐
- **[MCP_SERVER_GUIDE.md](MCP_SERVER_GUIDE.md)** - Complete guide (30,000 words)
- **[COOKING_GUIDE.md](COOKING_GUIDE.md)** - Cooking workflows and examples
- **[RECIPE_GUIDE.md](RECIPE_GUIDE.md)** - Recipe-specific features
- **[README_PYTHON.md](README_PYTHON.md)** - Python CLI documentation
- **[API_STATUS.md](API_STATUS.md)** - API availability and status
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Project architecture

### Support
- **Issues:** [GitHub Issues](https://github.com/shelbeely/pantrypilot/issues)
- **Discussions:** [GitHub Discussions](https://github.com/shelbeely/pantrypilot/discussions)

---

**🚀 Ready to automate your grocery shopping?**

👉 **[Start with 5-Minute Setup](MCP_QUICKSTART.md)**

**Questions? Check the [Complete MCP Guide](MCP_SERVER_GUIDE.md)**
- **"Cannot resolve host"**: Network connectivity issue or the API domain has changed
- **"Non 200 response"**: The API structure may have changed, or there's a temporary service issue

### Finding Updated API Information

If the API has changed, you may need to:
1. Use a proxy tool (like Charles Proxy or mitmproxy) to inspect the Safeway mobile app's network traffic
2. Look for updated OAuth endpoints and client credentials
3. Check the community for other tools that may have been updated

For more information on reverse engineering private APIs, see: https://blog.jonlu.ca/posts/safeway

