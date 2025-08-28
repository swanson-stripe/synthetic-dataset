# AI Integration Guide for Dashboard Synthetic Data

## 🎯 Quick Integration Patterns

### Pattern 1: Basic Dashboard
```html
<!DOCTYPE html>
<html>
<head><title>My Dashboard</title></head>
<body>
    <nav id="navbar"><h1>Dashboard</h1></nav>
    <main id="content"></main>
    
    <script src="https://swanson-stripe.github.io/synthetic-dataset/docs/dashboard-synthetic-data.js"></script>
    <script>
        const kit = new DashboardSyntheticData({
            target: '#navbar'
        });
        
        function updateDashboard() {
            const metrics = kit.getMetrics();
            const payments = kit.getData('payments');
            // Render logic here
        }
        
        updateDashboard();
    </script>
</body>
</html>
```

### Pattern 2: React Integration
```javascript
import { useEffect, useState } from 'react';

function Dashboard() {
    const [kit, setKit] = useState(null);
    const [data, setData] = useState(null);
    
    useEffect(() => {
        // Load script dynamically
        const script = document.createElement('script');
        script.src = 'https://swanson-stripe.github.io/synthetic-dataset/docs/dashboard-synthetic-data.js';
        script.onload = () => {
            const newKit = new window.DashboardSyntheticData({
                autoInject: false, // Handle UI manually in React
                onPersonaChange: (data, persona, stage) => {
                    setData({ data, persona, stage });
                }
            });
            setKit(newKit);
            setData({ 
                data: newKit.getDataClient().currentData, 
                persona: newKit.getCurrentPersona(),
                stage: newKit.getCurrentStage()
            });
        };
        document.head.appendChild(script);
    }, []);
    
    if (!data) return <div>Loading...</div>;
    
    return (
        <div>
            <h1>{data.persona} Dashboard</h1>
            {kit.getMetrics().map(metric => (
                <div key={metric.label}>{metric.label}: {metric.value}</div>
            ))}
        </div>
    );
}
```

### Pattern 3: Vue Integration
```javascript
<template>
  <div>
    <h1>{{ currentPersona }} Dashboard</h1>
    <div v-for="metric in metrics" :key="metric.label">
      {{ metric.label }}: {{ metric.value }}
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      kit: null,
      metrics: [],
      currentPersona: ''
    }
  },
  mounted() {
    const script = document.createElement('script');
    script.src = 'https://swanson-stripe.github.io/synthetic-dataset/docs/dashboard-synthetic-data.js';
    script.onload = () => {
      this.kit = new window.DashboardSyntheticData({
        autoInject: false,
        onPersonaChange: (data, persona, stage) => {
          this.updateData();
        }
      });
      this.updateData();
    };
    document.head.appendChild(script);
  },
  methods: {
    updateData() {
      this.metrics = this.kit.getMetrics();
      this.currentPersona = this.kit.getCurrentPersona();
    }
  }
}
</script>
```

## 🔒 Data Schema Contracts

### Metrics Structure (NEVER change):
```typescript
interface Metric {
    label: string;          // Display name
    value: string;          // Pre-formatted for display
    rawValue: number;       // Raw value for calculations
}
```

### Payment Structure (NEVER change):
```typescript
interface Payment {
    id: string;            // Format: py_xxxxx
    amount: number;        // Always in cents
    currency: string;      // Always "usd"
    status: "succeeded" | "pending" | "failed";
    created: number;       // Unix timestamp
    description: string;   // Business-specific
    customer: string;      // Format: cus_xxxxx
    metadata: object;      // Persona-specific fields
}
```

### Customer Structure (NEVER change):
```typescript
interface Customer {
    id: string;            // Format: cus_xxxxx
    email: string;         // Valid email format
    name: string;          // Customer display name
    created: number;       // Unix timestamp
    metadata: object;      // Persona-specific fields
}
```

## 🎨 UI Patterns

### Recommended Table Structure:
```html
<table>
    <thead>
        <tr>
            <th>ID</th>
            <th>Amount</th>
            <th>Status</th>
            <th>Date</th>
        </tr>
    </thead>
    <tbody>
        <!-- Use this pattern -->
        <tr>
            <td>{payment.id}</td>
            <td>{formatCurrency(payment.amount)}</td>
            <td><span class="status {payment.status}">{payment.status}</span></td>
            <td>{formatDate(payment.created)}</td>
        </tr>
    </tbody>
</table>

<style>
.status.succeeded { background: #d1fae5; color: #065f46; }
.status.pending { background: #fef3c7; color: #92400e; }
.status.failed { background: #fee2e2; color: #991b1b; }
</style>
```

