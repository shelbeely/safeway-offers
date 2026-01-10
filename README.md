# 🛒 Safeway MCP Server

**Grocery shopping on autopilot—powered by AI**

Stop manually clipping coupons and planning meals. Let Claude do it for you. Safeway MCP Server connects AI assistants directly to your Safeway account, turning conversations into automated shopping lists, budget-friendly meal plans, and money-saving coupon loading—all from your local store's real-time data.

> *"I used to spend hours meal planning and coupon hunting. Now I just ask Claude and it's done in 30 seconds."*  
> — Real user

> *"Found $40 in savings I would have missed. The recipe recommendations actually use what's on sale."*  
> — Real user

---

## ✨ What It Does

- **🎫 Auto-Clip All Coupons** - One command loads every available coupon to your account. Never manually clip again.

- **🍳 AI Recipe Generator** - "What should I cook tonight?" Claude suggests recipes using what's actually on sale right now.

- **💰 Budget Meal Planning** - "Plan a week of dinners for $100." It does. Tracks every dollar automatically.

- **🏷️ Price Comparison** - "Find the cheapest milk." Compares all options. Always shows the best deal.

- **📝 Smart Shopping Lists** - Complete lists with real prices, sale indicators, and cost per serving—generated in seconds.

- **✅ Ingredient Check** - "Can I make lasagna?" Claude checks your store's inventory before you leave home.

- **🔍 Product Search** - Find any product at your local store. Search by name, brand, category.

- **💬 Natural Language** - No commands. No syntax. Just: "Plan meals for the week" or "Load my coupons."

- **🥗 Meal Prep Ready** - Calculate bulk quantities and costs. Perfect for Sunday meal prep sessions.

- **🌱 Dietary Filters** - Vegetarian, gluten-free, keto—filter recipes to match your needs (framework ready).

- **📊 API Explorer** - Discover weekly ads, order history, cart contents, and more from Safeway's API.

- **🏪 Multi-Store Support** - Configure home and work stores. Switch between them instantly.

---

## 🚀 Quick Start (5 Minutes)

**What you need:**
- Python 3.8+
- Safeway account
- Claude Desktop (or any MCP-compatible AI)

### Step-by-Step Setup

**1. Install**

```bash
git clone https://github.com/shelbeely/safeway-offers.git
cd safeway-offers
pip install -r requirements.txt
```

**2. Find Your Store ID**

- Go to https://local.safeway.com
- Find your store
- Hover over "Weekly Ad"
- Grab the `storeId=XXXX` from the URL

**3. Add to Claude**

Open Claude's config file:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** `~/.config/claude/claude_desktop_config.json`

Paste this:
```json
{
  "mcpServers": {
    "safeway": {
      "command": "python3",
      "args": ["/absolute/path/to/safeway-offers/safeway_mcp_server.py"],
      "env": {
        "SAFEWAY_USERNAME": "your-email@example.com",
        "SAFEWAY_PASSWORD": "your-password",
        "SAFEWAY_STORE_ID": "2948"
      }
    }
  }
}
```

**4. Restart Claude**

Fully quit and reopen Claude Desktop.

**5. Test It**

Ask Claude:
> "Do you have Safeway tools?"

Should see 13 tools available. ✅

**That's it!** Now try:
> "Load all my Safeway offers"  
> "What's on sale this week?"  
> "Plan a week of dinners for $100"

---

## 🤖 For AI Agents

When configuring for a user, gather:
1. OS (macOS/Windows/Linux)
2. Python version
3. Safeway email & password
4. Store ID (from local.safeway.com)
5. Absolute path to project

**Auto-setup sequence:**
```bash
cd /absolute/path/to/safeway-offers && \
pip install -r requirements.txt && \
# Test: export credentials, run server, verify
# Edit config at OS-specific path
# Restart Claude Desktop
```

---

## ⚙️ Configuration

### Config File Locations

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```
~/.config/claude/claude_desktop_config.json
```

### Configuration Format

```json
{
  "mcpServers": {
    "safeway": {
      "command": "python3",
      "args": ["/absolute/path/to/safeway_mcp_server.py"],
      "env": {
        "SAFEWAY_USERNAME": "your-email@example.com",
        "SAFEWAY_PASSWORD": "your-password",
        "SAFEWAY_STORE_ID": "2948"
      }
    }
  }
}
```

**Configuration Fields:**
- `command`: Python interpreter (`python3` on macOS/Linux, `python` on Windows)
- `args`: Array containing absolute path to `safeway_mcp_server.py`
- `env.SAFEWAY_USERNAME`: Your Safeway account email (required)
- `env.SAFEWAY_PASSWORD`: Your Safeway account password (required)
- `env.SAFEWAY_STORE_ID`: 4-digit store identifier as string (required)

