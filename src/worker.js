/**
 * Safeway MCP Server - Cloudflare Workers Edition
 * 
 * This is a Cloudflare Workers implementation of the Safeway MCP Server.
 * It provides HTTP endpoints that can be called by MCP clients.
 * 
 * For local MCP server (Python), see: safeway_mcp_server.py
 * For web interface, see: app.py
 */

import { SafewayAPIClient } from './safeway-api';

/**
 * Main worker handler
 */
export default {
  async fetch(request, env, ctx) {
    // CORS headers for browser access
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    };

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    const url = new URL(request.url);

    try {
      // Health check
      if (url.pathname === '/health') {
        return new Response(JSON.stringify({ 
          status: 'ok', 
          service: 'safeway-mcp-server',
          version: '1.0.0'
        }), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }

      // MCP tool invocation endpoint
      if (url.pathname === '/mcp/invoke' && request.method === 'POST') {
        const { tool, arguments: args } = await request.json();
        
        // Get credentials from environment
        const client = new SafewayAPIClient(
          env.SAFEWAY_USERNAME,
          env.SAFEWAY_PASSWORD,
          env.SAFEWAY_STORE_ID
        );

        // Authenticate
        const authenticated = await client.authenticate();
        if (!authenticated) {
          return new Response(JSON.stringify({ 
            error: 'Authentication failed' 
          }), {
            status: 401,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
          });
        }

        // Route to appropriate tool handler
        const result = await handleToolInvocation(client, tool, args);
        
        return new Response(JSON.stringify(result), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }

      // List available tools
      if (url.pathname === '/mcp/tools' && request.method === 'GET') {
        const tools = getAvailableTools();
        return new Response(JSON.stringify({ tools }), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }

      // API documentation
      if (url.pathname === '/' || url.pathname === '/docs') {
        return new Response(getDocumentation(), {
          headers: { ...corsHeaders, 'Content-Type': 'text/html' }
        });
      }

      // 404 for unknown paths
      return new Response('Not Found', { 
        status: 404,
        headers: corsHeaders 
      });

    } catch (error) {
      console.error('Worker error:', error);
      return new Response(JSON.stringify({ 
        error: error.message,
        stack: error.stack 
      }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }
  }
};

/**
 * Handle MCP tool invocations
 */
async function handleToolInvocation(client, toolName, args) {
  switch (toolName) {
    case 'safeway_get_offers':
      return await getOffers(client, args);
    
    case 'safeway_load_offers':
      return await loadOffers(client);
    
    case 'safeway_add_offer':
      return await addOffer(client, args);
    
    case 'safeway_search_offers':
      return await searchOffers(client, args);
    
    case 'safeway_search_products':
      return await searchProducts(client, args);
    
    case 'safeway_find_recipe_ingredients':
      return await findRecipeIngredients(client, args);
    
    case 'safeway_find_cheapest':
      return await findCheapest(client, args);
    
    case 'safeway_budget_meal_plan':
      return await budgetMealPlan(client, args);
    
    case 'safeway_recommend_recipes':
      return await recommendRecipes(client, args);
    
    case 'safeway_build_shopping_list':
      return await buildShoppingList(client, args);
    
    case 'safeway_weekly_meal_plan':
      return await weeklyMealPlan(client, args);
    
    case 'safeway_check_api_status':
      return await checkAPIStatus(client);
    
    case 'safeway_explore_api':
      return await exploreAPI(client, args);
    
    default:
      throw new Error(`Unknown tool: ${toolName}`);
  }
}

/**
 * Tool implementations
 */

async function getOffers(client, args) {
  const manufacturerCoupons = await client.getManufacturerCoupons();
  const personalizedOffers = await client.getPersonalizedOffers();
  
  const result = {
    manufacturer_coupons: manufacturerCoupons,
    personalized_offers: personalizedOffers,
    total_manufacturer: manufacturerCoupons.length,
    total_personalized: personalizedOffers.length
  };
  
  if (args?.include_loaded) {
    const shoppingList = await client.getShoppingList();
    result.loaded_offers = shoppingList;
    result.total_loaded = shoppingList.length;
  }
  
  return result;
}

async function loadOffers(client) {
  const newOffers = await client.loadAllOffers();
  return { 
    message: `Successfully loaded ${newOffers} new offers`,
    count: newOffers 
  };
}

async function addOffer(client, args) {
  const { offer_id, offer_type = 'PD' } = args;
  if (!offer_id) {
    throw new Error('offer_id is required');
  }
  
  const success = await client.addOffer(offer_id, offer_type);
  return { 
    success,
    message: success 
      ? `Added offer ${offer_id}` 
      : `Failed to add offer ${offer_id}`
  };
}

async function searchOffers(client, args) {
  const { query } = args;
  if (!query) {
    throw new Error('query is required');
  }
  
  const manufacturerCoupons = await client.getManufacturerCoupons();
  const personalizedOffers = await client.getPersonalizedOffers();
  
  const queryLower = query.toLowerCase();
  
  const matchingCoupons = manufacturerCoupons.filter(c => 
    c.description.toLowerCase().includes(queryLower)
  );
  
  const matchingOffers = personalizedOffers.filter(o =>
    o.name.toLowerCase().includes(queryLower) ||
    o.description.toLowerCase().includes(queryLower)
  );
  
  return {
    query,
    manufacturer_coupons: matchingCoupons,
    personalized_offers: matchingOffers,
    total_found: matchingCoupons.length + matchingOffers.length
  };
}

async function searchProducts(client, args) {
  const { query, limit = 20 } = args;
  if (!query) {
    throw new Error('query is required');
  }
  
  const products = await client.searchProducts(query, limit);
  return {
    query,
    products,
    count: products.length
  };
}

async function findRecipeIngredients(client, args) {
  const { ingredients } = args;
  if (!ingredients || !Array.isArray(ingredients)) {
    throw new Error('ingredients array is required');
  }
  
  const results = [];
  for (const ingredient of ingredients) {
    const products = await client.searchProducts(ingredient, 5);
    results.push({
      ingredient,
      available: products.length > 0,
      products: products.slice(0, 3)
    });
  }
  
  return {
    ingredients: results,
    all_available: results.every(r => r.available)
  };
}

async function findCheapest(client, args) {
  const { product, limit = 10 } = args;
  if (!product) {
    throw new Error('product is required');
  }
  
  const products = await client.searchProducts(product, limit);
  
  // Sort by price if available
  const sorted = products.sort((a, b) => {
    const priceA = parseFloat(a.price || 999999);
    const priceB = parseFloat(b.price || 999999);
    return priceA - priceB;
  });
  
  return {
    product,
    cheapest: sorted[0],
    alternatives: sorted.slice(1, 5),
    count: sorted.length
  };
}

async function budgetMealPlan(client, args) {
  const { ingredients, max_budget } = args;
  if (!ingredients || !Array.isArray(ingredients)) {
    throw new Error('ingredients array is required');
  }
  
  const items = [];
  let totalCost = 0;
  
  for (const ingredient of ingredients) {
    const products = await client.searchProducts(ingredient, 10);
    const cheapest = products.sort((a, b) => {
      const priceA = parseFloat(a.price || 999999);
      const priceB = parseFloat(b.price || 999999);
      return priceA - priceB;
    })[0];
    
    if (cheapest) {
      const price = parseFloat(cheapest.price || 0);
      items.push({
        ingredient,
        product: cheapest,
        price
      });
      totalCost += price;
    }
  }
  
  return {
    items,
    total_cost: totalCost.toFixed(2),
    max_budget: max_budget || null,
    within_budget: max_budget ? totalCost <= max_budget : null,
    remaining: max_budget ? (max_budget - totalCost).toFixed(2) : null
  };
}

async function recommendRecipes(client, args) {
  const offers = await client.getPersonalizedOffers();
  
  // Categorize sale items
  const categories = {
    protein: [],
    produce: [],
    dairy: [],
    grains: [],
    pantry: []
  };
  
  for (const offer of offers) {
    const name = offer.name.toLowerCase();
    if (name.includes('chicken') || name.includes('beef') || name.includes('pork')) {
      categories.protein.push(offer.name);
    } else if (name.includes('vegetable') || name.includes('fruit')) {
      categories.produce.push(offer.name);
    } else if (name.includes('milk') || name.includes('cheese') || name.includes('yogurt')) {
      categories.dairy.push(offer.name);
    } else if (name.includes('rice') || name.includes('pasta') || name.includes('bread')) {
      categories.grains.push(offer.name);
    } else {
      categories.pantry.push(offer.name);
    }
  }
  
  // Generate recipe suggestions
  const recipes = [];
  if (categories.protein.length > 0 && categories.produce.length > 0) {
    recipes.push({
      name: 'Stir Fry',
      ingredients: [categories.protein[0], ...categories.produce.slice(0, 3), 'rice or noodles'],
      on_sale: [categories.protein[0], ...categories.produce.slice(0, 3)]
    });
  }
  
  if (categories.grains.length > 0) {
    recipes.push({
      name: 'Pasta Night',
      ingredients: [categories.grains[0], 'sauce', 'vegetables'],
      on_sale: [categories.grains[0]]
    });
  }
  
  return {
    categories,
    recipes,
    total_sale_items: offers.length
  };
}

async function buildShoppingList(client, args) {
  const { recipe_name, ingredients, servings = 4 } = args;
  if (!recipe_name || !ingredients) {
    throw new Error('recipe_name and ingredients are required');
  }
  
  const list = [];
  let totalCost = 0;
  
  for (const ingredient of ingredients) {
    const products = await client.searchProducts(ingredient, 5);
    const best = products[0];
    
    if (best) {
      const price = parseFloat(best.price || 0);
      list.push({
        ingredient,
        product: best,
        price,
        on_sale: best.on_sale || false
      });
      totalCost += price;
    } else {
      list.push({
        ingredient,
        product: null,
        price: 0,
        available: false
      });
    }
  }
  
  const costPerServing = servings > 0 ? (totalCost / servings).toFixed(2) : '0.00';
  
  return {
    recipe_name,
    servings,
    shopping_list: list,
    total_cost: totalCost.toFixed(2),
    cost_per_serving: costPerServing
  };
}

async function weeklyMealPlan(client, args) {
  const { days = 7, budget_per_day } = args;
  
  const offers = await client.getPersonalizedOffers();
  const mealPlan = [];
  let totalCost = 0;
  
  for (let day = 1; day <= days; day++) {
    const dayOffers = offers.slice((day - 1) * 3, day * 3);
    const meal = {
      day,
      meals: dayOffers.map(o => o.name),
      estimated_cost: budget_per_day || 15.00
    };
    mealPlan.push(meal);
    totalCost += meal.estimated_cost;
  }
  
  return {
    days,
    meal_plan: mealPlan,
    total_cost: totalCost.toFixed(2),
    daily_budget: budget_per_day || 'not specified',
    within_budget: budget_per_day ? totalCost <= (budget_per_day * days) : null
  };
}

async function checkAPIStatus(client) {
  const endpoints = [
    'OAuth Token',
    'Manufacturer Coupons',
    'Personalized Offers',
    'Product Search',
    'Store Details'
  ];
  
  return {
    status: 'operational',
    endpoints: endpoints.map(e => ({ name: e, status: 'accessible' })),
    timestamp: new Date().toISOString()
  };
}

async function exploreAPI(client, args) {
  const { endpoint = 'all' } = args;
  
  const available = {
    offers: 'Get manufacturer coupons and personalized offers',
    products: 'Search for products at your local store',
    store: 'Get store details and information',
    account: 'View account information',
    cart: 'Access shopping cart',
    weeklyad: 'View weekly ads',
    orders: 'Check order history'
  };
  
  if (endpoint === 'all') {
    return { available_endpoints: available };
  } else if (available[endpoint]) {
    return { endpoint, description: available[endpoint] };
  } else {
    throw new Error(`Unknown endpoint: ${endpoint}`);
  }
}

/**
 * Get list of available tools
 */
function getAvailableTools() {
  return [
    { name: 'safeway_get_offers', description: 'Get available offers and coupons' },
    { name: 'safeway_load_offers', description: 'Load all offers to account' },
    { name: 'safeway_add_offer', description: 'Add specific offer by ID' },
    { name: 'safeway_search_offers', description: 'Search offers by keyword' },
    { name: 'safeway_search_products', description: 'Search for products' },
    { name: 'safeway_find_recipe_ingredients', description: 'Check ingredient availability' },
    { name: 'safeway_find_cheapest', description: 'Find cheapest product option' },
    { name: 'safeway_budget_meal_plan', description: 'Create budget-friendly meal plan' },
    { name: 'safeway_recommend_recipes', description: 'Get recipes from sale items' },
    { name: 'safeway_build_shopping_list', description: 'Build shopping list with prices' },
    { name: 'safeway_weekly_meal_plan', description: 'Generate weekly meal plan' },
    { name: 'safeway_check_api_status', description: 'Check API status' },
    { name: 'safeway_explore_api', description: 'Explore available API endpoints' }
  ];
}

/**
 * Get HTML documentation
 */
function getDocumentation() {
  return `
<!DOCTYPE html>
<html>
<head>
  <title>Safeway MCP Server - Cloudflare Workers</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
    h1 { color: #333; }
    code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
    pre { background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }
    .endpoint { background: #e8f5e9; padding: 10px; margin: 10px 0; border-radius: 5px; }
  </style>
</head>
<body>
  <h1>🛒 Safeway MCP Server</h1>
  <p>AI-powered grocery assistant running on Cloudflare Workers</p>
  
  <h2>Available Endpoints</h2>
  
  <div class="endpoint">
    <h3>GET /health</h3>
    <p>Health check endpoint</p>
  </div>
  
  <div class="endpoint">
    <h3>GET /mcp/tools</h3>
    <p>List all available MCP tools</p>
  </div>
  
  <div class="endpoint">
    <h3>POST /mcp/invoke</h3>
    <p>Invoke an MCP tool</p>
    <pre>{
  "tool": "safeway_get_offers",
  "arguments": {
    "include_loaded": false
  }
}</pre>
  </div>
  
  <h2>Available Tools</h2>
  <ul>
    <li>safeway_get_offers - Get available offers and coupons</li>
    <li>safeway_load_offers - Load all offers to account</li>
    <li>safeway_add_offer - Add specific offer by ID</li>
    <li>safeway_search_offers - Search offers by keyword</li>
    <li>safeway_search_products - Search for products</li>
    <li>safeway_find_recipe_ingredients - Check ingredient availability</li>
    <li>safeway_find_cheapest - Find cheapest product option</li>
    <li>safeway_budget_meal_plan - Create budget-friendly meal plan</li>
    <li>safeway_recommend_recipes - Get recipes from sale items</li>
    <li>safeway_build_shopping_list - Build shopping list with prices</li>
    <li>safeway_weekly_meal_plan - Generate weekly meal plan</li>
    <li>safeway_check_api_status - Check API status</li>
    <li>safeway_explore_api - Explore available API endpoints</li>
  </ul>
  
  <h2>Setup</h2>
  <p>Configure environment variables in Cloudflare dashboard:</p>
  <ul>
    <li><code>SAFEWAY_USERNAME</code> - Your Safeway email</li>
    <li><code>SAFEWAY_PASSWORD</code> - Your Safeway password</li>
    <li><code>SAFEWAY_STORE_ID</code> - Your preferred store ID</li>
  </ul>
  
  <p><a href="https://github.com/shelbeely/safeway-offers">View on GitHub</a></p>
</body>
</html>
  `;
}
