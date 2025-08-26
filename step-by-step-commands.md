# Step-by-Step Terminal Commands to Set Up SAIL MCP

## Step 1: Connect to Stripe VPN
**Action:** Use your Stripe VPN client to connect to the corporate network.
- This is required before any of the following commands will work
- Verify you're connected before proceeding

## Step 2: Add Your SSH Key
```bash
ssh-add ~/.ssh/id_rsa_swanson@stripe.com
```
**Expected:** You'll be prompted for your SSH key passphrase. Enter it.

## Step 3: Verify SSH Connection (Optional Test)
```bash
ssh -T org-631@git.corp.stripe.com
```
**Expected:** Should connect successfully (may show git-related message)

## Step 4: Navigate to Stripe Directory and Clone Repository
```bash
cd ~/stripe
git clone org-631@git.corp.stripe.com:stripe-internal/pay-server.git
```
**Expected:** Repository cloning progress, should complete successfully

## Step 5: Verify the Shim Script Exists
```bash
ls -la ~/stripe/pay-server/.cursor/toolshed_stdio_shim.sh
```
**Expected:** Should show the file exists with executable permissions

## Step 6: Make Shim Script Executable (if needed)
```bash
chmod +x ~/stripe/pay-server/.cursor/toolshed_stdio_shim.sh
```

## Step 7: Run Verification Script
```bash
cd ~/dash2
./get-pay-server.sh
```
**Expected:** Should show ✅ checks confirming everything is set up correctly

## Step 8: Check Current MCP Configuration
```bash
cat ~/.cursor/mcp.json
```
**Expected:** Should show toolshed-local configuration pointing to the shim script

## Step 9: Restart Cursor
1. Quit Cursor completely (Cmd+Q on Mac)
2. Wait a few seconds
3. Restart Cursor
4. Open this project

## Step 10: Test SAIL Access
In Cursor, try using Claude and look for SAIL/toolshed tools in the MCP interface.

---

## If Something Goes Wrong:

### If SSH key add fails:
```bash
ssh-agent bash
ssh-add ~/.ssh/id_rsa_swanson@stripe.com
```

### If git clone fails with timeout:
- Double-check VPN connection
- Try: `ping git.corp.stripe.com`

### If shim script doesn't exist:
```bash
find ~/stripe -name "toolshed_stdio_shim.sh" -type f
```

### If MCP doesn't work after restart:
```bash
npx @modelcontextprotocol/inspector ~/stripe/pay-server/.cursor/toolshed_stdio_shim.sh cursor
```

## Quick Copy-Paste Version:
```bash
# Step 2
ssh-add ~/.ssh/id_rsa_swanson@stripe.com

# Step 4
cd ~/stripe && git clone org-631@git.corp.stripe.com:stripe-internal/pay-server.git

# Step 5-6
ls -la ~/stripe/pay-server/.cursor/toolshed_stdio_shim.sh
chmod +x ~/stripe/pay-server/.cursor/toolshed_stdio_shim.sh

# Step 7
cd ~/dash2 && ./get-pay-server.sh
```

