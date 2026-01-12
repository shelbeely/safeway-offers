#!/usr/bin/env python3
"""
PantryPilot API Client
A Python client for interacting with Safeway's unofficial mobile API
"""

import os
import sys
import json
import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# API Endpoints
class SafewayEndpoints:
    """Safeway API endpoint URLs"""
    OAUTH_TOKEN = "https://albertsons.okta.com/oauth2/ausp6soxrIyPrm8rS2p6/v1/token"
    MANUFACTURER_COUPONS = "https://nimbus.safeway.com/emmd/service/gallery/offer/mfg"
    PERSONALIZED_OFFERS = "https://nimbus.safeway.com/emmd/service/gallery/offer/pd"
    ADD_OFFER = "https://nimbus.safeway.com/Clipping1/services/clip/items"
    SHOPPING_LIST = "https://nimbus.safeway.com/emmd/service/mylist/default/details"
    
    # Additional endpoints
    PRODUCT_SEARCH = "https://nimbus.safeway.com/emmd/service/product/search"
    STORE_DETAILS = "https://nimbus.safeway.com/emmd/service/store/details"
    ACCOUNT_DETAILS = "https://nimbus.safeway.com/emmd/service/account/details"
    CART = "https://nimbus.safeway.com/emmd/service/cart/details"
    WEEKLY_AD = "https://nimbus.safeway.com/emmd/service/weeklyad"
    ORDER_HISTORY = "https://nimbus.safeway.com/emmd/service/order/history"


# OAuth Credentials
SAFEWAY_CLIENT_ID = "0oap6kkp7Sefg24rB2p6"
SAFEWAY_CLIENT_SECRET = "4UpmzD4hlF2VYQqYjDUoamgLu2Bo1OzagpfG7yus"
USER_AGENT = "Safeway/3373 CFNetwork/978.0.7 Darwin/18.6.0"


@dataclass
class Coupon:
    """Represents a manufacturer coupon"""
    coupon_id: str
    description: str
    offer_type: str
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Coupon':
        return cls(
            coupon_id=data.get('couponID', ''),
            description=data.get('description', ''),
            offer_type=data.get('offerPgm', '')
        )


@dataclass
class Offer:
    """Represents a personalized offer"""
    offer_id: str
    name: str
    description: str
    offer_type: str
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Offer':
        return cls(
            offer_id=data.get('offerID', ''),
            name=data.get('name', ''),
            description=data.get('description', ''),
            offer_type=data.get('offerPgm', '')
        )


