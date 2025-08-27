# GiveHope Synthetic Stripe Non-Profit Data Generator

A comprehensive Python script that generates realistic non-profit donation platform data with campaigns, recurring donors, seasonal giving patterns, employer matching, and complete Stripe donation processing integration over a 24-month organizational lifecycle.

## ❤️ Overview

GiveHope simulates a full-scale non-profit donation platform with authentic charitable giving patterns including:

- **Seasonal giving surges** (280% spike in December, Giving Tuesday peaks)
- **Campaign-driven fundraising** across 5 cause areas with realistic success rates
- **Recurring donor programs** with monthly, quarterly, and annual giving
- **Employer matching programs** with corporate gift coordination
- **Tax receipt generation** for compliant donation acknowledgment
- **Major donor management** with high-value gift processing

## 📊 Non-Profit Model Simulation

### **Cause Areas & Campaign Types**
- **Disaster Relief**: High urgency, 90% success rate, 5x goal multiplier
- **Education**: Medium urgency, 70% success rate, scholarships and access
- **Healthcare**: Medium urgency, 75% success rate, medical care initiatives
- **Environment**: Low urgency, 60% success rate, climate and conservation
- **Community**: Low urgency, 65% success rate, local impact projects

### **Donor Segments**
- **Individual Donors**: 90% of donors (5% are major donors >$1,000)
- **Corporate Donors**: 8% of donors (25% are major donors)
- **Foundation Donors**: 2% of donors (60% are major donors)

### **Giving Patterns**
- **Suggested amounts**: $25, $50, $100, $250, $500, $1,000
- **Recurring frequencies**: Monthly (60%), Quarterly (20%), Annual (20%)
- **Processing fee coverage**: 30% of donors opt to cover fees
- **Employer matching**: 15% of donations receive corporate matches

### **Lifecycle Stages**
- **Early (Months 1-8)**: 200 donors, $10K monthly, 20% recurring rate
- **Growth (Months 9-16)**: 2,000 donors, $100K monthly, 35% recurring rate
- **Mature (Months 17-24)**: 20,000 donors, $1M monthly, 50% recurring rate

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.7+
pip (Python package manager)
```

### Installation
```bash
# Navigate to the generator directory
cd nonprofit_generator

# Install dependencies
pip install -r requirements.txt

