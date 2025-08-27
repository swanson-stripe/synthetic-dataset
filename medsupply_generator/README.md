# MedSupply Pro Synthetic Stripe B2B Data Generator

A comprehensive Python script that generates realistic B2B medical equipment wholesaler data with net payment terms, high-value transactions, purchase order systems, and complete Stripe B2B product integration over a 24-month business lifecycle.

## 🏥 Overview

MedSupply Pro simulates a full-scale B2B medical equipment distribution platform with realistic healthcare industry patterns including:

- **Complex B2B invoicing** with net terms (NET-30, NET-60, NET-90)
- **Purchase order matching** with detailed line items and approval workflows
- **Volume-based pricing** with tiered discount structures
- **Stripe Capital financing** for large equipment purchases
- **ACH/Wire payment processing** optimized for B2B transactions
- **Credit limit management** with aging reports and collections

## 📊 Business Model Simulation

### **Customer Types**
- **Hospitals**: Enterprise clients with $500K credit limits and NET-60 terms
- **Clinics**: Established practices with $100K credit limits and NET-30 terms
- **Laboratories**: Diagnostic facilities with $100K credit limits and NET-30 terms
- **Pharmacies**: Smaller operations with $25K credit limits and NET-30 terms

### **Volume Discount Tiers**
- **$0-$10K**: No discount
- **$10K-$50K**: 5% volume discount
- **$50K-$100K**: 10% volume discount
- **$100K+**: 15% volume discount

### **Product Categories**
- **Surgical Equipment**: $50-$1,500 per unit (Operating tables, anesthesia machines)
- **Diagnostic Equipment**: $100-$5,000 per unit (MRI, CT, ultrasound systems)
- **PPE & Disposables**: $5-$50 per unit (Masks, gloves, protective equipment)
- **Laboratory Supplies**: $20-$800 per unit (Centrifuges, microscopes, analyzers)
- **Medical Furniture**: $10-$250 per unit (Hospital beds, exam tables, carts)

### **Lifecycle Stages**
- **Early (Months 1-8)**: 10 clients, $50K monthly volume, 20% late payments
- **Growth (Months 9-16)**: 100 clients, $1M monthly volume, 10% late payments
- **Mature (Months 17-24)**: 1,000 clients, $10M monthly volume, 5% late payments

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.7+
pip (Python package manager)
```

### Installation
```bash
# Navigate to the generator directory
cd medsupply_generator

# Install dependencies
pip install -r requirements.txt

