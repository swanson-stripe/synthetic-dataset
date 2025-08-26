# Payment Data Metrics Visualizer

A standalone Python script that transforms raw payment/subscription data into visualization-ready formats. Works with any JSON payment data and outputs chart-ready data for popular visualization libraries like Chart.js, D3, Plotly, or custom dashboards.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Use with your own data file
python format_metrics.py your_payments.json

# Generate sample data automatically
python format_metrics.py

# Create a sample input file
python format_metrics.py --create-sample

# Specify custom output directory
python format_metrics.py data.json --output-dir custom_output
```

## 📁 Directory Structure

```
/metrics_visualizer/
├── format_metrics.py          # Main script (complete standalone)
├── sample_input.json          # Example data for testing
├── requirements.txt           # Python dependencies
└── /formatted_output/         # Visualization-ready data
    ├── time_series_charts.json
    ├── categorical_charts.json
    ├── metric_cards.json
    ├── table_data.json
    └── dashboard_config.json
```

## 📊 Input Data Format

The script accepts any JSON file containing payment data. It automatically detects and handles various data structures:

### Direct Array Format
```json
[
  {
    "id": "pi_1ABC123...",
    "amount": 2599,
    "currency": "usd", 
    "status": "succeeded",
    "created": 1693929600,
    "customer": "cus_ABC123...",
    "payment_method": "card"
  }
]
```

### Nested Object Format
```json
{
  "payments": [...],     // or
  "data": [...],         // or
  "payment_intents": [...],
  "transactions": [...]
}
```

### Required Fields
- `id`: Payment identifier
- `amount`: Amount in cents (integer)
- `currency`: Currency code (string)
- `status`: Payment status ("succeeded", "failed", etc.)
- `created`: Unix timestamp (integer)

### Optional Fields
- `customer`: Customer identifier
- `payment_method`: Payment method type
- `failure_code`: Failure reason (for failed payments)
- `description`: Payment description
- `metadata`: Additional data object

## 📈 Generated Visualizations

### 1. Time Series Charts (`time_series_charts.json`)

#### Daily Payment Volume
```json
{
  "type": "line",
  "title": "Daily Payment Volume",
  "labels": ["2023-08-01", "2023-08-02", ...],
  "datasets": [{
    "label": "Payment Volume",
    "data": [12450.50, 15230.75, ...],
    "borderColor": "#3B82F6",
    "backgroundColor": "#3B82F620"
  }]
}
```

#### Payment Success Rate
```json
{
  "type": "line", 
  "title": "Payment Success Rate",
  "labels": ["2023-08-01", "2023-08-02", ...],
  "datasets": [{
    "label": "Success Rate (%)",
    "data": [98.5, 97.2, 99.1, ...],
    "borderColor": "#10B981"
  }]
}
```

#### Daily Transaction Count
```json
{
  "type": "bar",
  "title": "Daily Transaction Count", 
  "datasets": [{
    "label": "Transactions",
    "data": [145, 167, 132, ...],
    "backgroundColor": "#10B98180"
  }]
}
```

### 2. Categorical Charts (`categorical_charts.json`)

#### Payment Method Distribution (Doughnut)
```json
{
  "type": "doughnut",
  "title": "Payment Method Distribution",
  "labels": ["card", "digital_wallet", "bank_transfer"],
  "datasets": [{
    "data": [450, 230, 120],
    "backgroundColor": ["#3B82F6", "#10B981", "#F59E0B"]
  }]
}
```

#### Currency Distribution (Pie)
#### Payment Failure Reasons (Bar)
#### Payment Volume by Currency (Bar)

### 3. Metric Cards (`metric_cards.json`)

```json
{
  "cards": [
    {
      "id": "total_volume",
      "title": "Total Volume",
      "value": 91907.62,
      "format": "currency",
      "change": -3.99,
      "trend": "down",
      "sparkline": [1879.31, 3134.55, 2601.04, ...],
      "description": "Total payment volume (last 30 days)"
    },
    {
      "id": "success_rate", 
      "title": "Success Rate",
      "value": 94.41,
      "format": "percentage",
      "change": 0.09,
      "trend": "up",
      "sparkline": [94.2, 95.1, 93.8, ...],
      "description": "Payment success rate (last 30 days)"
    }
  ]
}
```

Available metric cards:
- **Total Volume**: Payment volume with currency formatting
- **Success Rate**: Success percentage with trend indicators  
- **Average Transaction**: Average payment amount
- **Active Customers**: Unique customer count

### 4. Data Tables (`table_data.json`)

#### Recent Transactions
```json
{
  "title": "Recent Transactions",
  "columns": [
    {"key": "id", "title": "Payment ID", "sortable": true, "format": "text"},
    {"key": "datetime", "title": "Date", "sortable": true, "format": "datetime"},
    {"key": "amount_dollars", "title": "Amount", "sortable": true, "format": "currency"}
  ],
  "data": [...],
  "pagination": {
    "page_size": 25,
    "total_records": 100,
    "total_pages": 4
  }
}
```

Available tables:
- **Recent Transactions**: Latest 100 payments
- **Top Customers by Spend**: Highest-value customers
- **Failed Payments**: Failed payment analysis

### 5. Dashboard Configuration (`dashboard_config.json`)

```json
{
  "layout": {
    "metric_cards": {"order": 1, "columns": 4, "height": "auto"},
    "time_series_charts": {"order": 2, "columns": 2, "height": "400px"},
    "categorical_charts": {"order": 3, "columns": 2, "height": "300px"},
    "data_tables": {"order": 4, "columns": 1, "height": "auto"}
  },
  "theme": {
    "primary_color": "#3B82F6",
    "success_color": "#10B981",
    "error_color": "#EF4444"
  },
  "features": {
    "real_time_updates": false,
    "export_enabled": true,
    "filters_enabled": true
  }
}
```

## 🔧 Command Line Options

```bash
# Basic usage
python format_metrics.py [input_file.json]

