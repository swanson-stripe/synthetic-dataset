# Quick Start for Designers

Get a working dashboard with realistic business data in **2 minutes**.

## 🚀 Step 1: Add One Script

Add this single line to your HTML:

```html
<script src="https://swanson-stripe.github.io/synthetic-dataset/docs/dashboard-synthetic-data.js"></script>
```

## ✨ Step 2: Initialize (One Line)

Add this JavaScript code:

```javascript
const kit = new DashboardSyntheticData();
```

**That's it!** You now have:
- ✅ A persona selector in your page  
- ✅ 9 different business scenarios
- ✅ Realistic payment data for each business
- ✅ Automatic switching between businesses

## 📊 Step 3: Use the Data

```javascript
// Get business metrics
const metrics = kit.getMetrics();
// Returns: [{ label: "Total Revenue", value: "$2.1M" }, ...]

// Get payment data  
const payments = kit.getData('payments');
// Returns: [{ id: "py_123", amount: 5000, status: "succeeded" }, ...]

// Get customer data
const customers = kit.getData('customers');
// Returns: [{ id: "cus_123", email: "user@example.com" }, ...]
```

## 🎯 Complete Example

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Dashboard</title>
</head>
<body>
    <h1>My Prototype</h1>
    
    <div id="metrics"></div>
    <div id="data"></div>

    <script src="https://swanson-stripe.github.io/synthetic-dataset/docs/dashboard-synthetic-data.js"></script>
    <script>
        const kit = new DashboardSyntheticData({
            onPersonaChange: (data, persona, stage) => {
                // Update your UI when user switches businesses
                updateMetrics(kit.getMetrics());
                updatePayments(kit.getData('payments'));
            }
        });

        function updateMetrics(metrics) {
            document.getElementById('metrics').innerHTML = 
                metrics.map(m => `<p>${m.label}: ${m.value}</p>`).join('');
        }

        function updatePayments(payments) {
            document.getElementById('data').innerHTML = 
                payments.map(p => `<p>Payment: ${p.amount/100} USD</p>`).join('');
        }

        // Initial load
        updateMetrics(kit.getMetrics());
        updatePayments(kit.getData('payments'));
    </script>
</body>
</html>
```

## 🏢 Available Businesses

Your users can switch between these 9 business scenarios:

- **Modaic** - Fashion e-commerce
- **Mindora** - Online education  
- **Keynest** - Property management
- **Pulseon** - Fitness subscriptions
- **Fluxly** - Creator platform
- **Brightfund** - Non-profit fundraising
- **Procura** - B2B medical supplies
- **Stratus** - Cloud infrastructure
- **Forksy** - Food delivery

Each business has realistic data patterns and growth stages (Early, Growth, Mature).

## 🎮 Try It Live

- **Live Demo**: https://swanson-stripe.github.io/synthetic-dataset/docs/examples/efficient-integration-example.html
- **Advanced Example**: https://swanson-stripe.github.io/synthetic-dataset/docs/examples/prototype-base-example.html

## 💡 Pro Tips

1. **Console Testing**: Use `kit.switchPersona('mindora')` in browser console
2. **Get All Data**: Use `kit.getData('customers')`, `kit.getData('payments')`, etc.
3. **Check Current State**: Use `kit.getCurrentPersona()` and `kit.getCurrentStage()`
4. **Auto-Updates**: The script automatically gets updates - no need to change your code

## 🎨 Customize Placement

```javascript
// Put selector in specific location
const kit = new DashboardSyntheticData({
    target: '#my-navbar'  // CSS selector for where to put the business selector
});
```

## 🔧 All Available Data Types

```javascript
kit.getData('payments')          // Payment transactions
kit.getData('customers')         // Customer profiles  
kit.getData('connected_accounts') // Connected accounts (marketplaces)
kit.getData('transfers')         // Money transfers
kit.getData('balances')          // Account balances
kit.getData('subscriptions')     // Recurring subscriptions
kit.getData('invoices')          // Invoices (B2B businesses)
kit.getData('issuing_cards')     // Issued cards (some businesses)
```

---

**Questions?** 
- **Full Documentation**: https://swanson-stripe.github.io/synthetic-dataset/docs/
- **Repository**: https://github.com/swanson-stripe/synthetic-dataset
- **This Guide**: https://github.com/swanson-stripe/synthetic-dataset/blob/main/instructions.md
