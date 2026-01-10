# Safeway MCP Server

**AI-powered grocery assistant for meal planning, budgeting, and automated offer management**

Safeway MCP Server connects Claude and other AI assistants directly to your Safeway account through the Model Context Protocol. Ask questions in natural language to manage offers, plan meals, compare prices, and generate shopping lists—all based on real-time data from your local store.

---

## Features

- **Automated Offer Management** - Load all manufacturer coupons and personalized deals to your account with one command. Never miss a money-saving offer.

- **Recipe Recommendations from Sales** - Get meal ideas based on what's currently on sale at your store. Saves money by building recipes around discounted items.

- **Budget-Aware Meal Planning** - Generate weekly meal plans that stay within your budget. Tracks spending per meal and per day.

- **Price Comparison** - Find the cheapest option for any product. Compare alternatives across brands and sizes.

- **Smart Shopping Lists** - Build shopping lists with real price estimates. Shows which items are on sale and calculates cost per serving.

- **Ingredient Availability Checking** - Verify all recipe ingredients are in stock before you shop. Avoids wasted trips.

- **Product Search** - Find specific products at your local store. Search by name, brand, or category.

- **Natural Language Interface** - No commands to memorize. Just talk to Claude: "Plan a week of dinners for $100 using sale items."

- **Meal Prep Planning** - Calculate ingredient quantities and costs for bulk cooking. Perfect for weekly meal prep.

- **Dietary Support** - Filter recipes and recommendations by dietary needs (framework ready for vegetarian, gluten-free, etc.).

- **API Exploration** - Discover additional data available from Safeway's API including weekly ads, order history, and cart contents.

- **Status Monitoring** - Check if Safeway API endpoints are operational before attempting authentication.

- **Multi-Store Support** - Configure multiple store locations for home and work shopping.

---

## Installation

### For Humans

**Prerequisites:**
- Python 3.8 or higher
- Safeway account (email and password)
- Your local Safeway store ID (4-digit number)
- Claude Desktop or another MCP-compatible AI assistant

**Step 1: Install Python dependencies**

```bash
cd /path/to/safeway-offers
pip install -r requirements.txt
```

**Step 2: Find your Safeway store ID**

1. Visit https://local.safeway.com/safeway.html
2. Search for your local store
3. Hover over "Weekly Ad" link
4. Note the store ID in the URL: `storeId=2948`

**Step 3: Configure Claude Desktop**

**macOS:**
```bash
open ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```
notepad %APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```bash
nano ~/.config/claude/claude_desktop_config.json
```

**Add this configuration:**
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

**Important:**
- Use absolute paths (no `~` or relative paths)
- Replace placeholder values with your actual credentials
- Store ID must be a string in quotes
- On Windows, use `python` instead of `python3`

**Step 4: Restart Claude Desktop**

Completely quit and reopen Claude Desktop (not just close the window).

**Step 5: Verify installation**

In Claude, ask:
```
Do you have access to Safeway tools?
```

Claude should confirm it has 13 Safeway tools available.

### For LLMs / Agents

When setting up this tool for a user, collect the following information:

**Required Information:**
1. Operating system (macOS, Windows, or Linux)
2. Python version (`python3 --version`)
3. Safeway account email
4. Safeway account password
5. Local Safeway store ID (4-digit number)
6. Absolute path to project directory
7. AI assistant being used (Claude Desktop, etc.)

**Setup Questions:**
```
What is your operating system? (macOS/Windows/Linux)
What is your Safeway account email?
What is your Safeway account password?
What is your local Safeway store ID? (Find at local.safeway.com)
Where is the safeway-offers directory located? (absolute path)
```

**Setup Commands:**

```bash
# Install dependencies
cd /absolute/path/to/safeway-offers
pip install -r requirements.txt

# Test server
export SAFEWAY_USERNAME="email@example.com"
export SAFEWAY_PASSWORD="password"
export SAFEWAY_STORE_ID="2948"
python3 safeway_mcp_server.py
# Press Ctrl+C if no errors appear

# Configure Claude Desktop
# macOS:
echo '{
  "mcpServers": {
    "safeway": {
      "command": "python3",
      "args": ["/absolute/path/to/safeway-offers/safeway_mcp_server.py"],
      "env": {
        "SAFEWAY_USERNAME": "email@example.com",
        "SAFEWAY_PASSWORD": "password",
        "SAFEWAY_STORE_ID": "2948"
      }
    }
  }
}' > ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Restart Claude Desktop completely
```

---

## Configuration

### Configuration File Location

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

### Multiple Store Configuration

Configure different stores for different locations:

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

Alternative to MCP config (less secure):

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

## Usage

### For Humans

**Basic Workflow:**

1. Open Claude Desktop
2. Start a conversation about groceries
3. Claude automatically uses Safeway tools when relevant

**Example Conversation:**

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

**Common Tasks:**

**Load all offers:**
```
Load all my Safeway offers
```

**Find cheapest item:**
```
Find the cheapest milk at my store
```

**Weekly meal plan:**
```
Plan a week of dinners for $100 using sale items
```

**Check ingredient availability:**
```
Can I make lasagna with what's at my Safeway?
Check for: lasagna noodles, ricotta, mozzarella, ground beef, tomato sauce
```

**Price comparison:**
```
Compare chicken breast prices and show me the cheapest option
```

**Budget meal planning:**
```
I have $20 for dinner tonight. What can I make?
```

### For Agents

**Tool Call Sequence for Common Workflows:**

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

## Architecture / Components

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

### Authentication Flow

```
1. User provides credentials via MCP config
2. Server creates SafewayAPIClient instance
3. Client sends OAuth request to albertsons.okta.com
4. Okta returns access token
5. Token cached for session
6. All API requests use Bearer token authentication
7. Token refreshed automatically if expired
```

### Data Flow

```
User → Claude Desktop → MCP Protocol → safeway_mcp_server.py
    → safeway_api.py → Safeway API → Store Database
    → Response ← Response ← Response ← Response
```

---

## Examples

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

## Uninstallation

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

## Contributing

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

## License

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

## Footer

### Documentation
- **[MCP_QUICKSTART.md](MCP_QUICKSTART.md)** - 5-minute setup guide
- **[MCP_SERVER_GUIDE.md](MCP_SERVER_GUIDE.md)** - Complete 30,000-word reference
- **[COOKING_GUIDE.md](COOKING_GUIDE.md)** - Recipe and meal planning workflows
- **[RECIPE_GUIDE.md](RECIPE_GUIDE.md)** - Recipe-specific features
- **[API_STATUS.md](API_STATUS.md)** - API availability and status

### Project Links
- **Repository:** https://github.com/shelbeely/safeway-offers
- **Issues:** https://github.com/shelbeely/safeway-offers/issues
- **Discussions:** https://github.com/shelbeely/safeway-offers/discussions

### Contact & Community
- **Original Author:** @giwty (Go version)
- **Python/MCP Rewrite:** @copilot
- **Community:** GitHub Discussions for questions and ideas

### Related Projects
- **Claude Desktop:** https://claude.ai/download
- **MCP Protocol:** https://modelcontextprotocol.io
- **Safeway:** https://www.safeway.com

### Acknowledgments
- Safeway/Albertsons for (unintentionally) providing API access
- Anthropic for Model Context Protocol
- Open source community for contributions and testing

---

**Ready to automate your grocery shopping?**

👉 **[Start with 5-Minute Setup](MCP_QUICKSTART.md)**
