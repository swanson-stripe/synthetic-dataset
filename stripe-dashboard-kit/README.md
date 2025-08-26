# @stripe-synthetic/dashboard-kit

A complete React component library for rendering Stripe-style payment analytics dashboards. Consumes formatted metrics data and provides beautiful, responsive dashboard components out of the box.

## 🚀 Quick Start

```bash
npm install @stripe-synthetic/dashboard-kit
```

```jsx
import { Dashboard } from '@stripe-synthetic/dashboard-kit';
import '@stripe-synthetic/dashboard-kit/dist/dashboard-kit.css';

function App() {
  return (
    <Dashboard 
      dataSource="/api/metrics"
      title="Payment Analytics"
      theme="light"
    />
  );
}
```

## 📦 What's Included

- **Dashboard**: Complete dashboard with automatic layout
- **MetricCard**: KPI cards with sparklines and trends  
- **LineChart**: Time series charts with multiple lines
- **BarChart**: Bar, pie, and doughnut charts
- **DataTable**: Sortable, paginated data tables
- **Hooks**: `useMetrics` and `useDataLoader` for data management
- **Utilities**: Formatting functions for currency, dates, numbers
- **TypeScript**: Full TypeScript support with detailed types

## 🎨 Components

### Dashboard (Complete Solution)

The main component that renders a complete dashboard:

```jsx
import { Dashboard } from '@stripe-synthetic/dashboard-kit';

<Dashboard
  dataSource="/api/formatted-metrics"
  title="Payment Analytics Dashboard"
  layout="stripe"
  theme="light"
  refreshInterval={30000}
  onError={(error) => console.error(error)}
/>
```

**Props:**
- `dataSource`: URL string or async function returning metrics data
- `layout`: `'stripe' | 'custom'` - predefined layouts
- `theme`: `'light' | 'dark'` - color scheme
- `refreshInterval`: Auto-refresh interval in milliseconds
- `onError`: Error callback function

### MetricCard (KPI Cards)

Individual metric cards with sparklines:

```jsx
import { MetricCard } from '@stripe-synthetic/dashboard-kit';

<MetricCard
  title="Total Revenue"
  value={125000}
  format="currency"
  change={5.2}
  changeLabel="vs last month"
  sparkline={[100, 120, 115, 130, 125]}
  description="Gross payment volume"
/>
```

**Props:**
- `title`: Card title
- `value`: Numeric value to display
- `format`: `'currency' | 'percentage' | 'number'`
- `change`: Percentage change (optional)
- `sparkline`: Array of numbers for mini chart (optional)
- `loading`: Show loading skeleton (optional)

### LineChart (Time Series)

Multi-line charts for time series data:

```jsx
import { LineChart } from '@stripe-synthetic/dashboard-kit';

const data = [
  { date: '2024-01-01', revenue: 1000, orders: 50 },
  { date: '2024-01-02', revenue: 1200, orders: 60 },
  // ...
];

<LineChart
  data={data}
  lines={[
    { dataKey: 'revenue', stroke: '#3B82F6', name: 'Revenue' },
    { dataKey: 'orders', stroke: '#10B981', name: 'Orders' }
  ]}
  xAxisKey="date"
  xAxisFormat="date"
  yAxisFormat="currency"
  height={350}
  title="Revenue Trends"
/>
```

### BarChart (Categorical Data)

Bar, pie, and doughnut charts:

```jsx
import { BarChart } from '@stripe-synthetic/dashboard-kit';

const data = [
  { name: 'Card', value: 450 },
  { name: 'Bank Transfer', value: 230 },
  { name: 'Digital Wallet', value: 180 }
];

<BarChart
  data={data}
  dataKey="value"
  type="doughnut"
  title="Payment Methods"
  colors={['#3B82F6', '#10B981', '#F59E0B']}
/>
```

### DataTable (Tabular Data)

Sortable, paginated tables:

```jsx
import { DataTable } from '@stripe-synthetic/dashboard-kit';

const columns = [
  { key: 'id', title: 'Payment ID', sortable: true, format: 'text' },
  { key: 'amount', title: 'Amount', sortable: true, format: 'currency' },
  { key: 'status', title: 'Status', sortable: true, format: 'status' },
  { key: 'created', title: 'Date', sortable: true, format: 'datetime' }
];

<DataTable
  columns={columns}
  data={transactions}
  pageSize={25}
  title="Recent Transactions"
  onRowClick={(row) => console.log(row)}
/>
```

## 🔧 Hooks

### useMetrics

Load and process metrics data:

```jsx
import { useMetrics } from '@stripe-synthetic/dashboard-kit';

function CustomDashboard() {
  const {
    data,
    loading,
    error,
    refresh,
    metricCards,
    timeSeriesCharts,
    categoricalCharts,
    dataTables
  } = useMetrics('/api/metrics', {
    refreshInterval: 60000,
    onError: (error) => console.error(error),
    onLoad: (data) => console.log('Data loaded:', data)
  });

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      {metricCards.map(card => (
        <MetricCard key={card.id} {...card} />
      ))}
    </div>
  );
}
```

### useDataLoader

Generic data loading hook:

```jsx
import { useDataLoader } from '@stripe-synthetic/dashboard-kit';

const { data, loading, error, refresh } = useDataLoader(
  async () => {
    const response = await fetch('/api/custom-data');
    return response.json();
  },
  30000, // refresh interval
  (rawData) => transformData(rawData) // transform function
);
```