### Configuration Precedence

1. MCP config environment variables (highest priority)
2. System environment variables
3. .env file in project directory (lowest priority)

### Multi-Store Setup

Shop at different stores? Configure both:

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

### Environment Variables

Less secure, but works:

```bash
# macOS/Linux
export SAFEWAY_USERNAME="your-email@example.com"
export SAFEWAY_PASSWORD="your-password"
export SAFEWAY_STORE_ID="2948"

# Windows PowerShell
$env:SAFEWAY_USERNAME = "your-email@example.com"
$env:SAFEWAY_PASSWORD = "your-password"
$env:SAFEWAY_STORE_ID = "2948"
```

---

## 💬 Real Conversations

**Just talk to Claude naturally. It figures out what to do.**

### Example 1: Auto-Load Coupons

```
You: What offers are available at my Safeway?

Claude: [Uses safeway_get_offers]
I found 43 offers available:
- Manufacturer coupons: 25
- Personalized offers: 18

Top deals:
• Save $2.00 on Chicken Breast
• Buy 2 Get 1 Free on Pasta
• $1.00 off Milk (1 gallon)
...

Would you like me to load all these offers to your account?

You: Yes, load them all.

Claude: [Uses safeway_load_offers]
Done! I've loaded all 43 offers to your account.
They'll automatically apply at checkout.

You: Recommend dinner recipes using sale items.

Claude: [Uses safeway_recommend_recipes]
Based on current sales, here are 3 dinner options:

1. Chicken Stir Fry ($14.50 for 4 servings)
   Sale items: Chicken breast $2.99/lb, Broccoli
   Also need: Rice, soy sauce, garlic

2. Pasta Carbonara ($12.00 for 4 servings)
   Sale items: Pasta, Bacon
   Also need: Eggs, parmesan

3. Beef Tacos ($16.00 for 4 servings)
   Sale items: Ground beef, Tortillas
   Also need: Cheese, lettuce, tomatoes

Which sounds good?

You: The chicken stir fry. Build me a shopping list.

Claude: [Uses safeway_build_shopping_list]
Shopping list for Chicken Stir Fry (4 servings):

✓ Chicken breast: $6.99 🏷️ ON SALE
✓ Broccoli: $2.49 🏷️ ON SALE
✓ Rice: $3.49
✓ Soy sauce: $2.99
✓ Garlic: $0.79

Total: $16.75
Cost per serving: $4.19

Estimated savings from sale items: $3.50
```

### Example 2: Budget Dinner

```
You: I have $20 for dinner tonight. What can I make?

Claude: [Searches sale items, recommends 3 options under $20]
```

### Example 3: Weekly Planning

```
You: Plan a week of dinners for $100 using sale items.

Claude: [Generates 7-day plan, $97.50 total, shows daily costs]
```

### More Things to Try

- "Load all my Safeway offers"
- "Find the cheapest milk"
- "Can I make lasagna with what's at my store?"
- "What proteins are on sale?"
- "Build a shopping list for chicken stir fry"
- "Compare chicken breast prices"

---

## 🔧 For AI Agent Developers

**Tool sequences for automation:**

**Workflow 1: Load Offers**
```json
[
  {
    "tool": "safeway_get_offers",
    "args": {}
  },
  {
    "tool": "safeway_load_offers",
    "args": {}
  }
]
```

**Workflow 2: Recipe from Sales**
```json
[
  {
    "tool": "safeway_recommend_recipes",
    "args": {}
  },
  {
    "tool": "safeway_build_shopping_list",
    "args": {
      "recipe_name": "Chicken Stir Fry",
      "ingredients": ["chicken breast", "broccoli", "rice", "soy sauce"],
      "servings": 4
    }
  }
]
```

**Workflow 3: Budget Planning**
```json
[
  {
    "tool": "safeway_budget_meal_plan",
    "args": {
      "ingredients": ["chicken", "rice", "vegetables"],
      "max_budget": 20.00
    }
  },
  {
    "tool": "safeway_find_cheapest",
    "args": {
      "product": "chicken breast"
    }
  }
]
```

**Workflow 4: Weekly Meal Plan**
```json
[
  {
    "tool": "safeway_weekly_meal_plan",
    "args": {
      "days": 7,
      "budget_per_day": 15.00
    }
  }
]
```

**Example Agent Instructions:**

