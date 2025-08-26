# TechStyle Synthetic Stripe Payment Data Generator

A comprehensive Python script that generates realistic Stripe payment data for an e-commerce fashion retailer called "TechStyle". This tool creates synthetic payment data across a 24-month business lifecycle with proper Stripe API structure.

## 🎯 Overview

This generator simulates the payment evolution of a fashion e-commerce business across three distinct phases:

- **Early Stage (Months 1-8)**: 50-200 orders/month, USD only, 4.5% failure rate
- **Growth Stage (Months 9-16)**: 500-2000 orders/month, USD/EUR/GBP, 2.5% failure rate  
- **Mature Stage (Months 17-24)**: 5000-15000 orders/month, 10+ currencies, 1.75% failure rate

## 📋 Features

### Complete Stripe API Structure
- Properly formatted Stripe IDs (`pi_`, `cus_`, `ch_`, `pm_`)
- Full payment intent objects with nested charge data
- Customer profiles with realistic demographics
- Payment method details and metadata
- Dispute records for failed payments

### Realistic Business Logic
- Lifecycle-based growth patterns
- Currency expansion over time
- Seasonal variations in order volume
- Product category distribution (clothing, shoes, accessories)
- Payment method preferences (cards, digital wallets)

### Comprehensive Output
- Raw payment data in Stripe format
- Customer profiles and metadata
- Pre-calculated daily/monthly metrics
- Chart-ready visualization data
- Summary statistics and KPIs

## 🚀 Quick Start

### Prerequisites

```bash
Python 3.7+
pip (Python package manager)
```

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/swanson-stripe/synthetic-dataset.git
cd synthetic-dataset/techstyle_generator
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the generator:**
```bash
python generate_techstyle.py
```

## 📊 Generated Data Structure

### Payment Intent Object
```json
{
  "id": "pi_1ABC123def456GHI789jkl012",
  "object": "payment_intent",
  "amount": 5999,
  "currency": "usd",
  "status": "succeeded",
  "customer": "cus_ABC123def456",
  "created": 1704067200,
  "description": "Order #ORD-123456",
  "payment_method": "pm_1ABC123def456GHI",
  "payment_method_types": ["card"],
  "charges": {
    "data": [{
      "id": "ch_1ABC123def456GHI789",
      "amount": 5999,
      "currency": "usd",
      "paid": true,
      "refunded": false,
      "disputed": false,
      "failure_code": null,
      "payment_method_details": {
        "type": "card",
        "card": {
          "brand": "visa",
          "last4": "4242",
          "exp_month": 12,
          "exp_year": 2025
        }
      }
    }]
  },
  "metadata": {
    "order_id": "ORD-123456",
    "product_category": "womens_clothing",
    "lifecycle_stage": "growth"
  }
}
```

### Customer Object
```json
{
  "id": "cus_ABC123def456",
  "object": "customer",
  "email": "customer@example.com",
  "name": "Jane Doe",
  "phone": "+1-555-123-4567",
  "address": {
    "line1": "123 Fashion St",
    "city": "New York",
    "state": "NY",
    "postal_code": "10001",
    "country": "US"
  },
  "metadata": {
    "customer_number": "1001",
    "acquisition_channel": "social",
    "preferred_category": "womens_clothing"
  }
}
```

## 📁 Output Files

The script generates the following files in the `/output/` directory:

| File | Description |
|------|-------------|
| `payments_raw.json` | Complete payment intent records (~150k records) |
| `customers.json` | Customer profiles and demographics |
| `daily_metrics.json` | Day-by-day aggregated metrics |
| `chart_data.json` | Visualization-ready data formats |
| `summary_stats.json` | High-level KPIs and statistics |
| `disputes.json` | Dispute records (if any generated) |

## 🔧 Configuration

### Product Categories
The generator includes realistic product categories for a fashion retailer:

- **Women's Clothing**: $25-150, 30% of orders
- **Men's Clothing**: $30-120, 25% of orders  
- **Shoes**: $40-250, 20% of orders
- **Accessories**: $15-80, 15% of orders
- **Outerwear**: $80-350, 10% of orders

### Supported Currencies
- **Early Stage**: USD only
- **Growth Stage**: USD, EUR, GBP
- **Mature Stage**: USD, EUR, GBP, CAD, AUD, JPY, CHF, SEK, NOK, DKK

### Payment Methods
- **Card**: 85% (Visa, Mastercard, Amex, Discover)
- **Apple Pay**: 8%
- **Google Pay**: 5%
- **PayPal**: 2%

## 📈 Sample Metrics

After generation, you'll see output like:

```
📊 TECHSTYLE DATA GENERATION SUMMARY
============================================================
Generated 146,234 payments
Success rate: 97.23%
Average order value: $89.45
Total volume: $13,078,456.78
Date range: 2022-01-15 to 2024-01-15
Unique customers: 98,567
Disputes generated: 487

Currency distribution:
  USD: 89,234 payments
  EUR: 32,145 payments
  GBP: 24,855 payments
  ...

⏱️  Execution time: 18.3 seconds
✅ TechStyle data generation complete!
```

## 🎛️ Customization

### Modify Lifecycle Stages
Edit the `LIFECYCLE_STAGES` configuration to adjust:
- Monthly order volumes
- Currency availability
- Failure and dispute rates
- Timeline duration

### Adjust Product Mix
Update `PRODUCT_CATEGORIES` to change:
- Price ranges
- Category weights
- Product names

### Currency Support
Modify `CURRENCY_RATES` to add new currencies or update exchange rates.

## 🔍 Data Validation

The generator includes built-in validation:
- Stripe ID format compliance
- Currency amount conversion accuracy
- Timestamp consistency
- Status logic validation
- Metadata completeness

## 🛠️ Technical Details

### Performance
- Generates ~150,000 records in under 30 seconds
- Memory efficient batch processing
- Optimized pandas operations for metrics

### Dependencies
- `faker`: Realistic fake data generation
- `pandas`: Data manipulation and analysis
- `numpy`: Numerical operations

### Reproducibility
- Fixed random seeds for consistent output
- Deterministic generation patterns
- Version-controlled dependencies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is for educational and testing purposes. Generated data is synthetic and should not be used for actual payment processing.

## 🆘 Support

For questions or issues:
1. Check the generated `summary_stats.json` for data validation
2. Review console output for error messages
3. Ensure all dependencies are properly installed
4. Verify Python version compatibility (3.7+)

---

**Generated with ❤️ for realistic payment data testing**
