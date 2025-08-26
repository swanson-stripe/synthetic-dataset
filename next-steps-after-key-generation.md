# Next Steps After SSH Key Generation ✅

## Your New SSH Key Info:
- **Private key**: `/Users/swanson/.ssh/id_rsa_swanson_new`
- **Public key**: `/Users/swanson/.ssh/id_rsa_swanson_new.pub`
- **Fingerprint**: `SHA256:P6xeNuFATap8N851U/GxXvKwiyBfG5yDXdihcUPmdoM`

## Step 1: Register Public Key with Stripe Git 🔑

**You need to add this public key to your Stripe Git account:**

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC0igZeRM2KIW2e6PUJlEuuYY1cAdV7B0zqDOaWjCB1gUWf08eGgAL0kbWn+bE7uFNMdDD2Q0f85vpMS20oT1Pp80WUd7HZKWRh398uHzCKvHhsjtZh9P/HkZQkW1flFR+koY5uPgC64Uv8ZgvmatqcgwwmN+XxGTzvFO7kwhDVmbDmhIgICMRWI/n/CyhwGBmh26XJB6K0an7Yb9KVsirmjfidOrKrt0eTgpKcSXcTqvc/uCIh+dmSJORmnMqtJduZGVSXtq1Ke5q/WzHfMO58VyCEbcjWITIPgKBtDgv7cnrirVyvxHMmHBP+NvMR1wur/T7uFk+NyB6kZjcfJlvMiki9g1wpoxRiKKi1IeV0XVLuAm1oKxEQSoynR416oTCyrvMGi1XZsEAJIB385XrefrZG656sDNqpv4vpxbcL7V3jdylv1kJFeImbO1gKmBrycupHhJw/U3Vfq3Utm99RkfMzWmNzHZYa2JTmhX1qgMl7wRGNLjLKag5aWY0MMuMkJp/8nqQQgaigtgaXHnCjAuwfppIvSJ81xjfxXV+FuDf6lSvK1mVhfctMxraKonp06P8A2JC32Gad0G8p7Upa2imqoSQaWb2rwFYt3opTAg5sXdAWW+NdT0CbC1yGnSHxSim1Gsm/bBm6tRtCL1tGFF0X2VwhlFTqBPcTtd1PcQ== swanson@stripe.com
```

**How to add it:**
1. Go to your Stripe Git account settings
2. Find "SSH Keys" or "Deploy Keys" section
3. Click "Add SSH Key"
4. Paste the entire public key above
5. Give it a name like "Laptop - SAIL MCP Access"

## Step 2: Update SSH Config to Use New Key

**Copy the old config as backup:**
```bash
cp ~/.ssh/config ~/.ssh/config.backup
```

**Edit the SSH config:**
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

**Save:** Ctrl+X, then Y, then Enter

## Step 3: Add New Key to SSH Agent
```bash
ssh-add ~/.ssh/id_rsa_swanson_new
```
*Enter your passphrase when prompted*

## Step 4: Test SSH Connection
```bash
ssh -T org-631@git.corp.stripe.com
```
*Should connect successfully after entering passphrase*

## Step 5: Clone Repository
```bash
cd ~/stripe
git clone org-631@git.corp.stripe.com:stripe-internal/pay-server.git
```

**Let me know when you've completed Step 1 (adding the public key to Stripe Git) and we'll continue!**

