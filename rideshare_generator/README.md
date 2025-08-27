# RideShare Plus Synthetic Stripe Data Generator

A comprehensive Python script that generates realistic on-demand transportation platform data with drivers, dynamic pricing, fraud patterns, and complete Stripe Connect/Issuing integration over a 24-month business lifecycle.

## 🚗 Overview

RideShare Plus simulates a full-scale rideshare platform with realistic transportation industry patterns including:

- **Stripe Connect Express accounts** for driver onboarding and payouts
- **Dynamic surge pricing** based on time patterns and demand
- **Stripe Issuing cards** for driver fuel and expense management
- **Fraud detection scenarios** with ML-style pattern recognition
- **Multi-city expansion** across 25 major US markets
- **Complete ride lifecycle** from request to payout

## 📊 Business Model Simulation

### **Platform Economics**
- **Base fare**: $2.50 + $1.50/mile + $0.35/minute
- **Driver take rate**: 75% of fare
- **Platform fee**: 25% of fare + $1.99 booking fee
- **Instant payout fee**: $0.50 for immediate transfers
- **Airport surcharge**: $3.50 for airport pickups/dropoffs

### **Vehicle Types**
- **RideShare Standard**: 4 passengers, 1.0x pricing (70% of rides)
- **RideShare Premium**: 4 passengers, 1.5x pricing (20% of rides)
- **RideShare XL**: 6 passengers, 1.8x pricing (10% of rides)

### **Lifecycle Stages**
- **Early (Months 1-8)**: 50 drivers, 150 rides/week, 1 city
- **Growth (Months 9-16)**: 150 drivers, 600 rides/week, 3 cities
- **Mature (Months 17-24)**: 300 drivers, 1,200 rides/week, 5 cities

### **Dynamic Pricing Patterns**
- **Rush hour surge**: 7-9 AM (1.5x), 5-7 PM (1.8x)
- **Late night**: 11 PM-2 AM (1.3x boost)
- **Weekend nights**: Friday/Saturday 10 PM-2 AM (2.0x boost)
- **Airport surge**: Additional 1.4x multiplier for airport rides

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.7+
pip (Python package manager)
```

### Installation
```bash
# Navigate to the generator directory
cd rideshare_generator

# Install dependencies
pip install -r requirements.txt

