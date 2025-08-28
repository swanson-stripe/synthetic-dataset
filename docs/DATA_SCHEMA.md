# Data Schema Reference

Complete reference for all data structures in the Dashboard Synthetic Data system.

## 🏢 Business Personas

### Available Personas:
| ID | Name | Business Model | Description |
|---|---|---|---|
| `modaic` | Modaic | E-commerce | Fashion retailer with global payments |
| `mindora` | Mindora | Education | Online education marketplace |
| `keynest` | Keynest | Property | Property management platform |
| `pulseon` | Pulseon | Subscription | Fitness subscription platform |
| `fluxly` | Fluxly | Creator Economy | Content monetization platform |
| `brightfund` | Brightfund | Non-profit | Fundraising and donation platform |
| `procura` | Procura | B2B | Medical supply marketplace |
| `stratus` | Stratus | SaaS | Cloud infrastructure platform |
| `forksy` | Forksy | Marketplace | Food delivery marketplace |

### Business Stages:
- `early` - Early-stage business (30% of growth metrics)
- `growth` - Growth-stage business (100% of base metrics)
- `mature` - Mature business (280% of growth metrics)

## 📊 Core Data Objects

### Metrics
```typescript
interface Metric {
    label: string;          // Display name (e.g., "Total Revenue")
    value: string;          // Pre-formatted display value (e.g., "$2,145,623.45")
    rawValue: number;       // Raw value for calculations (e.g., 214562345 cents)
}

// Example
[
    {
        "label": "Total Revenue",
        "value": "$2,145,623.45",
        "rawValue": 214562345
    },
    {
        "label": "Conversion Rate", 
        "value": "3.15%",
        "rawValue": 0.0315
    }
]
```

### Payments
```typescript
interface Payment {
    id: string;             // Format: py_[14-char string]
    amount: number;         // Amount in cents (e.g., 5000 = $50.00)
    currency: string;       // Always "usd"
    status: "succeeded" | "pending" | "failed";
    created: number;        // Unix timestamp
    description: string;    // Business-specific description
    customer: string;       // Customer ID (format: cus_[14-char string])
    metadata: object;       // Persona-specific metadata
}

// Example
{
    "id": "py_1234567890abcd",
    "amount": 5000,
    "currency": "usd",
    "status": "succeeded", 
    "created": 1640995200,
    "description": "Fashion purchase",
    "customer": "cus_9876543210wxyz",
    "metadata": {
        "product_category": "clothing",
        "size": "M",
        "color": "blue"
    }
}
```

### Customers
```typescript
interface Customer {
    id: string;             // Format: cus_[14-char string]
    email: string;          // Valid email address
    name: string;           // Customer display name
    created: number;        // Unix timestamp
    metadata: object;       // Persona-specific metadata
}

// Example
{
    "id": "cus_9876543210wxyz",
    "email": "customer@example.com",
    "name": "John Doe",
    "created": 1640995200,
    "metadata": {
        "customer_segment": "premium",
        "preferred_size": "M"
    }
}
```

### Connected Accounts (Marketplace businesses)
```typescript
interface ConnectedAccount {
    id: string;             // Format: acct_[14-char string]
    type: string;           // Usually "express"
    country: string;        // Country code (e.g., "US")
    email: string;          // Account email
    created: number;        // Unix timestamp
    metadata: object;       // Persona-specific metadata
}

// Example
{
    "id": "acct_1234567890abcd",
    "type": "express",
    "country": "US",
    "email": "seller@example.com",
    "created": 1640995200,
    "metadata": {
        "instructor_specialty": "data_science",
        "experience_years": "5"
    }
}
```

### Transfers
```typescript
interface Transfer {
    id: string;             // Format: tr_[14-char string]
    amount: number;         // Amount in cents
    currency: string;       // Always "usd"
    created: number;        // Unix timestamp
    destination: string | null; // Destination account ID (null for platform transfers)
    metadata: object;       // Persona-specific metadata
}

// Example
{
    "id": "tr_1234567890abcd",
    "amount": 30000,
    "currency": "usd",
    "created": 1640995200,
    "destination": "acct_9876543210wxyz",
    "metadata": {
        "transfer_type": "instructor_payout",
        "course_earnings": "true"
    }
}
```

### Balances
```typescript
interface Balance {
    available: BalanceAmount[];
    pending: BalanceAmount[];
}

interface BalanceAmount {
    amount: number;         // Amount in cents
    currency: string;       // Always "usd"
}

// Example
{
    "available": [
        {
            "amount": 10000000,
            "currency": "usd"
        }
    ],
    "pending": [
        {
            "amount": 200000,
            "currency": "usd"
        }
    ]
}
```

