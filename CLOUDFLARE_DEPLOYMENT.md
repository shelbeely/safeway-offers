# 🌐 Cloudflare Deployment Guide

**Deploy PantryPilot to the cloud - always available, zero maintenance**

Run your AI grocery assistant on Cloudflare Workers for global availability and automatic scaling.

## ✨ Why Cloudflare?

- **Always Available** - No need to keep your computer running
- **Global Speed** - Cloudflare's edge network = fast anywhere
- **Free Tier** - 100,000 requests/day at no cost
- **Secure** - Encrypted credentials, enterprise-grade security
- **Zero Maintenance** - Automatic scaling and updates

## Architecture

```
Claude/AI Assistant
    ↓ (HTTP requests)
Cloudflare Worker (your-worker.workers.dev)
    ↓ (API calls)
Safeway API
    ↓
Your Store Data
```

## 📋 What You Need

### For Humans

1. **Cloudflare Account** (free) - [Sign up here](https://cloudflare.com)
2. **Node.js 18+** - [Download here](https://nodejs.org)
3. **Your Safeway Credentials**
   - Email address
   - Password
   - Store ID ([find yours](https://www.safeway.com/shop/store-locator.html))

### For AI Agents / LLMs

<details>
<summary><h3>Pre-Deployment Discovery</h3></summary>

**Step 0: Check Prerequisites**

```bash
# Check Node.js version
node --version
# Required: v18.0.0 or higher

# Check npm
npm --version

# Check if Cloudflare CLI installed
wrangler --version || echo "Wrangler not installed"
```

**Step 1: Gather Required Information**

Ask user for:
- Cloudflare account email (for authentication)
- Safeway username (email)
- Safeway password
- Safeway store ID

**Step 2: Verify Cloudflare Account**

```bash
# Login to Cloudflare
wrangler login
# Opens browser for OAuth authentication

# Verify authentication
wrangler whoami
```

Expected output:
```
 ⛅️ wrangler 3.50.0
-------------------
Getting User settings...
👋 You are logged in with an OAuth Token, associated with the email 'user@example.com'!
```

</details>

## 🚀 Quick Start (5 Minutes)

### For Humans

**Step 1: Install Wrangler CLI**

```bash
npm install -g wrangler
```

**Step 2: Clone & Setup**

```bash
cd /path/to/pantrypilot
npm install
```

**Step 3: Login to Cloudflare**

```bash
wrangler login
```

A browser window opens - click "Allow" to authenticate.

**Step 4: Get Your Account ID**

1. Visit [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Click "Workers & Pages"
3. Copy your Account ID from the right sidebar
4. Edit `wrangler.toml` and replace `YOUR_ACCOUNT_ID`

**Step 5: Set Your Credentials**

```bash
wrangler secret put SAFEWAY_USERNAME
# Type your Safeway email, press Enter

wrangler secret put SAFEWAY_PASSWORD
# Type your Safeway password, press Enter

wrangler secret put SAFEWAY_STORE_ID
# Type your store ID (e.g., 2948), press Enter
```

**Step 6: Deploy!**

```bash
wrangler deploy
```

Done! Your worker is live at `https://safeway-mcp-server.YOUR_ACCOUNT.workers.dev`

### For AI Agents / LLMs

<details>
<summary><h3>Automated Deployment Sequence</h3></summary>

**Step 1: Install Dependencies**

```bash
# Navigate to project directory
cd /path/to/pantrypilot

# Install Wrangler globally
npm install -g wrangler

# Install project dependencies
npm install
```

**Step 2: Authenticate with Cloudflare**

```bash
# Login (opens browser)
wrangler login

# Verify login
wrangler whoami
```

**Step 3: Get Account ID**

```bash
# Option 1: From API
wrangler whoami | grep "Account ID" || echo "Parse account ID from dashboard"

# Option 2: Instruct user
# Ask: "Please provide your Cloudflare Account ID from the dashboard"
```

**Step 4: Update Configuration**

```bash
# Backup original config
cp wrangler.toml wrangler.toml.backup

# Update account_id
# If user provided account_id as ABC123:
sed -i 's/YOUR_ACCOUNT_ID/ABC123/' wrangler.toml

# Verify change
grep "account_id" wrangler.toml
```

**Step 5: Set Secrets**

```bash
# Set credentials non-interactively
echo "SAFEWAY_USERNAME" | wrangler secret put SAFEWAY_USERNAME <<< "user@example.com"
echo "SAFEWAY_PASSWORD" | wrangler secret put SAFEWAY_PASSWORD <<< "password123"
echo "SAFEWAY_STORE_ID" | wrangler secret put SAFEWAY_STORE_ID <<< "2948"

# Note: In practice, use interactive mode or pipe from secure source
```

**Step 6: Deploy**

```bash
# Deploy to Cloudflare
wrangler deploy

# Capture output
# Expected: "Published safeway-mcp-server (X.XX sec)"
# Worker URL: https://safeway-mcp-server.ACCOUNT.workers.dev
```

**Step 7: Verify Deployment**

```bash
# Test health endpoint
curl https://safeway-mcp-server.ACCOUNT.workers.dev/health

# Expected output:
# {"status":"ok","service":"safeway-mcp-server","version":"1.0.0"}
```

**Error Handling:**

- If authentication fails: Run `wrangler login` again
- If account_id missing: Ask user for Account ID from dashboard
- If secrets fail: Use interactive `wrangler secret put` with user input
- If deployment fails: Check wrangler.toml syntax with `wrangler validate`

</details>

## ✅ Testing Your Deployment

### For Humans

**Quick Test - Health Check**

```bash
curl https://safeway-mcp-server.YOUR_ACCOUNT.workers.dev/health
```

You should see:
```json
{
  "status": "ok",
  "service": "safeway-mcp-server",
  "version": "1.0.0"
}
```

**See What's Available**

Visit your worker URL in a browser: `https://safeway-mcp-server.YOUR_ACCOUNT.workers.dev`

You'll see a nice HTML page listing all available tools.

**Try Loading Offers**

```bash
curl -X POST https://safeway-mcp-server.YOUR_ACCOUNT.workers.dev/mcp/invoke \
  -H "Content-Type: application/json" \
  -d '{"tool":"safeway_get_offers","arguments":{}}'
```

### For AI Agents / LLMs

<details>
<summary><h3>Automated Testing Sequence</h3></summary>

**Test 1: Health Check**

```bash
# Test health endpoint
HEALTH_RESPONSE=$(curl -s https://safeway-mcp-server.ACCOUNT.workers.dev/health)
echo "$HEALTH_RESPONSE"

# Verify response contains "ok"
if echo "$HEALTH_RESPONSE" | grep -q "ok"; then
  echo "✓ Health check passed"
else
  echo "✗ Health check failed"
  exit 1
fi
```

**Test 2: List Tools**

```bash
# Get available tools
TOOLS_RESPONSE=$(curl -s https://safeway-mcp-server.ACCOUNT.workers.dev/mcp/tools)
echo "$TOOLS_RESPONSE"

# Verify tools list is not empty
if echo "$TOOLS_RESPONSE" | grep -q "safeway_get_offers"; then
  echo "✓ Tools endpoint working"
else
  echo "✗ Tools endpoint failed"
  exit 1
fi
```

**Test 3: Invoke Tool**

```bash
# Test offer retrieval
INVOKE_RESPONSE=$(curl -s -X POST \
  https://safeway-mcp-server.ACCOUNT.workers.dev/mcp/invoke \
  -H "Content-Type: application/json" \
  -d '{"tool":"safeway_check_api_status","arguments":{}}')

echo "$INVOKE_RESPONSE"

# Check for successful response
if echo "$INVOKE_RESPONSE" | grep -q "operational"; then
  echo "✓ Tool invocation working"
else
  echo "✗ Tool invocation failed"
  exit 1
fi
```

**Complete Test Script**

```bash
#!/bin/bash
WORKER_URL="https://safeway-mcp-server.ACCOUNT.workers.dev"

echo "Testing Cloudflare Worker deployment..."

# Test 1: Health
echo "Test 1: Health check..."
curl -s "$WORKER_URL/health" | grep -q "ok" && echo "✓ Pass" || echo "✗ Fail"

# Test 2: Tools list
echo "Test 2: Tools endpoint..."
curl -s "$WORKER_URL/mcp/tools" | grep -q "safeway_get_offers" && echo "✓ Pass" || echo "✗ Fail"

# Test 3: Tool invocation
echo "Test 3: Tool invocation..."
curl -s -X POST "$WORKER_URL/mcp/invoke" \
  -H "Content-Type: application/json" \
  -d '{"tool":"safeway_check_api_status","arguments":{}}' \
  | grep -q "operational" && echo "✓ Pass" || echo "✗ Fail"

echo "Testing complete!"
```

</details>

## 💬 Using with Claude Desktop

### For Humans

You have two options for connecting Claude to your Cloudflare Worker:

**Option 1: HTTP Bridge (Simple)**

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "safeway-cloud": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-http",
        "https://safeway-mcp-server.YOUR_ACCOUNT.workers.dev"
      ]
    }
  }
}
```

Replace `YOUR_ACCOUNT` with your actual Cloudflare account name.

**Option 2: Keep Local Python (Hybrid)**

Keep using `safeway_mcp_server.py` locally - it's already perfect for MCP! The Cloudflare Worker is best for HTTP API access or sharing with others.

**Which Should I Use?**

- **Local Python MCP Server** → Best for personal use, fastest, most private
- **Cloudflare Worker** → Best for sharing, always-available, multi-device

### For AI Agents / LLMs

<details>
<summary><h3>Claude Desktop Configuration Steps</h3></summary>

**Step 1: Locate Config File**

```bash
# macOS
CONFIG_FILE="$HOME/Library/Application Support/Claude/claude_desktop_config.json"

# Windows
CONFIG_FILE="%APPDATA%/Claude/claude_desktop_config.json"

# Linux
CONFIG_FILE="$HOME/.config/Claude/claude_desktop_config.json"

# Check if file exists
if [ -f "$CONFIG_FILE" ]; then
  echo "Config file found"
else
  echo "Config file not found - will create"
  mkdir -p "$(dirname "$CONFIG_FILE")"
  echo "{}" > "$CONFIG_FILE"
fi
```

**Step 2: Backup Existing Config**

```bash
# Create backup
cp "$CONFIG_FILE" "$CONFIG_FILE.backup"
```

**Step 3: Add Worker Configuration**

```bash
# Read existing config
EXISTING_CONFIG=$(cat "$CONFIG_FILE")

# Add safeway-cloud server (preserving existing servers)
# Use jq if available, otherwise manual JSON manipulation
if command -v jq &> /dev/null; then
  echo "$EXISTING_CONFIG" | jq '.mcpServers["safeway-cloud"] = {
    "command": "npx",
    "args": [
      "@modelcontextprotocol/server-http",
      "https://safeway-mcp-server.ACCOUNT.workers.dev"
    ]
  }' > "$CONFIG_FILE"
