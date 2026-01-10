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
