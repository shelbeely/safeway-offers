# Complete Cooking & Recipe Features Guide

## Overview

The Safeway API tool now includes a **comprehensive cooking assistant** with everything you need for meal planning, budgeting, and recipe creation based on what's available and on sale at your local store.

## 🎯 Complete Feature List

### 1. Product Search & Availability
- Search for individual products
- Check ingredient availability
- Find product alternatives

### 2. Price Comparison & Budget Tools
- Find cheapest options for products
- Compare prices across alternatives
- Budget meal planning with cost estimates
- Track spending against daily/weekly budgets

### 3. Recipe Recommendations
- **NEW!** Get recipes based on current sales
- Recipes categorized by available ingredients
- Automatic recipe generation from sale items
- Dietary restriction support (coming soon)

### 4. Shopping List Builder
- Build complete shopping lists for recipes
- Get price estimates for all ingredients
- Identify which items are on sale
- Calculate cost per serving

### 5. Weekly Meal Planning
- **NEW!** Generate full week meal plans
- Based on current sales and specials
- Budget-conscious planning
- Automatic variety in meals

## 🚀 Quick Start Examples

### CLI Examples

```bash
# Set credentials
export SAFEWAY_USERNAME="your-email@example.com"
export SAFEWAY_PASSWORD="your-password"
export SAFEWAY_STORE_ID="2948"

# Get recipe recommendations from current sales
python safeway_api.py --recommend-recipes

# Find cheapest milk option
python safeway_api.py --find-cheapest "milk"

# Plan a budget meal
python safeway_api.py --budget-plan chicken rice vegetables --max-budget 20.00

# Build shopping list for a recipe
python safeway_api.py --build-shopping-list milk eggs flour butter sugar \
    --recipe-name "Pancakes" --servings 4

# Generate weekly meal plan
python safeway_api.py --weekly-meal-plan --days 7 --budget-per-day 15.00
```

### MCP Tools (for Claude/AI Assistants)

**Complete list of 12 cooking tools:**

1. `safeway_get_offers` - View current offers/coupons
2. `safeway_load_offers` - Load all offers to account
3. `safeway_add_offer` - Add specific offer
4. `safeway_explore_api` - Explore API capabilities
5. `safeway_check_api_status` - Check API health
6. `safeway_search_offers` - Search offers by keyword
7. `safeway_search_products` - Find products at store
8. `safeway_find_recipe_ingredients` - Check ingredient availability
9. `safeway_find_cheapest` - Find best price for item
10. `safeway_budget_meal_plan` - Budget-friendly ingredient planning
11. **`safeway_recommend_recipes`** - Get recipe ideas from sales ⭐ NEW
12. **`safeway_build_shopping_list`** - Complete shopping list with prices ⭐ NEW
13. **`safeway_weekly_meal_plan`** - Full week meal plan ⭐ NEW

## 💡 Complete Workflow Examples

### Workflow 1: Smart Weekly Meal Planning

**Goal:** Plan a week of meals using sale items, stay within budget

```
With Claude:
"I have $100 for groceries this week. Create a 7-day meal plan using 
items on sale at my Safeway, and build shopping lists for each recipe."

Claude will:
1. Use safeway_recommend_recipes to get ideas from sales
2. Use safeway_weekly_meal_plan for $14/day budget
3. Use safeway_build_shopping_list for each recipe
4. Calculate total costs and savings
```

**CLI:**
```bash
# Get recipe recommendations
python safeway_api.py --recommend-recipes

# Generate full week plan
python safeway_api.py --weekly-meal-plan --days 7 --budget-per-day 14.28
```

### Workflow 2: Budget-Conscious Recipe Selection

**Goal:** Make a specific dish as cheaply as possible

```
With Claude:
"I want to make chicken stir fry. Find the cheapest ingredients at Safeway 
and tell me the total cost."

Claude will:
1. Use safeway_find_cheapest for each ingredient
2. Use safeway_budget_meal_plan to calculate total
3. Use safeway_build_shopping_list for final list with prices
```

**CLI:**
```bash
# Find cheapest options
python safeway_api.py --find-cheapest "chicken breast"
python safeway_api.py --find-cheapest "broccoli"

# Build budget plan
python safeway_api.py --budget-plan "chicken breast" broccoli rice "soy sauce" --max-budget 15.00
```

### Workflow 3: Discover New Recipes from Sales

**Goal:** Get inspired by what's on sale

```
With Claude:
"What's on sale at Safeway this week? Suggest 3 dinner recipes I can make."

Claude will:
1. Use safeway_get_offers to see sales
2. Use safeway_recommend_recipes to generate ideas
3. Use safeway_search_products to verify availability
4. Use safeway_build_shopping_list for each recipe
```

**CLI:**
```bash
# See what recipes are recommended
python safeway_api.py --recommend-recipes

# Pick a recipe and build shopping list
python safeway_api.py --build-shopping-list chicken pasta "tomato sauce" cheese \
    --recipe-name "Chicken Pasta Bake" --servings 4
```

### Workflow 4: Price Comparison Shopping

