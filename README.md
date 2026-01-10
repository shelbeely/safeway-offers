# Safeway Offers

Safeway is a major US supermarket chain that offer a free members card.
Members can use the Safeway app or site to load offers (either personal offers based on your shopping history, or generic manufacturer coupons).
These offers are only applied if they are "loaded" into your member account.

This utility will use the Safeway mobile api's to get all offers, and load them all into your account.
This way you will not lose any money saving offers.

You can schedule this to run every week to load the new offers

## 🆕 Choose Your Version

This project is available in two versions:

### 🐍 Python Version (Recommended for Web Developers)
**New!** Full rewrite in Python with web interface and AI integration.

- ✅ Python-based for easier understanding
- ✅ Flask web interface
- ✅ Model Context Protocol (MCP) server for Claude and other AI assistants  
- ✅ GitHub Actions support for automation
- ✅ Enhanced API exploration

👉 **[See Python Documentation](README_PYTHON.md)**

### 🔧 Go Version (Original)
Original command-line tool written in Go.

- ✅ Fast and lightweight
- ✅ Single binary deployment
- ✅ Cross-platform (Windows, macOS, Linux)

👉 Continue reading below for Go version instructions

## API Status (Updated January 2026)

**The Safeway API appears to still be operational as of 2026**, though it's an unofficial/undocumented API used by the Safeway mobile app. The API endpoints (`nimbus.safeway.com` and `albertsons.okta.com`) continue to function, but note:

- ⚠️ This is an **unofficial API** - Safeway/Albertsons may change or discontinue it at any time
- The authentication system uses Okta OAuth 2.0, which receives regular updates
- If the tool stops working, the API may have changed

📋 **For detailed information about the API status, see [API_STATUS.md](API_STATUS.md)**

---

## Go Version Usage (Original)

### Checking API Status

Before using the tool, you can verify if the API endpoints are accessible:

**Windows:**
```
safeway-offers.exe -check-api
```

**macOS/Linux:**
```
./safeway-offers -check-api
```

This will test connectivity to all required API endpoints without requiring your credentials.

## Usage
##### Windows
- Run `cmd.exe`
- `cd` to the folder containing `safeway-offers.exe`
- Run `safeway-offers.exe -u "<SAFEWAY_USERNAME>" -p "<SAFEWAY_PASSWORD>" -id "<SAFEWAY-SHOP-ID>`
##### macOS or Linux
- Open your Terminal
- `cd` to the folder containing `safeway-offers`
- `chmod +x safeway-offers` to make it executable
- Run `./safeway-offers -u "<SAFEWAY_USERNAME>" -p "<SAFEWAY_PASSWORD>" -id "<SAFEWAY-STORE-ID>` 


## Finding your Safeway Store ID
- Go to https://local.safeway.com/safeway.html
- Find your local store
- Hover over the "weekly Ad" link, the link will appear at the bottom, and be something like
`https://www.safeway.com/set-store.html?storeId=2948&target=weeklyad` 
- The store id is the 4 digits that comes after `storeId=`

## Building
- Install and setup latest Go
- Get the module and its dependencies: `go get -u github.com/giwty/safeway-offers`
- Build it for the OS you need, and make sure to choose `amd64` architecture:
    - `env GOOS=target-OS GOARCH=amd64 go build github.com/giwty/safeway-offers`
    - `target-OS` can be `windows`, `darwin` (mac OS), `linux`, or any other (check the Go documentation for a complete list).

## Troubleshooting

### The tool isn't working anymore

1. **Check API Status First**: Run `./safeway-offers -check-api` to verify the endpoints are accessible
2. **Verify Credentials**: Make sure your Safeway username and password are correct
3. **Check Safeway App**: Try logging into the official Safeway mobile app. If that works but this tool doesn't, the API may have changed
4. **API Changes**: Safeway/Albertsons may have updated their API. Check for:
   - New authentication methods
   - Different API endpoints
   - Updated OAuth client IDs/secrets
   
### Common Issues

- **"401 Unauthorized"**: Your credentials may be incorrect, or the OAuth tokens may have expired
- **"Cannot resolve host"**: Network connectivity issue or the API domain has changed
- **"Non 200 response"**: The API structure may have changed, or there's a temporary service issue

### Finding Updated API Information

If the API has changed, you may need to:
1. Use a proxy tool (like Charles Proxy or mitmproxy) to inspect the Safeway mobile app's network traffic
2. Look for updated OAuth endpoints and client credentials
3. Check the community for other tools that may have been updated

For more information on reverse engineering private APIs, see: https://blog.jonlu.ca/posts/safeway

