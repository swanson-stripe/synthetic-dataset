# FitStream Synthetic Stripe Subscription Data Generator

A comprehensive Python script that generates realistic subscription data for a fitness streaming platform with trials, churn patterns, add-ons, and fitness-specific behaviors over a 24-month business lifecycle.

## 🏋️ Overview

FitStream simulates a subscription fitness platform offering streaming workouts with realistic subscription patterns, customer engagement metrics, and fitness industry-specific behaviors including:

- **Trial conversions** with engagement-based success rates
- **Seasonal patterns** (New Year spikes, summer prep, holiday drops)
- **Fitness-specific churn** based on engagement scores and workout frequency
- **Family plan management** with multiple users
- **Add-on services** (personal training, nutrition plans, equipment rental)
- **Payment failure patterns** with retry logic and recovery campaigns

## 📊 Business Model Simulation

### **Subscription Plans**
- **Basic**: $9.99/month (10 classes/month)
- **Unlimited**: $19.99/month (unlimited classes)
- **Family**: $39.99/month (5 users, unlimited classes)

### **Add-On Services**
- **Personal Training**: $49.99 per session
- **Nutrition Plan**: $14.99/month
- **Equipment Rental**: $29.99/month

### **Lifecycle Stages**
- **Early (Months 1-8)**: 250 total subscribers, 10% monthly churn, 15% trial conversion
- **Growth (Months 9-16)**: 1,500 total subscribers, 5% monthly churn, 25% trial conversion
- **Mature (Months 17-24)**: 5,000 total subscribers, 2% monthly churn, 35% trial conversion

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.7+
pip (Python package manager)
```

### Installation
```bash
# Navigate to the generator directory
cd fitstream_generator

# Install dependencies
pip install -r requirements.txt

