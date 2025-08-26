#!/usr/bin/env python3
"""
Payment Data Metrics Visualizer

Formats raw payment/subscription data for data visualization tools.
Works with any JSON payment data and outputs chart-ready formats.

Usage:
    python format_metrics.py [optional_input_file.json]
"""

import json
import sys
import os
import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import argparse
from collections import defaultdict

# Third-party imports
try:
    import pandas as pd
    import numpy as np
    from faker import Faker
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Please install dependencies with: pip install -r requirements.txt")
    sys.exit(1)

# =============================================================================
# CONFIGURATION AND CONSTANTS
# =============================================================================

# Sample data configuration
SAMPLE_DATA_CONFIG = {
    'payment_count': 1000,
    'currencies': ['usd', 'eur', 'gbp'],
    'payment_methods': ['card', 'bank_transfer', 'digital_wallet', 'ach'],
    'failure_codes': ['insufficient_funds', 'card_declined', 'expired_card', 'processing_error', 'fraud_detected'],
    'success_rate': 0.95,
    'amount_range': (1000, 50000),  # cents
    'days_back': 90,
}

# Visualization color schemes
COLOR_SCHEMES = {
    'primary': ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4', '#84CC16', '#F97316'],
    'success': '#10B981',
    'error': '#EF4444',
    'warning': '#F59E0B',
    'info': '#3B82F6',
    'neutral': '#6B7280'
}

# Chart configuration
CHART_CONFIG = {
    'time_series_limit': 90,  # days
    'sparkline_points': 30,
    'table_page_size': 25,
    'top_customers_limit': 50,
    'recent_transactions_limit': 100,
}

# Initialize Faker
fake = Faker()
fake.seed_instance(42)
random.seed(42)
np.random.seed(42)

# =============================================================================
# INPUT HANDLER
# =============================================================================

def generate_sample_payment(payment_id: int, base_date: datetime) -> Dict[str, Any]:
    """Generate a single sample payment record."""
    # Generate timestamp within the last 90 days
    days_offset = random.randint(0, SAMPLE_DATA_CONFIG['days_back'])
    created_date = base_date - timedelta(days=days_offset)
    
    # Determine payment status
    is_successful = random.random() < SAMPLE_DATA_CONFIG['success_rate']
    
    # Generate amounts (higher amounts on weekends)
    is_weekend = created_date.weekday() >= 5
    amount_multiplier = 1.3 if is_weekend else 1.0
    base_amount = random.randint(*SAMPLE_DATA_CONFIG['amount_range'])
    amount = int(base_amount * amount_multiplier)
    
    payment = {
        'id': f"pi_{uuid.uuid4().hex[:24]}",
        'amount': amount,
        'currency': random.choice(SAMPLE_DATA_CONFIG['currencies']),
        'status': 'succeeded' if is_successful else 'failed',
        'created': int(created_date.timestamp()),
        'customer': f"cus_{uuid.uuid4().hex[:24]}",
        'payment_method': random.choice(SAMPLE_DATA_CONFIG['payment_methods']),
        'description': f"Payment #{payment_id}",
        'metadata': {
            'order_id': str(payment_id),
            'source': 'sample_data'
        }
    }
    
    # Add failure code if payment failed
    if not is_successful:
        payment['failure_code'] = random.choice(SAMPLE_DATA_CONFIG['failure_codes'])
    
    return payment