# Run the generator
python generate_medsupply.py
```

### Expected Output
```
🏥 MedSupply Pro Synthetic B2B Data Generator
✅ Generated 728 clients, 6,264 orders, 101 financing offers
⏱️ Total execution time: 5.0 seconds
```

## 📁 Generated Output Files

All files are saved to the `/b2b_data/` directory:

### **Core B2B Data**
- **`clients.json`** - B2B customer profiles with credit limits, payment terms, and business information
- **`purchase_orders.json`** - Detailed purchase orders with line items, pricing, and approval workflows
- **`invoices.json`** - Stripe invoices with complex line items, volume discounts, and payment terms
- **`payments.json`** - ACH, wire transfer, and card payments with processing fees and timing

### **Financial Management**
- **`financing_offers.json`** - Stripe Capital offers for large equipment purchases
- **`aging_report.json`** - Accounts receivable aging analysis (30/60/90+ days)
- **`b2b_metrics.json`** - Complete B2B analytics including DSO, collection rates, and volume discounts

## 🎯 Key B2B Medical Industry Features

### **Purchase Order System**
- **PO number generation** with month/year tracking
- **Multi-line item orders** with up to 20 products per order
- **Product categorization** across 5 medical equipment categories
- **Volume discount calculations** based on order size
- **Tax exemption handling** for hospitals and non-profits
- **Shipping method selection** (standard, express, white-glove delivery)

### **Payment Terms & Credit Management**
- **Net payment terms** (NET-30: 66.9%, NET-60: 26.2%, NET-90: 6.9%)
- **Credit scoring** (600-850 range) affecting credit limits
- **Credit limit tiers** by customer type (Startup: $25K, Established: $100K, Enterprise: $500K)
- **Late payment tracking** with 1.5% monthly late fees
- **Aging bucket analysis** (Current, 1-30, 31-60, 61-90, 90+ days)

### **B2B Payment Processing**
- **ACH dominance** (62% of payments) with $5 flat fee and 3-day processing
- **Wire transfers** (24% of payments) with $25 fee and 1-day processing
- **Corporate cards** (14% of payments) with 2.9% + $0.30 fee structure
- **Payment timing patterns** based on customer type and business maturity

### **Stripe Capital Integration**
- **Equipment financing** for orders over $50K with qualifying credit scores
- **Risk-based pricing** (6-12% APR based on credit score 700-850)
- **Flexible terms** (12, 24, or 36 months based on order size)
- **55.5% acceptance rate** with realistic approval criteria

## 📈 Generated Metrics

### **Business Overview**
- Total B2B clients: 728
- Purchase orders: 6,264
- Average order value: $17,109
- Collection rate: 100.0%
- Days sales outstanding: 0.0 days

### **Financial Performance**
- Total order value: $107,171,000
- Total revenue: $105,805,619
- Volume discounts: $16,854,055 (15.7% of orders)
- Late payment rate: 1.4%

### **Customer Distribution**
- **Clinics**: 296 clients (40.7%) with avg $76K credit limit
- **Hospitals**: 183 clients (25.1%) with avg $542K credit limit
- **Labs**: 150 clients (20.6%) with avg $95K credit limit
- **Pharmacies**: 99 clients (13.6%) with avg $15K credit limit

### **Payment Analysis**
- **ACH**: 62.0% of payments (preferred B2B method)
- **Wire**: 24.3% of payments (large transactions)
- **Card**: 13.6% of payments (smaller/urgent orders)

### **Financing Metrics**
- Financing offers: 101 (for qualifying large orders)
- Acceptance rate: 55.5%
- Total financing offered: $6,078,145

## 🎨 Data Structure Examples

### **B2B Customer Profile**
```json
{
  "id": "cus_MED789abc123",
  "name": "Chicago Regional Medical Center",
  "metadata": {
    "business_type": "hospital",
    "tax_id": "12-3456789",
    "credit_limit_cents": 50000000,
    "credit_score": 785,
    "payment_terms": "net_60",
    "tax_exempt": true,
    "account_manager": "Sarah Johnson",
    "purchasing_contact": "Dr. Michael Chen",
    "order_frequency_per_month": 2.5,
    "avg_order_size_cents": 15000000
  }
}
```

### **Purchase Order with Line Items**
```json
{
  "po_number": "PO-202312-5678",
  "client_id": "cus_MED789abc123",
  "line_items": [
    {
      "product_code": "MED-SURGICAL-456",
      "description": "Anesthesia Machine",
      "category": "Surgical Equipment",
      "quantity": 2,
      "unit_price_cents": 12500000,
      "line_total_cents": 25000000,
      "warranty_months": 36
    }
  ],
  "subtotal_cents": 25000000,
  "volume_discount_cents": 2500000,
  "volume_discount_rate": 0.10,
  "tax_cents": 0,
  "shipping_cents": 500000,
  "total_cents": 23000000,
  "payment_terms": "net_60"
}
```

### **Complex Invoice with Terms**
```json
{
  "id": "in_MED123def456",
  "customer": "cus_MED789abc123",
  "amount_due": 23000000,
  "due_date": 1704067200,
  "status": "paid",
  "collection_method": "send_invoice",
  "payment_settings": {
    "payment_method_types": ["ach_debit", "wire_transfer", "card"]
  },
  "footer": "NET 60 payment terms. Late payments subject to 1.5% monthly fee.",
  "custom_fields": [
    {"name": "PO Number", "value": "PO-202312-5678"},
    {"name": "Account Manager", "value": "Sarah Johnson"},
    {"name": "Tax ID", "value": "12-3456789"}
  ]
}
```

### **ACH B2B Payment**
```json
{
  "id": "py_ACH789ghi012",
  "amount": 23000000,
  "payment_method": "ach_debit",
  "processing_time_days": 3,
  "fees": {
    "amount": 500,
    "description": "ACH processing fee"
  },
  "metadata": {
    "invoice_id": "in_MED123def456",
    "po_number": "PO-202312-5678",
    "payment_timing": "on_time",
    "late_fee_cents": 0
  }
}
```

### **Stripe Capital Financing Offer**
```json
{
  "id": "cap_OFFER789mno",
  "type": "stripe_capital",
  "amount": 23000000,
  "term_length_months": 24,
  "interest_rate": 0.08,
  "monthly_payment_cents": 1089524,
  "total_repayment": 26148576,
  "status": "accepted",
  "risk_assessment": {
    "credit_score": 785,
    "risk_tier": "low",
    "revenue_verification": "verified"
  }
}
```

## 🔄 Business Use Cases

### **For Product Teams**
- **Net terms optimization**: Test different payment term structures and collection strategies
- **Volume pricing**: Analyze discount tier effectiveness and customer behavior
- **Credit management**: Model credit limit policies and risk assessment
- **Purchase workflow**: Design approval processes and PO matching systems

### **For Developers**
- **B2B invoicing**: Test complex line items, discounts, and tax calculations
- **Payment processing**: Handle ACH, wire, and card payments with different fee structures
- **Capital integration**: Build financing application and approval workflows
- **Aging reports**: Develop collections dashboards and overdue notifications

### **For Data Teams**
- **DSO optimization**: Analyze payment timing and collections effectiveness
- **Customer segmentation**: Build credit scoring and risk assessment models
- **Volume analysis**: Optimize discount tiers and pricing strategies
- **Cash flow forecasting**: Model payment timing and financing impact

## ⚙️ Configuration Options

The script includes comprehensive configuration at the top of the file:

- **Payment terms**: Modify NET-30/60/90 distribution and late payment rates
- **Volume discounts**: Adjust discount tiers and percentage rates
- **Credit limits**: Customize limits by customer type and credit score
- **Product catalog**: Modify medical equipment categories and pricing
- **Lifecycle stages**: Adjust client growth and payment behavior by business phase

## 🔧 Technical Details

### **Performance**
- Generates 728 clients and 6,264 purchase orders in ~5 seconds
- Creates comprehensive B2B transaction data with realistic patterns
- Processes 24 months of business lifecycle with aging analysis
- Outputs detailed B2B analytics with industry-specific metrics

### **Data Quality**
- All Stripe objects match official Invoicing and Capital API structure
- Realistic B2B payment timing based on healthcare industry patterns
- Accurate volume discount calculations and tax exemption handling
- Proper aging analysis with 30/60/90+ day buckets

### **Healthcare Industry Accuracy**
- Customer types: Hospitals (25%), Clinics (41%), Labs (21%), Pharmacies (14%)
- Payment methods: ACH preferred (62%), Wire for large orders (24%), Cards for urgent (14%)
- Credit terms: NET-30 dominant (67%), NET-60 for large customers (26%), NET-90 rare (7%)
- Volume discounts: 15.7% of total order value with realistic tier adoption

## 📄 License

MIT License - Perfect for B2B medical equipment platform prototyping, healthcare marketplace analytics, and complex invoicing system development.

---

**Ready to prototype B2B medical equipment platforms with realistic net terms and volume pricing!** 🏥💊