# Run the generator
python generate_fitstream.py
```

### Expected Output
```
🏋️ FitStream Synthetic Subscription Data Generator
✅ Generated 5,296 customers, 5,296 subscriptions
⏱️ Total execution time: 20.6 seconds
```

## 📁 Generated Output Files

All files are saved to the `/output/` directory:

### **Core Data Files**
- **`customers.json`** (4.6MB) - Customer profiles with fitness preferences, engagement scores, and workout habits
- **`subscriptions.json`** (9.8MB) - Complete subscription lifecycle with trials, active, canceled, and paused states
- **`payments.json`** (20MB) - Recurring subscription payments and one-time purchases (personal training sessions)
- **`trials.json`** (1.3MB) - Trial tracking with conversion rates by acquisition channel

### **Analytics Files**
- **`churn_analysis.json`** (744KB) - Detailed churn events with reasons (cost, content, technical issues, life changes)
- **`engagement_metrics.json`** (1.4MB) - Customer engagement correlation with retention and plan types
- **`fitness_metrics.json`** (1.6KB) - Complete fitness industry KPIs and summary statistics

## 🎯 Key Fitness Industry Features

### **Customer Behavior Modeling**
- **Engagement scoring** based on workout frequency and platform usage
- **Device preferences** (iOS, Android, web, Roku, Apple TV, smart TV)
- **Workout type preferences** (strength, cardio, yoga, pilates, HIIT, dance, meditation)
- **Instructor preferences** and class booking patterns
- **Seasonal activity patterns** with New Year resolution spikes

### **Subscription Lifecycle**
- **Free trials** (7, 14, or 30 days) with realistic conversion rates
- **Vacation holds** for temporary subscription pauses during summer months
- **Win-back campaigns** with 15% success rate for churned customers
- **Family plan management** with multiple user profiles and admin controls

### **Payment Patterns**
- **Subscription billing** with monthly cycles and add-on charges
- **Failed payment recovery** with 3-attempt retry logic (30%, 20%, 10% success rates)
- **One-time purchases** for personal training sessions and equipment
- **Seasonal gift subscriptions** and promotional pricing

### **Churn Analysis**
- **Voluntary churn reasons**: Cost (35%), content dissatisfaction (25%), technical issues (15%), life changes (15%), competitor (10%)
- **Involuntary churn** due to payment failures with dunning management
- **Engagement-based retention** (highly engaged users churn 70% less)
- **At-risk customer identification** based on engagement decline

## 📈 Generated Metrics

### **Business Overview**
- Total customers: 5,296
- Active subscriptions: 2,285
- Monthly Recurring Revenue (MRR): $80,176
- Annual Recurring Revenue (ARR): $962,114
- Average Revenue Per User (ARPU): $35.09

### **Subscription Health**
- Trial conversion rate: 33.4%
- Monthly churn rate: 48.7% (cumulative over 24 months)
- Payment success rate: 97.7%
- Add-on attachment rate: 37.3%

### **Plan Distribution**
- Basic: 38.4% of active subscriptions
- Unlimited: 43.6% of active subscriptions
- Family: 18.0% of active subscriptions

### **Engagement Metrics**
- Average engagement score: 64.7/100
- High engagement customers (80+): 1,153
- At-risk customers (churn score >0.7): 184

## 🎨 Data Structure Examples

### **Customer Profile**
```json
{
  "id": "cus_FIT123abc456def",
  "email": "sarah.johnson@email.com",
  "name": "Sarah Johnson",
  "metadata": {
    "acquisition_channel": "paid_social",
    "engagement_score": 87.3,
    "workout_frequency": 18,
    "preferred_workout_types": ["strength", "yoga", "hiit"],
    "preferred_instructors": ["Sarah M.", "Mike T."],
    "device_preferences": ["ios", "apple_tv"],
    "churn_risk_score": 0.15
  }
}
```

### **Subscription with Add-ons**
```json
{
  "id": "sub_FIT789ghi012jkl",
  "customer": "cus_FIT123abc456def",
  "status": "active",
  "items": {
    "data": [
      {
        "price": {
          "unit_amount": 1999,
          "product": "prod_fitstream_unlimited"
        }
      },
      {
        "price": {
          "unit_amount": 1499,
          "product": "prod_fitstream_nutrition_plan"
        }
      }
    ]
  },
  "metadata": {
    "plan_type": "unlimited",
    "selected_addons": ["nutrition_plan"],
    "engagement_tier": "champion",
    "workout_streak": 14,
    "total_classes_booked": 127
  }
}
```

### **Trial Conversion Tracking**
```json
{
  "subscription_id": "sub_FIT789ghi012jkl",
  "trial_days": 30,
  "acquisition_channel": "paid_social",
  "converted": true,
  "conversion_date": 1672531200,
  "plan_type": "unlimited"
}
```

## 🔄 Business Use Cases

### **For Product Teams**
- **Trial optimization**: A/B test trial lengths (7, 14, 30 days) and conversion strategies
- **Churn prevention**: Identify at-risk customers and design retention campaigns
- **Engagement analysis**: Correlate workout frequency with subscription retention
- **Seasonal planning**: Plan marketing campaigns around fitness seasonal patterns

### **For Developers**
- **Subscription billing**: Test complex billing scenarios with add-ons and upgrades
- **Payment failure handling**: Develop robust retry logic and dunning management
- **Family account management**: Build multi-user subscription interfaces
- **Engagement tracking**: Prototype workout tracking and progress analytics

### **For Data Teams**
- **Cohort analysis**: Analyze retention patterns by acquisition channel and plan type
- **Revenue forecasting**: Model MRR growth and churn impact scenarios
- **Customer segmentation**: Build engagement-based customer segments
- **LTV modeling**: Develop customer lifetime value prediction models

## ⚙️ Configuration Options

The script includes comprehensive configuration at the top of the file:

- **Subscription plans**: Modify pricing, features, and plan distribution
- **Lifecycle stages**: Adjust subscriber growth and churn rates by business phase
- **Seasonal patterns**: Customize monthly subscription volume multipliers
- **Engagement patterns**: Modify workout frequency and retention correlation
- **Payment failure patterns**: Adjust failure rates and recovery success rates

## 🔧 Technical Details

### **Performance**
- Generates 5,296 customers and subscriptions in ~20 seconds
- Creates 16,414 payment records with realistic timing patterns
- Processes 24 months of subscription lifecycle events
- Outputs 38MB of realistic fitness platform data

### **Data Quality**
- All Stripe objects match official API structure
- Realistic engagement correlations with retention
- Seasonal business patterns based on fitness industry trends
- Proper trial-to-paid conversion funnels
- Family plan complexity with multiple users

### **Fitness Industry Accuracy**
- Trial conversion rates: 15-35% based on business maturity
- Monthly churn rates: 2-10% typical for fitness subscriptions
- Seasonal patterns: New Year +150%, Summer prep +60%, Holidays -40%
- Add-on attachment: 37% realistic for fitness platforms

## 📄 License

MIT License - Perfect for fitness platform prototyping, subscription analytics, and payment system development.

---

**Ready to prototype fitness subscription platforms with realistic engagement patterns and seasonal behaviors!** 🏋️‍♀️