## 🎯 Data Format

The library expects data in the format output by the `format_metrics.py` script:

### Metric Cards
```json
{
  "cards": [
    {
      "id": "total_volume",
      "title": "Total Volume",
      "value": 125000,
      "format": "currency",
      "change": 5.2,
      "trend": "up",
      "sparkline": [100, 120, 115, 130, 125],
      "description": "Total payment volume (last 30 days)"
    }
  ]
}
```

### Charts
```json
{
  "charts": [
    {
      "type": "line",
      "title": "Daily Payment Volume",
      "labels": ["2024-01-01", "2024-01-02", "2024-01-03"],
      "datasets": [{
        "label": "Volume",
        "data": [1000, 1200, 1100],
        "borderColor": "#3B82F6",
        "backgroundColor": "#3B82F620"
      }]
    }
  ]
}
```

### Tables
```json
{
  "tables": [
    {
      "title": "Recent Transactions",
      "columns": [
        {"key": "id", "title": "ID", "sortable": true, "format": "text"},
        {"key": "amount", "title": "Amount", "sortable": true, "format": "currency"}
      ],
      "data": [
        {"id": "pi_123", "amount": 2500},
        {"id": "pi_456", "amount": 3000}
      ],
      "pagination": {
        "page_size": 25,
        "total_records": 100,
        "total_pages": 4
      }
    }
  ]
}
```

## 🔨 Utilities

### Formatting Functions

```jsx
import {
  formatCurrency,
  formatPercentage,
  formatNumber,
  formatDateTime,
  formatValue
} from '@stripe-synthetic/dashboard-kit';

formatCurrency(250000);      // "$2,500.00"
formatPercentage(5.25);      // "5.3%"
formatNumber(1234567);       // "1,234,567"
formatDateTime(1640995200);  // "Jan 01, 2022"
formatValue(1500, 'currency'); // "$15.00"
```

### Data Processing

```jsx
import { formatChange, truncate } from '@stripe-synthetic/dashboard-kit';

formatChange(5.2);   // { formatted: "+5.2%", className: "positive", trend: "up" }
truncate("Long text here", 10); // "Long te..."
```

## 🎨 Theming

### CSS Variables

Customize the appearance using CSS variables:

```css
:root {
  --sdk-color-primary: #your-brand-color;
  --sdk-color-success: #your-success-color;
  --sdk-bg-primary: #your-background;
  --sdk-font-family: 'Your Font', sans-serif;
}
```

### Dark Mode

```jsx
<Dashboard 
  dataSource="/api/metrics"
  theme="dark"
/>
```

Or apply the dark theme class:

```css
.my-dashboard {
  /* Apply dark theme */
}
```

## 📱 Responsive Design

All components are fully responsive and work on:
- Desktop (1200px+)
- Tablet (768px - 1199px)  
- Mobile (320px - 767px)

The layout automatically adapts:
- Metric cards stack on smaller screens
- Charts resize responsively
- Tables scroll horizontally on mobile
- Pagination controls stack vertically

## 🛠️ Development

### Building the Library

```bash
npm install
npm run build
```

This creates the `dist/` folder with:
- `index.js` - CommonJS bundle
- `index.esm.js` - ES modules bundle
- `index.d.ts` - TypeScript declarations
- `dashboard-kit.css` - Bundled styles

### Development Mode

```bash
npm run dev
```

Runs Rollup in watch mode for development.

## 🔗 Integration Examples

### Next.js

```jsx
// pages/dashboard.js
import { Dashboard } from '@stripe-synthetic/dashboard-kit';
import '@stripe-synthetic/dashboard-kit/dist/dashboard-kit.css';

export default function DashboardPage() {
  return (
    <Dashboard 
      dataSource="/api/metrics"
      title="Payment Analytics"
    />
  );
}
```

### React App

```jsx
// App.js
import React from 'react';
import { Dashboard } from '@stripe-synthetic/dashboard-kit';
import '@stripe-synthetic/dashboard-kit/dist/dashboard-kit.css';

function App() {
  return (
    <div className="App">
      <Dashboard 
        dataSource={async () => {
          const response = await fetch('/api/metrics');
          return response.json();
        }}
      />
    </div>
  );
}
```

### Custom Dashboard

```jsx
import {
  useMetrics,
  MetricCard,
  LineChart,
  DataTable
} from '@stripe-synthetic/dashboard-kit';

function CustomDashboard() {
  const { metricCards, timeSeriesCharts, dataTables, loading } = useMetrics('/api/metrics');

  if (loading) return <div>Loading...</div>;

  return (
    <div className="custom-dashboard">
      <div className="metrics-grid">
        {metricCards.map(card => (
          <MetricCard key={card.id} {...card} />
        ))}
      </div>
      
      <div className="charts-section">
        {timeSeriesCharts.map((chart, index) => (
          <LineChart
            key={index}
            data={chart.data}
            lines={chart.lines}
            title={chart.title}
          />
        ))}
      </div>
      
      <div className="tables-section">
        {dataTables.map((table, index) => (
          <DataTable
            key={index}
            {...table}
          />
        ))}
      </div>
    </div>
  );
}
```

## 📋 Requirements

- React ^18.0.0
- react-dom ^18.0.0

## 📄 License

MIT

---

**Built for the Stripe synthetic dataset ecosystem. Perfect for payment analytics, financial dashboards, and data visualization projects.**
