# CreatorHub Synthetic Stripe Connect Data Generator

A comprehensive Python script that generates realistic content monetization platform data with creators, fan subscriptions, content sales, tips, and complete Stripe Connect integration over a 24-month platform lifecycle.

## 🎨 Overview

CreatorHub simulates a full-scale content creator monetization platform with authentic creator economy patterns including:

- **Tiered creator programs** with dynamic take rates based on follower counts
- **Multi-revenue streams** (subscriptions, content sales, tips) with different fee structures
- **Fan subscription tiers** from $4.99 to $49.99 with creator-specific perks
- **Content marketplace** with category-specific pricing across 5 content types
- **Creator analytics** with earnings tracking, fan engagement, and growth metrics
- **Fraud prevention** including card testing, account sharing, and suspicious purchase detection

## 📊 Creator Economy Model Simulation

### **Creator Tiers & Take Rates**
- **Starter**: 0-999 followers, 30% platform fee
- **Growth**: 1K-9.9K followers, 25% platform fee
- **Established**: 10K-99.9K followers, 20% platform fee
- **Premium**: 100K+ followers, 15% platform fee

### **Content Categories & Pricing**
- **Video Courses**: $19.99-$199.99 (Education/Tech premium pricing)
- **eBooks**: $9.99-$49.99 (Digital publishing standard)
- **Memberships**: $9.99-$99.99 (Recurring community access)
- **Coaching**: $99.99-$499.99 (High-value personal services)
- **Digital Downloads**: $1.99-$19.99 (Templates, assets, resources)

### **Subscription Tiers**
- **Supporter**: $4.99/month (Early access, Discord)
- **Fan**: $9.99/month (Fan perks + Monthly livestream)
- **Super Fan**: $19.99/month (Exclusive content + 1-on-1 Q&A)
- **VIP**: $49.99/month (All perks + Personal consultation)

### **Platform Economics**
- **Content sales**: 20% platform fee
- **Tips**: 10% platform fee (creator-friendly)
- **Subscriptions**: Variable fee based on creator tier

### **Lifecycle Stages**
- **Early (Months 1-8)**: 50 creators, $50K GMV, 20 fans per creator avg
- **Growth (Months 9-16)**: 500 creators, $500K GMV, 100 fans per creator avg
- **Mature (Months 17-24)**: 2,000 creators, $2M GMV, 500 fans per creator avg

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.7+
pip (Python package manager)
```

### Installation
```bash
# Navigate to the generator directory
cd creatorhub_generator

# Install dependencies
pip install -r requirements.txt