class SafewayAPIClient:
    """Client for interacting with Safeway's API"""
    
    def __init__(self, username: str, password: str, store_id: str):
        self.username = username
        self.password = password
        self.store_id = store_id
        self.access_token: Optional[str] = None
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
    
    def authenticate(self) -> bool:
        """Authenticate with Safeway OAuth and get access token"""
        try:
            logger.info("Authenticating with Safeway...")
            
            data = {
                'username': self.username,
                'password': self.password,
                'grant_type': 'password',
                'scope': 'openid profile offline_access'
            }
            
            response = self.session.post(
                SafewayEndpoints.OAUTH_TOKEN,
                data=data,
                auth=(SAFEWAY_CLIENT_ID, SAFEWAY_CLIENT_SECRET),
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            
            response.raise_for_status()
            token_data = response.json()
            self.access_token = token_data.get('access_token')
            
            if self.access_token:
                logger.info("✓ Authentication successful")
                self.session.headers.update({'Authorization': f'Bearer {self.access_token}'})
                return True
            else:
                logger.error("❌ No access token received")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Authentication failed: {e}")
            return False
    
    def _make_request(self, url: str, method: str = 'GET', **kwargs) -> Optional[Dict]:
        """Make an authenticated API request"""
        if not self.access_token:
            logger.error("Not authenticated. Call authenticate() first.")
            return None
        
        try:
            # Add store_id as query parameter if URL expects it
            if 'storeId=' in url or '?' not in url:
                if '?' in url:
                    url = f"{url}&storeId={self.store_id}"
                else:
                    url = f"{url}?storeId={self.store_id}"
            
            # Add cookie
            cookies = {'swyConsumerDirectoryPro': self.access_token}
            
            response = self.session.request(method, url, cookies=cookies, **kwargs)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None
    
    def get_manufacturer_coupons(self) -> List[Coupon]:
        """Get all manufacturer coupons"""
        data = self._make_request(SafewayEndpoints.MANUFACTURER_COUPONS)
        if data and 'manufacturerCoupons' in data:
            return [Coupon.from_dict(c) for c in data['manufacturerCoupons']]
        return []
    
    def get_personalized_offers(self) -> List[Offer]:
        """Get personalized offers"""
        data = self._make_request(SafewayEndpoints.PERSONALIZED_OFFERS)
        if data and 'personalizedDeals' in data:
            return [Offer.from_dict(o) for o in data['personalizedDeals']]
        return []
    
    def get_shopping_list(self) -> List[Dict]:
        """Get already loaded offers"""
        data = self._make_request(SafewayEndpoints.SHOPPING_LIST)
        if data and 'shoppingList' in data:
            return data['shoppingList']
        return []
    
    def add_offer(self, offer_id: str, offer_type: str) -> bool:
        """Add an offer to the account"""
        try:
            payload = {
                'items': [
                    {'clipType': 'L', 'itemId': offer_id, 'itemType': offer_type},
                    {'clipType': 'C', 'itemId': offer_id, 'itemType': offer_type}
                ]
            }
            
            url = SafewayEndpoints.ADD_OFFER
            response = self.session.post(
                f"{url}?storeId={self.store_id}",
                json=payload,
                headers={
                    'Authorization': f'Bearer {self.access_token}',
                    'Content-Type': 'application/json'
                }
            )
            
            return response.status_code == 200
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to add offer {offer_id}: {e}")
            return False
    
    def load_all_offers(self) -> int:
        """Load all available offers into the account"""
        if not self.authenticate():
            return 0
        
        logger.info("Getting manufacturer coupons...")
        coupons = self.get_manufacturer_coupons()
        
        logger.info("Getting personalized offers...")
        offers = self.get_personalized_offers()
        
        logger.info("Getting existing loaded offers...")
        shopping_list = self.get_shopping_list()
        loaded_ids = {item.get('offerId') for item in shopping_list}
        
        total_new = 0
        total_items = len(coupons) + len(offers)
        
        logger.info(f"Processing {total_items} offers...")
        
        # Add manufacturer coupons
        for coupon in coupons:
            if coupon.coupon_id not in loaded_ids:
                if self.add_offer(coupon.coupon_id, coupon.offer_type):
                    total_new += 1
        
        # Add personalized offers
        for offer in offers:
            if offer.offer_id not in loaded_ids:
                if self.add_offer(offer.offer_id, offer.offer_type):
                    total_new += 1
        
        logger.info(f"✓ Added {total_new} new offers")
        return total_new
    
    def search_products(self, query: str, limit: int = 20, sort_by_price: bool = False) -> List[Dict]:
        """Search for products by name or keyword"""
        if not self.authenticate():
            return []
        
        try:
            # Product search endpoint may require query parameter
            url = f"{SafewayEndpoints.PRODUCT_SEARCH}?storeId={self.store_id}&q={query}&limit={limit}"
            
            response = self.session.get(
                url,
                headers={'Authorization': f'Bearer {self.access_token}'},
                cookies={'swyConsumerDirectoryPro': self.access_token}
            )
            
            if response.status_code == 200:
                data = response.json()
                # Return products if found
                products = []
                if isinstance(data, dict) and 'products' in data:
                    products = data['products']
                elif isinstance(data, list):
                    products = data
                else:
                    products = [data]
                
                # Sort by price if requested
                if sort_by_price and products:
                    products = self._sort_by_price(products)
                
                return products
            else:
                logger.warning(f"Product search returned status {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"Product search failed: {e}")
            return []
    
    def _sort_by_price(self, products: List[Dict]) -> List[Dict]:
        """Sort products by price (lowest first)"""
        def get_price(product):
            # Try various price fields
            price = product.get('price') or product.get('salePrice') or product.get('regularPrice')
            if price:
                # Convert to float if string
                try:
                    return float(price) if isinstance(price, (int, float, str)) else float('inf')
                except (ValueError, TypeError):
                    return float('inf')
            return float('inf')
        
        return sorted(products, key=get_price)
    
    def find_cheapest_option(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Find the cheapest option for a product"""
        products = self.search_products(query, limit=limit, sort_by_price=True)
        
        if not products:
            return {
                'query': query,
                'found': False,
                'message': f'No products found for "{query}"'
            }
        
        cheapest = products[0]
        all_prices = [p for p in products if self._get_product_price(p) is not None]
        
        return {
            'query': query,
            'found': True,
            'cheapest': cheapest,
            'cheapest_price': self._get_product_price(cheapest),
            'alternatives_count': len(products) - 1,
            'all_options': products[:5],  # Top 5 cheapest
            'price_range': {
                'min': self._get_product_price(products[0]) if products else None,
                'max': self._get_product_price(products[-1]) if products else None
            } if all_prices else None
        }
    
    def _get_product_price(self, product: Dict) -> Optional[float]:
        """Extract price from product data"""
        price = product.get('price') or product.get('salePrice') or product.get('regularPrice')
        if price:
            try:
                return float(price)
            except (ValueError, TypeError):
                return None
        return None
    
    def get_sale_items(self) -> List[Dict]:
        """Get items currently on sale (from offers with price info)"""
        if not self.authenticate():
            return []
        
        sale_items = []
        
        # Get offers with savings
        coupons = self.get_manufacturer_coupons()
        offers = self.get_personalized_offers()
        
        for coupon in coupons:
            if coupon.description:
                sale_items.append({
                    'type': 'manufacturer_coupon',
                    'id': coupon.coupon_id,
                    'description': coupon.description,
                    'category': self._categorize_item(coupon.description)
                })
        
        for offer in offers:
            if offer.description or offer.name:
                sale_items.append({
                    'type': 'personalized_offer',
                    'id': offer.offer_id,
                    'name': offer.name,
                    'description': offer.description,
                    'category': self._categorize_item(offer.name or offer.description)
                })
        
        return sale_items
    
    def _categorize_item(self, text: str) -> str:
        """Categorize an item based on keywords"""
        text_lower = text.lower()
        
        categories = {
            'protein': ['chicken', 'beef', 'pork', 'fish', 'turkey', 'salmon', 'steak', 'meat', 'shrimp', 'tilapia'],
            'dairy': ['milk', 'cheese', 'yogurt', 'butter', 'cream', 'egg'],
            'produce': ['vegetable', 'fruit', 'lettuce', 'tomato', 'potato', 'apple', 'banana', 'carrot', 'broccoli'],
            'pantry': ['pasta', 'rice', 'bread', 'cereal', 'flour', 'sugar', 'oil', 'sauce'],
            'frozen': ['frozen', 'ice cream', 'pizza'],
            'bakery': ['bread', 'bagel', 'muffin', 'cake', 'cookie']
        }
        
        for category, keywords in categories.items():
            if any(keyword in text_lower for keyword in keywords):
                return category
        
        return 'other'
    
    def recommend_recipes_from_sales(self, cuisine_type: Optional[str] = None, 
                                     dietary_restrictions: Optional[List[str]] = None) -> Dict[str, Any]:
        """Recommend recipes based on current sale items"""
        if not self.authenticate():
            return {'error': 'Authentication failed'}
        
        logger.info("Analyzing sale items for recipe recommendations...")
        sale_items = self.get_sale_items()
        
        if not sale_items:
            return {
                'recommendations': [],
                'message': 'No sale items found to base recommendations on'
            }
        
        # Categorize sale items
        categorized = {}
        for item in sale_items:
            category = item.get('category', 'other')
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(item)
        
        # Generate recipe ideas based on available ingredients
        recommendations = []
        
        # Recipe templates based on ingredient categories
        recipe_templates = {
            'protein_and_produce': {
                'categories_needed': ['protein', 'produce'],
                'recipes': [
                    {'name': 'Stir Fry', 'additional': ['rice', 'soy sauce', 'garlic']},
                    {'name': 'Grilled Protein with Roasted Vegetables', 'additional': ['olive oil', 'seasonings']},
                    {'name': 'Sheet Pan Dinner', 'additional': ['potatoes', 'seasonings']}
                ]
            },
            'protein_and_dairy': {
                'categories_needed': ['protein', 'dairy'],
                'recipes': [
                    {'name': 'Creamy Chicken Pasta', 'additional': ['pasta', 'cream', 'garlic']},
                    {'name': 'Cheesy Casserole', 'additional': ['pasta', 'breadcrumbs']},
                    {'name': 'Protein and Cheese Quesadillas', 'additional': ['tortillas']}
                ]
            },
            'protein_and_pantry': {
                'categories_needed': ['protein', 'pantry'],
                'recipes': [
                    {'name': 'Protein Fried Rice', 'additional': ['eggs', 'vegetables']},
                    {'name': 'Pasta with Protein', 'additional': ['tomato sauce', 'herbs']},
                    {'name': 'Protein Tacos', 'additional': ['tortillas', 'toppings']}
                ]
            },
            'dairy_and_produce': {
                'categories_needed': ['dairy', 'produce'],
                'recipes': [
                    {'name': 'Fresh Salad with Cheese', 'additional': ['dressing']},
                    {'name': 'Vegetable Frittata', 'additional': ['eggs', 'herbs']},
                    {'name': 'Creamy Vegetable Soup', 'additional': ['broth', 'herbs']}
                ]
            }
        }
        
        # Match available categories with recipe templates
        available_categories = set(categorized.keys())
        
        for template_name, template in recipe_templates.items():
            needed = set(template['categories_needed'])
            if needed.issubset(available_categories):
                for recipe in template['recipes']:
                    # Get actual sale items for this recipe
                    sale_ingredients = []
                    for cat in template['categories_needed']:
                        if cat in categorized:
                            sale_ingredients.extend([
                                item.get('name') or item.get('description', '')[:50]
                                for item in categorized[cat][:2]  # Take up to 2 items per category
                            ])
                    
                    recommendations.append({
                        'recipe_name': recipe['name'],
                        'sale_ingredients_available': sale_ingredients,
                        'additional_ingredients_needed': recipe['additional'],
                        'categories_used': list(needed),
                        'estimated_savings': 'Using sale items'
                    })
        
        return {
            'total_sale_items': len(sale_items),
            'categories_on_sale': list(categorized.keys()),
            'sale_item_summary': {cat: len(items) for cat, items in categorized.items()},
            'recommended_recipes': recommendations[:10],  # Top 10 recommendations
            'sale_items_detail': categorized
        }
    
    def build_shopping_list_for_recipe(self, recipe_name: str, ingredients: List[str],
                                      servings: int = 4) -> Dict[str, Any]:
        """Build a shopping list for a recipe with price estimates"""
        if not self.authenticate():
            return {'error': 'Authentication failed'}
        
        shopping_list = []
        total_cost = 0.0
        items_on_sale = []
        
        # Check each ingredient
        for ingredient in ingredients:
            # Find cheapest option
            result = self.find_cheapest_option(ingredient, limit=5)
            
            if result['found']:
                shopping_list.append({
                    'ingredient': ingredient,
                    'found': True,
                    'cheapest_option': result['cheapest'],
                    'price': result['cheapest_price'],
                    'alternatives': len(result.get('all_options', [])) - 1
                })
                total_cost += result['cheapest_price']
                
                # Check if on sale
                if self._is_on_sale(ingredient):
                    items_on_sale.append(ingredient)
            else:
                shopping_list.append({
                    'ingredient': ingredient,
                    'found': False,
                    'price': None
                })
        
        cost_per_serving = total_cost / servings if servings > 0 else total_cost
        
        return {
            'recipe_name': recipe_name,
            'servings': servings,
            'shopping_list': shopping_list,
            'total_cost': round(total_cost, 2),
            'cost_per_serving': round(cost_per_serving, 2),
            'items_on_sale': items_on_sale,
            'potential_savings': len(items_on_sale) > 0
        }
    
    def _is_on_sale(self, ingredient: str) -> bool:
        """Check if an ingredient matches any current sale items"""
        sale_items = self.get_sale_items()
        ingredient_lower = ingredient.lower()
        
        for item in sale_items:
            text = (item.get('name', '') + ' ' + item.get('description', '')).lower()
            if ingredient_lower in text or any(word in text for word in ingredient_lower.split()):
                return True
        
        return False
    
    def get_weekly_meal_plan(self, days: int = 7, budget_per_day: Optional[float] = None) -> Dict[str, Any]:
        """Generate a weekly meal plan based on sales and budget"""
        if not self.authenticate():
            return {'error': 'Authentication failed'}
        
        # Get recipe recommendations based on sales
        recommendations = self.recommend_recipes_from_sales()
        
        if not recommendations.get('recommended_recipes'):
            return {
                'error': 'No recipes could be recommended based on current sales'
            }
        
        recipes = recommendations['recommended_recipes']
        meal_plan = []
        total_budget_used = 0.0
        
        for day in range(1, min(days + 1, len(recipes) + 1)):
            recipe = recipes[(day - 1) % len(recipes)]
            
            # Estimate cost (would need actual ingredient lookup for real costs)
            estimated_cost = 15.0  # Placeholder - would calculate from actual ingredients
            
            if budget_per_day and total_budget_used + estimated_cost > (budget_per_day * day):
                continue  # Skip if over budget
            
            meal_plan.append({
                'day': day,
                'recipe': recipe['recipe_name'],
                'sale_ingredients': recipe['sale_ingredients_available'],
                'additional_needed': recipe['additional_ingredients_needed'],
                'estimated_cost': estimated_cost
            })
            
            total_budget_used += estimated_cost
        
        return {
            'days_planned': len(meal_plan),
            'total_budget': budget_per_day * days if budget_per_day else None,
            'estimated_total_cost': round(total_budget_used, 2),
            'budget_remaining': round((budget_per_day * days) - total_budget_used, 2) if budget_per_day else None,
            'meal_plan': meal_plan,
            'shopping_summary': recommendations.get('sale_item_summary', {})
        }
    
    def budget_meal_plan(self, ingredients: List[str], max_budget: Optional[float] = None) -> Dict[str, Any]:
        """Find cheapest options for meal ingredients within budget"""
        if not self.authenticate():
            return {'error': 'Authentication failed'}
        
        results = {}
        total_cost = 0.0
        items_found = 0
        items_missing = []
        
        for ingredient in ingredients:
            logger.info(f"Finding cheapest option for: {ingredient}")
            result = self.find_cheapest_option(ingredient, limit=10)
            results[ingredient] = result
            
            if result['found']:
                items_found += 1
                price = result['cheapest_price']
                if price:
                    total_cost += price
            else:
                items_missing.append(ingredient)
        
        within_budget = max_budget is None or total_cost <= max_budget
        
        return {
            'ingredients': results,
            'summary': {
                'total_items': len(ingredients),
                'items_found': items_found,
                'items_missing': items_missing,
                'estimated_total': round(total_cost, 2),
                'budget': max_budget,
                'within_budget': within_budget,
                'budget_remaining': round(max_budget - total_cost, 2) if max_budget else None
            }
        }
    
    def find_recipe_ingredients(self, ingredients: List[str]) -> Dict[str, Any]:
        """Search for multiple recipe ingredients at once"""
        if not self.authenticate():
            return {'error': 'Authentication failed'}
        
        results = {}
        for ingredient in ingredients:
            logger.info(f"Searching for: {ingredient}")
            products = self.search_products(ingredient, limit=5)
            results[ingredient] = {
                'found': len(products) > 0,
                'count': len(products),
                'products': products[:5]  # Limit to top 5 results
            }
        
        return results
    
    def explore_api(self, endpoint: str = 'all') -> Dict[str, Any]:
        """Explore various API endpoints"""
        if not self.authenticate():
            return {'error': 'Authentication failed'}
        
        results = {}
        
        if endpoint in ['all', 'offers']:
            results['manufacturer_coupons'] = self._make_request(SafewayEndpoints.MANUFACTURER_COUPONS)
            results['personalized_offers'] = self._make_request(SafewayEndpoints.PERSONALIZED_OFFERS)
            results['shopping_list'] = self._make_request(SafewayEndpoints.SHOPPING_LIST)
        
        if endpoint in ['all', 'products']:
            results['products'] = self._make_request(SafewayEndpoints.PRODUCT_SEARCH)
        
        if endpoint in ['all', 'store']:
            results['store_details'] = self._make_request(SafewayEndpoints.STORE_DETAILS)
        
        if endpoint in ['all', 'account']:
            results['account_details'] = self._make_request(SafewayEndpoints.ACCOUNT_DETAILS)
        
        if endpoint in ['all', 'cart']:
            results['cart'] = self._make_request(SafewayEndpoints.CART)
        
        if endpoint in ['all', 'weeklyad']:
            results['weekly_ad'] = self._make_request(SafewayEndpoints.WEEKLY_AD)
        
        if endpoint in ['all', 'orders']:
            results['order_history'] = self._make_request(SafewayEndpoints.ORDER_HISTORY)
        
        return results


def main():
    """Main CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='PantryPilot API Client')
    parser.add_argument('-u', '--username', help='Safeway username/email', 
                       default=os.environ.get('SAFEWAY_USERNAME'))
    parser.add_argument('-p', '--password', help='Safeway password',
                       default=os.environ.get('SAFEWAY_PASSWORD'))
    parser.add_argument('-id', '--store-id', help='Safeway store ID',
                       default=os.environ.get('SAFEWAY_STORE_ID'))
    parser.add_argument('--check-api', action='store_true', help='Check API status')
    parser.add_argument('--explore', action='store_true', help='Explore API endpoints')
    parser.add_argument('--endpoint', default='all', 
                       help='Endpoint to explore: all, offers, products, store, account, cart, weeklyad, orders')
    parser.add_argument('--search-product', help='Search for a product by name')
    parser.add_argument('--find-ingredients', nargs='+', 
                       help='Find multiple recipe ingredients (e.g., --find-ingredients milk eggs flour)')
    parser.add_argument('--find-cheapest', help='Find the cheapest option for a product')
    parser.add_argument('--budget-plan', nargs='+', metavar='INGREDIENT',
                       help='Plan budget-friendly meal with ingredients (e.g., --budget-plan milk eggs flour)')
    parser.add_argument('--max-budget', type=float, 
                       help='Maximum budget for budget meal plan (e.g., --max-budget 25.00)')
    parser.add_argument('--recommend-recipes', action='store_true',
                       help='Get recipe recommendations based on current sales')
    parser.add_argument('--build-shopping-list', nargs='+', metavar='INGREDIENT',
                       help='Build shopping list for a recipe with price estimates')
    parser.add_argument('--recipe-name', help='Name of recipe for shopping list')
    parser.add_argument('--servings', type=int, default=4,
                       help='Number of servings for recipe (default: 4)')
    parser.add_argument('--weekly-meal-plan', action='store_true',
                       help='Generate a weekly meal plan based on sales')
    parser.add_argument('--days', type=int, default=7,
                       help='Number of days for meal plan (default: 7)')
    parser.add_argument('--budget-per-day', type=float,
                       help='Daily budget for meal plan (e.g., --budget-per-day 15.00)')
    
    args = parser.parse_args()
    
    if args.check_api:
        print("Checking Safeway API endpoints...")
        # Simple connectivity check
        endpoints = {
            'OAuth': SafewayEndpoints.OAUTH_TOKEN,
            'Manufacturer Coupons': SafewayEndpoints.MANUFACTURER_COUPONS,
            'Personalized Offers': SafewayEndpoints.PERSONALIZED_OFFERS,
        }
        
        for name, url in endpoints.items():
            try:
                response = requests.head(url, timeout=10, headers={'User-Agent': USER_AGENT})
                status = "✓ Accessible" if response.status_code in [200, 401, 403, 400] else f"⚠ Status {response.status_code}"
                print(f"{name}: {status}")
            except Exception as e:
                print(f"{name}: ❌ {e}")
        return
    
    if not all([args.username, args.password, args.store_id]):
        parser.print_help()
        print("\n❌ Error: Username, password, and store ID are required")
        print("Set via arguments or environment variables:")
        print("  SAFEWAY_USERNAME, SAFEWAY_PASSWORD, SAFEWAY_STORE_ID")
        sys.exit(1)
    
    client = SafewayAPIClient(args.username, args.password, args.store_id)
    
    if args.find_cheapest:
        print(f"Finding cheapest option for: {args.find_cheapest}")
        result = client.find_cheapest_option(args.find_cheapest)
        if result['found']:
            print(f"\n💰 Cheapest Option: ${result['cheapest_price']:.2f}")
            print(json.dumps(result, indent=2))
        else:
            print(f"❌ {result['message']}")
    elif args.budget_plan:
        budget_msg = f" (Budget: ${args.max_budget:.2f})" if args.max_budget else ""
        print(f"Budget meal plan for: {', '.join(args.budget_plan)}{budget_msg}")
        results = client.budget_meal_plan(args.budget_plan, args.max_budget)
        
        # Print summary
        summary = results['summary']
        print(f"\n📊 Budget Summary:")
        print(f"   Items found: {summary['items_found']}/{summary['total_items']}")
        print(f"   Estimated total: ${summary['estimated_total']:.2f}")
        if summary['budget']:
            status = "✓ Within budget" if summary['within_budget'] else "❌ Over budget"
            print(f"   Budget: ${summary['budget']:.2f} - {status}")
            if summary['within_budget']:
                print(f"   Remaining: ${summary['budget_remaining']:.2f}")
        if summary['items_missing']:
            print(f"   Missing: {', '.join(summary['items_missing'])}")
        
        print("\n📝 Detailed Results:")
        print(json.dumps(results, indent=2))
    elif args.recommend_recipes:
        print("🍳 Getting recipe recommendations based on current sales...")
        results = client.recommend_recipes_from_sales()
        if 'error' in results:
            print(f"❌ {results['error']}")
        else:
            print(f"\n📊 Analysis of {results['total_sale_items']} sale items")
            print(f"Categories on sale: {', '.join(results['categories_on_sale'])}")
            print(f"\n💡 {len(results['recommended_recipes'])} Recipe Recommendations:\n")
            for i, recipe in enumerate(results['recommended_recipes'][:10], 1):
                print(f"{i}. {recipe['recipe_name']}")
                print(f"   Sale items: {', '.join(recipe['sale_ingredients_available'][:3])}")
                print(f"   Also need: {', '.join(recipe['additional_ingredients_needed'][:3])}\n")
    elif args.build_shopping_list:
        if not args.recipe_name:
            print("❌ Error: --recipe-name is required with --build-shopping-list")
            sys.exit(1)
        print(f"🛒 Building shopping list for: {args.recipe_name} ({args.servings} servings)")
        result = client.build_shopping_list_for_recipe(args.recipe_name, args.build_shopping_list, args.servings)
        if 'error' in result:
            print(f"❌ {result['error']}")
        else:
            print(f"\n💵 Total cost: ${result['total_cost']:.2f} (${result['cost_per_serving']:.2f}/serving)")
            if result['items_on_sale']:
                print(f"💰 Items on sale: {', '.join(result['items_on_sale'])}")
            print("\n📝 Shopping list:")
            for item in result['shopping_list']:
                if item['found']:
                    sale_tag = " 🏷️  ON SALE" if item['ingredient'] in result['items_on_sale'] else ""
                    print(f"  ✓ {item['ingredient']}: ${item['price']:.2f}{sale_tag}")
                else:
                    print(f"  ❌ {item['ingredient']}: Not found")
    elif args.weekly_meal_plan:
        budget_msg = f" (${args.budget_per_day:.2f}/day)" if args.budget_per_day else ""
        print(f"📅 Generating {args.days}-day meal plan{budget_msg}...")
        result = client.get_weekly_meal_plan(args.days, args.budget_per_day)
        if 'error' in result:
            print(f"❌ {result['error']}")
        else:
            print(f"\n💵 Estimated total: ${result['estimated_total_cost']:.2f}")
            if result['total_budget']:
                print(f"Budget remaining: ${result['budget_remaining']:.2f}")
            print(f"\n🍽️  {result['days_planned']}-Day Meal Plan:\n")
            for meal in result['meal_plan']:
                print(f"Day {meal['day']}: {meal['recipe']}")
                print(f"  Sale items: {', '.join(meal['sale_ingredients'][:2])}")
                print(f"  Also need: {', '.join(meal['additional_needed'][:3])}")
                print(f"  Cost: ~${meal['estimated_cost']:.2f}\n")
    elif args.search_product:
        print(f"Searching for product: {args.search_product}")
        products = client.search_products(args.search_product)
        if products:
            print(f"\nFound {len(products)} products:")
            print(json.dumps(products, indent=2))
        else:
            print("No products found")
    elif args.find_ingredients:
        print(f"Finding ingredients for recipe: {', '.join(args.find_ingredients)}")
        results = client.find_recipe_ingredients(args.find_ingredients)
        print("\nRecipe Ingredient Availability:")
        print(json.dumps(results, indent=2))
    elif args.explore:
        print(f"Exploring Safeway API ({args.endpoint})...")
        results = client.explore_api(args.endpoint)
        print(json.dumps(results, indent=2))
    else:
        # Default: load all offers
        new_offers = client.load_all_offers()
        if new_offers == 0:
            print("No new offers to add")
        else:
            print(f"Successfully added {new_offers} new offers!")


if __name__ == '__main__':
    main()
