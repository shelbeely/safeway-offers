# Using Safeway API for AI-Generated Recipes

This guide shows how to use the Safeway API tools to find ingredients for your AI-generated recipes at your local store.

## Quick Start for Recipe Ingredients

### CLI Usage

**Find multiple recipe ingredients:**
```bash
# Set your credentials
export SAFEWAY_USERNAME="your-email@example.com"
export SAFEWAY_PASSWORD="your-password"
export SAFEWAY_STORE_ID="2948"

# Check if recipe ingredients are available
python safeway_api.py --find-ingredients milk eggs flour butter sugar

# Search for a specific product
python safeway_api.py --search-product "chicken breast"
```

### MCP Server for AI Assistants

The MCP server now includes **3 new tools** specifically for recipe planning:

#### 1. `safeway_search_products`
Search for individual products at your local store.

**Example prompts for Claude:**
- "Search for chicken breast at Safeway"
- "Find organic tomatoes at my local Safeway"
- "What milk options are available?"

#### 2. `safeway_find_recipe_ingredients`
Check availability of ALL ingredients in a recipe at once.

**Example prompts for Claude:**
- "Check if these ingredients are available at Safeway: milk, eggs, flour, butter, sugar"
- "Can I find all ingredients for chocolate chip cookies at my local store?"
- "Verify ingredient availability for a pasta carbonara recipe"

#### 3. Integration with Recipe Generation
Perfect workflow with AI assistants:

**Prompt Example:**
```
"Generate a dinner recipe using ingredients available at my local Safeway. 
First check what proteins are on sale, then create a recipe using those ingredients."
```

Claude will:
1. Use `safeway_get_offers` to see what's on sale
2. Use `safeway_search_products` to verify availability
3. Generate a recipe using available ingredients
4. Use `safeway_find_recipe_ingredients` to confirm all items are in stock

## Setup for Recipe Use Case

### 1. Configure MCP Server

Add to your Claude Desktop config:

**MacOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "safeway": {
      "command": "python",
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

### 2. Example Workflows

#### Workflow 1: Recipe from Available Ingredients
```
User: "What ingredients are on sale this week at Safeway?"
Claude: [uses safeway_get_offers]

User: "Create a recipe using those ingredients"
Claude: [generates recipe using sale items]

User: "Are all those ingredients available at my store?"
Claude: [uses safeway_find_recipe_ingredients to verify]
```

#### Workflow 2: Specific Recipe Validation
```
User: "I want to make lasagna. Check if I can get everything at Safeway"
Claude: [uses safeway_find_recipe_ingredients with: ground beef, 
         lasagna noodles, ricotta cheese, mozzarella, tomato sauce, etc.]

User: "What's missing?"
Claude: "All ingredients available! Here are the details..."
```

#### Workflow 3: Dietary Restrictions + Availability
```
User: "Generate a gluten-free dinner recipe using ingredients at my local Safeway"
Claude: [searches for gluten-free products, generates recipe, verifies availability]
```

## CLI Examples

### Search for Products
```bash
# Search for specific items
python safeway_api.py --search-product "almond milk"
python safeway_api.py --search-product "grass fed beef"
python safeway_api.py --search-product "organic spinach"
```

### Check Recipe Ingredients
```bash
# Ingredients for Pancakes
python safeway_api.py --find-ingredients flour eggs milk butter "maple syrup"

# Ingredients for Stir Fry
python safeway_api.py --find-ingredients "chicken breast" broccoli "soy sauce" rice garlic ginger

# Ingredients for Pasta Carbonara
python safeway_api.py --find-ingredients pasta eggs "parmesan cheese" bacon "black pepper"
```

## Output Format

### Product Search Output
```json
{
  "query": "chicken breast",
  "found": 5,
  "products": [
    {
      "name": "Organic Chicken Breast",
      "price": 8.99,
      "available": true,
      "size": "1 lb"
    }
  ]
}
```

### Recipe Ingredients Output
```json
{
  "milk": {
    "found": true,
    "count": 8,
    "products": [...]
  },
  "eggs": {
    "found": true,
    "count": 4,
    "products": [...]
  }
}
```

## Tips for Best Results

1. **Be Specific:** "boneless chicken breast" vs "chicken"
2. **Check Variations:** If "whole wheat flour" isn't found, try "flour"
3. **Use Quotes:** For multi-word items in CLI: `--find-ingredients "almond milk" "greek yogurt"`
4. **Combine with Offers:** Check what's on sale first, then plan recipes
5. **Store ID Matters:** Make sure you're using the correct store ID for your location

## Advanced: Meal Planning with AI

### Full Week Meal Plan
```
Prompt: "Create a weekly meal plan using ingredients available at my Safeway. 
Check current sales and make sure everything is in stock."
```

Claude will:
1. Check current offers (`safeway_get_offers`)
2. Search for featured products (`safeway_search_products`)
3. Generate 7 dinner recipes
4. Verify all ingredients (`safeway_find_recipe_ingredients`)
5. Provide shopping list with what's on sale

### Budget-Friendly Recipes
```
Prompt: "Find the best sale items at Safeway and create recipes using them"
```

### Seasonal Cooking
```
Prompt: "What produce is available at Safeway? Suggest seasonal recipes."
```

## Troubleshooting

**No products found?**
- Check your store ID is correct
- Try simpler search terms
- Some stores may have limited online inventory data

**Authentication errors?**
- Verify credentials in environment variables
- Try logging into Safeway.com directly first
- Check if your account is locked

**Slow searches?**
- API may be rate-limited
- Try smaller ingredient lists
- Use specific product names

## API Limitations

⚠️ **Important Notes:**
- This uses unofficial Safeway APIs
- Product availability is approximate
- Prices may vary from in-store
- Not all products may appear in search
- API may change without notice

For detailed API documentation, see [API_STATUS.md](API_STATUS.md)

## Get Help

- CLI Help: `python safeway_api.py --help`
- MCP Tools: Ask Claude "What Safeway tools are available?"
- Full Documentation: [README_PYTHON.md](README_PYTHON.md)
