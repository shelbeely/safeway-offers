/**
 * Safeway API Client for Cloudflare Workers
 * 
 * JavaScript/TypeScript implementation of the Safeway API client
 * that works in Cloudflare Workers environment.
 */

// API Endpoints
export const SafewayEndpoints = {
  OAUTH_TOKEN: 'https://albertsons.okta.com/oauth2/ausp6soxrIyPrm8rS2p6/v1/token',
  MANUFACTURER_COUPONS: 'https://nimbus.safeway.com/emmd/service/gallery/offer/mfg',
  PERSONALIZED_OFFERS: 'https://nimbus.safeway.com/emmd/service/gallery/offer/pd',
  ADD_OFFER: 'https://nimbus.safeway.com/Clipping1/services/clip/items',
  SHOPPING_LIST: 'https://nimbus.safeway.com/emmd/service/mylist/default/details',
  PRODUCT_SEARCH: 'https://nimbus.safeway.com/emmd/service/product/search',
  STORE_DETAILS: 'https://nimbus.safeway.com/emmd/service/store/details',
  ACCOUNT_DETAILS: 'https://nimbus.safeway.com/emmd/service/account/details',
  CART: 'https://nimbus.safeway.com/emmd/service/cart/details',
  WEEKLY_AD: 'https://nimbus.safeway.com/emmd/service/weeklyad',
  ORDER_HISTORY: 'https://nimbus.safeway.com/emmd/service/order/history'
};

// OAuth Credentials
const SAFEWAY_CLIENT_ID = '0oap6kkp7Sefg24rB2p6';
const SAFEWAY_CLIENT_SECRET = '4UpmzD4hlF2VYQqYjDUoamgLu2Bo1OzagpfG7yus';
const USER_AGENT = 'Safeway/3373 CFNetwork/978.0.7 Darwin/18.6.0';

/**
 * Safeway API Client
 */
export class SafewayAPIClient {
  constructor(username, password, storeId) {
    this.username = username;
    this.password = password;
    this.storeId = storeId;
    this.accessToken = null;
  }

  /**
   * Authenticate with Safeway OAuth
   */
  async authenticate() {
    try {
      const auth = btoa(`${SAFEWAY_CLIENT_ID}:${SAFEWAY_CLIENT_SECRET}`);
      
      const response = await fetch(SafewayEndpoints.OAUTH_TOKEN, {
        method: 'POST',
        headers: {
          'Authorization': `Basic ${auth}`,
          'Content-Type': 'application/x-www-form-urlencoded',
          'User-Agent': USER_AGENT
        },
        body: new URLSearchParams({
          'username': this.username,
          'password': this.password,
          'grant_type': 'password',
          'scope': 'openid profile offline_access'
        })
      });

      if (!response.ok) {
        console.error('Authentication failed:', response.status);
        return false;
      }

      const data = await response.json();
      this.accessToken = data.access_token;
      return true;
    } catch (error) {
      console.error('Authentication error:', error);
      return false;
    }
  }

  /**
   * Make authenticated API request
   */
  async makeRequest(url, options = {}) {
    if (!this.accessToken) {
      throw new Error('Not authenticated');
    }

    const response = await fetch(url, {
      ...options,
      headers: {
        'Authorization': `Bearer ${this.accessToken}`,
        'User-Agent': USER_AGENT,
        'Content-Type': 'application/json',
        ...options.headers
      }
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.status}`);
    }

    return response.json();
  }

  /**
   * Get manufacturer coupons
   */
  async getManufacturerCoupons() {
    try {
      const data = await this.makeRequest(
        `${SafewayEndpoints.MANUFACTURER_COUPONS}?storeId=${this.storeId}`
      );
      
      return (data.offers || []).map(offer => ({
        coupon_id: offer.offerId || offer.couponID,
        description: offer.description || offer.name,
        offer_type: offer.offerPgm || 'MF'
      }));
    } catch (error) {
      console.error('Error getting manufacturer coupons:', error);
      return [];
    }
  }

  /**
   * Get personalized offers
   */
  async getPersonalizedOffers() {
    try {
      const data = await this.makeRequest(
        `${SafewayEndpoints.PERSONALIZED_OFFERS}?storeId=${this.storeId}`
      );
      
      return (data.offers || []).map(offer => ({
        offer_id: offer.offerId || offer.offerID,
        name: offer.name || offer.title,
        description: offer.description || '',
        offer_type: offer.offerPgm || 'PD',
        price: offer.price
      }));
    } catch (error) {
      console.error('Error getting personalized offers:', error);
      return [];
    }
  }

  /**
   * Get shopping list
   */
  async getShoppingList() {
    try {
      const data = await this.makeRequest(SafewayEndpoints.SHOPPING_LIST);
      return data.items || [];
    } catch (error) {
      console.error('Error getting shopping list:', error);
      return [];
    }
  }

  /**
   * Load all offers
   */
  async loadAllOffers() {
    const manufacturerCoupons = await this.getManufacturerCoupons();
    const personalizedOffers = await this.getPersonalizedOffers();
    
    let loadedCount = 0;
    
    // Load manufacturer coupons
    for (const coupon of manufacturerCoupons) {
      if (await this.addOffer(coupon.coupon_id, 'MF')) {
        loadedCount++;
      }
    }
    
    // Load personalized offers
    for (const offer of personalizedOffers) {
      if (await this.addOffer(offer.offer_id, 'PD')) {
        loadedCount++;
      }
    }
    
    return loadedCount;
  }

  /**
   * Add offer to account
   */
  async addOffer(offerId, offerType = 'PD') {
    try {
      const response = await fetch(SafewayEndpoints.ADD_OFFER, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.accessToken}`,
          'User-Agent': USER_AGENT,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          items: [{
            clipType: 'C',
            itemId: offerId,
            itemType: offerType
          }]
        })
      });
      
      return response.ok;
    } catch (error) {
      console.error('Error adding offer:', error);
      return false;
    }
  }

  /**
   * Search products
   */
  async searchProducts(query, limit = 20) {
    try {
      const data = await this.makeRequest(
        `${SafewayEndpoints.PRODUCT_SEARCH}?q=${encodeURIComponent(query)}&storeId=${this.storeId}&limit=${limit}`
      );
      
      return (data.products || []).map(product => ({
        id: product.id,
        name: product.name,
        description: product.description,
        price: product.price,
        on_sale: product.onSale || false,
        image: product.imageUrl
      }));
    } catch (error) {
      console.error('Error searching products:', error);
      return [];
    }
  }
}
