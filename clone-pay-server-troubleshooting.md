# Cloning pay-server Repository - Troubleshooting

## Current Issue
The git clone is failing with SSH timeout on port 22222:
```
ssh: connect to host git.corp.stripe.com port 22222: Operation timed out
```

## Diagnosis
- ✅ DNS resolution works (git.corp.stripe.com resolves)
- ✅ Basic connectivity works (ping succeeds) 
- ❌ SSH on port 22222 times out

## Solutions to Try

### 1. Connect to Stripe VPN 🔑 (Most Likely Fix)
The SSH port 22222 timeout suggests you need to be on Stripe's internal network.

**Action**: Connect to Stripe VPN and try again:
```bash
cd ~/stripe
git clone https://git.corp.stripe.com/stripe-internal/pay-server
```

### 2. Check SSH Key Setup
Verify your SSH keys are set up for Stripe's git server:

```bash
# Check if you have SSH keys
ls -la ~/.ssh/

# Test SSH connection (after VPN)
ssh -T git.corp.stripe.com -p 22222

# Expected response: something like "Hi username! You've successfully authenticated..."
```

### 3. Try HTTPS Instead of SSH
If SSH continues to fail, try HTTPS:
```bash
cd ~/stripe
git clone https://git.corp.stripe.com/stripe-internal/pay-server.git
```

### 4. Alternative: Manual Download
If git clone fails entirely, you might need to:
1. Access the repository via web browser
2. Download as ZIP
3. Extract to ~/stripe/pay-server

## After Successful Clone

Once you have the repository, run:
```bash
cd ~/dash2
./get-pay-server.sh
```

This will verify the toolshed shim is in place and working.

## Expected File Structure
After successful clone, you should have:
```
~/stripe/pay-server/.cursor/toolshed_stdio_shim.sh
```

## Next Steps
1. **Connect to Stripe VPN**
2. **Try the git clone again**
3. **Run the verification script**
4. **Restart Cursor**
5. **SAIL tool should be available!**

## If Still Having Issues
- Contact your Stripe IT team about git.corp.stripe.com access
- Ask in #toolshed-help about alternative ways to get the shim script
- Verify your SSH keys are registered with Stripe's git server