# Run the generator
python generate_creatorhub.py
```

### Expected Output
```
🎨 CreatorHub Synthetic Content Monetization Data Generator
✅ Generated 1,688 creators, 8,237 fans, 0 content sales
⏱️ Total execution time: 11.0 seconds
```

## 📁 Generated Output Files

All files are saved to the `/creator_data/` directory:

### **Core Platform Data**
- **`creators.json`** - Stripe Connect Express accounts with creator profiles, tiers, and metadata
- **`fans.json`** - Customer profiles with spending tiers and content preferences
- **`content_items.json`** - Digital content catalog with pricing and creator attribution
- **`subscriptions.json`** - Fan-to-creator subscriptions with tier management

### **Transaction Data**
- **`content_sales.json`** - One-time content purchases with application fees
- **`tips.json`** - Creator tip transactions with lower platform fees
- **`payouts.json`** - Creator earnings transfers to bank accounts

### **Analytics & Security**
- **`fraud_prevention.json`** - Fraud detection results (card testing, account sharing)
- **`creator_analytics.json`** - Individual creator performance metrics
- **`platform_metrics.json`** - Overall platform analytics and revenue breakdown

## 🎯 Key Creator Economy Features

### **Creator Onboarding & Verification**
- **Express Connect accounts** with streamlined onboarding for individuals
- **Identity verification** with document upload and background checks
- **Bank account setup** for automated payouts and tax reporting
- **Content category selection** across 5 major creator verticals
- **Social platform integration** (YouTube, Instagram, TikTok, Twitch, etc.)

### **Multi-Revenue Stream Support**
- **Subscription management** with automatic billing and fan portal access
- **Content marketplace** with instant delivery for digital products
- **Tip processing** with optional messages and anonymous giving
- **Tiered pricing** that adjusts platform fees based on creator success
- **Application fee handling** with transparent creator earnings tracking

### **Fan Engagement Systems**
- **Spending tier classification** (Low, Medium, High, Premium) affecting behavior
- **Content preference tracking** across creator categories
- **Subscription upgrade paths** from supporter to VIP tiers
- **Gift subscription handling** with 5% of subscriptions being gifts
- **Platform referral tracking** (organic, social, creator referral, paid ads)

### **Content Management**
- **Dynamic pricing** based on content type and creator category
- **Difficulty ratings** (beginner, intermediate, advanced)
- **Review and rating systems** with realistic engagement patterns
- **Download tracking** for digital asset distribution
- **Category optimization** with pricing multipliers by vertical

### **Creator Analytics Dashboard**
- **Revenue breakdown** across subscriptions, content sales, and tips
- **Fan acquisition metrics** with unique customer tracking
- **Monthly recurring revenue** calculations for subscription creators
- **Average revenue per fan** for monetization optimization
- **Growth rate tracking** across follower count and earnings

## 📈 Generated Metrics

### **Platform Overview**
- Active creators: 1,688
- Total fans: 8,237
- Active subscriptions: 19,381
- Total GMV: $269,204
- Platform take rate: 21.2%

### **Revenue Distribution**
- **Subscriptions**: $180,486 (67.0% of GMV)
- **Tips**: $88,718 (33.0% of GMV)
- **Content sales**: $0 (0.0% - rare in early platform)
- **Monthly recurring revenue**: $180,486
- **Estimated ARR**: $2.17M

### **Creator Tier Distribution**
- **Starter**: 777 creators (46.0% - typical long-tail)
- **Growth**: 668 creators (39.6% - scaling creators)
- **Established**: 220 creators (13.0% - successful creators)
- **Premium**: 23 creators (1.4% - top-tier creators)

### **Content Categories**
- **Education**: 344 creators (20.4%)
- **Lifestyle**: 345 creators (20.4%)
- **Business**: 336 creators (19.9%)
- **Tech**: 336 creators (19.9%)
- **Entertainment**: 327 creators (19.4%)

## 🎨 Data Structure Examples

### **Creator Connect Account**
```json
{
  "id": "acct_abc123creator",
  "type": "express",
  "business_type": "individual",
  "individual": {
    "first_name": "Alex",
    "last_name": "Johnson",
    "email": "alex99@email.com",
    "verification": {"status": "verified"}
  },
  "business_profile": {
    "name": "alex99 Creative",
    "product_description": "Education content creator",
    "url": "https://creatorhub.com/alex99"
  },
  "metadata": {
    "creator_id": "CREATOR_000001",
    "username": "alex99",
    "category": "education",
    "tier": "growth",
    "follower_count": "5432",
    "engagement_rate": "0.047",
    "primary_platform": "youtube"
  }
}
```

### **Fan Subscription**
```json
{
  "id": "sub_fan_subscription",
  "customer": "cus_fan123abc",
  "status": "active",
  "application_fee_percent": 25.0,
  "transfer_data": {
    "destination": "acct_abc123creator"
  },
  "items": {
    "data": [{
      "price": {
        "unit_amount": 1999,
        "recurring": {"interval": "month"}
      }
    }]
  },
  "metadata": {
    "creator_id": "CREATOR_000001",
    "tier_name": "Super Fan",
    "perks": "All Fan perks,Exclusive content,1-on-1 Q&A monthly"
  }
}
```

### **Content Sale**
```json
{
  "id": "pi_content_purchase",
  "amount": 4999,
  "currency": "usd",
  "status": "succeeded",
  "customer": "cus_fan123abc",
  "description": "Purchase: Complete Education Masterclass",
  "application_fee_amount": 1000,
  "transfer_data": {
    "destination": "acct_abc123creator"
  },
  "metadata": {
    "content_id": "content_xyz789",
    "content_type": "video_course",
    "creator_id": "CREATOR_000001",
    "downloadable": "false",
    "category": "education"
  }
}
```

### **Creator Tip**
```json
{
  "id": "pi_tip_creator",
  "amount": 500,
  "currency": "usd",
  "customer": "cus_fan123abc",
  "description": "Tip for alex99 Creative",
  "application_fee_amount": 50,
  "metadata": {
    "type": "tip",
    "creator_id": "CREATOR_000001",
    "tip_amount_cents": "500",
    "platform_fee_cents": "50",
    "message": "Keep up the great work!",
    "anonymous": "false"
  }
}
```

### **Creator Analytics**
```json
{
  "creator_id": "CREATOR_000001",
  "username": "alex99",
  "category": "education",
  "tier": "growth",
  "follower_count": 5432,
  "fan_count": 127,
  "monthly_recurring_revenue_cents": 15432,
  "total_earnings_cents": 87640,
  "revenue_breakdown": {
    "subscriptions_percent": 72.5,
    "content_sales_percent": 18.2,
    "tips_percent": 9.3
  },
  "average_revenue_per_fan": 689
}
```

## 🔄 Business Use Cases

### **For Creator Platforms**
- **Monetization optimization**: Test different fee structures and creator tier programs
- **Content strategy**: Analyze pricing patterns across categories and creator types
- **Fan engagement**: Model subscription upgrade paths and retention strategies
- **Creator retention**: Design incentive programs based on tier progression

### **For Developers**
- **Connect integration**: Test Express account onboarding and verification flows
- **Multi-revenue processing**: Handle subscriptions, one-time sales, and tips
- **Application fees**: Implement dynamic fee structures based on creator success
- **Fraud prevention**: Build ML models for card testing and suspicious activity detection

### **For Data Teams**
- **Creator economics**: Analyze revenue distribution and long-tail monetization
- **Fan behavior**: Build engagement models and lifetime value predictions
- **Growth analytics**: Track creator tier progression and platform expansion
- **Marketplace optimization**: Optimize content pricing and discovery algorithms

## ⚙️ Configuration Options

The script includes comprehensive configuration at the top of the file:

- **Creator tiers**: Modify follower thresholds and fee structures
- **Content pricing**: Adjust price ranges by content type and category
- **Subscription tiers**: Customize tier prices and perk offerings
- **Platform economics**: Modify take rates for different revenue streams
- **Lifecycle stages**: Adjust creator growth and fan acquisition patterns

## 🔧 Technical Details

### **Performance**
- Generates 1,688 creators and 8,237 fans in ~11 seconds
- Creates 19,381 subscriptions and 6,453 tips with realistic patterns
- Processes 24 months of platform growth with creator tier progression
- Outputs comprehensive creator economy analytics

### **Data Quality**
- All Stripe objects match official Connect and Billing API structure
- Realistic creator tier distribution following power law patterns
- Authentic fan spending behavior based on creator economy research
- Proper application fee handling with transparent creator earnings

### **Creator Economy Accuracy**
- **Follower distribution**: Log-normal with long tail (most creators <10K followers)
- **Revenue streams**: Subscription-heavy (67%) with tip culture (33%)
- **Creator tiers**: Starter majority (46%) with premium elite (1.4%)
- **Fan spending**: Tiered behavior from low ($5) to premium ($100+) supporters
- **Category distribution**: Even split across education, lifestyle, business, tech, entertainment

## 📄 License

MIT License - Perfect for creator economy platform prototyping, content monetization analytics, and multi-sided marketplace development.

---

**Ready to prototype creator monetization platforms with authentic multi-revenue streams and fan engagement patterns!** 🎨💰