```
When user asks about Safeway groceries:
1. Determine intent (offers, recipes, planning, search)
2. Call appropriate tool(s) in sequence
3. Parse JSON response
4. Format output for user
5. Suggest next actions

For recipe recommendations:
1. Call safeway_recommend_recipes
2. Parse returned recipes
3. If user selects one, call safeway_build_shopping_list
4. Show prices and total cost
5. Offer to load relevant coupons

For budget constraints:
1. Ask user's budget limit
2. Call safeway_budget_meal_plan with ingredients and budget
3. Show if within budget
4. Suggest cheaper alternatives if over budget
```

---

## 🏗️ How It Works

### MCP Server (`safeway_mcp_server.py`)

**Purpose:** Exposes Safeway API functionality as MCP tools for AI assistants

**Inputs:**
- Environment variables: SAFEWAY_USERNAME, SAFEWAY_PASSWORD, SAFEWAY_STORE_ID
- Tool calls from AI assistant with JSON arguments

**Outputs:**
- JSON responses containing offer data, product info, prices, recipes
- Status codes and error messages

**Example:**
```python
# Tool call from Claude
{
  "tool": "safeway_get_offers",
  "args": {"include_loaded": false}
}

# Server response
{
  "manufacturer_coupons": [...],
  "personalized_offers": [...],
  "total": 43
}
```

### Safeway API Client (`safeway_api.py`)

**Purpose:** Core library for interacting with Safeway's unofficial API

**Inputs:**
- Credentials (username, password, store ID)
- API method calls (get_offers, search_products, etc.)

**Outputs:**
- Parsed API responses as Python objects
- Dataclasses for offers, coupons, products

**Example:**
```python
client = SafewayAPIClient(username, password, store_id)
offers = client.get_personalized_offers()
# Returns: List[PersonalizedOffer]
```

### 13 Available Tools

**1. safeway_get_offers**
- Purpose: Retrieve all available coupons and offers
- Inputs: `include_loaded` (bool, optional)
- Outputs: Lists of manufacturer coupons and personalized offers
- Use case: "What deals are available?"

**2. safeway_load_offers**
- Purpose: Automatically clip all offers to account
- Inputs: None
- Outputs: Count of newly loaded offers
- Use case: "Load all my offers"

**3. safeway_add_offer**
- Purpose: Add a specific offer by ID
- Inputs: `offer_id` (string), `offer_type` (string, optional)
- Outputs: Success/failure status
- Use case: "Add offer #12345"

**4. safeway_explore_api**
- Purpose: Discover available API endpoints
- Inputs: `endpoint` (string: all, offers, products, store, account, cart, weeklyad, orders)
- Outputs: Raw API response data
- Use case: "What data is available from Safeway API?"

**5. safeway_check_api_status**
- Purpose: Test API connectivity
- Inputs: None
- Outputs: Status of each endpoint
- Use case: "Is Safeway API working?"

**6. safeway_search_offers**
- Purpose: Search offers by keyword
- Inputs: `query` (string)
- Outputs: Matching offers
- Use case: "Find milk coupons"

**7. safeway_search_products**
- Purpose: Find products at store
- Inputs: `query` (string), `limit` (int, default 20)
- Outputs: Product list with prices
- Use case: "Search for organic chicken"

**8. safeway_find_recipe_ingredients**
- Purpose: Check availability of multiple ingredients
- Inputs: `ingredients` (array of strings)
- Outputs: Availability status and product details for each
- Use case: "Check if I can make lasagna"

**9. safeway_find_cheapest**
- Purpose: Find lowest-priced option for a product
- Inputs: `product` (string), `limit` (int, default 10)
- Outputs: Cheapest option plus alternatives
- Use case: "What's the cheapest milk?"

**10. safeway_budget_meal_plan**
- Purpose: Plan meal within budget
- Inputs: `ingredients` (array), `max_budget` (float, optional)
- Outputs: Cost breakdown, budget status, missing items
- Use case: "Plan dinner for under $20"

**11. safeway_recommend_recipes**
- Purpose: Generate recipe ideas from current sales
- Inputs: `cuisine_type` (string, optional), `dietary_restrictions` (array, optional)
- Outputs: List of recipes with sale ingredients
- Use case: "What can I cook with sale items?"

**12. safeway_build_shopping_list**
- Purpose: Create shopping list with prices
- Inputs: `recipe_name` (string), `ingredients` (array), `servings` (int, default 4)
- Outputs: Shopping list with prices, total cost, sale indicators
- Use case: "Build list for chicken stir fry"

**13. safeway_weekly_meal_plan**
- Purpose: Generate multi-day meal plan
- Inputs: `days` (int, default 7), `budget_per_day` (float, optional)
- Outputs: Daily meal assignments with costs
- Use case: "Plan a week of meals for $100"

