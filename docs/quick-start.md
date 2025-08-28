# Stripe Synthetic Dataset - Quick Start Guide

## 🎯 **What This Gives You**

A **completely independent dataset package** that serves realistic Stripe payment data across 5 different business personas. Your prototype automatically gets:

- ✅ **5 business scenarios** ready to use
- ✅ **Persona switcher** built-in (dropdown component) 
- ✅ **Real-time data switching** - change personas, app updates instantly
- ✅ **Zero setup** - just include 2 JavaScript files
- ✅ **Independent updates** - dataset evolves separately from your prototype

---

## 🚀 **For Designers: 3-Minute Setup**

### **Step 1: Include the Libraries**
Add these 2 lines to your HTML:

```html
<script src="https://swanson-stripe.github.io/synthetic-dataset/docs/stripe-data-client.js"></script>
<script src="https://swanson-stripe.github.io/synthetic-dataset/docs/persona-switcher.js"></script>
```

### **Step 2: Initialize with Default Persona**
```javascript
// Choose your default business scenario
const dataClient = new StripeDataClient({
  defaultPersona: 'techstyle' // or 'edutech', 'propertyflow', 'fitstream', 'creatorhub'
});

// Add persona switcher (dropdown appears automatically)
const switcher = new PersonaSwitcher(dataClient, {
  onSwitch: (personaId) => {
    console.log(`Switched to ${personaId} - your app auto-updates!`);
  }
});
```

### **Step 3: Use the Data**
```javascript
// Get business-appropriate metrics (automatically calculated)
const metrics = dataClient.calculateMetrics();
// Returns: [{ label: "Total Revenue", value: "$2.1M" }, ...]

// Get raw data for tables/charts
const payments = dataClient.getData('payments');
const customers = dataClient.getData('customers');
const summary = dataClient.getSummary();
```

**That's it!** Your prototype now has 5 business scenarios with a switcher.

---

## 📋 **Available Business Personas**

| Persona | Business Model | What You Get |
|---------|---------------|--------------|
| **🛍️ Modaic** | E-commerce Fashion | Payments, customers, multi-currency, disputes |
| **🎓 Mindora** | Education Marketplace | Instructors, students, courses, revenue sharing |
| **🏠 Keynest** | Property Management | Rent collection, landlords, maintenance, escrow |
| **💪 Pulseon** | Fitness Subscriptions | Trials, churn, family plans, engagement |
| **🎨 Fluxly** | Creator Economy | Content sales, tips, fan subscriptions, payouts |

Each persona includes:
- **Realistic data patterns** (growth lifecycle, seasonal trends)
- **Business-specific metrics** (MRR, churn, take rates, etc.)
- **Stripe product usage** (Connect, Billing, Treasury, etc.)
- **Complete data objects** (customers, payments, subscriptions, etc.)

---

## 🎨 **Designer Experience**

### **What the Switcher Looks Like**
- Appears as floating dropdown (top-right by default)
- Shows current business scenario with icon
- Click to see all 5 personas with descriptions
- Select new persona → entire app updates automatically

### **What Happens When You Switch**
1. User clicks persona dropdown
2. Selects "🏠 Keynest"
3. **Instantly**:
   - Metrics change: "Total Revenue" → "Rent Collected"
   - Tables update: Payment data → Rent payments 
   - Your custom components get new data via callbacks

### **Responsive Design**
- Desktop: Floating switcher
- Mobile: Bottom sheet on mobile devices
- Dark/light theme support

---

## 💻 **Integration Examples**

### **Basic Dashboard**
```javascript
// Metrics cards that auto-update
dataClient.subscribe((data, personaId) => {
  const metrics = dataClient.calculateMetrics();
  updateMetricsCards(metrics); // Your function
});

// Table that shows appropriate data
function updateTable(personaId) {
  switch(personaId) {
    case 'techstyle':
      showPaymentsTable(dataClient.getData('payments'));
      break;
    case 'edutech': 
      showEnrollmentsTable(dataClient.getData('enrollments'));
      break;
    // ... etc
  }
}
```