# Run the generator
python generate_rideshare.py
```

### Expected Output
```
🚗 RideShare Plus Synthetic Platform Data Generator
✅ Generated 328 drivers, 60,884 rides, 1,547 fraud cases
⏱️ Total execution time: 44.5 seconds
```

## 📁 Generated Output Files

All files are saved to the `/rideshare_data/` directory:

### **Core Platform Data**
- **`drivers.json`** - Stripe Connect Express accounts with driver ratings, vehicle info, and earnings history
- **`passengers.json`** - Customer profiles with ride preferences and payment methods
- **`rides.json`** - Complete ride records with pickup/dropoff, pricing, and completion status
- **`payments.json`** - Ride payments with surge pricing and booking fees

### **Financial Data**
- **`payouts.json`** - Driver earnings transfers (weekly standard vs instant payouts)
- **`issuing_cards.json`** - Virtual fuel cards with spending controls for drivers
- **`issuing_authorizations.json`** - Gas station purchases and expense transactions

### **Risk & Analytics**
- **`fraud_cases.json`** - Suspicious activity detection with ML-style risk scoring
- **`platform_metrics.json`** - Complete rideshare analytics and KPIs

## 🎯 Key Rideshare Industry Features

### **Driver Onboarding & Management**
- **Express Connect accounts** with background check verification
- **Vehicle registration** with make, model, year, and license plates
- **Performance metrics** including acceptance rate, completion rate, and passenger ratings
- **Payout preferences** (70% weekly, 30% instant with fees)
- **City-specific deployment** with market expansion patterns

### **Dynamic Pricing Engine**
- **Time-based surge** patterns for rush hours, late nights, and weekends
- **Location-based multipliers** for airports and high-demand areas
- **Supply-demand modeling** with realistic surge frequency (15-35% of rides)
- **Multi-tier pricing** with standard, premium, and XL vehicle options

### **Ride Lifecycle Management**
- **GPS-based routing** with realistic distance and duration calculations
- **Driver-passenger matching** within city boundaries
- **Completion tracking** with 95% success rate and cancellation patterns
- **Rating systems** for both drivers and passengers post-ride

### **Stripe Issuing Integration**
- **Virtual fuel cards** for drivers with spending controls
- **Category restrictions** (gas stations, parking, tolls allowed; bars, gambling blocked)
- **Daily/weekly limits** ($200/day, $1,000/week per driver)
- **Real transaction patterns** based on driving frequency

### **Fraud Detection & Risk**
- **Fake ride detection** (GPS anomalies, duration mismatches, repeat patterns)
- **Stolen card identification** (velocity checks, location inconsistencies)
- **Account takeover** (behavior changes, device switches, unusual destinations)
- **Promo abuse** (similar signup patterns, payment overlaps, location clustering)

## 📈 Generated Metrics

### **Platform Overview**
- Total drivers: 328
- Active drivers: 326 (99.4% active)
- Total rides: 60,884
- Completion rate: 95.0%

### **Financial Performance**
- Gross bookings: $1,401,266
- Platform revenue: $465,144 (33.2% take rate)
- Driver earnings: $963,993
- Average fare: $24.24

### **Operational Metrics**
- Average distance: 2.2 miles per ride
- Average duration: 12.4 minutes
- Rides per active driver: 186.8
- Surge frequency: 72.1% of rides

### **Risk Management**
- Fraud cases detected: 1,547 (2.54% of rides)
- Fake rides: 40.4% of fraud cases
- Stolen cards: 29.3% of fraud cases
- Account takeovers: 20.4% of fraud cases

## 🎨 Data Structure Examples

### **Driver Connect Account**
```json
{
  "id": "acct_DRIVER_abc123",
  "type": "express",
  "capabilities": {
    "transfers": {"status": "active"},
    "card_issuing": {"status": "active"}
  },
  "individual": {
    "first_name": "Michael",
    "last_name": "Johnson",
    "email": "michael.johnson@email.com",
    "verification": {"status": "verified"}
  },
  "metadata": {
    "driver_id": "DRIVER_000001",
    "vehicle_type": "standard",
    "vehicle_make": "Toyota",
    "vehicle_model": "Camry",
    "rating": 4.78,
    "acceptance_rate": 0.891,
    "city": "San Francisco",
    "payout_preference": "weekly"
  }
}
```

### **Ride with Dynamic Pricing**
```json
{
  "id": "RIDE_00012345",
  "driver_account": "acct_DRIVER_abc123",
  "status": "completed",
  "pickup_location": {"lat": 37.7849, "lng": -122.4094},
  "dropoff_location": {"lat": 37.7749, "lng": -122.4194},
  "distance_miles": 3.2,
  "duration_minutes": 14.7,
  "pricing": {
    "base_fare": 250,
    "distance_fare": 480,
    "time_fare": 515,
    "surge_multiplier": 1.75,
    "airport_surcharge": 0,
    "booking_fee": 199,
    "total": 2721
  },
  "city": "San Francisco"
}
```

### **Fraud Detection Case**
```json
{
  "id": "fraud_def456",
  "ride_id": "RIDE_00012345",
  "fraud_type": "fake_ride",
  "risk_score": 0.847,
  "patterns_detected": [
    "GPS_ANOMALY: No movement detected during ride",
    "DURATION_MISMATCH: Ride completed in unrealistic time",
    "REPEAT_PATTERN: Same driver-rider pair multiple times"
  ],
  "status": "confirmed",
  "action_taken": "account_suspended"
}
```

### **Driver Fuel Card Authorization**
```json
{
  "id": "iauth_ghi789",
  "amount": 4750,
  "approved": true,
  "merchant_data": {
    "category": "gas_stations",
    "name": "Shell",
    "city": "San Francisco"
  },
  "metadata": {
    "driver_account": "acct_DRIVER_abc123",
    "purchase_type": "fuel",
    "gallons": 12.1
  }
}
```

## 🔄 Business Use Cases

### **For Product Teams**
- **Surge pricing optimization**: Test dynamic pricing algorithms and driver supply balancing
- **Driver retention**: Analyze payout preferences and earnings patterns
- **Market expansion**: Model city-by-city rollout strategies
- **Fraud prevention**: Develop ML models for suspicious activity detection

### **For Developers**
- **Connect integration**: Test Express account onboarding and verification flows
- **Payment processing**: Handle complex pricing with surge, fees, and splits
- **Issuing implementation**: Build driver expense management with spending controls
- **Real-time pricing**: Prototype dynamic fare calculation engines

### **For Data Teams**
- **Driver analytics**: Build utilization dashboards and earnings forecasting
- **Demand modeling**: Analyze surge patterns and supply-demand balancing
- **Fraud detection**: Train ML models on realistic fraud patterns
- **City performance**: Compare market metrics and expansion ROI

## ⚙️ Configuration Options

The script includes comprehensive configuration at the top of the file:

- **Pricing structure**: Modify base fares, per-mile rates, and surge multipliers
- **Lifecycle stages**: Adjust driver onboarding and ride volume by business phase
- **Geographic expansion**: Customize city rollout and market characteristics
- **Fraud patterns**: Modify fraud types and detection sensitivity
- **Vehicle mix**: Adjust standard/premium/XL distribution

## 🔧 Technical Details

### **Performance**
- Generates 328 drivers and 60,884 rides in ~45 seconds
- Creates 1,547 fraud cases with realistic risk scoring
- Processes 24 months of marketplace lifecycle events
- Outputs comprehensive rideshare platform data

### **Data Quality**
- All Stripe objects match official Connect/Issuing API structure
- Realistic surge pricing based on transportation industry patterns
- Geographic accuracy with real city coordinates and distances
- Fraud detection patterns based on actual rideshare security challenges

### **Industry Accuracy**
- Driver take rates: 75% typical for rideshare platforms
- Surge frequency: 15-35% based on market maturity
- Completion rates: 95% realistic for established platforms
- Fraud rates: 2-5% typical for transportation marketplaces

## 📄 License

MIT License - Perfect for rideshare platform prototyping, marketplace analytics, and payment system development.

---

**Ready to prototype on-demand transportation platforms with realistic surge pricing and fraud detection!** 🚗💨
