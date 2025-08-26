# 🚨 SSH Connection Hanging - VPN Issue

## Current Status:
- ✅ **DNS resolution works** (ping git.corp.stripe.com succeeds)
- ✅ **SSH key is configured** properly
- ❌ **SSH connection times out** (cannot reach port 22222)
- ❌ **Cannot reach internal.stripe.com**

## Root Cause: VPN Connection Issue 🔑

You have VPN tunnel interfaces (`utun0-utun5`) but cannot reach Stripe internal services. This suggests:

1. **VPN client is running** but not properly connected
2. **VPN is connected** but routing isn't working correctly
3. **Wrong VPN profile** or authentication issue

## Troubleshooting Steps:

### 1. Check VPN Client Status
Look at your VPN client (likely Cisco AnyConnect, GlobalProtect, or similar):
- Is it showing "Connected"?
- What's the connection status?
- Try disconnecting and reconnecting

### 2. Test VPN Connectivity
```bash
# Test internal Stripe services
curl -s --connect-timeout 5 --max-time 10 https://internal.stripe.com
curl -s --connect-timeout 5 --max-time 10 https://go.stripe.com

# Test git server specifically  
nc -z git.corp.stripe.com 22222
```

### 3. Try Different VPN Approaches
- **Disconnect/Reconnect VPN**
- **Try different VPN server** if available
- **Check VPN credentials** are correct

### 4. Alternative Git Access Methods
If VPN continues to fail, try:

**HTTPS Clone (might work without SSH):**
```bash
cd ~/stripe
git clone https://git.corp.stripe.com/stripe-internal/pay-server.git
```

**Ask colleague for shim file:**
- Contact #toolshed-help 
- Ask someone to share the `toolshed_stdio_shim.sh` file directly

## Immediate Next Steps:

1. **Check your VPN client status**
2. **Try disconnecting/reconnecting VPN**
3. **Test again:** `timeout 10 ssh -T org-631@git.corp.stripe.com`
4. **If still failing:** Try HTTPS clone or contact #toolshed-help

## Expected Timeline:
- **2-5 minutes**: Fix VPN connection
- **1 minute**: SSH test + git clone
- **TOTAL**: Should be working within 5-10 minutes

Let me know your VPN client status and we'll get this resolved! 🚀