### **React Integration**
```jsx
function Dashboard() {
  const [dataClient] = useState(() => new StripeDataClient());
  const [data, setData] = useState(null);
  const [persona, setPersona] = useState('techstyle');
  
  useEffect(() => {
    return dataClient.subscribe((newData, personaId) => {
      setData(newData);
      setPersona(personaId);
    });
  }, []);
  
  return (
    <div>
      <MetricsCards metrics={dataClient.calculateMetrics()} />
      <DataTable data={data?.payments} persona={persona} />
    </div>
  );
}
```

### **Chart Integration**
```javascript
// Charts automatically get appropriate data
dataClient.subscribe((data, personaId) => {
  const chartData = formatForCharts(data.metrics, personaId);
  updateCharts(chartData);
});

function formatForCharts(metrics, persona) {
  switch(persona) {
    case 'fitstream':
      return formatSubscriptionMetrics(metrics);
    case 'creatorhub':
      return formatCreatorMetrics(metrics);
    // ...
  }
}
```

---

## 🔧 **Advanced Configuration**

### **Custom Position & Styling**
```javascript
const switcher = new PersonaSwitcher(dataClient, {
  position: 'top-left',    // top-right, bottom-left, bottom-right
  theme: 'dark',           // light, dark
  showInfo: true,          // Show persona details panel
  container: document.getElementById('my-nav') // Custom container
});
```

### **Custom Business Metrics**
```javascript
// Override default metrics calculation
const metrics = dataClient.calculateMetrics();

// Add your own metrics
const customMetrics = [
  ...metrics,
  { 
    label: 'Custom KPI', 
    value: calculateMyKPI(dataClient.currentData) 
  }
];
```

### **Error Handling**
```javascript
dataClient.subscribe((data, personaId) => {
  // Your update logic
}, (error) => {
  console.error('Data update failed:', error);
  showErrorMessage('Failed to switch personas');
});
```

---

## 🌐 **API Endpoints (For Advanced Use)**

If you prefer direct API access:

```javascript
// Base URL
const API_BASE = 'https://swanson-stripe.github.io/synthetic-dataset/api/v1';

// Available endpoints
GET /personas.json              // List all personas
GET /techstyle/payments.json    // E-commerce payments
GET /edutech/instructors.json   // Education instructors
GET /propertyflow/rent_payments.json // Property rent data
// ... etc
```

### **Direct Fetch Example**
```javascript
const response = await fetch(`${API_BASE}/fitstream/subscriptions.json`);
const subscriptions = await response.json();
```

---

## 🎯 **Perfect For**

- **Dashboard prototypes** - Realistic payment data
- **Demo applications** - Multiple business scenarios  
- **Component testing** - Real data patterns
- **Client presentations** - Switch scenarios live
- **A/B testing** - Different business models
- **Learning Stripe APIs** - See real object structures

---

## 🔄 **Updates & Versioning**

- **Dataset updates independently** - New personas, improved data
- **Your prototype keeps working** - Backward compatible API
- **No breaking changes** - Versioned endpoints (/v1/, /v2/, etc.)
- **New personas automatically available** - Just refresh persona dropdown

---

## 🆘 **Troubleshooting**

### **Persona switcher not appearing?**
Check console for errors, ensure both JavaScript files are loaded.

### **Data not updating?**
Verify you're subscribing to data changes and updating your UI in the callback.

### **CORS errors?**
The GitHub Pages API should work from any domain. If issues persist, check browser console.

### **Need help?**
- Check the [full example](./examples/prototype-base-example.html)
- Review the [API documentation](https://github.com/swanson-stripe/synthetic-dataset)

---

**🚀 Ready to prototype with realistic payment data in minutes, not hours!**
