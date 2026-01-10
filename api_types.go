package main

// Additional Safeway API endpoints discovered through research
const (
	// Product endpoints
	safewayProductSearchUrl = "https://nimbus.safeway.com/emmd/service/product/search?storeId="
	safewayProductDetailsUrl = "https://nimbus.safeway.com/emmd/service/product/details?storeId="
	
	// Store endpoints
	safewayStoreDetailsUrl = "https://nimbus.safeway.com/emmd/service/store/details?storeId="
	safewayStoreSearchUrl = "https://nimbus.safeway.com/emmd/service/store/search?"
	
	// Account/User endpoints
	safewayAccountDetailsUrl = "https://nimbus.safeway.com/emmd/service/account/details"
	safewayOrderHistoryUrl = "https://nimbus.safeway.com/emmd/service/order/history"
	
	// Cart/Shopping endpoints
	safewayCartUrl = "https://nimbus.safeway.com/emmd/service/cart/details?storeId="
	
	// Weekly ad and sales
	safewayWeeklyAdUrl = "https://nimbus.safeway.com/emmd/service/weeklyad?storeId="
)

// ProductSearchResult represents product search results
type ProductSearchResult struct {
	Products []Product `json:"products"`
}

// Product represents a Safeway product
type Product struct {
	ProductID   string  `json:"productId"`
	Name        string  `json:"name"`
	Description string  `json:"description"`
	Brand       string  `json:"brand"`
	Price       float64 `json:"price"`
	SalePrice   float64 `json:"salePrice"`
	Category    string  `json:"category"`
	ImageURL    string  `json:"imageUrl"`
	InStock     bool    `json:"inStock"`
}

// StoreDetails represents store information
type StoreDetails struct {
	StoreID   string   `json:"storeId"`
	Name      string   `json:"name"`
	Address   Address  `json:"address"`
	Phone     string   `json:"phone"`
	Hours     []string `json:"hours"`
	Services  []string `json:"services"`
}

// Address represents a physical address
type Address struct {
	Street  string `json:"street"`
	City    string `json:"city"`
	State   string `json:"state"`
	ZipCode string `json:"zipCode"`
}

// AccountDetails represents user account information
type AccountDetails struct {
	UserID    string `json:"userId"`
	Email     string `json:"email"`
	FirstName string `json:"firstName"`
	LastName  string `json:"lastName"`
	Phone     string `json:"phone"`
}

// OrderHistory represents past orders
type OrderHistory struct {
	Orders []Order `json:"orders"`
}

// Order represents a single order
type Order struct {
	OrderID   string    `json:"orderId"`
	OrderDate string    `json:"orderDate"`
	Total     float64   `json:"total"`
	Status    string    `json:"status"`
	Items     []Product `json:"items"`
}

// Cart represents the shopping cart
type Cart struct {
	CartID string    `json:"cartId"`
	Items  []Product `json:"items"`
	Total  float64   `json:"total"`
}

// WeeklyAd represents weekly ad items
type WeeklyAd struct {
	WeekStart string    `json:"weekStart"`
	WeekEnd   string    `json:"weekEnd"`
	Items     []Product `json:"items"`
}
