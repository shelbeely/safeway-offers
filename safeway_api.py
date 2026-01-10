#!/usr/bin/env python3
"""
Safeway Offers API Client
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
    
    parser = argparse.ArgumentParser(description='Safeway Offers API Client')
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
    
    if args.explore:
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
