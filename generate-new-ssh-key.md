# Generate New SSH Key with Passphrase

## Step 1: Generate New SSH Key
```bash
ssh-keygen -t rsa -b 4096 -C "swanson@stripe.com" -f ~/.ssh/id_rsa_swanson_new
```

**What this does:**
- `-t rsa`: Use RSA algorithm
- `-b 4096`: 4096-bit key size (secure)
- `-C "swanson@stripe.com"`: Comment with your email
- `-f ~/.ssh/id_rsa_swanson_new`: Specific filename (won't overwrite existing key)

**Expected prompts:**
1. **"Enter passphrase (empty for no passphrase):"** → Enter a strong passphrase
2. **"Enter same passphrase again:"** → Confirm the passphrase

## Step 2: Verify New Key was Created
```bash
ls -la ~/.ssh/id_rsa_swanson_new*
```
**Expected:** Should show two files:
- `id_rsa_swanson_new` (private key)
- `id_rsa_swanson_new.pub` (public key)

## Step 3: Display Public Key for Stripe Git Registration
```bash
cat ~/.ssh/id_rsa_swanson_new.pub
```
**Copy the entire output** - you'll need to add this to your Stripe git account

## Step 4: Add New Key to SSH Agent
```bash
ssh-add ~/.ssh/id_rsa_swanson_new
```
**Enter your new passphrase when prompted**

## Step 5: Update SSH Config to Use New Key for Stripe Git
```bash
cp ~/.ssh/config ~/.ssh/config.backup
```

Then edit the config:
```bash
nano ~/.ssh/config
```

**Find this section:**
```
Host git.corp.stripe.com
    Port 22222
    user git
```

**Change it to:**
```
Host git.corp.stripe.com
    Port 22222
    user git
    IdentityFile ~/.ssh/id_rsa_swanson_new
```

**Save and exit:** Ctrl+X, then Y, then Enter

## Step 6: Test SSH Connection
```bash
ssh -T org-631@git.corp.stripe.com
```
**Expected:** Should prompt for passphrase, then connect successfully

## Step 7: Clone Repository with New Key
```bash
cd ~/stripe
git clone org-631@git.corp.stripe.com:stripe-internal/pay-server.git
```

---

## Alternative: Add Passphrase to Existing Key

If you prefer to add a passphrase to your existing key instead:

```bash
ssh-keygen -p -f ~/.ssh/id_rsa_swanson@stripe.com
```

**Prompts:**
1. **"Enter old passphrase:"** → Press Enter (if no current passphrase)
2. **"Enter new passphrase:"** → Enter your new passphrase
3. **"Enter same passphrase again:"** → Confirm

Then add to agent:
```bash
ssh-add ~/.ssh/id_rsa_swanson@stripe.com
```

---

## Quick Commands Summary:

### For New Key:
```bash
# Generate new key
ssh-keygen -t rsa -b 4096 -C "swanson@stripe.com" -f ~/.ssh/id_rsa_swanson_new

# Show public key (copy this to Stripe git)
cat ~/.ssh/id_rsa_swanson_new.pub

# Add to SSH agent
ssh-add ~/.ssh/id_rsa_swanson_new

# Test connection
ssh -T org-631@git.corp.stripe.com
```

### For Adding Passphrase to Existing Key:
```bash
# Add passphrase to existing key
ssh-keygen -p -f ~/.ssh/id_rsa_swanson@stripe.com

# Add to SSH agent
ssh-add ~/.ssh/id_rsa_swanson@stripe.com
```

**Choose the approach you prefer and let me know when you're ready for the next step!**