def load_payment_data(filepath: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Load payment data from file or generate sample data.
    
    Args:
        filepath: Path to JSON file containing payment data
        
    Returns:
        List of payment dictionaries
    """
    if filepath and os.path.exists(filepath):
        try:
            print(f"📁 Loading payment data from {filepath}...")
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Handle different data structures
            if isinstance(data, list):
                payments = data
            elif isinstance(data, dict):
                # Look for common payment data keys
                for key in ['payments', 'data', 'payment_intents', 'transactions']:
                    if key in data:
                        payments = data[key]
                        break
                else:
                    # If no standard key found, assume single payment object
                    payments = [data] if 'id' in data else []
            else:
                payments = []
            
            print(f"✅ Loaded {len(payments):,} payment records")
            return payments
            
        except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
            print(f"⚠️  Error loading {filepath}: {e}")
            print("🔄 Generating sample data instead...")
    
    # Generate sample data
    print(f"🎲 Generating {SAMPLE_DATA_CONFIG['payment_count']:,} sample payment records...")
    base_date = datetime.now()
    payments = []
    
    for i in range(SAMPLE_DATA_CONFIG['payment_count']):
        payment = generate_sample_payment(i + 1, base_date)
        payments.append(payment)
    
    print(f"✅ Generated {len(payments):,} sample payments")
    return payments

# =============================================================================
# METRIC CALCULATORS
# =============================================================================

def calculate_time_series_metrics(payments_df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate time series metrics for line/area charts."""
    print("📊 Calculating time series metrics...")
    
    # Convert timestamps to dates
    payments_df['date'] = pd.to_datetime(payments_df['created'], unit='s').dt.date
    payments_df['datetime'] = pd.to_datetime(payments_df['created'], unit='s')
    
    # Filter to last 90 days for performance
    cutoff_date = datetime.now() - timedelta(days=CHART_CONFIG['time_series_limit'])
    recent_payments = payments_df[payments_df['datetime'] >= cutoff_date].copy()
    
    # Group by date for daily metrics
    daily_metrics = recent_payments.groupby('date').agg({
        'amount': ['sum', 'count', 'mean'],
        'status': lambda x: (x == 'succeeded').sum() / len(x) * 100,
        'customer': 'nunique'
    }).reset_index()
    
    # Flatten column names
    daily_metrics.columns = ['date', 'volume', 'transaction_count', 'avg_amount', 'success_rate', 'unique_customers']
    daily_metrics = daily_metrics.sort_values('date')
    
    # Format for charts
    labels = [date.strftime('%Y-%m-%d') for date in daily_metrics['date']]
    
    # Calculate period comparison (current vs previous 30 days)
    current_period = recent_payments[recent_payments['datetime'] >= (datetime.now() - timedelta(days=30))]
    previous_period = recent_payments[
        (recent_payments['datetime'] >= (datetime.now() - timedelta(days=60))) &
        (recent_payments['datetime'] < (datetime.now() - timedelta(days=30)))
    ]
    
    # Payment Volume Chart
    volume_chart = {
        'type': 'line',
        'title': 'Daily Payment Volume',
        'labels': labels,
        'datasets': [
            {
                'label': 'Payment Volume',
                'data': [float(vol) / 100 for vol in daily_metrics['volume']],  # Convert to dollars
                'borderColor': COLOR_SCHEMES['primary'][0],
                'backgroundColor': COLOR_SCHEMES['primary'][0] + '20',
                'tension': 0.4,
                'fill': True
            }
        ],
        'options': {
            'scales': {
                'y': {
                    'beginAtZero': True,
                    'ticks': {'callback': 'currency'}
                }
            }
        }
    }
    
    # Success Rate Chart
    success_rate_chart = {
        'type': 'line',
        'title': 'Payment Success Rate',
        'labels': labels,
        'datasets': [
            {
                'label': 'Success Rate (%)',
                'data': [float(rate) for rate in daily_metrics['success_rate']],
                'borderColor': COLOR_SCHEMES['success'],
                'backgroundColor': COLOR_SCHEMES['success'] + '20',
                'tension': 0.4,
                'fill': True
            }
        ],
        'options': {
            'scales': {
                'y': {
                    'min': 80,
                    'max': 100,
                    'ticks': {'callback': 'percentage'}
                }
            }
        }
    }
    
    # Transaction Count Chart
    transaction_count_chart = {
        'type': 'bar',
        'title': 'Daily Transaction Count',
        'labels': labels,
        'datasets': [
            {
                'label': 'Transactions',
                'data': [int(count) for count in daily_metrics['transaction_count']],
                'backgroundColor': COLOR_SCHEMES['primary'][1] + '80',
                'borderColor': COLOR_SCHEMES['primary'][1],
                'borderWidth': 1
            }
        ],
        'options': {
            'scales': {
                'y': {
                    'beginAtZero': True
                }
            }
        }
    }
    
    # Period comparison data
    comparison_data = {
        'current_period': {
            'volume': float(current_period['amount'].sum() / 100),
            'transactions': int(current_period.shape[0]),
            'success_rate': float((current_period['status'] == 'succeeded').sum() / current_period.shape[0] * 100) if current_period.shape[0] > 0 else 0,
            'avg_amount': float(current_period['amount'].mean() / 100) if current_period.shape[0] > 0 else 0
        },
        'previous_period': {
            'volume': float(previous_period['amount'].sum() / 100),
            'transactions': int(previous_period.shape[0]),
            'success_rate': float((previous_period['status'] == 'succeeded').sum() / previous_period.shape[0] * 100) if previous_period.shape[0] > 0 else 0,
            'avg_amount': float(previous_period['amount'].mean() / 100) if previous_period.shape[0] > 0 else 0
        }
    }
    
    return {
        'charts': [volume_chart, success_rate_chart, transaction_count_chart],
        'comparison': comparison_data,
        'date_range': {
            'start': labels[0] if labels else None,
            'end': labels[-1] if labels else None,
            'total_days': len(labels)
        }
    }

def calculate_categorical_metrics(payments_df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate categorical metrics for bar/pie/donut charts."""
    print("📈 Calculating categorical metrics...")
    
    # Payment Method Distribution
    payment_methods = payments_df['payment_method'].value_counts()
    payment_method_chart = {
        'type': 'doughnut',
        'title': 'Payment Method Distribution',
        'labels': payment_methods.index.tolist(),
        'datasets': [{
            'data': payment_methods.values.tolist(),
            'backgroundColor': COLOR_SCHEMES['primary'][:len(payment_methods)],
            'borderWidth': 2,
            'borderColor': '#ffffff'
        }],
        'options': {
            'plugins': {
                'legend': {'position': 'right'}
            }
        }
    }
    
    # Currency Distribution
    currency_dist = payments_df['currency'].value_counts()
    currency_chart = {
        'type': 'pie',
        'title': 'Currency Distribution',
        'labels': [curr.upper() for curr in currency_dist.index.tolist()],
        'datasets': [{
            'data': currency_dist.values.tolist(),
            'backgroundColor': COLOR_SCHEMES['primary'][:len(currency_dist)],
            'borderWidth': 2,
            'borderColor': '#ffffff'
        }]
    }
    
    # Failure Reasons (for failed payments only)
    failed_payments = payments_df[payments_df['status'] != 'succeeded']
    if len(failed_payments) > 0 and 'failure_code' in failed_payments.columns:
        failure_reasons = failed_payments['failure_code'].value_counts()
        failure_chart = {
            'type': 'bar',
            'title': 'Payment Failure Reasons',
            'labels': failure_reasons.index.tolist(),
            'datasets': [{
                'label': 'Failed Payments',
                'data': failure_reasons.values.tolist(),
                'backgroundColor': COLOR_SCHEMES['error'] + '80',
                'borderColor': COLOR_SCHEMES['error'],
                'borderWidth': 1
            }],
            'options': {
                'indexAxis': 'y',
                'scales': {
                    'x': {
                        'beginAtZero': True
                    }
                }
            }
        }
    else:
        failure_chart = {
            'type': 'bar',
            'title': 'Payment Failure Reasons',
            'labels': ['No Failures'],
            'datasets': [{
                'label': 'Failed Payments',
                'data': [0],
                'backgroundColor': COLOR_SCHEMES['success'] + '80',
                'borderColor': COLOR_SCHEMES['success'],
                'borderWidth': 1
            }]
        }
    
    # Payment Volume by Currency
    currency_volume = payments_df.groupby('currency')['amount'].sum() / 100  # Convert to dollars
    currency_volume_chart = {
        'type': 'bar',
        'title': 'Payment Volume by Currency',
        'labels': [curr.upper() for curr in currency_volume.index.tolist()],
        'datasets': [{
            'label': 'Volume',
            'data': currency_volume.values.tolist(),
            'backgroundColor': COLOR_SCHEMES['primary'][2] + '80',
            'borderColor': COLOR_SCHEMES['primary'][2],
            'borderWidth': 1
        }],
        'options': {
            'scales': {
                'y': {
                    'beginAtZero': True,
                    'ticks': {'callback': 'currency'}
                }
            }
        }
    }
    
    return {
        'charts': [payment_method_chart, currency_chart, failure_chart, currency_volume_chart]
    }

def generate_metric_cards(payments_df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Generate KPI metric cards with sparklines and comparisons."""
    print("💳 Generating metric cards...")
    
    current_date = datetime.now()
    
    # Define periods
    current_period = payments_df[
        pd.to_datetime(payments_df['created'], unit='s') >= (current_date - timedelta(days=30))
    ]
    previous_period = payments_df[
        (pd.to_datetime(payments_df['created'], unit='s') >= (current_date - timedelta(days=60))) &
        (pd.to_datetime(payments_df['created'], unit='s') < (current_date - timedelta(days=30)))
    ]
    
    # Generate sparkline data (last 30 days)
    sparkline_df = payments_df[
        pd.to_datetime(payments_df['created'], unit='s') >= (current_date - timedelta(days=30))
    ].copy()
    sparkline_df['date'] = pd.to_datetime(sparkline_df['created'], unit='s').dt.date
    
    def calculate_change_percentage(current: float, previous: float) -> Tuple[float, str]:
        """Calculate percentage change and trend direction."""
        if previous == 0:
            return 0.0, 'neutral'
        change = ((current - previous) / previous) * 100
        trend = 'up' if change > 0 else 'down' if change < 0 else 'neutral'
        return change, trend
    
    # Total Volume Card
    current_volume = current_period['amount'].sum() / 100
    previous_volume = previous_period['amount'].sum() / 100
    volume_change, volume_trend = calculate_change_percentage(current_volume, previous_volume)
    
    volume_sparkline = sparkline_df.groupby('date')['amount'].sum().fillna(0).tolist()
    volume_sparkline = [float(v) / 100 for v in volume_sparkline[-30:]]  # Last 30 days
    
    volume_card = {
        'id': 'total_volume',
        'title': 'Total Volume',
        'value': current_volume,
        'format': 'currency',
        'change': volume_change,
        'trend': volume_trend,
        'sparkline': volume_sparkline,
        'description': 'Total payment volume (last 30 days)'
    }
    
    # Success Rate Card
    current_success_rate = (current_period['status'] == 'succeeded').sum() / len(current_period) * 100 if len(current_period) > 0 else 0
    previous_success_rate = (previous_period['status'] == 'succeeded').sum() / len(previous_period) * 100 if len(previous_period) > 0 else 0
    success_change, success_trend = calculate_change_percentage(current_success_rate, previous_success_rate)
    
    success_sparkline = sparkline_df.groupby('date')['status'].apply(
        lambda x: (x == 'succeeded').sum() / len(x) * 100 if len(x) > 0 else 0
    ).fillna(0).tolist()[-30:]
    
    success_card = {
        'id': 'success_rate',
        'title': 'Success Rate',
        'value': current_success_rate,
        'format': 'percentage',
        'change': success_change,
        'trend': success_trend,
        'sparkline': success_sparkline,
        'description': 'Payment success rate (last 30 days)'
    }
    
    # Average Transaction Card
    current_avg = current_period['amount'].mean() / 100 if len(current_period) > 0 else 0
    previous_avg = previous_period['amount'].mean() / 100 if len(previous_period) > 0 else 0
    avg_change, avg_trend = calculate_change_percentage(current_avg, previous_avg)
    
    avg_sparkline = sparkline_df.groupby('date')['amount'].mean().fillna(0).tolist()
    avg_sparkline = [float(v) / 100 for v in avg_sparkline[-30:]]
    
    avg_card = {
        'id': 'average_transaction',
        'title': 'Average Transaction',
        'value': current_avg,
        'format': 'currency',
        'change': avg_change,
        'trend': avg_trend,
        'sparkline': avg_sparkline,
        'description': 'Average payment amount (last 30 days)'
    }
    
    # Customer Count Card
    current_customers = current_period['customer'].nunique()
    previous_customers = previous_period['customer'].nunique()
    customers_change, customers_trend = calculate_change_percentage(current_customers, previous_customers)
    
    customers_sparkline = sparkline_df.groupby('date')['customer'].nunique().fillna(0).tolist()[-30:]
    
    customers_card = {
        'id': 'customer_count',
        'title': 'Active Customers',
        'value': current_customers,
        'format': 'number',
        'change': customers_change,
        'trend': customers_trend,
        'sparkline': customers_sparkline,
        'description': 'Unique customers (last 30 days)'
    }
    
    return [volume_card, success_card, avg_card, customers_card]

def format_table_data(payments_df: pd.DataFrame) -> Dict[str, Any]:
    """Format table data for paginated displays."""
    print("📋 Formatting table data...")
    
    # Recent Transactions Table
    recent_payments = payments_df.nlargest(CHART_CONFIG['recent_transactions_limit'], 'created').copy()
    recent_payments['datetime'] = pd.to_datetime(recent_payments['created'], unit='s')
    recent_payments['amount_dollars'] = recent_payments['amount'] / 100
    
    recent_transactions = {
        'title': 'Recent Transactions',
        'columns': [
            {'key': 'id', 'title': 'Payment ID', 'sortable': True, 'format': 'text'},
            {'key': 'datetime', 'title': 'Date', 'sortable': True, 'format': 'datetime'},
            {'key': 'amount_dollars', 'title': 'Amount', 'sortable': True, 'format': 'currency'},
            {'key': 'currency', 'title': 'Currency', 'sortable': True, 'format': 'text'},
            {'key': 'status', 'title': 'Status', 'sortable': True, 'format': 'status'},
            {'key': 'payment_method', 'title': 'Method', 'sortable': True, 'format': 'text'},
            {'key': 'customer', 'title': 'Customer', 'sortable': False, 'format': 'text'}
        ],
        'data': recent_payments[['id', 'datetime', 'amount_dollars', 'currency', 'status', 'payment_method', 'customer']].to_dict('records'),
        'pagination': {
            'page_size': CHART_CONFIG['table_page_size'],
            'total_records': len(recent_payments),
            'total_pages': (len(recent_payments) + CHART_CONFIG['table_page_size'] - 1) // CHART_CONFIG['table_page_size']
        }
    }
    
    # Top Customers by Spend
    customer_spend = payments_df[payments_df['status'] == 'succeeded'].groupby('customer').agg({
        'amount': ['sum', 'count'],
        'created': 'max'
    }).reset_index()
    customer_spend.columns = ['customer_id', 'total_spend', 'transaction_count', 'last_payment']
    customer_spend['total_spend_dollars'] = customer_spend['total_spend'] / 100
    customer_spend['last_payment_date'] = pd.to_datetime(customer_spend['last_payment'], unit='s')
    customer_spend = customer_spend.nlargest(CHART_CONFIG['top_customers_limit'], 'total_spend')
    
    top_customers = {
        'title': 'Top Customers by Spend',
        'columns': [
            {'key': 'customer_id', 'title': 'Customer ID', 'sortable': True, 'format': 'text'},
            {'key': 'total_spend_dollars', 'title': 'Total Spend', 'sortable': True, 'format': 'currency'},
            {'key': 'transaction_count', 'title': 'Transactions', 'sortable': True, 'format': 'number'},
            {'key': 'last_payment_date', 'title': 'Last Payment', 'sortable': True, 'format': 'datetime'}
        ],
        'data': customer_spend[['customer_id', 'total_spend_dollars', 'transaction_count', 'last_payment_date']].to_dict('records'),
        'pagination': {
            'page_size': CHART_CONFIG['table_page_size'],
            'total_records': len(customer_spend),
            'total_pages': (len(customer_spend) + CHART_CONFIG['table_page_size'] - 1) // CHART_CONFIG['table_page_size']
        }
    }
    
    # Failed Payments Table
    failed_payments = payments_df[payments_df['status'] != 'succeeded'].copy()
    if len(failed_payments) > 0:
        failed_payments['datetime'] = pd.to_datetime(failed_payments['created'], unit='s')
        failed_payments['amount_dollars'] = failed_payments['amount'] / 100
        failed_payments = failed_payments.nlargest(100, 'created')
        
        # Check if failure_code column exists
        columns_to_include = ['id', 'datetime', 'amount_dollars', 'customer', 'payment_method']
        table_columns = [
            {'key': 'id', 'title': 'Payment ID', 'sortable': True, 'format': 'text'},
            {'key': 'datetime', 'title': 'Date', 'sortable': True, 'format': 'datetime'},
            {'key': 'amount_dollars', 'title': 'Amount', 'sortable': True, 'format': 'currency'},
            {'key': 'customer', 'title': 'Customer', 'sortable': True, 'format': 'text'},
        ]
        
        if 'failure_code' in failed_payments.columns:
            columns_to_include.append('failure_code')
            table_columns.append({'key': 'failure_code', 'title': 'Failure Reason', 'sortable': True, 'format': 'text'})
        
        table_columns.append({'key': 'payment_method', 'title': 'Method', 'sortable': True, 'format': 'text'})
        
        failed_payments_table = {
            'title': 'Failed Payments',
            'columns': table_columns,
            'data': failed_payments[columns_to_include].fillna('Unknown').to_dict('records'),
            'pagination': {
                'page_size': CHART_CONFIG['table_page_size'],
                'total_records': len(failed_payments),
                'total_pages': (len(failed_payments) + CHART_CONFIG['table_page_size'] - 1) // CHART_CONFIG['table_page_size']
            }
        }
    else:
        failed_payments_table = {
            'title': 'Failed Payments',
            'columns': [],
            'data': [],
            'pagination': {'page_size': 0, 'total_records': 0, 'total_pages': 0}
        }
    
    return {
        'tables': [recent_transactions, top_customers, failed_payments_table]
    }

# =============================================================================
# OUTPUT GENERATOR
# =============================================================================

def save_formatted_data(time_series: Dict, categorical: Dict, metric_cards: List[Dict], 
                       table_data: Dict, output_dir: str) -> None:
    """Save all formatted data to JSON files."""
    print(f"💾 Saving formatted data to {output_dir}/...")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Custom JSON encoder for datetime objects
    def json_serializer(obj):
        if isinstance(obj, (datetime, pd.Timestamp)):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    # Time Series Charts
    with open(f'{output_dir}/time_series_charts.json', 'w') as f:
        json.dump(time_series, f, indent=2, default=json_serializer)
    
    # Categorical Charts
    with open(f'{output_dir}/categorical_charts.json', 'w') as f:
        json.dump(categorical, f, indent=2, default=json_serializer)
    
    # Metric Cards
    with open(f'{output_dir}/metric_cards.json', 'w') as f:
        json.dump({'cards': metric_cards}, f, indent=2, default=json_serializer)
    
    # Table Data
    with open(f'{output_dir}/table_data.json', 'w') as f:
        json.dump(table_data, f, indent=2, default=json_serializer)
    
    # Dashboard Configuration
    dashboard_config = {
        'layout': {
            'metric_cards': {
                'order': 1,
                'columns': 4,
                'height': 'auto'
            },
            'time_series_charts': {
                'order': 2,
                'columns': 2,
                'height': '400px'
            },
            'categorical_charts': {
                'order': 3,
                'columns': 2,
                'height': '300px'
            },
            'data_tables': {
                'order': 4,
                'columns': 1,
                'height': 'auto'
            }
        },
        'theme': {
            'primary_color': COLOR_SCHEMES['primary'][0],
            'success_color': COLOR_SCHEMES['success'],
            'error_color': COLOR_SCHEMES['error'],
            'warning_color': COLOR_SCHEMES['warning'],
            'font_family': 'Inter, -apple-system, BlinkMacSystemFont, sans-serif'
        },
        'features': {
            'real_time_updates': False,
            'export_enabled': True,
            'filters_enabled': True,
            'responsive_design': True
        },
        'generated_at': datetime.now().isoformat(),
        'data_summary': {
            'charts_count': len(time_series['charts']) + len(categorical['charts']),
            'metric_cards_count': len(metric_cards),
            'tables_count': len(table_data['tables'])
        }
    }
    
    with open(f'{output_dir}/dashboard_config.json', 'w') as f:
        json.dump(dashboard_config, f, indent=2, default=json_serializer)

# =============================================================================
# SAMPLE INPUT DATA GENERATOR
# =============================================================================

def create_sample_input_file(filepath: str) -> None:
    """Create a sample input file for testing."""
    print(f"📝 Creating sample input file: {filepath}")
    
    sample_payments = []
    base_date = datetime.now()
    
    # Generate 50 sample payments for demonstration
    for i in range(50):
        payment = generate_sample_payment(i + 1, base_date)
        sample_payments.append(payment)
    
    with open(filepath, 'w') as f:
        json.dump(sample_payments, f, indent=2)
    
    print(f"✅ Sample input file created with {len(sample_payments)} payments")

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description='Format payment data for visualization')
    parser.add_argument('input_file', nargs='?', help='JSON file containing payment data')
    parser.add_argument('--output-dir', default='formatted_output', help='Output directory for formatted data')
    parser.add_argument('--create-sample', action='store_true', help='Create sample input file')
    
    args = parser.parse_args()
    
    print("🎯 Payment Data Metrics Visualizer")
    print("=" * 50)
    
    # Create sample input file if requested
    if args.create_sample:
        create_sample_input_file('sample_input.json')
        return
    
    try:
        # Load payment data
        payments = load_payment_data(args.input_file)
        
        if not payments:
            print("❌ No payment data found or generated")
            return
        
        # Convert to DataFrame
        payments_df = pd.DataFrame(payments)
        
        # Validate required columns
        required_columns = ['id', 'amount', 'currency', 'status', 'created']
        missing_columns = [col for col in required_columns if col not in payments_df.columns]
        
        if missing_columns:
            print(f"❌ Missing required columns: {missing_columns}")
            return
        
        # Calculate metrics
        print("\n🔄 Processing payment data...")
        time_series_metrics = calculate_time_series_metrics(payments_df)
        categorical_metrics = calculate_categorical_metrics(payments_df)
        metric_cards = generate_metric_cards(payments_df)
        table_data = format_table_data(payments_df)
        
        # Save formatted data
        save_formatted_data(
            time_series_metrics, 
            categorical_metrics, 
            metric_cards, 
            table_data, 
            args.output_dir
        )
        
        # Print validation summary
        print("\n" + "=" * 60)
        print("📊 PAYMENT METRICS FORMATTING COMPLETE")
        print("=" * 60)
        print(f"Number of payments processed: {len(payments_df):,}")
        print(f"Number of time series charts generated: {len(time_series_metrics['charts'])}")
        print(f"Number of categorical charts generated: {len(categorical_metrics['charts'])}")
        print(f"Number of metric cards generated: {len(metric_cards)}")
        print(f"Number of data tables generated: {len(table_data['tables'])}")
        print(f"Output directory location: {os.path.abspath(args.output_dir)}")
        
        # Data insights
        successful_payments = payments_df[payments_df['status'] == 'succeeded']
        print(f"\n📈 Data Insights:")
        print(f"Success rate: {len(successful_payments) / len(payments_df) * 100:.1f}%")
        print(f"Total volume: ${successful_payments['amount'].sum() / 100:,.2f}")
        print(f"Average transaction: ${payments_df['amount'].mean() / 100:.2f}")
        print(f"Date range: {pd.to_datetime(payments_df['created'], unit='s').min().date()} to {pd.to_datetime(payments_df['created'], unit='s').max().date()}")
        
        currencies = payments_df['currency'].value_counts()
        print(f"Currencies: {', '.join([f'{curr.upper()}: {count}' for curr, count in currencies.head(3).items()])}")
        
        payment_methods = payments_df['payment_method'].value_counts()
        print(f"Top payment methods: {', '.join([f'{method}: {count}' for method, count in payment_methods.head(3).items()])}")
        
        print(f"\n✅ Visualization data ready!")
        print(f"🔗 Import the JSON files into your preferred visualization tool")
        
    except Exception as e:
        print(f"❌ Error during processing: {str(e)}")
        raise

if __name__ == "__main__":
    main()