**Goal:** Find best deals for pantry staples

```
With Claude:
"Compare prices for milk, eggs, and bread at my Safeway. 
Show me the cheapest options and total cost."

Claude will:
1. Use safeway_find_cheapest for each item
2. Compare alternatives
3. Calculate savings
```

**CLI:**
```bash
python safeway_api.py --find-cheapest "milk"
python safeway_api.py --find-cheapest "eggs"
python safeway_api.py --find-cheapest "bread"
```

## 🎨 Advanced Use Cases

### Dietary Restrictions

```
"Generate vegetarian recipes using sale items at Safeway"
"Find gluten-free ingredients on sale and suggest recipes"
"Create a keto meal plan with my $100 budget"
```

### Meal Prep

```
"Plan 5 meal prep recipes that use similar ingredients to minimize cost"
"What proteins are on sale? Create meal prep recipes for the week"
```

### Special Occasions

```
"Plan a dinner party for 8 people with a $75 budget using Safeway sales"
"Create a holiday meal shopping list with price estimates"
```

### Learning to Cook

```
"Suggest 3 easy recipes for beginners using 5 ingredients or less"
"What's the cheapest complete meal I can make at Safeway?"
```

## 📊 Understanding the Output

### Recipe Recommendations Output

```json
{
  "total_sale_items": 45,
  "categories_on_sale": ["protein", "produce", "dairy"],
  "recommended_recipes": [
    {
      "recipe_name": "Stir Fry",
      "sale_ingredients_available": ["Chicken Breast $2.99/lb", "Broccoli $1.99"],
      "additional_ingredients_needed": ["rice", "soy sauce", "garlic"],
      "estimated_savings": "Using sale items"
    }
  ]
}
```

### Shopping List Output

```json
{
  "recipe_name": "Pancakes",
  "servings": 4,
  "total_cost": 8.47,
  "cost_per_serving": 2.12,
  "items_on_sale": ["milk", "eggs"],
  "shopping_list": [
    {"ingredient": "milk", "found": true, "price": 2.99},
    {"ingredient": "eggs", "found": true, "price": 3.49},
    {"ingredient": "flour", "found": true, "price": 1.99}
  ]
}
```

### Weekly Meal Plan Output

```json
{
  "days_planned": 7,
  "estimated_total_cost": 98.50,
  "budget_remaining": 1.50,
  "meal_plan": [
    {
      "day": 1,
      "recipe": "Chicken Stir Fry",
      "sale_ingredients": ["Chicken Breast", "Broccoli"],
      "estimated_cost": 14.00
    }
  ]
}
```

## 🔧 Pro Tips

### 1. Maximize Savings
- Always run `--recommend-recipes` first to see what's on sale
- Use `--find-cheapest` to compare before buying
- Check if ingredients are on sale with `--build-shopping-list`

### 2. Efficient Meal Planning
- Plan multiple meals using overlapping ingredients
- Use `--weekly-meal-plan` to get variety
- Set realistic `--budget-per-day` limits

### 3. Recipe Success
- Verify all ingredients available before starting
- Use `--find-ingredients` to check everything
- Build shopping list to avoid missing items

### 4. Budget Management
- Use `--max-budget` to stay on track
- Compare `--find-cheapest` options
- Track savings from sale items

## 🚨 Common Issues

### "No recipe recommendations available"
- Check if you have offers loaded
- Try running without dietary restrictions first
- Verify your store has sale items

### Prices seem high/low
- Prices are estimates from API
- May not include sales tax
- Some prices may be per pound/unit

### Missing ingredients
- Not all products available via API
- Try simpler/more common ingredient names
- Check alternative brands

## 📱 Mobile App Comparison

**What the Safeway app does:**
- Browse products
- View offers manually
- Clip coupons one by one

**What this tool does:**
- Automatic recipe recommendations from sales ✨
- Budget planning and cost estimates ✨
- Complete shopping lists with prices ✨
- Weekly meal plans ✨
- Price comparisons ✨
- Bulk offer loading ✨

## 🎯 Next Steps

1. **Try basic features first:**
   ```bash
   python safeway_api.py --recommend-recipes
   ```

2. **Experiment with budget planning:**
   ```bash
   python safeway_api.py --weekly-meal-plan --budget-per-day 15.00
   ```

3. **Use with AI assistants:**
   - Configure MCP server in Claude
   - Ask for recipe recommendations
   - Let AI plan your week

4. **Automate your workflow:**
   - Set up weekly GitHub Action
   - Get recipe emails
   - Track spending over time

## 📚 Additional Resources

- [Main Python Documentation](README_PYTHON.md)
- [Recipe-Specific Guide](RECIPE_GUIDE.md)
- [API Status Information](API_STATUS.md)
- [MCP Configuration Example](mcp_config_example.json)

---

**Ready to start cooking smarter? Try your first command:**

```bash
python safeway_api.py --recommend-recipes
```

**Or ask Claude:**

```
"What recipes can I make with items on sale at my Safeway this week?"
```

🍳 Happy cooking!
