# 🚀 Quick Start - Get Synthetic Data Instantly

## Zero-Setup Data Access

### Option 1: Direct Download (No Installation)
```bash
# TechStyle e-commerce payments
curl -o payments.json https://raw.githubusercontent.com/swanson-stripe/synthetic-dataset/main/pre_generated_data/techstyle/payments.json

# EduTech education marketplace students  
curl -o students.json https://raw.githubusercontent.com/swanson-stripe/synthetic-dataset/main/pre_generated_data/edutech/students.json

# Download complete dataset
wget -r --no-parent https://raw.githubusercontent.com/swanson-stripe/synthetic-dataset/main/pre_generated_data/techstyle/
```

### Option 2: CLI Tool (Recommended)
```bash
# One-time setup
git clone https://github.com/swanson-stripe/synthetic-dataset.git
cd synthetic-dataset

# Get any dataset instantly
./tools/get-data.sh techstyle
./tools/get-data.sh edutech ./my-project/data/

# Explore available options  
./tools/get-data.sh --help
./tools/get-data.sh --list-files techstyle
```

### Option 3: Generate Fresh Data
```bash
# For full-scale custom data generation
cd techstyle_generator
pip install -r requirements.txt
python generate_techstyle.py  # Generates 150K+ payments
```

## 📊 Available Datasets

| Dataset | Business Model | Sample Size | Full Scale | Description |
|---------|---------------|-------------|------------|-------------|
| **techstyle** | E-commerce | 1K payments | 150K payments | Fashion retailer with global currencies |
| **edutech** | Marketplace | 500 students | 73K students | Education platform with instructor payouts |

**More datasets coming soon**: PropertyFlow, CreatorHub, FitStream, RideShare+, MedSupply, GiveHope

## 🎯 What You Get

### Realistic Data Patterns
- **Lifecycle Growth**: Early → Growth → Mature stages
- **Seasonal Trends**: Holiday spikes, summer slumps
- **Payment Methods**: Cards, ACH, wire transfers, digital wallets
- **Global Markets**: Multiple currencies and regions
- **Business Metrics**: Revenue, churn, LTV, conversion rates

### Stripe Product Coverage
- **Payment Intents**: Complete payment flow simulation
- **Connect**: Marketplace and platform integrations
- **Billing**: Subscription and recurring payment patterns
- **Capital**: Business financing and lending
- **Issuing**: Virtual cards and spending controls
- **Treasury**: Money movement and financial accounts

## 💡 Use Cases

### Prototyping
```bash
# Get sample data and start building
./tools/get-data.sh techstyle ./prototype/data/
# Your prototype now has 1K realistic payments!
```

### Demo Preparation
```bash
# Download specific business model for your demo
./tools/get-data.sh edutech
# Perfect for showing education marketplace features
```

### Testing & Development
```bash
# Generate fresh data with different parameters
cd edutech_generator && python generate_edutech.py
# Creates 73K students, 218 courses, $201M in transactions
```

## 🔄 Auto-Updated Data

Pre-generated datasets are automatically refreshed monthly via GitHub Actions:
- ✅ Latest generator algorithms  
- ✅ Fresh synthetic data patterns
- ✅ Updated business metrics
- ✅ Always under 100MB for fast downloads

## 🛠️ Developer Experience

### Instant Access Patterns
```bash
# JavaScript/Node.js
fetch('https://raw.githubusercontent.com/swanson-stripe/synthetic-dataset/main/pre_generated_data/techstyle/payments.json')

# Python
import requests
data = requests.get('https://raw.githubusercontent.com/swanson-stripe/synthetic-dataset/main/pre_generated_data/techstyle/payments.json').json()

# Command Line
curl -s https://raw.githubusercontent.com/swanson-stripe/synthetic-dataset/main/pre_generated_data/techstyle/payments.json | jq '.[0]'
```

### CLI Features
- 🎯 **Smart Downloads**: Only fetches files you need
- 📊 **Dataset Metadata**: Manifests with business context
- 🎨 **Pretty Output**: Colored progress and summaries
- 🔍 **File Exploration**: List available files before downloading
- 📁 **Custom Directories**: Download anywhere you want

## 🚀 Start Prototyping in 30 Seconds

```bash
# 1. Get the data
curl -o payments.json https://raw.githubusercontent.com/swanson-stripe/synthetic-dataset/main/pre_generated_data/techstyle/payments.json

# 2. Explore it  
head payments.json

# 3. Build your prototype!
# You now have 1,000 realistic Stripe payments to work with
```

Perfect for hackathons, demos, prototypes, and development! 🎉
