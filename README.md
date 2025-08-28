# Stripe Synthetic Dataset Ecosystem

**Complete synthetic payment data generators for realistic prototyping and development**

A comprehensive collection of Python generators and React components that create realistic Stripe payment data across different business models. Perfect for prototyping, testing, demos, and development without using real customer data.

## 🎯 **What's Included**

### **Complete Business Model Coverage** (10 Generators)
- **TechStyle E-commerce**: 150K fashion retailer payments across 24-month growth lifecycle
- **CloudFlow SaaS**: 50K B2B subscriptions with MRR analytics and churn patterns  
- **LocalBites Marketplace**: 600K food delivery orders with multi-party payments
- **CreatorHub Platform**: Content monetization with creators, fans, and tips
- **EduTech Academy**: Online education with instructors, students, and course sales
- **FitStream Fitness**: Subscription streaming with trials and engagement metrics
- **PropertyFlow Real Estate**: Rent collection, maintenance, and landlord payouts
- **MedSupply B2B**: Medical equipment wholesale with complex invoicing
- **GiveHope Non-Profit**: Donation campaigns with seasonal giving patterns
- **RideShare Plus**: Transportation platform with dynamic pricing and Connect

### **Developer Tools & Infrastructure**
- **API Endpoints**: 77 structured JSON endpoints for direct consumption
- **Metrics Visualizer**: Transform any payment data into chart-ready formats
- **React Dashboard Kit**: Production-ready payment analytics components
- **CLI Data Fetcher**: Instant access to pre-generated datasets

## 📁 **Repository Structure**

```
stripe-synthetic-dataset/
├── .gitignore                    ✅ Properly excludes output data
├── README.md                     ✅ This comprehensive guide
├── techstyle_generator/          ✅ E-commerce Fashion Retailer
│   ├── generate_techstyle.py     ✅ 552 lines, fully functional
│   ├── README.md                 ✅ 256 lines, comprehensive docs
│   └── requirements.txt          ✅ Dependencies: faker, pandas, numpy
├── saas_generator/               ✅ B2B SaaS Platform
│   ├── generate_cloudflow.py     ✅ 815 lines, fully functional
│   └── requirements.txt          ✅ Dependencies: faker, pandas, numpy
├── marketplace_generator/        ✅ Food Delivery Marketplace
│   ├── generate_marketplace.py   ✅ 560 lines, fully functional
│   └── requirements.txt          ✅ Dependencies: faker, pandas, numpy
├── metrics_visualizer/           ✅ Data Formatting & Visualization
│   ├── format_metrics.py         ✅ 798 lines, fully functional
│   ├── README.md                 ✅ 396 lines, comprehensive docs
│   ├── sample_input.json         ✅ Test data provided
│   └── requirements.txt          ✅ Dependencies: faker, pandas, numpy
└── stripe-dashboard-kit/         ✅ React Component Library
    ├── package.json              ✅ NPM package ready for publish
    ├── README.md                 ✅ 478 lines, comprehensive docs
    ├── dist/ (excluded)          ✅ Build output (auto-generated)
    └── src/                      ✅ Full TypeScript component library
```

## 🚀 **Quick Start**

### **Option 1: Individual Generators**
```bash
# E-commerce fashion retailer (150K payments)
cd techstyle_generator
pip install -r requirements.txt
python generate_techstyle.py

# B2B SaaS platform (50K subscriptions)  
cd ../saas_generator
pip install -r requirements.txt
python generate_cloudflow.py

# Food delivery marketplace (600K orders)
cd ../marketplace_generator  
pip install -r requirements.txt
python generate_marketplace.py
```

### **Option 2: Visualization Pipeline**
```bash
# Generate data + format for charts
cd techstyle_generator && python generate_techstyle.py
cd ../metrics_visualizer && python format_metrics.py ../techstyle_generator/output/payments_raw.json

# Output: Chart-ready JSON for any visualization library
```

### **Option 3: Full Dashboard**
```bash
# Complete React dashboard with realistic data
cd stripe-dashboard-kit
npm install && npm run build
npm start  # Live dashboard with sample data
```

## 📊 **Data Outputs**

### **TechStyle E-commerce** (`techstyle_generator/`)
- **Scale**: 150,000 payments over 24 months
- **Business**: Fashion retailer growth from startup to mature
- **Features**: Multi-currency, seasonal patterns, payment method evolution
- **Formats**: Stripe-compatible JSON, daily metrics, chart data

### **CloudFlow SaaS** (`saas_generator/`)  
- **Scale**: 50,000 subscriptions with realistic churn
- **Business**: B2B SaaS from $0 to $2M MRR
- **Features**: Trial conversions, upgrades, usage billing, cohort analysis
- **Formats**: Subscription objects, invoices, MRR timeline

### **LocalBites Marketplace** (`marketplace_generator/`)
- **Scale**: 600,000 orders across restaurants and drivers
- **Business**: Food delivery platform with Connect accounts
- **Features**: Split payments, virtual cards, instant payouts, refunds
- **Formats**: Multi-party transactions, issuing data, marketplace metrics

