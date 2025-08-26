#!/bin/bash

echo "=== MCP Configuration Debug ==="
echo

echo "1. Checking current MCP configuration..."
echo "MCP config file: ~/.cursor/mcp.json"
cat ~/.cursor/mcp.json
echo

echo "2. Testing toolshed connection with different approaches..."

# Test 1: Direct URL access
echo "Testing direct URL access:"
curl -v --connect-timeout 10 --max-time 15 \
  -H "Accept: application/json, text/event-stream" \
  https://toolshed.corp.stripe.com/mcp/sail 2>&1 | head -20

echo
echo "3. Testing with MCP Inspector..."

# Test different URL patterns for SAIL
URLS=(
  "https://toolshed.corp.stripe.com/mcp/sail"
  "https://toolshed.corp.stripe.com/sail/mcp"
  "https://toolshed.corp.stripe.com/api/mcp/sail"
)

for url in "${URLS[@]}"; do
  echo "Testing URL: $url"
  timeout 10 npx @modelcontextprotocol/inspector \
    --transport http \
    --server-url "$url" \
    2>&1 | head -5
  echo "---"
done

echo
echo "4. Checking Stripe authentication..."
echo "Looking for Stripe credentials..."

# Check for common Stripe auth locations
AUTH_LOCATIONS=(
  "~/.stripe/config"
  "~/.config/stripe"
  "$HOME/.stripe"
  "$HOME/stripe/.env"
)

for location in "${AUTH_LOCATIONS[@]}"; do
  expanded_path=$(eval echo "$location")
  if [ -f "$expanded_path" ] || [ -d "$expanded_path" ]; then
    echo "Found: $expanded_path"
    if [ -f "$expanded_path" ]; then
      echo "  File contents (redacted):"
      grep -v "secret\|key\|token\|password" "$expanded_path" 2>/dev/null | head -5 || echo "  (Unable to read safely)"
    fi
  fi
done

echo
echo "5. Network and VPN check..."
echo "Checking if you're on Stripe network..."

# Test Stripe internal endpoints
if curl -s --connect-timeout 5 --max-time 10 internal.stripe.com >/dev/null 2>&1; then
  echo "✅ Connected to Stripe internal network"
else
  echo "❌ Not connected to Stripe internal network - VPN required"
fi

echo
echo "=== Recommended Actions ==="
echo "1. Ensure you're connected to Stripe VPN"
echo "2. Try restarting Cursor after MCP config changes"
echo "3. Check if SAIL tool requires special authentication"
echo "4. Contact #toolshed-help for SAIL MCP setup assistance"


