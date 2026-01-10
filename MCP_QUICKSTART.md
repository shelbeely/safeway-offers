# Safeway MCP Server - Quick Start

**Get started with the Safeway MCP Server in 5 minutes**

## What You Need

1. Python 3.8+
2. Claude Desktop
3. Safeway account (email, password, store ID)

## Installation

```bash
# Install dependencies
cd /path/to/safeway-offers
pip install -r requirements.txt
```

## Configuration

### Step 1: Find Your Store ID

Go to https://local.safeway.com/safeway.html, search for your store, and note the 4-digit ID.

### Step 2: Configure Claude Desktop

**macOS:**
```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```powershell
notepad %APPDATA%\Claude\claude_desktop_config.json
```

**Add this:**
```json
{
  "mcpServers": {
    "safeway": {
      "command": "python3",
      "args": ["/FULL/PATH/TO/safeway_mcp_server.py"],
      "env": {
        "SAFEWAY_USERNAME": "your-email@example.com",
        "SAFEWAY_PASSWORD": "your-password",
        "SAFEWAY_STORE_ID": "2948"
      }
    }
  }
}
```

**Replace:**
- `/FULL/PATH/TO/` with actual path (no `~`, use absolute path)
- Your actual Safeway email, password, and store ID
- Use `python` instead of `python3` on Windows

### Step 3: Restart Claude

Completely quit and reopen Claude Desktop.

## Verify Installation

In Claude, ask:
```
Do you have access to Safeway tools?
```

Claude should confirm it has 13 Safeway tools.

## First Commands

Try these to get started:

```
"What offers are available at my Safeway?"
```

```
"Load all my Safeway offers"
```

```
"Recommend dinner recipes using items on sale"
```

```
"Plan a week of meals for $100"
```

```
"Find the cheapest milk at my store"
```

## What the MCP Server Does

**13 AI-powered tools:**

1. **safeway_get_offers** - View all coupons/offers
2. **safeway_load_offers** - Load all offers to account
3. **safeway_add_offer** - Add specific offer
4. **safeway_explore_api** - Explore API capabilities
5. **safeway_check_api_status** - Check API health
6. **safeway_search_offers** - Search offers by keyword
7. **safeway_search_products** - Find products at store
8. **safeway_find_recipe_ingredients** - Check availability
9. **safeway_find_cheapest** - Find best prices
10. **safeway_budget_meal_plan** - Budget planning
11. **safeway_recommend_recipes** - Recipe ideas from sales
12. **safeway_build_shopping_list** - Shopping lists with prices
13. **safeway_weekly_meal_plan** - Weekly meal planning

## Example Use Cases

### Use Case 1: Weekly Meal Planning
```
"I have $100 for groceries this week. Plan 7 dinners using items on sale at Safeway."
```

### Use Case 2: Recipe from Sales
```
"What can I make for dinner tonight using items on sale?"
```

### Use Case 3: Budget Shopping
```
"Find the cheapest ingredients for chicken stir fry at my store."
```

### Use Case 4: Price Comparison
```
"Compare milk prices and tell me the cheapest option."
```

### Use Case 5: Complete Workflow
```
"I'm having a dinner party for 8 people with a $60 budget. 
Suggest a recipe, build a shopping list, and tell me if it fits my budget."
```

## Troubleshooting

**Tools not showing?**
- Restart Claude completely
- Check config file path is absolute
- Verify JSON syntax at jsonlint.com

**Authentication errors?**
- Test login at safeway.com
- Check credentials in config
- No spaces or typos in store ID

**Slow responses?**
- Safeway API can be slow
- Try again in a minute
- Reduce scope of request

## Full Documentation

For complete details, see:
- **[MCP_SERVER_GUIDE.md](MCP_SERVER_GUIDE.md)** - Complete guide (30,000 words!)
- **[COOKING_GUIDE.md](COOKING_GUIDE.md)** - Cooking workflows
- **[README_PYTHON.md](README_PYTHON.md)** - Python features

## Why Use MCP Server?

**Instead of typing commands:**
```bash
python safeway_api.py --recommend-recipes
python safeway_api.py --find-cheapest "milk"
python safeway_api.py --budget-plan chicken rice vegetables --max-budget 20
python safeway_api.py --build-shopping-list ...
```

**Just talk naturally:**
```
"Recommend recipes, find cheapest ingredients, 
plan a meal for under $20, and build me a shopping list"
```

Claude handles everything automatically!

## Get Help

- Review examples in [MCP_SERVER_GUIDE.md](MCP_SERVER_GUIDE.md)
- Check troubleshooting section
- Ask Claude: "How do I use Safeway tools?"

---

**You're ready!** Start chatting with Claude about your groceries. 🛒