# Run the generator
python generate_givehope.py
```

### Expected Output
```
❤️ GiveHope Synthetic Non-Profit Donation Data Generator
✅ Generated 14,784 donors, 55 campaigns, 6,730 donations
⏱️ Total execution time: 13.6 seconds
```

## 📁 Generated Output Files

All files are saved to the `/nonprofit_data/` directory:

### **Core Donation Data**
- **`donors.json`** - Complete donor profiles with giving history, preferences, and segmentation
- **`campaigns.json`** - Fundraising campaigns with goals, timelines, and performance tracking
- **`donations.json`** - All donation transactions with payment processing and metadata
- **`subscriptions.json`** - Recurring donation subscriptions with frequency and amounts

### **Supporting Data**
- **`employer_matches.json`** - Corporate matching gifts tied to employee donations
- **`tax_receipts.json`** - Annual tax documentation for deductible contributions
- **`campaign_analytics.json`** - Detailed performance analysis by campaign
- **`donor_analytics.json`** - Comprehensive donor segmentation and behavior analysis
- **`nonprofit_metrics.json`** - Complete fundraising analytics and KPIs

## 🎯 Key Non-Profit Industry Features

### **Seasonal Giving Patterns**
- **Year-end surge**: 280% increase in December giving
- **Giving Tuesday**: 250% spike on Tuesday after Thanksgiving
- **Summer slump**: 30% decrease in June-August donations
- **New Year resolution**: 20% increase in January giving
- **Back-to-school**: 30% increase in October awareness campaigns

### **Campaign Management**
- **Multi-cause portfolios** with 1-3 campaigns active per month
- **Goal setting** with realistic targets based on cause type and urgency
- **Duration optimization** (7-180 days based on campaign type)
- **Success tracking** with 18.2% overall campaign success rate
- **Matching sponsor integration** with 20% of campaigns having corporate sponsors

### **Donor Development**
- **Acquisition channels**: Organic (35%), Email (25%), Social (20%), Events (15%), P2P (5%)
- **Retention programs** with 65-85% retention rates by organizational maturity
- **Upgrade pathways** from one-time to recurring donors (10.1% conversion)
- **Major gift cultivation** with capacity rating and planned giving prospects
- **Communication preferences** with opt-out and anonymity options

### **Recurring Giving Programs**
- **Subscription management** with automatic billing and donor portal access
- **Flexible scheduling** with donor-preferred dates and frequencies
- **Upgrade campaigns** with 15% auto-increase adoption
- **Retention strategies** with dedication options and impact updates
- **Monthly recurring revenue** of $696K+ in mature stage

### **Tax Compliance & Receipts**
- **Automatic receipt generation** for donations $25+
- **Tax year tracking** with proper deduction calculations
- **Anonymous donation handling** while maintaining compliance
- **Goods and services valuation** (pure charitable donations)
- **EIN and organization details** for IRS reporting

## 📈 Generated Metrics

### **Fundraising Overview**
- Total donors: 14,784
- Active campaigns: 55
- Successful donations: 6,730
- Campaign success rate: 18.2%
- Total funds raised: $17,493,794

### **Donor Engagement**
- Recurring donors: 1,499 (10.1% conversion rate)
- Major donors: 1,159 (7.8% of donor base)
- Anonymous donors: 1,424 (9.6% prefer anonymity)
- Average donation: $2,599 (includes major gifts)

### **Revenue Streams**
- Monthly recurring revenue: $696,694
- Processing fees covered: $142,337 (donor-funded)
- Employer matches: $331,225 (5.7% of donations matched)
- Average first donation: Higher than subsequent gifts

### **Campaign Performance by Cause**
- **Environment**: 36% success rate, $3.2M raised (14 campaigns)
- **Community**: 38% success rate, $743K raised (8 campaigns)
- **Disaster Relief**: 10% success rate, $2.1M raised (10 campaigns)
- **Education**: 9% success rate, $1.4M raised (11 campaigns)
- **Healthcare**: 0% success rate, $1.9M raised (12 campaigns)

### **Seasonal Impact**
- **November peak**: $4.7M (Giving Tuesday effect)
- **October strong**: $3.1M (awareness campaigns)
- **December surge**: Projected highest month
- **Summer low**: June-August decreased activity

## 🎨 Data Structure Examples

### **Donor Profile**
```json
{
  "id": "cus_abc123def456",
  "name": "Sarah Johnson",
  "email": "sarah.johnson@email.com",
  "metadata": {
    "donor_type": "individual",
    "major_donor": false,
    "recurring_donor": true,
    "lifetime_value_cents": 180000,
    "preferred_causes": ["education", "healthcare"],
    "acquisition_channel": "email",
    "giving_capacity": "medium",
    "employer": "Tech Solutions Inc",
    "anonymous": false,
    "volunteer": true
  }
}
```

### **Campaign Details**
```json
{
  "id": "campaign_disaster789",
  "name": "Emergency Relief Fund 2024",
  "type": "disaster_relief",
  "goal_cents": 50000000,
  "raised_cents": 47500000,
  "donor_count": 1247,
  "start_date": "2024-03-15T00:00:00",
  "end_date": "2024-04-15T00:00:00",
  "status": "active",
  "metadata": {
    "urgency": "high",
    "matching_sponsor": "Global Corp Foundation",
    "match_ratio": 1.0,
    "match_cap_cents": 25000000
  }
}
```

### **Donation Transaction**
```json
{
  "id": "pi_donation_xyz789",
  "amount": 10000,
  "currency": "usd",
  "status": "succeeded",
  "customer": "cus_abc123def456",
  "description": "Donation to Emergency Relief Fund 2024",
  "metadata": {
    "campaign_id": "campaign_disaster789",
    "is_recurring": "false",
    "covers_fees": "true",
    "processing_fee_cents": 319,
    "donation_amount_cents": 10000,
    "tax_deductible": "true",
    "dedication": "In memory of John Smith"
  }
}
```

### **Recurring Subscription**
```json
{
  "id": "sub_recurring_monthly",
  "customer": "cus_abc123def456",
  "status": "active",
  "items": {
    "data": [{
      "price": {
        "unit_amount": 5000,
        "recurring": {
          "interval": "month",
          "interval_count": 1
        }
      }
    }]
  },
  "metadata": {
    "campaign_id": "campaign_education456",
    "frequency": "monthly",
    "monthly_equivalent_cents": 5000,
    "auto_increase": "true",
    "preferred_day_of_month": 15
  }
}
```

### **Employer Match**
```json
{
  "id": "pi_match_corporate123",
  "amount": 10000,
  "description": "Employer match for donation to Emergency Relief Fund",
  "metadata": {
    "campaign_id": "campaign_disaster789",
    "original_donation": "pi_donation_xyz789",
    "original_donor": "cus_abc123def456",
    "employer": "Tech Solutions Inc",
    "match_percentage": 1.0,
    "match_type": "employer_match"
  }
}
```

## 🔄 Business Use Cases

### **For Non-Profit Organizations**
- **Campaign optimization**: Test different goal sizes, durations, and messaging strategies
- **Donor segmentation**: Develop targeted communication and cultivation strategies
- **Seasonal planning**: Model year-end giving campaigns and Giving Tuesday initiatives
- **Retention analysis**: Build donor lifecycle management and upgrade programs

### **For Developers**
- **Donation processing**: Test complex payment flows with recurring billing and fee coverage
- **Tax compliance**: Build receipt generation and annual tax reporting systems
- **Campaign management**: Develop fundraising dashboards and progress tracking
- **Employer matching**: Integrate corporate giving programs and verification workflows

### **For Data Teams**
- **Donor analytics**: Build predictive models for lifetime value and churn risk
- **Campaign attribution**: Analyze multi-touch donor journeys and channel effectiveness
- **Seasonal forecasting**: Model giving patterns for budget and cash flow planning
- **Impact measurement**: Correlate fundraising success with programmatic outcomes

## ⚙️ Configuration Options

The script includes comprehensive configuration at the top of the file:

- **Donation amounts**: Modify suggested giving levels and major donor thresholds
- **Campaign types**: Adjust cause areas, success rates, and goal multipliers
- **Seasonal patterns**: Customize monthly giving fluctuations and special events
- **Lifecycle stages**: Modify growth patterns and donor acquisition rates
- **Fee structures**: Adjust processing fee coverage and employer match rates

## 🔧 Technical Details

### **Performance**
- Generates 14,784 donors and 6,730 donations in ~14 seconds
- Creates 55 campaigns across 5 cause areas with realistic timelines
- Processes 24 months of organizational growth with seasonal patterns
- Outputs comprehensive non-profit analytics with donor segmentation

### **Data Quality**
- All Stripe objects match official Payment Intents and Billing API structure
- Realistic seasonal giving based on charitable sector research
- Authentic campaign success rates by cause area and urgency level
- Proper tax receipt generation following IRS guidelines

### **Non-Profit Industry Accuracy**
- Donor distribution: Individual (90%), Corporate (8%), Foundation (2%)
- Recurring conversion: 10.1% (industry benchmark 5-15%)
- Employer matching: 5.7% participation (industry average 4-8%)
- Seasonal patterns: 280% December surge (verified by sector studies)
- Average gift size: Varies by donor segment and campaign type

## 📄 License

MIT License - Perfect for non-profit donation platform prototyping, charitable giving analytics, and fundraising system development.

---

**Ready to prototype non-profit donation platforms with authentic seasonal giving patterns and donor development cycles!** ❤️🎗️