### Subscriptions (Subscription businesses)
```typescript
interface Subscription {
    id: string;             // Format: sub_[14-char string]
    status: "active" | "trialing" | "canceled" | "past_due";
    current_period_start: number; // Unix timestamp
    current_period_end: number;   // Unix timestamp
    customer: string;       // Customer ID
    metadata: object;       // Persona-specific metadata
}

// Example
{
    "id": "sub_1234567890abcd",
    "status": "active",
    "current_period_start": 1640995200,
    "current_period_end": 1643673600,
    "customer": "cus_9876543210wxyz",
    "metadata": {
        "plan_name": "premium",
        "features": "unlimited_classes"
    }
}
```

### Invoices (B2B businesses)
```typescript
interface Invoice {
    id: string;             // Format: in_[14-char string]
    amount_paid: number;    // Amount in cents
    currency: string;       // Always "usd"
    status: "paid" | "open" | "draft" | "void";
    created: number;        // Unix timestamp
    customer: string;       // Customer ID
    metadata: object;       // Persona-specific metadata
}

// Example
{
    "id": "in_1234567890abcd",
    "amount_paid": 80000,
    "currency": "usd",
    "status": "paid",
    "created": 1640995200,
    "customer": "cus_9876543210wxyz",
    "metadata": {
        "invoice_type": "bulk_order",
        "net_terms": "30"
    }
}
```

### Issuing Cards (Some businesses)
```typescript
interface IssuingCard {
    id: string;             // Format: ic_[14-char string]
    status: "active" | "inactive" | "canceled";
    type: string;           // Usually "virtual"
    brand: string;          // Card brand (e.g., "visa")
    created: number;        // Unix timestamp
    metadata: object;       // Persona-specific metadata
}

// Example
{
    "id": "ic_1234567890abcd",
    "status": "active",
    "type": "virtual",
    "brand": "visa",
    "created": 1640995200,
    "metadata": {
        "card_purpose": "delivery_payments",
        "driver_id": "driver_123"
    }
}
```

## 🎯 Persona-Specific Metrics

### Modaic (Fashion E-commerce)
```javascript
[
    { label: "Total Revenue", value: "$2,145,623.45", rawValue: 214562345 },
    { label: "New Customers", value: "1,247", rawValue: 1247 },
    { label: "Average Order Value", value: "$89.32", rawValue: 8932 },
    { label: "Conversion Rate", value: "3.15%", rawValue: 0.0315 }
]
```

### Mindora (Online Education)
```javascript
[
    { label: "Gross Volume", value: "$1,987,234.56", rawValue: 198723456 },
    { label: "Total Payments", value: "45,123", rawValue: 45123 },
    { label: "Total Customers", value: "12,456", rawValue: 12456 },
    { label: "Retention Rate", value: "87.65%", rawValue: 0.8765 }
]
```

### Keynest (Property Management)
```javascript
[
    { label: "Total Revenue", value: "$892,456.78", rawValue: 89245678 },
    { label: "Connected Accounts", value: "342", rawValue: 342 },
    { label: "Total Customers", value: "1,234", rawValue: 1234 },
    { label: "Average Order Value", value: "$723.45", rawValue: 72345 }
]
```

### Pulseon (Fitness Subscriptions)
```javascript
[
    { label: "Total Revenue", value: "$1,456,789.23", rawValue: 145678923 },
    { label: "Active Subscribers", value: "8,945", rawValue: 8945 },
    { label: "Average Order Value", value: "$49.99", rawValue: 4999 },
    { label: "Churn Rate", value: "5.23%", rawValue: 0.0523 }
]
```

### And so on for each persona...

## 🔍 Data Access Methods

### Available Methods:
```javascript
// Get formatted metrics for current persona
kit.getMetrics() → Metric[]

// Get raw data by type
kit.getData('payments') → Payment[]
kit.getData('customers') → Customer[]
kit.getData('connected_accounts') → ConnectedAccount[]
kit.getData('transfers') → Transfer[]
kit.getData('balances') → Balance
kit.getData('subscriptions') → Subscription[]
kit.getData('invoices') → Invoice[]
kit.getData('issuing_cards') → IssuingCard[]

// Get current state
kit.getCurrentPersona() → string
kit.getCurrentStage() → string
kit.getAvailablePersonas() → PersonaMap

// Control
kit.switchPersona(personaId: string, stage?: string) → void
```

## 🚫 Data Constraints

### Immutable Fields:
- All `id` fields follow specific formats
- `amount` fields are always in cents
- `currency` is always "usd"
- `created` timestamps are Unix timestamps
- Status fields have predefined enum values

### Never Modify:
- Don't change the data structure
- Don't convert amounts from cents to dollars in the data
- Don't cache data manually (kit handles this)
- Don't create custom ID formats

### Always Use:
- `kit.getMetrics()` for display metrics
- `kit.getData(type)` for raw data
- Provided formatting utilities for display
- The persona switching methods for state changes