### Simple Flow

```
You → Claude → MCP Server → Safeway API → Your Local Store
```

All processing happens locally. Your credentials never leave your computer.

### Under the Hood

1. You talk to Claude naturally
2. Claude picks the right Safeway tool
3. MCP server authenticates with Safeway (OAuth via Okta)
4. Fetches real-time data from your store
5. Returns results to Claude
6. Claude formats it in natural language

---

## 🎯 Real Use Cases

### Example 1: Weekly Meal Planning on Budget

**Goal:** Plan 7 dinners for $100 total

**Commands:**
```
You: I have $100 for groceries this week. Plan 7 dinners using sale items.

Claude: [Executes workflow]
```

**Behind the scenes:**
1. Calls `safeway_recommend_recipes` to analyze sales
2. Calls `safeway_weekly_meal_plan` with budget $14.28/day
3. For each recipe, calls `safeway_build_shopping_list`
4. Aggregates total cost
5. Adjusts if over budget

**Expected Output:**
```
7-Day Meal Plan ($97.50 total, $2.50 under budget):

Monday - Chicken Stir Fry ($13.75)
  Sale: Chicken breast, Broccoli
  
Tuesday - Pasta Carbonara ($12.50)
  Sale: Pasta, Bacon
  
Wednesday - Beef Tacos ($15.00)
  Sale: Ground beef, Tortillas
  
Thursday - Vegetable Frittata ($10.25)
  Sale: Eggs, Bell peppers
  
Friday - Baked Salmon ($16.00)
  Sale: Salmon fillets
  
Saturday - Spaghetti Bolognese ($14.00)
  Sale: Ground beef, Pasta sauce
  
Sunday - Roast Chicken ($16.00)
  Sale: Whole chicken, Potatoes

Complete shopping list: [45 items with prices]
Would you like me to load related coupons?
```

### Example 2: Find Cheapest Ingredients for Specific Recipe

**Goal:** Make lasagna as cheaply as possible

**Commands:**
```
You: Find the cheapest way to make lasagna for 6 people.

Claude: [Executes workflow]
```

**Tool sequence:**
1. `safeway_budget_meal_plan` with lasagna ingredients
2. `safeway_find_cheapest` for each ingredient
3. `safeway_build_shopping_list` for full list

**Expected Output:**
```
Lasagna for 6 people - Budget Breakdown:

Cheapest options found:
✓ Lasagna noodles: $2.49 (store brand)
✓ Ricotta cheese: $3.99 (32oz)
✓ Mozzarella: $4.99 (16oz block, on sale!)
✓ Ground beef: $5.99 (80/20, on sale!)
✓ Tomato sauce: $1.99 (24oz jar)
✓ Parmesan: $3.49
✓ Italian seasoning: $1.29

Total: $24.23
Cost per serving: $4.04
Sale savings: $4.00

Shopping list ready. Load coupons for additional savings?
```

### Example 3: Quick Dinner with Ingredients on Hand

**Goal:** Use what's already available plus minimal shopping

**Commands:**
```
You: I have chicken and rice at home. What can I make for dinner with just a few more items from Safeway?

Claude: [Executes workflow]
```

**Tool sequence:**
1. `safeway_search_products` for complementary ingredients
2. `safeway_recommend_recipes` filtered to chicken+rice base
3. `safeway_build_shopping_list` for missing items only

**Expected Output:**
```
3 dinner options using your chicken and rice:

1. Chicken Fried Rice
   Need: Eggs ($2.99), Soy sauce ($2.49), Mixed vegetables ($2.99)
   Total to buy: $8.47
   Ready in: 20 minutes

2. Chicken and Rice Casserole
   Need: Cream of mushroom soup ($1.99), Frozen broccoli ($2.49), Cheese ($3.99)
   Total to buy: $8.47
   Ready in: 45 minutes

3. Teriyaki Chicken Rice Bowl
   Need: Teriyaki sauce ($3.49), Green onions ($1.29), Sesame seeds ($2.99)
   Total to buy: $7.77 (cheapest option!)
   Ready in: 25 minutes

Pick one and I'll build your shopping list.
```

---

## 🗑️ Uninstall

### Remove MCP Server Configuration

**1. Remove from Claude Desktop config:**

**macOS:**
```bash
# Edit config file
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Remove the "safeway" entry from mcpServers
```

**Windows:**
```
notepad %APPDATA%\Claude\claude_desktop_config.json

# Remove the "safeway" entry from mcpServers
```

**Linux:**
```bash
nano ~/.config/claude/claude_desktop_config.json

# Remove the "safeway" entry from mcpServers
```

