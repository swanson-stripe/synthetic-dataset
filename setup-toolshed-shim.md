# Setting Up Toolshed MCP with Local Shim

Based on the internal Stripe documentation, you need to use a **local shim script** instead of connecting directly via HTTP.

## Step 1: Set Up pay-server Repository

You need to clone/set up the stripe/pay-server repository to get the toolshed shim script.

```bash
# Navigate to your stripe directory (create if needed)
mkdir -p ~/stripe
cd ~/stripe

# Clone the pay-server repository
# (Replace with the actual internal git URL for pay-server)
git clone <pay-server-git-url> pay-server

# OR if you already have access, navigate to the existing repo
cd pay-server
git pull origin main
```

## Step 2: Verify Shim Script Exists

After setting up pay-server, check for the shim:

```bash
ls -la ~/stripe/pay-server/.cursor/toolshed_stdio_shim.sh
```

The script should be at: `/Users/swanson/stripe/pay-server/.cursor/toolshed_stdio_shim.sh`

## Step 3: Update MCP Configuration

Your `~/.cursor/mcp.json` should use this configuration:

```json
{
  "mcpServers": {
    "Figma": {
      "url": "http://127.0.0.1:3845/mcp",
      "headers": {
        "Accept": "application/json, text/event-stream"
      }
    },
    "toolshed-local": {
      "command": "~/stripe/pay-server/.cursor/toolshed_stdio_shim.sh",
      "args": ["cursor"]
    }
  }
}
```

## Step 4: Test the Connection

After setup, test with MCP Inspector:

```bash
npx @modelcontextprotocol/inspector ~/stripe/pay-server/.cursor/toolshed_stdio_shim.sh cursor
```

## Step 5: Add SAIL Tool Access

To specifically access the SAIL tool, you might need to modify the args:

```json
"args": ["cursor,sail"]
```

Or whatever config string enables SAIL access.

## Alternative: Remote Dev Setup

If you're using Cursor in remote dev mode (v0.50+), use this config instead:

```json
"toolshed-remote": {
  "command": "/pay/src/pay-server/.cursor/toolshed_stdio_shim.sh",
  "args": ["cursor"]
}
```

## Troubleshooting

1. **Script not found**: Ensure pay-server repo is properly cloned
2. **Permission denied**: Make the shim script executable: `chmod +x ~/stripe/pay-server/.cursor/toolshed_stdio_shim.sh`
3. **Connection issues**: The shim handles network/VPN requirements automatically
4. **Wrong tools available**: Adjust the config string in args to enable specific toolsets

## Next Steps

1. Set up pay-server repository
2. Verify shim script exists
3. Update MCP configuration to use shim
4. Restart Cursor
5. Test SAIL tool access


