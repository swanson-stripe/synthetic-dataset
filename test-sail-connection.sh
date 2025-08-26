#!/bin/bash

echo "=== Testing SAIL MCP Tool Connection ==="
echo

# Test 1: Basic connectivity
echo "1. Testing basic connectivity to toolshed.corp.stripe.com..."
if ping -c 3 toolshed.corp.stripe.com >/dev/null 2>&1; then
    echo "✅ DNS resolution successful"
else
    echo "❌ DNS resolution failed - check your network/VPN connection"
    exit 1
fi

# Test 2: HTTPS connectivity
echo
echo "2. Testing HTTPS connectivity..."
if curl -k --connect-timeout 10 --max-time 20 -s -I https://toolshed.corp.stripe.com >/dev/null 2>&1; then
    echo "✅ HTTPS connection successful"
else
    echo "❌ HTTPS connection failed - you may need to connect to Stripe VPN"
    echo "Error details:"
    curl -k --connect-timeout 10 --max-time 20 -v https://toolshed.corp.stripe.com 2>&1 | head -20
fi

# Test 3: Try different SAIL endpoints
echo
echo "3. Testing SAIL MCP endpoints..."
ENDPOINTS=(
    "https://toolshed.corp.stripe.com/mcp/sail"
    "https://toolshed.corp.stripe.com/mcp/sail/"
    "https://toolshed.corp.stripe.com/mcp/sail/sse"
    "https://toolshed.corp.stripe.com/mcp/sail/health"
)

for endpoint in "${ENDPOINTS[@]}"; do
    echo "Testing: $endpoint"
    response=$(curl -k --connect-timeout 10 --max-time 20 -s -w "%{http_code}" -o /dev/null "$endpoint" 2>/dev/null)
    if [ "$response" = "000" ]; then
        echo "  ❌ Connection failed"
    elif [ "$response" = "200" ]; then
        echo "  ✅ Success (HTTP $response)"
    elif [ "$response" = "404" ]; then
        echo "  ⚠️  Endpoint not found (HTTP $response)"
    else
        echo "  ⚠️  Response code: $response"
    fi
done

# Test 4: MCP Inspector connection
echo
echo "4. Testing MCP Inspector connection..."
echo "Attempting to connect to SAIL with MCP Inspector..."

# Try different transport methods
TRANSPORTS=("http" "sse")
for transport in "${TRANSPORTS[@]}"; do
    echo "Testing with $transport transport..."
    timeout 15 npx @modelcontextprotocol/inspector \
        --transport "$transport" \
        --server-url "https://toolshed.corp.stripe.com/mcp/sail" \
        2>&1 | head -10 &
    
    sleep 3
    pkill -f "inspector" 2>/dev/null
done

echo
echo "=== Connection Test Complete ==="
echo
echo "Next steps:"
echo "1. If DNS/HTTPS tests failed: Connect to Stripe VPN"
echo "2. If endpoints return 404: The SAIL tool might be at a different path"
echo "3. If connections time out: Contact Stripe IT about SAIL MCP access"
echo "4. Try running: npx @modelcontextprotocol/inspector --cli"
echo "   Then manually configure the connection in the web interface"


