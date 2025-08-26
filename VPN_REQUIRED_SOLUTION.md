# ⚠️ VPN Required: Cannot Clone pay-server Repository

## Current Status: BLOCKED on Network Access

### What's Happening:
- ✅ SSH key exists: `~/.ssh/id_rsa_swanson@stripe.com`
- ✅ SSH config is correct for git.corp.stripe.com:22222
- ✅ MCP configuration is properly set up in `~/.cursor/mcp.json`
- ❌ **Cannot connect to git.corp.stripe.com:22222** (times out)

### Root Cause: VPN Access Required 🔑
The SSH connection to `git.corp.stripe.com` port 22222 is timing out, which indicates you need to be connected to **Stripe's VPN** to access the internal git server.

## Immediate Actions Required:

### 1. Connect to Stripe VPN
- **This is the blocking issue** - you must be on Stripe's internal network
- Connect to your corporate VPN client
- Verify VPN connection is active

### 2. Add SSH Key (After VPN Connection)
```bash
ssh-add ~/.ssh/id_rsa_swanson@stripe.com
# Enter your SSH key passphrase when prompted
```

### 3. Clone Repository (After VPN + SSH Key)
```bash
cd ~/stripe
git clone org-631@git.corp.stripe.com:stripe-internal/pay-server.git
```

### 4. Verify Setup
```bash
cd ~/dash2
./get-pay-server.sh
```

### 5. Restart Cursor
- Quit Cursor completely
- Restart it to pick up the new MCP configuration
- SAIL tool should now be available in Claude

## Alternative: Manual Setup (If Git Clone Still Fails)

If you continue having git access issues after VPN connection:

1. **Contact #toolshed-help** for alternative access to the shim script
2. **Ask a colleague** to share the `toolshed_stdio_shim.sh` file
3. **Manual download** from internal Stripe systems

The file you need is:
```
~/stripe/pay-server/.cursor/toolshed_stdio_shim.sh
```

## Current MCP Configuration (Ready to Use)
Your `~/.cursor/mcp.json` is already correctly configured:
```json
{
  "mcpServers": {
    "toolshed-local": {
      "command": "~/stripe/pay-server/.cursor/toolshed_stdio_shim.sh",
      "args": ["cursor"]
    }
  }
}
```

## Expected Timeline:
- **5 minutes**: Connect to VPN + add SSH key + clone repo
- **2 minutes**: Run verification script  
- **1 minute**: Restart Cursor
- **TOTAL: ~8 minutes** to have SAIL working

## Next Steps:
1. **Connect to Stripe VPN** (blocking issue)
2. **Try the clone again** after VPN connection
3. **Contact #toolshed-help** if git access issues persist

**Bottom Line**: Everything is set up correctly - you just need VPN access to complete the final step! 🚀