### Recommended Metric Cards:
```html
<div class="metric-card">
    <div class="metric-label">{metric.label}</div>
    <div class="metric-value">{metric.value}</div>
</div>

<style>
.metric-card {
    background: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
.metric-label {
    font-size: 14px;
    color: #666;
    margin-bottom: 8px;
}
.metric-value {
    font-size: 24px;
    font-weight: bold;
    color: #1a1a1a;
}
</style>
```

### Utility Functions:
```javascript
// Always provide these helper functions
function formatCurrency(cents) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(cents / 100);
}

function formatDate(timestamp) {
    return new Date(timestamp).toLocaleDateString();
}

function formatDateTime(timestamp) {
    return new Date(timestamp).toLocaleString();
}
```

## 🚫 Anti-Patterns (What NOT to do)

### 1. Don't copy the script contents:
```javascript
// ❌ BAD - Never do this
const DataClient = class { /* copied code */ };

// ✅ GOOD - Always use CDN
<script src="https://swanson-stripe.github.io/.../dashboard-synthetic-data.js"></script>
```

### 2. Don't create custom selectors:
```html
<!-- ❌ BAD - Kit provides this -->
<select id="persona-picker">
    <option value="modaic">Fashion</option>
</select>

<!-- ✅ GOOD - Auto-injected -->
<script>const kit = new DashboardSyntheticData();</script>
```

### 3. Don't manipulate amounts:
```javascript
// ❌ BAD - Don't modify the data
payment.amount = payment.amount / 100;

// ✅ GOOD - Use helper functions
function formatCurrency(cents) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(cents / 100);
}
```

### 4. Don't hardcode persona data:
```javascript
// ❌ BAD - Hardcoded data
const metrics = [
    { label: "Revenue", value: "$100,000" }
];

// ✅ GOOD - Dynamic data
const metrics = kit.getMetrics();
```

### 5. Don't use old persona names:
```javascript
// ❌ BAD - Old names
kit.switchPersona('techstyle');
kit.switchPersona('edutech');

// ✅ GOOD - New names
kit.switchPersona('modaic');
kit.switchPersona('mindora');
```

## 💡 Context Clues for AI

When user says:
- **"realistic data"** → Suggest dashboard synthetic data
- **"multiple business types"** → Explain personas
- **"payment data"** → Show `kit.getData('payments')`
- **"business metrics"** → Show `kit.getMetrics()`
- **"switch scenarios"** → Explain persona switching
- **"demo data"** → Use the synthetic dataset
- **"prototype dashboard"** → Use full integration pattern
- **"fake data"** → Clarify this is realistic synthetic data
- **"test data"** → Show how to access different data types

## 🔧 Advanced Configuration

### Custom Target Placement:
```javascript
// Place in specific navigation
const kit = new DashboardSyntheticData({
    target: '#navbar .persona-container'
});

// Multiple selectors (not recommended)
const kit1 = new DashboardSyntheticData({
    target: '#sidebar',
    autoInject: true
});
```

### Manual UI Control:
```javascript
// For React/Vue applications
const kit = new DashboardSyntheticData({
    autoInject: false, // Don't auto-inject UI
    onPersonaChange: (data, persona, stage) => {
        // Handle in your framework
        updateAppState(data, persona, stage);
    }
});

// Create UI manually
kit.createSelector('#my-container');
```

## 🧪 Testing & Development

### Console Commands for Testing:
```javascript
// Quick testing commands
kit.getMetrics()                    // See current metrics
kit.getData('payments')             // See payment data
kit.switchPersona('fluxly')         // Switch to creator platform
kit.getCurrentPersona()             // Check current business
kit.getAvailablePersonas()          // See all options

// Advanced testing
kit.getDataClient().currentData     // See all raw data
kit.getDataClient().cache          // See cached data
```

### Development Tips:
```javascript
// Make kit globally available for debugging
window.kit = kit;
window.dataClient = kit.getDataClient();

// Log all persona changes
const kit = new DashboardSyntheticData({
    onPersonaChange: (data, persona, stage) => {
        console.log(`Switched to ${persona} (${stage})`, data);
        updateUI(data, persona, stage);
    }
});
```

## 📚 Reference Links

- **Live Demo**: https://swanson-stripe.github.io/synthetic-dataset/docs/examples/efficient-integration-example.html
- **Advanced Demo**: https://swanson-stripe.github.io/synthetic-dataset/docs/examples/prototype-base-example.html
- **Instructions**: https://github.com/swanson-stripe/synthetic-dataset/blob/main/instructions.md
- **Full Documentation**: https://swanson-stripe.github.io/synthetic-dataset/docs/
- **Repository**: https://github.com/swanson-stripe/synthetic-dataset