# With custom output directory  
python format_metrics.py data.json --output-dir custom_folder

# Create sample input file
python format_metrics.py --create-sample

# Help and options
python format_metrics.py --help
```

### Arguments
- `input_file` (optional): Path to JSON file with payment data
- `--output-dir`: Custom output directory (default: `formatted_output`)
- `--create-sample`: Generate `sample_input.json` file for testing

### Behavior
- If no input file specified: Generates 1,000 sample payment records automatically
- If input file not found: Falls back to generating sample data
- If input file has wrong format: Displays error and generates sample data

## 🎨 Integration Examples

### Chart.js Integration
```javascript
// Load time series data
fetch('formatted_output/time_series_charts.json')
  .then(response => response.json())
  .then(data => {
    const chart = new Chart(ctx, data.charts[0]);
  });
```

### React Dashboard
```jsx
import { useEffect, useState } from 'react';

function Dashboard() {
  const [metrics, setMetrics] = useState(null);
  
  useEffect(() => {
    fetch('/formatted_output/metric_cards.json')
      .then(res => res.json())
      .then(data => setMetrics(data.cards));
  }, []);
  
  return (
    <div className="dashboard">
      {metrics?.map(card => (
        <MetricCard key={card.id} {...card} />
      ))}
    </div>
  );
}
```

### D3.js Visualization
```javascript
d3.json('formatted_output/categorical_charts.json').then(data => {
  const chartConfig = data.charts[0]; // Payment method distribution
  // Use chartConfig.labels and chartConfig.datasets[0].data
});
```

## 📦 Data Compatibility

### Works With
- ✅ **Stripe Payments**: Direct integration with Stripe payment data
- ✅ **Custom Payment Systems**: Any system outputting JSON payment data  
- ✅ **TechStyle Generator**: E-commerce payment data
- ✅ **CloudFlow Generator**: SaaS subscription data (converted to payments)
- ✅ **LocalBites Generator**: Marketplace payment data
- ✅ **Multiple Currencies**: Automatic currency handling
- ✅ **Large Datasets**: Optimized for 100K+ payment records

### Generated Sample Data
When no input file is provided, generates realistic sample data with:
- 1,000 payment records across 90 days
- 95% success rate (configurable)
- Multiple currencies (USD, EUR, GBP)
- Various payment methods
- Realistic failure codes
- Weekend volume variations

## 🔍 Data Insights

The script automatically calculates and displays:
- Total payments processed
- Success rate percentage  
- Total payment volume
- Average transaction amount
- Date range coverage
- Currency distribution
- Top payment methods
- Failed payment analysis

## 🎯 Use Cases

1. **Business Intelligence Dashboards**: Import formatted data into BI tools
2. **Payment Analytics**: Analyze payment trends and success rates  
3. **Financial Reporting**: Generate executive summaries and KPIs
4. **A/B Testing**: Compare payment performance across different periods
5. **Customer Insights**: Understand customer payment behaviors
6. **Fraud Detection**: Analyze failure patterns and suspicious activity
7. **Performance Monitoring**: Track payment system health over time

## 🛠️ Technical Details

### Performance
- Handles 100K+ payment records efficiently
- Uses pandas for fast data processing
- Optimized time series calculations
- Memory-efficient data structures

### Dependencies
- `pandas`: Data manipulation and analysis
- `numpy`: Numerical computations
- `faker`: Sample data generation

### Output Format
- Pure JSON files (no proprietary formats)
- Compatible with all major visualization libraries
- Includes metadata and configuration
- Human-readable structure

### Error Handling
- Graceful fallback to sample data generation
- Validates required data fields
- Handles missing optional fields
- Provides detailed error messages

## 📚 Example Output

Running with 1,000 sample payments:
```
🎯 Payment Data Metrics Visualizer
==================================================
🎲 Generating 1,000 sample payment records...
✅ Generated 1,000 sample payments

📊 PAYMENT METRICS FORMATTING COMPLETE  
==================================================
Number of payments processed: 1,000
Number of time series charts generated: 3
Number of categorical charts generated: 4
Number of metric cards generated: 4
Number of data tables generated: 3

📈 Data Insights:
Success rate: 95.2%
Total volume: $268,517.38
Average transaction: $283.46
Currencies: GBP: 353, USD: 333, EUR: 314
Top payment methods: card: 271, ach: 252, digital_wallet: 239

✅ Visualization data ready!
```

---

**Ready to visualize your payment data? Run the script and import the JSON files into your favorite visualization tool!**
