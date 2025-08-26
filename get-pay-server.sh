#!/bin/bash

echo "=== Setting up Stripe pay-server for Toolshed MCP ==="
echo

# Create stripe directory if it doesn't exist
echo "1. Creating ~/stripe directory..."
mkdir -p ~/stripe
cd ~/stripe

echo "2. Checking for existing pay-server..."
if [ -d "pay-server" ]; then
    echo "✅ pay-server directory exists"
    cd pay-server
    echo "Updating repository..."
    git pull origin main 2>/dev/null || echo "⚠️  Could not update - check git access"
else
    echo "❌ pay-server directory not found"
    echo
    echo "You need to clone the pay-server repository:"
    echo "  cd ~/stripe"
    echo "  git clone <internal-pay-server-git-url> pay-server"
    echo
    echo "Contact your team for the correct git URL for pay-server"
    exit 1
fi

echo
echo "3. Checking for toolshed shim script..."
SHIM_PATH="$HOME/stripe/pay-server/.cursor/toolshed_stdio_shim.sh"

if [ -f "$SHIM_PATH" ]; then
    echo "✅ Toolshed shim found at: $SHIM_PATH"
    
    # Make it executable
    chmod +x "$SHIM_PATH"
    echo "✅ Made shim executable"
    
    echo
    echo "4. Testing shim script..."
    if "$SHIM_PATH" --help 2>/dev/null | head -5; then
        echo "✅ Shim script responds to --help"
    else
        echo "⚠️  Shim script may need network access"
    fi
    
else
    echo "❌ Toolshed shim NOT found at: $SHIM_PATH"
    echo
    echo "Expected location: ~/.cursor/toolshed_stdio_shim.sh"
    echo "Please check:"
    echo "  1. Repository is up to date"
    echo "  2. .cursor directory exists in pay-server"
    echo "  3. You have the correct branch checked out"
    exit 1
fi

echo
echo "5. Current MCP Configuration:"
cat ~/.cursor/mcp.json 2>/dev/null || echo "❌ No MCP config found at ~/.cursor/mcp.json"

echo
echo "=== Setup Complete! ==="
echo
echo "Next steps:"
echo "1. Restart Cursor to pick up the MCP configuration"
echo "2. Test with: npx @modelcontextprotocol/inspector $SHIM_PATH cursor"
echo "3. Look for toolshed tools in Claude's MCP interface"
echo
echo "If you need SAIL specifically, you may need to modify the args in mcp.json:"
echo '  "args": ["cursor,sail"]'


