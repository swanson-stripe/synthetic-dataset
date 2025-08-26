# SAIL MCP Tool Setup Guide

## Summary

You're trying to add the SAIL (Stripe Analytics Intelligence Layer) tool as an MCP (Model Context Protocol) server. The tool is hosted at `https://toolshed.corp.stripe.com/mcp/sail`.

## Current Issue: VPN Connection Required

**Problem**: The connection tests show that while DNS resolution works, HTTPS connections are failing with SSL errors. This indicates you need to be connected to Stripe's internal VPN to access the toolshed.corp.stripe.com domain.

## Setup Steps

### 1. Connect to Stripe VPN
- Ensure you're connected to Stripe's corporate VPN
- The error suggests the SSL handshake is failing, which typically indicates network-level access restrictions

### 2. Test Connection After VPN
Run the connection test script:
```bash
./test-sail-connection.sh
```

### 3. Use MCP Inspector for Testing

#### Option A: Web Interface
```bash
npx @modelcontextprotocol/inspector --cli
```
This starts a web interface where you can manually configure the connection.

#### Option B: Direct Connection
Once VPN is working, try:
```bash
npx @modelcontextprotocol/inspector --transport http --server-url https://toolshed.corp.stripe.com/mcp/sail
```

### 4. Alternative Transport Methods
If HTTP doesn't work, try SSE (Server-Sent Events):
```bash
npx @modelcontextprotocol/inspector --transport sse --server-url https://toolshed.corp.stripe.com/mcp/sail/sse
```

## Configuration Files Created

1. **mcp-config.json** - MCP server configuration
2. **test-sail-connection.sh** - Connection diagnostic script

## Debugging Steps

### If still having issues after VPN connection:

1. **Check SAIL endpoints**:
   ```bash
   curl -v https://toolshed.corp.stripe.com/mcp/sail
   curl -v https://toolshed.corp.stripe.com/mcp/sail/health
   ```

2. **Try different paths**:
   - `/mcp/sail`
   - `/mcp/sail/sse` 
   - `/mcp/sail/http`

3. **Check authentication requirements**:
   - The tool might require Stripe authentication headers
   - Look for API key requirements

4. **Contact Stripe IT**:
   - If the above doesn't work, the SAIL MCP tool might not be publicly accessible
   - You may need special permissions or configuration

## Expected Behavior Once Working

When properly connected, the MCP Inspector should:
- Show available tools from SAIL
- Allow you to test tool calls
- Display response schemas

## Integration with Claude

Once the connection is working:
1. The SAIL tool will be available as an MCP server
2. Claude can call SAIL functions for Stripe analytics
3. You can query Stripe data using natural language through SAIL

## Next Steps

1. **Connect to Stripe VPN** ← Most important step
2. Run the test script again
3. Use MCP Inspector to verify connection
4. Test SAIL functionality

## Files Created
- `mcp-config.json` - Configuration for the SAIL MCP server
- `test-sail-connection.sh` - Diagnostic script for troubleshooting
- `SAIL_MCP_Setup_Guide.md` - This guide