else
  # Manual JSON addition (ask user to edit manually)
  echo "Please add this to your Claude config:"
  cat << EOF
{
  "mcpServers": {
    "safeway-cloud": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-http",
        "https://safeway-mcp-server.YOUR_ACCOUNT.workers.dev"
      ]
    }
  }
}
EOF
fi
```

**Step 4: Restart Claude**

```bash
# macOS
killall Claude 2>/dev/null || true
open -a Claude

# Windows
taskkill /IM Claude.exe /F 2>NUL || echo "Claude not running"
start Claude

# Linux
pkill -f claude 2>/dev/null || true
claude &
```

**Step 5: Verify Connection**

Instruct user to:
1. Open Claude Desktop
2. Type: "What Safeway offers are available?"
3. Verify Claude uses the `safeway-cloud` MCP server

</details>

## Development Workflow

### Local Development

Test your worker locally before deploying:

```bash
wrangler dev
```

This starts a local server at `http://localhost:8787`

Test locally:
```bash
curl http://localhost:8787/health
```

### View Logs

```bash
wrangler tail
```

This streams real-time logs from your deployed worker.

### Update Worker

After making code changes:

```bash
wrangler deploy
```

## Custom Domain (Optional)

### Add Custom Domain

1. Go to Cloudflare Dashboard
2. Select your worker
3. Settings → Triggers → Custom Domains
4. Add your domain: `api.yourdomain.com`

