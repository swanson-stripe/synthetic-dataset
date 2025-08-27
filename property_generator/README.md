# PropertyFlow Property Management Platform - Synthetic Data Generator

Generate realistic Stripe payment data for a property management platform with rent collection, security deposits, maintenance, and landlord payouts.

## 🏠 Business Model

PropertyFlow simulates a comprehensive property management platform that:
- **Manages properties** for multiple landlords
- **Collects rent** from tenants using ACH, cards, and wire transfers
- **Handles security deposits** in Treasury escrow accounts
- **Processes maintenance** requests with vendor payments
- **Distributes net income** to landlords after fees

## 🏗️ Platform Features

### Core Operations
- **Multi-landlord management**: Individual and company landlord accounts
- **Automated rent collection**: ACH debits (70%), cards (25%), wire (5%)
- **Late payment handling**: $50 flat late fees, NSF charges
- **Security deposit escrow**: Treasury accounts with refund processing
- **Maintenance coordination**: Vendor payments with markup to tenants
- **Financial reporting**: Net income calculations and payouts

### Stripe Products Used
- **Connect**: Landlord onboarding and net income payouts
- **Treasury**: Security deposit escrow management
- **ACH Debits**: Primary rent collection method (70% of volume)
- **Financial Connections**: Tenant bank verification
- **Invoicing**: Maintenance and utility billing
- **Issuing**: Maintenance contractor payment cards

## 📊 Generated Data Structure

### Core Entities
- **Landlords**: 40 Connect accounts (individuals and companies)
- **Properties**: 126 rental properties with tenant details
- **Rent Payments**: 1,988 monthly rent collections with outcomes
- **Security Deposits**: Treasury escrow accounts with refunds
- **Maintenance**: Vendor payments and tenant charges
- **Payouts**: Net income transfers to landlords

### Lifecycle Stages (24 months)
1. **Early (Months 1-8)**: 50 properties, 10 landlords, 15% late rate
2. **Growth (Months 9-16)**: 500 properties, 100 landlords, 8% late rate  
3. **Mature (Months 17-24)**: 5,000 properties, 1,000 landlords, 4% late rate

## 💰 Financial Patterns

### Revenue Streams
- **Management Fees**: 8% of collected rent
- **Late Fees**: $50 flat fee for late payments
- **NSF Fees**: $35 for bounced payments
- **Maintenance Markup**: 10% on tenant-charged repairs

### Payment Outcomes
- **On-time**: 85% of payments (varies by credit score)
- **Late**: 12% with additional fees
- **NSF**: 3% failed payments requiring retry

## 🔧 Maintenance Management

### Issue Types & Frequency
- **HVAC**: 20% of requests, $300-$2,000 cost
- **Plumbing**: 15% of requests, $150-$800 cost
- **Electrical**: 10% of requests, $200-$1,200 cost
- **Cleaning**: 25% of requests, $50-$300 cost
- **Damage Repair**: 10% of requests, $200-$1,500 cost

### Cost Allocation
- **Landlord-paid**: Normal wear and maintenance
- **Tenant-charged**: Damage and tenant-caused issues (20% of cases)

## 📁 Output Files

### Core Data
- `landlords.json` - Landlord Connect accounts with portfolio details
- `properties.json` - Property listings with tenant information
- `rent_payments.json` - Monthly rent collection transactions
- `security_deposits.json` - Escrow accounts and refund processing

### Operations Data  
- `maintenance_payments.json` - Vendor payments and tenant charges
- `landlord_payouts.json` - Net income transfers after fees
- `late_payments.json` - Late fee and penalty transactions
- `property_metrics.json` - Platform performance analytics

## 🚀 Usage

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Generate data
python generate_propertyflow.py
```

### Sample Metrics Output
```
📊 GENERATION SUMMARY:
   Total properties: 126
   Active landlords: 40
   Occupancy rate: 100.0%
   Rent payments processed: 1,988

💰 FINANCIAL METRICS:
   Total rent collected: $579,549,400.00
   Collection rate: 98.3%
   Late payment rate: 4.2%
   NSF rate: 1.7%
   Average rent: $294,396.03

🔧 OPERATIONS METRICS:
   Maintenance costs: $9,856,500.00
   Security deposits held: $37,093,900.00
   Total landlord payouts: $523,328,948.00
   Management fee revenue: $46,363,952.00
```

## 🏢 Property Types

- **Apartments**: 40% of portfolio, $1,200-$3,500 rent
- **Houses**: 30% of portfolio, $1,800-$5,000 rent  
- **Condos**: 20% of portfolio, $1,500-$4,000 rent
- **Townhouses**: 10% of portfolio, $1,600-$4,500 rent

## 📈 Key Metrics Tracked

### Financial Performance
- **Collection Rate**: Percentage of successful rent payments
- **Late Payment Rate**: Percentage of payments with late fees
- **NSF Rate**: Percentage of failed payment attempts
- **Management Fee Revenue**: Platform income from 8% fee

### Operational Efficiency
- **Occupancy Rate**: Percentage of occupied properties
- **Maintenance Requests**: Average requests per property
- **Landlord Retention**: Properties managed per landlord
- **Security Deposit Management**: Escrow and refund processing

## 🎯 Use Cases

### Product Development
- **Payment flow optimization**: Test ACH vs card collection rates
- **Late payment prevention**: Analyze patterns and interventions
- **Maintenance coordination**: Vendor payment and tenant charging
- **Financial reporting**: Landlord dashboard and analytics

### Data Analysis
- **Collection performance**: Payment success by method and timing
- **Tenant behavior**: Credit score correlation with payment patterns
- **Property performance**: Rent collection by property type
- **Platform growth**: Landlord acquisition and retention metrics

## ⚡ Performance

- **Generation Time**: ~0.2 seconds
- **Data Volume**: 1,988 rent payments across 126 properties
- **Memory Usage**: Optimized for large property portfolios
- **File Sizes**: JSON outputs range from 50KB to 2MB

## 🔒 Data Privacy

All generated data is synthetic and contains no real PII:
- Fake addresses using Faker library
- Generated email addresses and phone numbers  
- Simulated bank account and payment details
- Synthetic tenant and landlord profiles

Perfect for prototyping property management platforms without privacy concerns.