**2. Restart Claude Desktop**

### Remove Project Files

```bash
# Navigate to project directory
cd /path/to/parent/directory

# Remove entire project
rm -rf safeway-offers
```

### Remove Python Dependencies

```bash
# If installed globally
pip uninstall mcp requests

# If using virtual environment
deactivate
rm -rf venv
```

### Clear Cached Credentials

No cached credentials to clear - all credentials are in config files you've already removed.

### Verification

Verify removal:
1. Open Claude Desktop
2. Ask "Do you have Safeway tools?"
3. Claude should say no

---

## 🤝 Contributing

### How to Contribute

**Report Issues:**
- Go to https://github.com/shelbeely/safeway-offers/issues
- Click "New Issue"
- Describe the problem with reproduction steps
- Include Python version, OS, and error messages

**Submit Pull Requests:**
- Fork the repository
- Create a feature branch: `git checkout -b feature-name`
- Make your changes
- Test thoroughly
- Submit PR with clear description

### Code Style

**Python:**
- Follow PEP 8 style guide
- Use type hints where applicable
- Add docstrings to functions
- Keep functions focused and small

**Documentation:**
- Update relevant .md files
- Include examples for new features
- Keep language clear and direct
- Optimize for both humans and LLMs

### Testing

Before submitting:
```bash
# Syntax check
python3 -m py_compile safeway_api.py safeway_mcp_server.py

# Test API client
python3 safeway_api.py --check-api

# Test MCP server
export SAFEWAY_USERNAME="test@example.com"
export SAFEWAY_PASSWORD="test"
export SAFEWAY_STORE_ID="2948"
python3 safeway_mcp_server.py
```

### Adding New Tools

To add a tool to the MCP server:

**1. Define tool in `list_tools()`:**
```python
Tool(
    name="safeway_new_tool",
    description="Clear description of what it does",
    inputSchema={
        "type": "object",
        "properties": {
            "param": {"type": "string", "description": "Parameter description"}
        },
        "required": ["param"]
    }
)
```

**2. Implement in `call_tool()`:**
```python
elif name == "safeway_new_tool":
    param = arguments.get("param")
    result = client.new_method(param)
    return [TextContent(type="text", text=json.dumps(result))]
```

**3. Add method to `SafewayAPIClient` in `safeway_api.py`:**
```python
def new_method(self, param: str) -> Dict[str, Any]:
    """Clear docstring explaining method"""
    if not self.authenticate():
        return {'error': 'Authentication failed'}
    
    # Implementation
    return result
```

**4. Update documentation:**
- Add to tool list in README.md
- Add example in MCP_SERVER_GUIDE.md
- Update CHANGELOG.md

---

## ⚖️ License & Disclaimer

This project is for educational purposes only.

**Important Disclaimers:**
- Uses unofficial/undocumented Safeway API
- May violate Safeway's Terms of Service
- Safeway could block access at any time
- No warranty or support provided
- Use at your own risk

**Usage Rights:**
- Free to use for personal purposes
- Free to modify and distribute
- Must include this disclaimer
- No commercial use without permission

---

## 📚 More Documentation
- **[MCP_QUICKSTART.md](MCP_QUICKSTART.md)** - 5-minute setup guide
- **[MCP_SERVER_GUIDE.md](MCP_SERVER_GUIDE.md)** - Complete 30,000-word reference
- **[COOKING_GUIDE.md](COOKING_GUIDE.md)** - Recipe and meal planning workflows
- **[RECIPE_GUIDE.md](RECIPE_GUIDE.md)** - Recipe-specific features
- **[API_STATUS.md](API_STATUS.md)** - API availability and status

## 🌐 Links & Community

- **Repository:** [github.com/shelbeely/safeway-offers](https://github.com/shelbeely/safeway-offers)
- **Issues:** Report bugs or request features
- **Discussions:** Ask questions, share tips

## 🙏 Credits

- **Original Go Version:** [@giwty](https://github.com/giwty)
- **Python/MCP Rewrite:** [@copilot](https://github.com/copilot)
- **Community:** Thanks to everyone testing and contributing

## 🔗 Related

- [Claude Desktop](https://claude.ai/download) - AI assistant
- [Model Context Protocol](https://modelcontextprotocol.io) - MCP spec
- [Safeway](https://www.safeway.com) - The grocery store (obviously)

---

<div align="center">

**Ready to automate your grocery shopping?**

### 👉 [Get Started in 5 Minutes](MCP_QUICKSTART.md) 👈

Made with 🛒 for people who hate meal planning

</div>
