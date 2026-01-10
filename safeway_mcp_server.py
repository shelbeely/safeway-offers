#!/usr/bin/env python3
"""
Safeway API MCP Server

A Model Context Protocol server that exposes the Safeway API to AI assistants.
This allows Claude and other MCP-compatible AI systems to interact with Safeway's
unofficial mobile API for offers, products, and more.

Usage:
    python safeway_mcp_server.py

Configuration via environment variables:
    SAFEWAY_USERNAME - Your Safeway account email
    SAFEWAY_PASSWORD - Your Safeway account password
    SAFEWAY_STORE_ID - Your preferred store ID
"""

import os
import sys
import json
import asyncio
from typing import Any, Optional
import logging

# MCP SDK imports
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
except ImportError:
    print("Error: MCP SDK not installed. Install with: pip install mcp", file=sys.stderr)
    sys.exit(1)

from safeway_api import SafewayAPIClient, SafewayEndpoints

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("safeway-mcp-server")

# Initialize MCP server
app = Server("safeway-api")

# Global client (will be initialized with credentials)
_client: Optional[SafewayAPIClient] = None


def get_client() -> SafewayAPIClient:
    """Get or create Safeway API client"""
    global _client
    
    if _client is None:
        username = os.environ.get('SAFEWAY_USERNAME')
        password = os.environ.get('SAFEWAY_PASSWORD')
        store_id = os.environ.get('SAFEWAY_STORE_ID')
        
        if not all([username, password, store_id]):
            raise ValueError(
                "Missing credentials. Set SAFEWAY_USERNAME, SAFEWAY_PASSWORD, "
                "and SAFEWAY_STORE_ID environment variables"
            )
        
        _client = SafewayAPIClient(username, password, store_id)
        
        if not _client.authenticate():
            raise RuntimeError("Failed to authenticate with Safeway API")
    
    return _client


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available Safeway API tools"""
    return [
        Tool(
            name="safeway_get_offers",
            description=(
                "Get available Safeway offers and coupons. Returns manufacturer coupons "
                "and personalized offers for the authenticated user."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "include_loaded": {
                        "type": "boolean",
                        "description": "Include already loaded offers in results",
                        "default": False
                    }
                }
            }
        ),
        Tool(
            name="safeway_load_offers",
            description=(
                "Load all available offers into the Safeway account. This clips all "
                "manufacturer coupons and personalized deals to the user's account."
            ),
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="safeway_add_offer",
            description=(
                "Add a specific offer to the Safeway account by ID. "
                "Use this to clip individual coupons or deals."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "offer_id": {
                        "type": "string",
                        "description": "The offer or coupon ID to add"
                    },
                    "offer_type": {
                        "type": "string",
                        "description": "The offer type (e.g., 'PD', 'MF')",
                        "default": "PD"
                    }
                },
                "required": ["offer_id"]
            }
        ),
        Tool(
            name="safeway_explore_api",
            description=(
                "Explore Safeway API endpoints to discover what data is available. "
                "Can query offers, products, store info, account details, cart, weekly ads, and order history."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "endpoint": {
                        "type": "string",
                        "description": "Endpoint to explore",
                        "enum": ["all", "offers", "products", "store", "account", "cart", "weeklyad", "orders"],
                        "default": "all"
                    }
                }
            }
        ),
        Tool(
            name="safeway_check_api_status",
            description=(
                "Check if Safeway API endpoints are accessible. "
                "Tests connectivity to key API endpoints without requiring authentication."
            ),
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="safeway_search_offers",
            description=(
                "Search through available offers by keyword. "
                "Searches in offer names and descriptions."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (e.g., 'milk', 'save $5', 'bread')"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="safeway_search_products",
            description=(
                "Search for products available at your local Safeway store. "
                "Perfect for finding recipe ingredients or checking product availability."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Product name or keyword (e.g., 'milk', 'chicken breast', 'tomatoes')"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 20)",
                        "default": 20
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="safeway_find_recipe_ingredients",
            description=(
                "Check availability of multiple recipe ingredients at once. "
                "Ideal for AI-generated recipes - provide a list of ingredients and get availability status."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "ingredients": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of ingredient names (e.g., ['milk', 'eggs', 'flour', 'butter'])"
                    }
                },
                "required": ["ingredients"]
            }
        ),
        Tool(
            name="safeway_find_cheapest",
            description=(
                "Find the cheapest option for a specific product. "
                "Perfect for budget meal planning - compares prices and shows alternatives."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "product": {
                        "type": "string",
                        "description": "Product to find cheapest option for (e.g., 'milk', 'chicken breast')"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of alternatives to compare (default: 10)",
                        "default": 10
                    }
                },
                "required": ["product"]
            }
        ),
        Tool(
            name="safeway_budget_meal_plan",
            description=(
                "Create a budget-friendly meal plan by finding cheapest options for all ingredients. "
                "Calculates total cost and checks against budget. Perfect for cost-conscious cooking."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "ingredients": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of meal ingredients"
                    },
                    "max_budget": {
                        "type": "number",
                        "description": "Optional maximum budget in dollars (e.g., 25.00)"
                    }
                },
                "required": ["ingredients"]
            }
        ),
        Tool(
            name="safeway_recommend_recipes",
            description=(
                "Get recipe recommendations based on what's currently on sale at Safeway. "
                "Perfect for budget-conscious meal planning - uses sale items to suggest recipes."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "cuisine_type": {
                        "type": "string",
                        "description": "Optional cuisine preference (e.g., 'Italian', 'Mexican', 'Asian')"
                    },
                    "dietary_restrictions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional dietary restrictions (e.g., ['vegetarian', 'gluten-free'])"
                    }
                }
            }
        ),
        Tool(
            name="safeway_build_shopping_list",
            description=(
                "Build a complete shopping list for a recipe with price estimates. "
                "Checks availability, finds best prices, and calculates total cost."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "recipe_name": {
                        "type": "string",
                        "description": "Name of the recipe"
                    },
                    "ingredients": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of ingredients needed"
                    },
                    "servings": {
                        "type": "integer",
                        "description": "Number of servings (default: 4)",
                        "default": 4
                    }
                },
                "required": ["recipe_name", "ingredients"]
            }
        ),
        Tool(
            name="safeway_weekly_meal_plan",
            description=(
                "Generate a complete weekly meal plan based on current sales and budget. "
                "Creates a full week of meals using items on sale."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "days": {
                        "type": "integer",
                        "description": "Number of days to plan for (default: 7)",
                        "default": 7
                    },
                    "budget_per_day": {
                        "type": "number",
                        "description": "Optional daily budget in dollars (e.g., 15.00)"
                    }
                },
                "required": []
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""
    
    try:
        if name == "safeway_get_offers":
            client = get_client()
            
            manufacturer_coupons = client.get_manufacturer_coupons()
            personalized_offers = client.get_personalized_offers()
            
            result = {
                "manufacturer_coupons": [
                    {
                        "id": c.coupon_id,
                        "description": c.description,
                        "type": c.offer_type
                    }
                    for c in manufacturer_coupons
                ],
                "personalized_offers": [
                    {
                        "id": o.offer_id,
                        "name": o.name,
                        "description": o.description,
                        "type": o.offer_type
                    }
                    for o in personalized_offers
                ],
                "total_manufacturer": len(manufacturer_coupons),
                "total_personalized": len(personalized_offers)
            }
            
            if arguments.get("include_loaded", False):
                shopping_list = client.get_shopping_list()
                result["loaded_offers"] = shopping_list
                result["total_loaded"] = len(shopping_list)
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "safeway_load_offers":
            client = get_client()
            new_offers = client.load_all_offers()
            
            return [TextContent(
                type="text",
                text=f"Successfully loaded {new_offers} new offers to your Safeway account."
            )]
        
        elif name == "safeway_add_offer":
            client = get_client()
            offer_id = arguments.get("offer_id")
            offer_type = arguments.get("offer_type", "PD")
            
            if not offer_id:
                return [TextContent(
                    type="text",
                    text="Error: offer_id is required"
                )]
            
            success = client.add_offer(offer_id, offer_type)
            
            if success:
                return [TextContent(
                    type="text",
                    text=f"Successfully added offer {offer_id} to your account."
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"Failed to add offer {offer_id}. It may already be loaded or invalid."
                )]
        
        elif name == "safeway_explore_api":
            client = get_client()
            endpoint = arguments.get("endpoint", "all")
            
            results = client.explore_api(endpoint)
            
            return [TextContent(
                type="text",
                text=json.dumps(results, indent=2)
            )]
        
        elif name == "safeway_check_api_status":
            import requests
            
            endpoints = {
                'OAuth Token': SafewayEndpoints.OAUTH_TOKEN,
                'Manufacturer Coupons': SafewayEndpoints.MANUFACTURER_COUPONS,
                'Personalized Offers': SafewayEndpoints.PERSONALIZED_OFFERS,
                'Shopping List': SafewayEndpoints.SHOPPING_LIST,
                'Product Search': SafewayEndpoints.PRODUCT_SEARCH,
                'Store Details': SafewayEndpoints.STORE_DETAILS,
            }
            
            status_report = []
            all_accessible = True
            
            for name_ep, url in endpoints.items():
                try:
                    response = requests.head(url, timeout=5)
                    accessible = response.status_code in [200, 401, 403, 400]
                    status = "✓ Accessible" if accessible else f"⚠ Status {response.status_code}"
                    status_report.append(f"{name_ep}: {status}")
                    if not accessible:
                        all_accessible = False
                except Exception as e:
                    status_report.append(f"{name_ep}: ❌ {str(e)}")
                    all_accessible = False
            
            summary = "✓ All endpoints accessible" if all_accessible else "⚠ Some endpoints not accessible"
            status_report.insert(0, summary)
            status_report.insert(1, "")
            
            return [TextContent(
                type="text",
                text="\n".join(status_report)
            )]
        
        elif name == "safeway_search_offers":
            client = get_client()
            query = arguments.get("query", "").lower()
            
            if not query:
                return [TextContent(
                    type="text",
                    text="Error: search query is required"
                )]
            
            manufacturer_coupons = client.get_manufacturer_coupons()
            personalized_offers = client.get_personalized_offers()
            
            # Search in descriptions and names
            matching_coupons = [
                c for c in manufacturer_coupons
                if query in c.description.lower()
            ]
            
            matching_offers = [
                o for o in personalized_offers
                if query in o.name.lower() or query in o.description.lower()
            ]
            
            result = {
                "query": query,
                "matching_manufacturer_coupons": [
                    {
                        "id": c.coupon_id,
                        "description": c.description,
                        "type": c.offer_type
                    }
                    for c in matching_coupons
                ],
                "matching_personalized_offers": [
                    {
                        "id": o.offer_id,
                        "name": o.name,
                        "description": o.description,
                        "type": o.offer_type
                    }
                    for o in matching_offers
                ],
                "total_matches": len(matching_coupons) + len(matching_offers)
            }
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "safeway_search_products":
            client = get_client()
            query = arguments.get("query", "")
            limit = arguments.get("limit", 20)
            
            if not query:
                return [TextContent(
                    type="text",
                    text="Error: search query is required"
                )]
            
            products = client.search_products(query, limit)
            
            if products:
                result = {
                    "query": query,
                    "found": len(products),
                    "products": products
                }
                return [TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"No products found for '{query}' at your local store."
                )]
        
        elif name == "safeway_find_recipe_ingredients":
            client = get_client()
            ingredients = arguments.get("ingredients", [])
            
            if not ingredients:
                return [TextContent(
                    type="text",
                    text="Error: ingredients list is required"
                )]
            
            results = client.find_recipe_ingredients(ingredients)
            
            # Format a nice summary
            summary_lines = ["Recipe Ingredient Availability Check:", ""]
            for ingredient, data in results.items():
                status = "✓ Available" if data['found'] else "❌ Not found"
                summary_lines.append(f"{ingredient}: {status} ({data['count']} products)")
            
            summary_lines.append("\nDetailed Results:")
            summary_lines.append(json.dumps(results, indent=2))
            
            return [TextContent(
                type="text",
                text="\n".join(summary_lines)
            )]
        
        elif name == "safeway_find_cheapest":
            client = get_client()
            product = arguments.get("product", "")
            limit = arguments.get("limit", 10)
            
            if not product:
                return [TextContent(
                    type="text",
                    text="Error: product name is required"
                )]
            
            result = client.find_cheapest_option(product, limit)
            
            if result['found']:
                summary = f"💰 Cheapest option for '{product}': ${result['cheapest_price']:.2f}\n"
                summary += f"Found {result['alternatives_count']} alternative(s)\n\n"
                summary += json.dumps(result, indent=2)
                return [TextContent(type="text", text=summary)]
            else:
                return [TextContent(
                    type="text",
                    text=f"❌ {result['message']}"
                )]
        
        elif name == "safeway_budget_meal_plan":
            client = get_client()
            ingredients = arguments.get("ingredients", [])
            max_budget = arguments.get("max_budget")
            
            if not ingredients:
                return [TextContent(
                    type="text",
                    text="Error: ingredients list is required"
                )]
            
            results = client.budget_meal_plan(ingredients, max_budget)
            summary = results['summary']
            
            # Format summary
            output_lines = ["🍳 Budget Meal Plan Results:", ""]
            output_lines.append(f"Items found: {summary['items_found']}/{summary['total_items']}")
            output_lines.append(f"Estimated total: ${summary['estimated_total']:.2f}")
            
            if summary['budget']:
                status = "✓ Within budget" if summary['within_budget'] else "❌ Over budget"
                output_lines.append(f"Budget: ${summary['budget']:.2f} - {status}")
                if summary['within_budget']:
                    output_lines.append(f"Remaining: ${summary['budget_remaining']:.2f}")
            
            if summary['items_missing']:
                output_lines.append(f"\n❌ Missing items: {', '.join(summary['items_missing'])}")
            
            output_lines.append("\n📝 Detailed ingredient pricing:")
            output_lines.append(json.dumps(results, indent=2))
            
            return [TextContent(
                type="text",
                text="\n".join(output_lines)
            )]
        
        elif name == "safeway_recommend_recipes":
            client = get_client()
            cuisine_type = arguments.get("cuisine_type")
            dietary_restrictions = arguments.get("dietary_restrictions")
            
            logger.info("Generating recipe recommendations from sale items...")
            results = client.recommend_recipes_from_sales(cuisine_type, dietary_restrictions)
            
            if 'error' in results:
                return [TextContent(type="text", text=f"Error: {results['error']}")]
            
            output_lines = ["🍳 Recipe Recommendations Based on Current Sales:", ""]
            output_lines.append(f"Total sale items analyzed: {results['total_sale_items']}")
            output_lines.append(f"Categories on sale: {', '.join(results['categories_on_sale'])}")
            output_lines.append("")
            
            recipes = results.get('recommended_recipes', [])
            if recipes:
                output_lines.append(f"📋 {len(recipes)} Recipe Ideas:")
                for i, recipe in enumerate(recipes[:5], 1):  # Show top 5
                    output_lines.append(f"\n{i}. {recipe['recipe_name']}")
                    output_lines.append(f"   Sale ingredients: {', '.join(recipe['sale_ingredients_available'][:3])}")
                    output_lines.append(f"   You'll also need: {', '.join(recipe['additional_ingredients_needed'][:3])}")
            else:
                output_lines.append("No recipe recommendations available based on current sales.")
            
            output_lines.append("\n📝 Full details:")
            output_lines.append(json.dumps(results, indent=2))
            
            return [TextContent(type="text", text="\n".join(output_lines))]
        
        elif name == "safeway_build_shopping_list":
            client = get_client()
            recipe_name = arguments.get("recipe_name", "")
            ingredients = arguments.get("ingredients", [])
            servings = arguments.get("servings", 4)
            
            if not recipe_name or not ingredients:
                return [TextContent(
                    type="text",
                    text="Error: recipe_name and ingredients are required"
                )]
            
            result = client.build_shopping_list_for_recipe(recipe_name, ingredients, servings)
            
            if 'error' in result:
                return [TextContent(type="text", text=f"Error: {result['error']}")]
            
            output_lines = [f"🛒 Shopping List for {recipe_name} ({servings} servings):", ""]
            output_lines.append(f"Total cost: ${result['total_cost']:.2f}")
            output_lines.append(f"Cost per serving: ${result['cost_per_serving']:.2f}")
            
            if result['items_on_sale']:
                output_lines.append(f"💰 Items on sale: {', '.join(result['items_on_sale'])}")
            
            output_lines.append("\n📝 Shopping list:")
            for item in result['shopping_list']:
                if item['found']:
                    status = f"✓ ${item['price']:.2f}"
                    if item['ingredient'] in result['items_on_sale']:
                        status += " (ON SALE)"
                    output_lines.append(f"  {item['ingredient']}: {status}")
                else:
                    output_lines.append(f"  {item['ingredient']}: ❌ Not found")
            
            output_lines.append("\n📊 Full details:")
            output_lines.append(json.dumps(result, indent=2))
            
            return [TextContent(type="text", text="\n".join(output_lines))]
        
        elif name == "safeway_weekly_meal_plan":
            client = get_client()
            days = arguments.get("days", 7)
            budget_per_day = arguments.get("budget_per_day")
            
            logger.info(f"Generating {days}-day meal plan...")
            result = client.get_weekly_meal_plan(days, budget_per_day)
            
            if 'error' in result:
                return [TextContent(type="text", text=f"Error: {result['error']}")]
            
            output_lines = [f"📅 {result['days_planned']}-Day Meal Plan:", ""]
            output_lines.append(f"Estimated total cost: ${result['estimated_total_cost']:.2f}")
            
            if result['total_budget']:
                output_lines.append(f"Total budget: ${result['total_budget']:.2f}")
                output_lines.append(f"Budget remaining: ${result['budget_remaining']:.2f}")
            
            output_lines.append("\n🍽️ Daily meal plan:")
            for meal in result['meal_plan']:
                output_lines.append(f"\nDay {meal['day']}: {meal['recipe']}")
                output_lines.append(f"  💰 Sale ingredients: {', '.join(meal['sale_ingredients'][:2])}")
                output_lines.append(f"  🛒 Also need: {', '.join(meal['additional_needed'][:3])}")
                output_lines.append(f"  💵 Est. cost: ${meal['estimated_cost']:.2f}")
            
            output_lines.append("\n📊 Full plan:")
            output_lines.append(json.dumps(result, indent=2))
            
            return [TextContent(type="text", text="\n".join(output_lines))]
        
        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]
    
    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}", exc_info=True)
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]


async def main():
    """Run the MCP server"""
    logger.info("Starting Safeway API MCP Server...")
    
    # Verify credentials are available
    if not all([
        os.environ.get('SAFEWAY_USERNAME'),
        os.environ.get('SAFEWAY_PASSWORD'),
        os.environ.get('SAFEWAY_STORE_ID')
    ]):
        logger.warning(
            "Safeway credentials not found in environment variables. "
            "Set SAFEWAY_USERNAME, SAFEWAY_PASSWORD, and SAFEWAY_STORE_ID"
        )
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
