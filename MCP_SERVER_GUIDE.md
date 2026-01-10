# PantryPilot - Complete Documentation

**Model Context Protocol Server for Safeway API Integration**

The PantryPilot is the **primary and recommended interface** for interacting with Safeway's API. It enables AI assistants like Claude to directly access your Safeway account for recipe planning, meal budgeting, and grocery shopping.

---

## Table of Contents

1. [What is MCP?](#what-is-mcp)
2. [Why Use the MCP Server?](#why-use-the-mcp-server)
3. [Installation & Setup](#installation--setup)
4. [Configuration Guide](#configuration-guide)
5. [Available Tools](#available-tools)
6. [Usage Examples](#usage-examples)
7. [Advanced Features](#advanced-features)
8. [Troubleshooting](#troubleshooting)
9. [Security Considerations](#security-considerations)
10. [API Reference](#api-reference)

---

## What is MCP?

**Model Context Protocol (MCP)** is a standard protocol that allows AI assistants to interact with external tools and services. The PantryPilot implements this protocol to give AI assistants like Claude direct access to the Safeway API.

### Key Benefits

- **Natural Language Interface**: Talk to your Safeway account in plain English
- **No Manual Commands**: AI assistant handles all API interactions
- **Context-Aware**: AI understands your grocery needs and preferences
- **Automated Workflows**: Complex tasks handled in a single conversation
- **Real-time Data**: Always uses current sale prices and availability

### How It Works

```
You (natural language)
    ↓
Claude (AI Assistant)
    ↓
MCP Server (this tool)
    ↓
Safeway API
    ↓
Your Local Store Data
```

---

## Why Use the MCP Server?

The MCP Server is the **recommended way** to interact with Safeway's API because:

### 1. Simplicity
**Without MCP:**
```bash
# Manual command for each task
python safeway_api.py --search-product "milk"
python safeway_api.py --find-cheapest "milk"
python safeway_api.py --budget-plan milk eggs bread --max-budget 15
# ... multiple separate commands
```

**With MCP:**
```
You: "Find the cheapest milk at my Safeway and add it to a shopping list"
Claude: [Automatically searches, compares prices, and creates list]
```

### 2. Intelligence
The AI assistant can:
- Understand context ("that recipe" vs "the stir fry we discussed")
- Make recommendations based on your budget
- Suggest alternatives when items aren't available
- Remember preferences across conversation
- Handle complex multi-step workflows

### 3. Flexibility
One conversation can:
- Get recipe recommendations
- Check ingredient availability
- Compare prices
- Build shopping list
- Estimate costs
- Track budget
- Load coupons

### 4. No Learning Curve
- No commands to memorize
- No syntax to learn
- Just talk naturally about your grocery needs

---

## Installation & Setup

### Prerequisites

1. **Python 3.8 or higher**
   ```bash
   python3 --version
   # Should show 3.8 or higher
   ```

2. **Safeway Account**
   - Email and password
   - Your local store ID ([How to find](#finding-your-store-id))

3. **Claude Desktop** (or other MCP-compatible AI assistant)
   - Download from https://claude.ai/download

### Step 1: Install Python Dependencies

```bash
# Navigate to project directory
cd /path/to/pantrypilot

# Install required packages
pip install -r requirements.txt

# Verify MCP SDK is installed
python3 -c "import mcp; print('MCP SDK installed successfully')"
```

**If MCP is not installed:**
```bash
pip install mcp
```

### Step 2: Test the MCP Server

Before configuring Claude, test that the server works:

```bash
# Set your credentials temporarily
export SAFEWAY_USERNAME="your-email@example.com"
export SAFEWAY_PASSWORD="your-password"
export SAFEWAY_STORE_ID="2948"

# Test the server (should show no errors)
python3 safeway_mcp_server.py
```

**Expected output:**
```
INFO:safeway-mcp-server:Starting Safeway API MCP Server...
```

Press `Ctrl+C` to stop the test.

### Step 3: Configure Claude Desktop

#### On macOS

1. **Open configuration file:**
   ```bash
   # Open in default editor
   open ~/Library/Application\ Support/Claude/claude_desktop_config.json
   
   # Or use specific editor
   nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

2. **Add this configuration:**
   ```json
   {
     "mcpServers": {
       "safeway": {
         "command": "python3",
         "args": ["/absolute/path/to/pantrypilot/safeway_mcp_server.py"],
         "env": {
           "SAFEWAY_USERNAME": "your-email@example.com",
           "SAFEWAY_PASSWORD": "your-password",
           "SAFEWAY_STORE_ID": "2948"
         }
       }
     }
   }
   ```

3. **Important:**
   - Replace `/absolute/path/to/pantrypilot/` with your actual path
   - Use `python3` not `python` (unless your system uses `python`)
   - Use your actual Safeway credentials
   - Store ID must be a string in quotes

#### On Windows

1. **Open configuration file:**
   ```powershell
   # In PowerShell or Command Prompt
   notepad %APPDATA%\Claude\claude_desktop_config.json
   ```

2. **Add this configuration:**
   ```json
   {
     "mcpServers": {
       "safeway": {
         "command": "python",
         "args": ["C:\\full\\path\\to\\pantrypilot\\safeway_mcp_server.py"],
         "env": {
           "SAFEWAY_USERNAME": "your-email@example.com",
           "SAFEWAY_PASSWORD": "your-password",
           "SAFEWAY_STORE_ID": "2948"
         }
       }
     }
   }
   ```

3. **Important:**
   - Use double backslashes `\\` in Windows paths
   - Or use forward slashes: `C:/path/to/safeway_mcp_server.py`

#### On Linux

1. **Open configuration file:**
   ```bash
   # Create directory if it doesn't exist
   mkdir -p ~/.config/claude
   
   # Edit configuration
   nano ~/.config/claude/claude_desktop_config.json
   ```

2. **Add configuration** (same as macOS example above)

### Step 4: Restart Claude Desktop

**Important:** You MUST restart Claude Desktop for changes to take effect.

1. Quit Claude completely (not just close window)
2. Reopen Claude Desktop
3. The Safeway tools will now be available

### Step 5: Verify Installation

In Claude, try:

```
"Do you have access to Safeway tools?"
```

Claude should respond confirming it has access to 13 Safeway tools.

---

## Configuration Guide

### Finding Your Store ID

Your store ID is a 4-digit number that identifies your local Safeway.

**Method 1: From Safeway Website**

1. Go to https://local.safeway.com/safeway.html
2. Search for your local store
3. Click on your store
4. Look at the URL or hover over "Weekly Ad"
5. You'll see: `storeId=2948` (your number may differ)

**Method 2: From Safeway App**

1. Open Safeway mobile app
2. Go to "Store" or "My Store"
3. The store ID is usually shown in store details

**Common Store IDs:**
- San Francisco area: 2948, 0534, 1614
- Seattle area: 1024, 1574, 3132
- Denver area: 3124, 1520, 0354

### Environment Variables

The MCP server reads credentials from environment variables. You have three options:

#### Option 1: In MCP Configuration (Recommended)

Already shown in setup. Credentials are in `claude_desktop_config.json`.

#### Option 2: System Environment Variables

**macOS/Linux:**
```bash
# Add to ~/.bashrc or ~/.zshrc
export SAFEWAY_USERNAME="your-email@example.com"
export SAFEWAY_PASSWORD="your-password"
export SAFEWAY_STORE_ID="2948"
```

**Windows:**
```powershell
# In PowerShell (persistent)
[System.Environment]::SetEnvironmentVariable('SAFEWAY_USERNAME', 'your-email', 'User')
[System.Environment]::SetEnvironmentVariable('SAFEWAY_PASSWORD', 'your-password', 'User')
[System.Environment]::SetEnvironmentVariable('SAFEWAY_STORE_ID', '2948', 'User')
```

#### Option 3: .env File

Create `.env` file in project directory:
```bash
SAFEWAY_USERNAME=your-email@example.com
SAFEWAY_PASSWORD=your-password
SAFEWAY_STORE_ID=2948
```

Then modify MCP config to load it (requires python-dotenv).

### Multiple Store Support

To use different stores, create multiple MCP server configurations:

```json
{
  "mcpServers": {
    "safeway-home": {
      "command": "python3",
      "args": ["/path/to/safeway_mcp_server.py"],
      "env": {
        "SAFEWAY_USERNAME": "email@example.com",
        "SAFEWAY_PASSWORD": "password",
        "SAFEWAY_STORE_ID": "2948"
      }
    },
    "safeway-work": {
      "command": "python3",
      "args": ["/path/to/safeway_mcp_server.py"],
      "env": {
        "SAFEWAY_USERNAME": "email@example.com",
        "SAFEWAY_PASSWORD": "password",
        "SAFEWAY_STORE_ID": "1024"
      }
    }
  }
}
```

Then specify which to use:
```
"Check sales at my home Safeway" (uses safeway-home)
"What's on sale at work Safeway?" (uses safeway-work)
```

---

## Available Tools

The MCP server provides **13 tools** for comprehensive grocery management.

### 1. safeway_get_offers

**Purpose:** View all available coupons and offers

**What it does:**
- Retrieves manufacturer coupons
- Gets personalized offers based on your shopping history
- Optionally includes already-loaded offers

**Use cases:**
- "What offers are available at Safeway?"
- "Show me current Safeway coupons"
- "What deals do I have?"

**Parameters:**
- `include_loaded` (optional): Include offers already in your account

**Example output:**
```json
{
  "manufacturer_coupons": [
    {"id": "123", "description": "Save $1 on Milk", "type": "MF"}
  ],
  "personalized_offers": [
    {"id": "456", "name": "Chicken Sale", "description": "$2 off", "type": "PD"}
  ],
  "total_manufacturer": 25,
  "total_personalized": 18
}
```

### 2. safeway_load_offers

**Purpose:** Automatically load all available offers to your account

**What it does:**
- Clips all manufacturer coupons
- Loads all personalized deals
- Skips offers already in your account

**Use cases:**
- "Load all my Safeway offers"
- "Clip all available coupons"
- "Add all deals to my account"

**Parameters:** None

**Returns:** Number of new offers loaded

### 3. safeway_add_offer

**Purpose:** Add a specific offer by ID

**What it does:**
- Clips one specific coupon/offer
- Useful for selective loading

**Use cases:**
- "Add offer #12345 to my account"
- "Clip the $5 off chicken coupon"

**Parameters:**
- `offer_id` (required): The offer ID
- `offer_type` (optional): Type code (default: "PD")

### 4. safeway_explore_api

**Purpose:** Discover what data the Safeway API provides

**What it does:**
- Queries various API endpoints
- Shows available data structures
- Useful for development/debugging

**Use cases:**
- "What data is available from Safeway API?"
- "Explore Safeway API endpoints"

**Parameters:**
- `endpoint` (optional): Specific endpoint to explore
  - Options: all, offers, products, store, account, cart, weeklyad, orders

### 5. safeway_check_api_status

**Purpose:** Test if Safeway API is accessible

**What it does:**
- Checks connectivity to API endpoints
- No authentication required
- Quick health check

**Use cases:**
- "Is Safeway API working?"
- "Check Safeway API status"

**Parameters:** None

### 6. safeway_search_offers

**Purpose:** Search offers by keyword

**What it does:**
- Searches offer names and descriptions
- Finds relevant coupons

**Use cases:**
- "Search for milk offers"
- "Find bread coupons"
- "Show offers with 'save $5'"

**Parameters:**
- `query` (required): Search term

### 7. safeway_search_products

**Purpose:** Find products available at your store

**What it does:**
- Searches product catalog
- Shows availability at your store
- Returns up to specified limit

**Use cases:**
- "Search for chicken breast"
- "Find organic tomatoes"
- "What milk options are available?"

**Parameters:**
- `query` (required): Product name/keyword
- `limit` (optional): Max results (default: 20)

### 8. safeway_find_recipe_ingredients

**Purpose:** Check availability of multiple ingredients

**What it does:**
- Searches for each ingredient
- Reports found/not found status
- Returns product details

**Use cases:**
- "Can I find milk, eggs, and flour at Safeway?"
- "Check if ingredients for lasagna are available"

**Parameters:**
- `ingredients` (required): List of ingredient names

**Example:**
```json
{
  "ingredients": ["milk", "eggs", "flour", "butter"]
}
```

### 9. safeway_find_cheapest

**Purpose:** Find the lowest-priced option for a product

**What it does:**
- Searches for product
- Sorts by price
- Shows cheapest option and alternatives

**Use cases:**
- "What's the cheapest milk?"
- "Find the best price for chicken"

**Parameters:**
- `product` (required): Product name
- `limit` (optional): Number of alternatives (default: 10)

### 10. safeway_budget_meal_plan

**Purpose:** Plan a meal within budget constraints

**What it does:**
- Finds cheapest option for each ingredient
- Calculates total cost
- Checks against budget
- Shows what's missing

**Use cases:**
- "Plan a meal with chicken, rice, vegetables for $15"
- "Can I make pasta dinner for under $20?"

**Parameters:**
- `ingredients` (required): List of ingredients
- `max_budget` (optional): Budget limit in dollars

### 11. safeway_recommend_recipes ⭐

**Purpose:** Get recipe suggestions based on current sales

**What it does:**
- Analyzes items currently on sale
- Categorizes ingredients
- Matches to recipe templates
- Suggests complete recipes

**Use cases:**
- "What recipes can I make with sale items?"
- "Recommend dinners based on Safeway sales"
- "What should I cook this week?"

**Parameters:**
- `cuisine_type` (optional): Preferred cuisine
- `dietary_restrictions` (optional): List of restrictions

**This is one of the most powerful tools!**

### 12. safeway_build_shopping_list ⭐

**Purpose:** Create complete shopping list with prices

**What it does:**
- Checks availability of all ingredients
- Finds prices for each item
- Calculates total cost and per-serving cost
- Identifies sale items

**Use cases:**
- "Build a shopping list for chicken stir fry"
- "Create a list for chocolate chip cookies with prices"

**Parameters:**
- `recipe_name` (required): Name of recipe
- `ingredients` (required): List of ingredients
- `servings` (optional): Number of servings (default: 4)

### 13. safeway_weekly_meal_plan ⭐

**Purpose:** Generate complete weekly meal plan

**What it does:**
- Creates meal plan for multiple days
- Based on current sales
- Tracks daily budget
- Ensures variety in meals

**Use cases:**
- "Plan meals for the week"
- "Create 7 days of dinners for $100"
- "Generate meal plan with $15/day budget"

**Parameters:**
- `days` (optional): Number of days (default: 7)
- `budget_per_day` (optional): Daily budget limit

---

## Usage Examples

### Basic Examples

#### Example 1: Check What's On Sale

**You:**
```
What offers are available at my Safeway?
```

**Claude will:**
1. Use `safeway_get_offers`
2. Format the response nicely
3. Summarize key deals

**Claude's response:**
```
Here are your current Safeway offers:

Manufacturer Coupons (25 total):
- Save $1.00 on Milk (1 gallon)
- $2.00 off Chicken Breast
- Buy 2, Get 1 Free on Pasta
...

Personalized Offers (18 total):
- 20% off Fresh Produce
- $3.00 off $15 Meat Purchase
- Free bakery item with $10 purchase
...

Would you like me to load all these offers to your account?
```

#### Example 2: Load All Offers

**You:**
```
Yes, load all offers to my account
```

**Claude will:**
1. Use `safeway_load_offers`
2. Report results

**Claude's response:**
```
Done! I've loaded 43 new offers to your Safeway account:
- 25 manufacturer coupons
- 18 personalized deals

These are now active and will automatically apply at checkout.
```

#### Example 3: Search for Specific Product

**You:**
```
Search for organic chicken breast at my Safeway
```

**Claude will:**
1. Use `safeway_search_products` with query "organic chicken breast"
2. Show results

**Claude's response:**
```
Found 3 organic chicken breast options:

1. Foster Farms Organic Chicken Breast
   - Price: $8.99/lb
   - Available: Yes
   
2. Perdue Organic Boneless Breast
   - Price: $9.99/lb
   - Available: Yes
   
3. Store Brand Organic Chicken Breast
   - Price: $7.99/lb (BEST PRICE)
   - Available: Yes

Would you like me to add any to a shopping list?
```

### Intermediate Examples

#### Example 4: Recipe Ingredient Check

**You:**
```
I want to make pancakes. Check if I can get all ingredients at Safeway: 
flour, eggs, milk, butter, sugar, baking powder
```

**Claude will:**
1. Use `safeway_find_recipe_ingredients`
2. Check each item
3. Report availability

**Claude's response:**
```
Good news! All pancake ingredients are available at your Safeway:

✓ Flour - 8 products found
✓ Eggs - 4 products found  
✓ Milk - 12 products found
✓ Butter - 6 products found
✓ Sugar - 5 products found
✓ Baking powder - 3 products found

Would you like me to:
1. Find the cheapest options for each?
2. Build a shopping list with prices?
3. Check if any are on sale?
```

#### Example 5: Budget Planning

**You:**
```
I have $20 for dinner tonight. What's the cheapest way to make chicken stir fry?
```

**Claude will:**
1. Use `safeway_budget_meal_plan` with ingredients and budget
2. Find cheapest options
3. Calculate total

**Claude's response:**
```
Here's your budget chicken stir fry plan:

Ingredients (cheapest options):
- Chicken breast: $6.99
- Broccoli: $2.49
- Bell peppers: $2.99
- Rice: $3.49
- Soy sauce: $2.99
- Garlic: $0.79

Total: $19.74
Remaining budget: $0.26 ✓

This stays within your $20 budget! Would you like me to create a detailed shopping list?
```

### Advanced Examples

#### Example 6: Complete Meal Planning Workflow

**You:**
```
I have $100 for groceries this week. Plan 7 dinners using items on sale at Safeway.
```

**Claude will:**
1. Use `safeway_recommend_recipes` to see what's on sale
2. Use `safeway_weekly_meal_plan` with $14.28/day budget
3. For each recipe, use `safeway_build_shopping_list`
4. Compile comprehensive plan

**Claude's response:**
```
I've created your 7-day meal plan using Safeway sales:

Week Overview:
- Total budget: $100.00
- Estimated cost: $97.50
- Remaining: $2.50 ✓

Daily Meal Plan:

Monday - Chicken Stir Fry ($13.75)
Sale items used: Chicken breast ($2.99/lb), Broccoli
Additional: Rice, soy sauce, garlic

Tuesday - Pasta Carbonara ($12.50)
Sale items used: Pasta, Bacon
Additional: Eggs, parmesan, black pepper

Wednesday - Beef Tacos ($15.00)
Sale items used: Ground beef, Tortillas
Additional: Cheese, lettuce, tomatoes

Thursday - Vegetable Frittata ($10.25)
Sale items used: Eggs, Bell peppers
Additional: Cheese, onions, milk

Friday - Baked Salmon ($16.00)
Sale items used: Salmon fillets
Additional: Asparagus, lemon, olive oil

Saturday - Spaghetti Bolognese ($14.00)
Sale items used: Ground beef, Pasta sauce
Additional: Pasta, onions, garlic

Sunday - Roast Chicken Dinner ($16.00)
Sale items used: Whole chicken, Potatoes
Additional: Carrots, herbs, butter

Complete Shopping List:
[Detailed list with prices for all ingredients]

Would you like me to:
1. Create a detailed shopping list with exact quantities?
2. Adjust any meals to lower the cost?
3. Check for additional coupons?
```

#### Example 7: Recipe Discovery from Sales

**You:**
```
What can I make for dinner tonight? Show me 3 recipes using items on sale.
```

**Claude will:**
1. Use `safeway_recommend_recipes`
2. Pick top 3 most practical
3. Use `safeway_build_shopping_list` for each
4. Present options

**Claude's response:**
```
Based on current Safeway sales, here are 3 dinner options:

1. Honey Garlic Chicken ($14.50 for 4 servings)
   Sale items: Chicken thighs $2.99/lb, Honey
   Also need: Garlic, soy sauce, rice
   Cook time: 30 minutes
   
2. Vegetable Lasagna ($18.00 for 6 servings)
   Sale items: Lasagna noodles, Ricotta cheese, Mozzarella
   Also need: Tomato sauce, spinach, herbs
   Cook time: 60 minutes
   
3. Beef and Broccoli ($16.00 for 4 servings)
   Sale items: Flank steak $4.99/lb, Broccoli
   Also need: Soy sauce, ginger, rice
   Cook time: 25 minutes

Which would you like to make? I can create a detailed shopping list.
```

#### Example 8: Price Comparison Shopping

**You:**
```
Compare milk prices at Safeway. I need 2 gallons this week.
```

**Claude will:**
1. Use `safeway_find_cheapest` for "milk"
2. Calculate cost for 2 gallons
3. Show alternatives

**Claude's response:**
```
Here are your milk options at Safeway:

Cheapest Option:
Store Brand Whole Milk - $2.99/gallon
Cost for 2 gallons: $5.98 ✓ BEST PRICE

Alternatives:
1. Store Brand 2% Milk - $2.99/gallon ($5.98 for 2)
2. Horizon Organic Whole Milk - $4.99/gallon ($9.98 for 2)
3. Lactaid Milk - $5.49/gallon ($10.98 for 2)

Price range: $5.98 - $10.98 for 2 gallons
Savings with cheapest: $5.00

Current offers:
- No active milk coupons found

Recommendation: Go with store brand to save $5.00
```

---

## Advanced Features

### Context and Memory

The AI assistant remembers context within a conversation:

```
You: "What chicken is on sale?"
Claude: [Shows chicken options]

You: "What recipes can I make with the cheapest one?"
Claude: [Recommends recipes using that specific chicken]

You: "Build a shopping list for the first recipe"
Claude: [Creates list for that exact recipe]
```

### Multi-Step Workflows

Complex tasks in one request:

```
You: "I'm having 6 people for dinner Saturday. Budget is $40. 
     Find recipes using sale items, build shopping list, 
     and tell me cost per person."

Claude will automatically:
1. Check sales
2. Recommend recipes for 6 people
3. Find prices
4. Build shopping list
5. Calculate per-person cost
6. Suggest adjustments if over budget
```

### Intelligent Recommendations

The AI can make smart suggestions:

```
You: "Plan meals for the week"

Claude might ask:
- "What's your weekly budget?"
- "Any dietary restrictions?"
- "Prefer quick meals or okay with longer cooking?"

Then creates personalized plan.
```

### Error Handling and Alternatives

When items aren't available:

```
You: "Check if I can make beef wellington"

Claude: "Some ingredients aren't available:
- Beef tenderloin: Not found
- Puff pastry: ✓ Available
- Mushrooms: ✓ Available

Alternative suggestion: Make mushroom wellington instead?
Or try a different beef cut like ribeye?"
```

---

## Troubleshooting

### Server Won't Start

**Problem:** Error when Claude tries to use Safeway tools

**Solutions:**

1. **Check Python path**
   ```bash
   which python3
   # Use this exact path in config
   ```

2. **Test manually**
   ```bash
   export SAFEWAY_USERNAME="your-email"
   export SAFEWAY_PASSWORD="your-password"
   export SAFEWAY_STORE_ID="2948"
   python3 safeway_mcp_server.py
   ```

3. **Check logs**
   - macOS: `~/Library/Logs/Claude/`
   - Windows: `%APPDATA%\Claude\Logs\`

4. **Verify MCP SDK**
   ```bash
   pip install --upgrade mcp
   ```

### Authentication Failures

**Problem:** "Authentication failed" or "401 Unauthorized"

**Solutions:**

1. **Verify credentials**
   - Try logging into safeway.com with same credentials
   - Check for typos in config file
   
2. **Account locked?**
   - Reset password on safeway.com
   - Update config with new password
   
3. **Two-factor authentication**
   - MCP server may not support 2FA
   - Try disabling 2FA temporarily

### No Tools Available

**Problem:** Claude says it doesn't have Safeway tools

**Solutions:**

1. **Restart Claude Desktop completely**
   - Don't just close window
   - Quit application fully
   - Reopen

2. **Check config file location**
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Linux: `~/.config/claude/claude_desktop_config.json`

3. **Validate JSON syntax**
   - Use https://jsonlint.com/
   - Common errors: missing commas, wrong quotes

4. **Check file paths**
   - Must be absolute paths
   - No `~` or environment variables
   - Use forward slashes or double backslashes

### Tools Timeout

**Problem:** "Tool execution timed out"

**Solutions:**

1. **API may be slow**
   - Try again in a few minutes
   - Safeway API sometimes has delays

2. **Network issues**
   - Check internet connection
   - Try accessing safeway.com in browser

3. **Reduce scope**
   - Instead of weekly plan, try single day
   - Search fewer items at once

### Wrong Store Data

**Problem:** Getting data from wrong store

**Solutions:**

1. **Verify store ID**
   ```
   You: "What's my store ID?"
   Claude: [Will show configured store ID]
   ```

2. **Update config**
   - Find correct store ID
   - Update `claude_desktop_config.json`
   - Restart Claude

### Price Data Missing

**Problem:** No prices shown for products

**Solutions:**

1. **Not all products have prices in API**
   - This is normal
   - Try search with different terms

2. **Store-specific availability**
   - Some items only at certain stores
   - Try nearby store ID

---

## Security Considerations

### Credential Storage

**Where credentials are stored:**
- MCP config file on your computer
- Not sent to Claude's servers
- Only used by local MCP server

**Best practices:**
1. Never share your `claude_desktop_config.json`
2. Don't commit config to git repositories
3. Use strong, unique Safeway password
4. Consider using password manager

### Data Privacy

**What data is accessed:**
- Your Safeway offers and coupons
- Product prices at your store
- Your shopping list (if created)

**What data is NOT accessed:**
- Past purchase history (unless you request it)
- Payment information
- Personal details beyond what Safeway API provides

**Data transmission:**
- MCP server runs locally on your computer
- Communicates directly with Safeway API
- Claude only sees tool results, not credentials

### API Usage

**Rate limiting:**
- Be reasonable with requests
- Don't spam the API
- Safeway may throttle excessive use

**Terms of Service:**
- This uses unofficial Safeway API
- May violate Safeway's terms of service
- Use at your own risk
- Safeway could block access

---

## API Reference

### Server Architecture

```
Claude Desktop
    ↓ (stdio)
MCP Server (Python)
    ↓ (HTTPS)
Safeway API
    ↓
Your Store Data
```

### Authentication Flow

1. Server reads credentials from env vars
2. OAuth request to Okta (Safeway's auth provider)
3. Receives access token
4. Token used for all API requests
5. Token cached for session

### Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 401 | Unauthorized | Check credentials |
| 403 | Forbidden | Account may be locked |
| 404 | Not Found | Item/endpoint doesn't exist |
| 429 | Too Many Requests | Slow down, wait a minute |
| 500 | Server Error | Safeway API issue, try later |

### Tool Response Format

All tools return TextContent with JSON data:

```python
{
  "type": "text",
  "text": "{...json data...}" or "human readable text"
}
```

### Adding Custom Tools

To add your own tools to the MCP server:

1. **Define tool in `list_tools()`:**
   ```python
   Tool(
       name="safeway_my_custom_tool",
       description="What it does",
       inputSchema={...}
   )
   ```

2. **Implement in `call_tool()`:**
   ```python
   elif name == "safeway_my_custom_tool":
       # Your logic here
       return [TextContent(type="text", text=result)]
   ```

3. **Restart Claude to load new tool**

---

## Complete Example Session

Here's a real-world example of using the MCP server:

**You:** "Hey, I need help with groceries for the week."

**Claude:** "I'd be happy to help! I have access to your Safeway account. What would you like to do?"

**You:** "I have $120 for the week. Plan 7 dinners using sale items."

**Claude:** "Let me check what's on sale at your Safeway..."

[Uses `safeway_recommend_recipes`]

**Claude:** "Great! I found several items on sale. Based on current sales, here's a 7-day meal plan for $118.50:

Monday: Chicken Stir Fry ($15)
Tuesday: Spaghetti Bolognese ($14)
Wednesday: Fish Tacos ($16)
Thursday: Vegetable Curry ($13)
Friday: Pork Chops with Roasted Vegetables ($18)
Saturday: Beef Stew ($19.50)
Sunday: Baked Chicken with Rice ($23)

Total: $118.50 (under budget by $1.50!)

Would you like me to create a complete shopping list with prices?"

**You:** "Yes, and show me what's on sale."

**Claude:** [Uses `safeway_build_shopping_list` for each recipe]

**Claude:** "Here's your complete shopping list:

PROTEINS (on sale):
- Chicken thighs $2.99/lb ✓ SALE
- Ground beef $3.99/lb ✓ SALE
- Tilapia $5.99/lb
- Pork chops $4.99/lb ✓ SALE

PRODUCE (on sale):
- Bell peppers $0.99 each ✓ SALE
- Onions $1.49/lb
- Potatoes $2.99/5lb bag ✓ SALE
... (full list with 45 items)

Total: $118.50
Items on sale: 18 of 45
Estimated savings: $23.40

Would you like me to load any additional coupons to save more?"

**You:** "Yes, load all available coupons."

**Claude:** [Uses `safeway_load_offers`]

**Claude:** "Done! I've loaded 37 new offers to your account, including:
- $1 off chicken (you're buying this!)
- $0.50 off pasta (also on your list!)
- Buy 2 get 1 free on vegetables

Your new estimated total: $113.25
Total savings with coupons: $28.65!

Anything else you need help with?"

---

## Summary

The **PantryPilot is the recommended way** to interact with Safeway's API because it:

✅ Uses natural language - no commands to learn
✅ Handles complexity - AI figures out the workflow
✅ Provides intelligence - makes smart recommendations
✅ Saves time - one conversation instead of many commands
✅ Stays current - always uses latest sale data
✅ Budget aware - tracks spending automatically
✅ Recipe focused - perfect for meal planning

**Get started:**
1. Install dependencies: `pip install -r requirements.txt`
2. Configure Claude Desktop
3. Start chatting about groceries!

**Need help?**
- Check [Troubleshooting](#troubleshooting) section
- Review [Usage Examples](#usage-examples)
- See [COOKING_GUIDE.md](COOKING_GUIDE.md) for workflows

**The MCP server is the future of this tool.**