Update `wrangler.toml`:
```toml
routes = [
  { pattern = "api.yourdomain.com/*", zone_name = "yourdomain.com" }
]
```

Deploy:
```bash
wrangler deploy
```

## Advanced Configuration

### Enable Caching (Optional)

Add KV namespace for caching offers:

```bash
# Create KV namespace
wrangler kv:namespace create "SAFEWAY_CACHE"

# Get namespace ID and add to wrangler.toml
[[kv_namespaces]]
binding = "SAFEWAY_CACHE"
id = "your-kv-namespace-id"
```

### Rate Limiting

Cloudflare Workers includes built-in rate limiting. Configure in dashboard or via Wrangler:

```toml
[env.production]
vars = { RATE_LIMIT = "100" }  # requests per minute
```

### Monitoring

Enable analytics in Cloudflare Dashboard:
- Workers & Pages → Your Worker → Metrics
- View requests, errors, CPU time

## Security Best Practices

### Secrets Management

✅ **DO:**
- Store credentials as Wrangler secrets
- Use `wrangler secret put` command
- Never commit secrets to git

❌ **DON'T:**
- Put credentials in `wrangler.toml`
- Commit `.env` files
- Hardcode passwords in code

### Access Control

Consider adding authentication to your worker:

```javascript
// In worker.js
async function authenticate(request) {
  const apiKey = request.headers.get('X-API-Key');
  return apiKey === env.API_KEY;
}
```

