package main

import (
	"flag"
	"fmt"
	"net/http"
	"os"
	"time"
)

var checkApi = flag.Bool("check-api", false, "check if Safeway API endpoints are accessible")

// CheckAPIStatus checks if the key API endpoints are accessible
func CheckAPIStatus() {
	fmt.Println("Checking Safeway API endpoint status...")
	fmt.Println("=" + string(make([]byte, 50)))
	
	endpoints := map[string]string{
		"OAuth Token Endpoint":      safewayOauthGetTokenUrl,
		"Manufacturer Coupons API":  safewayManufacturerCouponsUrl + "2948",
		"Personalized Coupons API":  safewayPersonalizedCouponsUrl + "2948",
		"Add Offer API":             safewayAddOfferUrl + "2948",
		"Shopping List API":         safewayShoppingListUrl + "2948",
	}

	allAccessible := true
	httpClient := http.Client{
		Timeout: time.Duration(10) * time.Second,
	}

	for name, url := range endpoints {
		fmt.Printf("\nChecking %s...\n", name)
		fmt.Printf("URL: %s\n", url)
		
		req, err := http.NewRequest("HEAD", url, nil)
		if err != nil {
			fmt.Printf("❌ Error creating request: %v\n", err)
			allAccessible = false
			continue
		}
		
		req.Header.Set("User-Agent", "Safeway/3373 CFNetwork/978.0.7 Darwin/18.6.0")
		
		resp, err := httpClient.Do(req)
		if err != nil {
			fmt.Printf("❌ Not accessible: %v\n", err)
			allAccessible = false
			continue
		}
		resp.Body.Close()
		
		if resp.StatusCode == http.StatusUnauthorized || resp.StatusCode == http.StatusForbidden || 
		   resp.StatusCode == http.StatusOK || resp.StatusCode == http.StatusBadRequest {
			// These status codes indicate the endpoint exists
			fmt.Printf("✓ Endpoint is accessible (Status: %d %s)\n", resp.StatusCode, resp.Status)
		} else if resp.StatusCode == http.StatusNotFound {
			fmt.Printf("❌ Endpoint not found (Status: 404)\n")
			allAccessible = false
		} else {
			fmt.Printf("⚠ Unexpected status: %d %s\n", resp.StatusCode, resp.Status)
		}
	}

	fmt.Println("\n" + string(make([]byte, 50)))
	if allAccessible {
		fmt.Println("✓ All API endpoints appear to be accessible!")
		fmt.Println("\nNote: Authentication is required to use these endpoints.")
		fmt.Println("Run the program with your credentials to test full functionality.")
		os.Exit(0)
	} else {
		fmt.Println("❌ Some API endpoints are not accessible.")
		fmt.Println("\nPossible reasons:")
		fmt.Println("  1. The API may have been deprecated or moved to new URLs")
		fmt.Println("  2. Network connectivity issues")
		fmt.Println("  3. Safeway may have changed their API infrastructure")
		fmt.Println("\nRecommendation: Check the official Safeway mobile app to see if it's working.")
		fmt.Println("If the app works, the API may have changed and this tool needs updating.")
		os.Exit(1)
	}
}