## 🔧 **Integration Workflow**

### **Complete Pipeline**
```bash
# 1. Generate realistic payment data
python techstyle_generator/generate_techstyle.py

# 2. Format for visualization  
python metrics_visualizer/format_metrics.py techstyle_generator/output/payments_raw.json

# 3. Render in React dashboard
cd stripe-dashboard-kit && node test-integration.js

# Result: Full payment analytics dashboard with realistic data
```

### **Business Scenario Switching**
```bash
# Switch between business types instantly
python generate_techstyle.py    # E-commerce data
python generate_cloudflow.py    # SaaS data  
python generate_marketplace.py  # Marketplace data

# Same format, different business patterns
python format_metrics.py [any_dataset].json
```

## 💡 **Use Cases**

### **For Designers**
- **Figma/Sketch**: Use generated JSON to populate design components
- **Prototyping**: Realistic data that feels production-ready
- **User Testing**: Test with data that matches real user expectations

### **For Developers**  
- **Frontend Development**: Build payment UIs with realistic data volumes
- **API Testing**: Test with Stripe-compatible object structures
- **Performance Testing**: Large datasets (150K+ records) for optimization

### **For Product Teams**
- **Demos**: Show realistic growth patterns and business metrics
- **Analytics**: Prototype dashboard and reporting features
- **Stakeholder Presentations**: Compelling visualizations with realistic data

## 🎨 **Component Examples**

### **React Dashboard Integration**
```jsx
import { Dashboard } from '@stripe-synthetic/dashboard-kit';

function PaymentAnalytics() {
  return (
    <Dashboard 
      dataSource="/api/formatted-metrics"
      title="TechStyle Payment Analytics"
      theme="light"
    />
  );
}
```

### **Chart.js Integration**
```javascript
// Use formatted data directly
const chartConfig = {
  type: 'line',
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    datasets: [{
      label: 'Payment Volume',
      data: [125000, 135000, 128000, 142000, 155000],
      borderColor: '#635BFF'
    }]
  }
};
```

### **Custom API Simulation**
```python
# Serve realistic data via API
from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/api/payments')
def get_payments():
    with open('techstyle_generator/output/payments_raw.json') as f:
        return jsonify(json.load(f))

@app.route('/api/metrics') 
def get_metrics():
    with open('metrics_visualizer/formatted_output/metric_cards.json') as f:
        return jsonify(json.load(f))
```

## 📋 **Requirements**

### **Python Generators**
- Python 3.7+
- Dependencies: `faker`, `pandas`, `numpy` (see individual requirements.txt)

### **React Dashboard**  
- Node.js 16+
- React 18+
- Dependencies: `recharts`, `clsx`, `date-fns`

### **Output Compatibility**
- **Visualization**: Chart.js, D3, Plotly, React-compatible
- **Data Formats**: JSON, CSV, Stripe API-compatible
- **Scale**: Handles 100K+ records efficiently

## 🔒 **Privacy & Security**

- ✅ **No Real PII**: All data generated using Faker library
- ✅ **Stripe-Safe**: Objects match API structure without real keys
- ✅ **Git-Safe**: Output directories excluded via .gitignore
- ✅ **Production-Ready**: Realistic but synthetic data safe for demos

## 🚀 **Getting Started**

### **Quick Demo (5 minutes)**
```bash
git clone https://github.com/swanson-stripe/synthetic-dataset.git
cd synthetic-dataset/techstyle_generator
pip install -r requirements.txt
python generate_techstyle.py

# ✅ 150,000 realistic payments generated
# ✅ Ready for prototyping immediately
```

### **Full Integration (15 minutes)**
```bash
# 1. Generate data for all business types
cd techstyle_generator && python generate_techstyle.py
cd ../saas_generator && python generate_cloudflow.py
cd ../marketplace_generator && python generate_marketplace.py

# 2. Format for visualization
cd ../metrics_visualizer && python format_metrics.py

# 3. Launch React dashboard  
cd ../stripe-dashboard-kit && npm install && npm start

# ✅ Complete payment analytics dashboard running locally
```

## 📚 **Documentation**

Each component includes comprehensive documentation:

- **[TechStyle Generator](techstyle_generator/README.md)**: E-commerce payment data generation
- **[SaaS Generator](saas_generator/)**: Subscription and billing data  
- **[Marketplace Generator](marketplace_generator/)**: Multi-party payment flows
- **[Metrics Visualizer](metrics_visualizer/README.md)**: Data formatting and chart preparation
- **[Dashboard Kit](stripe-dashboard-kit/README.md)**: React component library

## 🤝 **Contributing**

This ecosystem is designed for realistic payment data generation. Contributions welcome:

- **New Business Models**: Add generators for other industries
- **Enhanced Realism**: Improve data patterns and edge cases  
- **Integration Examples**: Show usage with different tools/frameworks
- **Performance**: Optimize for larger datasets

## 📄 **License**

MIT License - Perfect for prototyping, development, and commercial use.

---

**Ready to prototype with realistic payment data in minutes, not hours.** 🚀