Set API key:
```bash
wrangler secret put API_KEY
```

### CORS Configuration

Restrict CORS to specific origins:

```javascript
const corsHeaders = {
  'Access-Control-Allow-Origin': 'https://yourdomain.com',
  // ... other headers
};
```

## Troubleshooting

### Authentication Fails

```
Error: Failed to authenticate with Safeway API
```

**Solution:**
- Verify secrets are set: `wrangler secret list`
- Check credentials are correct
- Try logging into Safeway website with same credentials

### Worker Deployment Fails

```
Error: No account_id found
```

**Solution:**
- Set `account_id` in `wrangler.toml`
- Run `wrangler whoami` to verify authentication

### Timeout Errors

```
Error: Script exceeded time limit
```

**Solution:**
- Cloudflare Workers have 50ms CPU time limit (free tier)
- Consider upgrading to paid plan for 50ms+ CPU time
- Optimize code to reduce processing time

### Module Not Found

```
Error: Cannot find module 'mcp'
```

**Solution:**
- Run `npm install` in project directory
- Verify `package.json` includes all dependencies

## Cost Estimation

### Free Tier

- **Requests:** 100,000/day
- **CPU Time:** 10ms per request
- **Perfect for:** Personal use, testing

### Paid Plan ($5/month)

- **Requests:** 10 million/month
- **CPU Time:** 50ms per request
- **Perfect for:** Multiple users, production use

### Typical Usage

- **Loading offers daily:** ~10 requests/day
- **Recipe planning:** ~50 requests/week
- **Heavy usage:** ~500 requests/month

**Recommendation:** Start with free tier

## Migration from Local to Cloudflare

If you're currently using the local Python MCP server:

### Step 1: Test Cloudflare Worker

Deploy and test worker doesn't affect your local setup.

### Step 2: Update Claude Desktop Config

Change from:
```json
{
  "mcpServers": {
    "safeway": {
      "command": "python3",
      "args": ["/path/to/safeway_mcp_server.py"]
    }
  }
}
```

To:
```json
{
  "mcpServers": {
    "safeway": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-http",
        "https://safeway-mcp-server.YOUR_ACCOUNT.workers.dev"
      ]
    }
  }
}
```

### Step 3: Restart Claude

Close and reopen Claude Desktop to load new config.

### Step 4: Test

Ask Claude: "What Safeway offers are available?"

## Hybrid Deployment

Run both local and cloud versions:

```json
{
  "mcpServers": {
    "safeway-local": {
      "command": "python3",
      "args": ["/path/to/safeway_mcp_server.py"]
    },
    "safeway-cloud": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-http",
        "https://safeway-mcp-server.YOUR_ACCOUNT.workers.dev"
      ]
    }
  }
}
```

Claude can use either depending on context.

## Comparison: Local vs Cloudflare

| Feature | Local Python | Cloudflare Workers |
|---------|--------------|-------------------|
| Setup | Medium | Medium |
| Cost | Free | Free (100k req/day) |
| Always Available | No (must run) | Yes |
| Latency | Lowest | Low |
| Maintenance | Manual updates | Auto-scaling |
| Privacy | Stays local | In Cloudflare |
| Best For | Power users | Always-on access |

## Support

### Resources

- [Wrangler Docs](https://developers.cloudflare.com/workers/wrangler/)
- [Workers Docs](https://developers.cloudflare.com/workers/)
- [GitHub Issues](https://github.com/shelbeely/pantrypilot/issues)

### Common Questions

**Q: Can I use both local and Cloudflare?**  
A: Yes! Configure both in Claude Desktop.

**Q: Are my credentials secure?**  
A: Yes, Cloudflare encrypts secrets at rest and in transit.

**Q: What happens if I hit the free tier limit?**  
A: Requests will return 429 errors. Upgrade to paid plan or wait for reset.

**Q: Can I self-host instead?**  
A: Yes, the worker code works on any platform supporting Service Workers.

## Next Steps

1. ✅ Deploy your worker
2. ✅ Test all endpoints
3. ✅ Update Claude Desktop config
4. ✅ Try some recipes!

---

**Made with 🛒 for cloud-first grocery automation**
