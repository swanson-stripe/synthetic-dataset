#!/usr/bin/env python3
"""
MedSupply Pro Synthetic Stripe B2B Data Generator

Generates realistic B2B medical equipment wholesaler data with net terms,
high-value transactions, purchase orders, and B2B payment patterns.

Usage:
    python generate_medsupply.py
"""

import json
import random
import uuid
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional
import os
import sys
from collections import defaultdict
import calendar

# Third-party imports
try:
    from faker import Faker
    import pandas as pd
    import numpy as np
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Please install dependencies with: pip install -r requirements.txt")
    sys.exit(1)

# =============================================================================
# CONFIGURATION & CONSTANTS
# =============================================================================

# B2B business configuration
BUSINESS_CONFIG = {
    'payment_terms': {
        'net_30': 0.5,  # 50% of clients on NET-30
        'net_60': 0.3,  # 30% on NET-60
        'net_90': 0.2   # 20% on NET-90
    },
    'volume_discounts': [
        {'min': 0, 'max': 10000, 'discount': 0},           # No discount under $10K
        {'min': 10000, 'max': 50000, 'discount': 0.05},    # 5% discount $10K-$50K
        {'min': 50000, 'max': 100000, 'discount': 0.10},   # 10% discount $50K-$100K
        {'min': 100000, 'max': None, 'discount': 0.15}     # 15% discount over $100K
    ],
    'credit_limits': {
        'startup': 25000,      # $25K for startups
        'established': 100000,  # $100K for established
        'enterprise': 500000    # $500K for enterprise
    },
    'late_payment_fee': 0.015  # 1.5% per month
}

# Business lifecycle stages
LIFECYCLE = {
    'early': {
        'clients': 10,
        'monthly_volume': 50000,    # $50K per month
        'months': range(0, 8),
        'late_payment_rate': 0.20,  # 20% late payments
        'financing_adoption': 0.10   # 10% use financing
    },
    'growth': {
        'clients': 100,
        'monthly_volume': 1000000,  # $1M per month
        'months': range(8, 16),
        'late_payment_rate': 0.10,  # 10% late payments
        'financing_adoption': 0.25   # 25% use financing
    },
    'mature': {
        'clients': 1000,
        'monthly_volume': 10000000, # $10M per month
        'months': range(16, 24),
        'late_payment_rate': 0.05,  # 5% late payments
        'financing_adoption': 0.40   # 40% use financing
    }
}

# Medical equipment categories
MEDICAL_PRODUCTS = {
    'surgical': {
        'category': 'Surgical Equipment',
        'products': [
            'Surgical Instrument Set', 'Anesthesia Machine', 'Operating Table',
            'Surgical Lights', 'Electrosurgical Unit', 'Suction System'
        ],
        'unit_price_range': (5000, 150000),  # $50 to $1,500
        'avg_quantity': 5
    },
    'diagnostic': {
        'category': 'Diagnostic Equipment',
        'products': [
            'X-Ray Machine', 'MRI Scanner', 'CT Scanner', 'Ultrasound System',
            'ECG Machine', 'Blood Analyzer', 'Microscope'
        ],
        'unit_price_range': (10000, 500000),  # $100 to $5,000
        'avg_quantity': 2
    },
    'ppe': {
        'category': 'PPE & Disposables',
        'products': [
            'N95 Respirators', 'Surgical Masks', 'Isolation Gowns',
            'Nitrile Gloves', 'Face Shields', 'Surgical Drapes'
        ],
        'unit_price_range': (500, 5000),  # $5 to $50
        'avg_quantity': 100
    },
    'lab': {
        'category': 'Laboratory Supplies',
        'products': [
            'Centrifuge', 'Incubator', 'Autoclave', 'PCR Machine',
            'Spectrophotometer', 'Lab Refrigerator', 'Safety Cabinet'
        ],
        'unit_price_range': (2000, 80000),  # $20 to $800
        'avg_quantity': 10
    },
    'furniture': {
        'category': 'Medical Furniture',
        'products': [
            'Hospital Bed', 'Exam Table', 'Medical Cart', 'IV Stand',
            'Wheelchair', 'Patient Lift', 'Medical Stool'
        ],
        'unit_price_range': (1000, 25000),  # $10 to $250
        'avg_quantity': 20
    }
}

# Customer types and their characteristics
CUSTOMER_TYPES = {
    'hospital': {
        'name_suffix': ['General Hospital', 'Medical Center', 'Regional Medical Center'],
        'credit_score_range': (700, 850),
        'credit_limit_category': 'enterprise',
        'order_frequency': 2.5,  # orders per month
        'avg_order_size': 150000,  # $1,500
        'preferred_terms': 'net_60',
        'tax_exempt': True
    },
    'clinic': {
        'name_suffix': ['Family Clinic', 'Medical Clinic', 'Urgent Care'],
        'credit_score_range': (650, 800),
        'credit_limit_category': 'established',
        'order_frequency': 1.5,  # orders per month
        'avg_order_size': 50000,   # $500
        'preferred_terms': 'net_30',
        'tax_exempt': False
    },
    'lab': {
        'name_suffix': ['Diagnostic Lab', 'Laboratory Services', 'Pathology Lab'],
        'credit_score_range': (680, 820),
        'credit_limit_category': 'established',
        'order_frequency': 2.0,   # orders per month
        'avg_order_size': 75000,  # $750
        'preferred_terms': 'net_30',
        'tax_exempt': False
    },
    'pharmacy': {
        'name_suffix': ['Pharmacy', 'Drug Store', 'Compounding Pharmacy'],
        'credit_score_range': (600, 750),
        'credit_limit_category': 'startup',
        'order_frequency': 3.0,   # orders per month
        'avg_order_size': 25000,  # $250
        'preferred_terms': 'net_30',
        'tax_exempt': False
    }
}

# Payment method preferences by business type
PAYMENT_METHODS = {
    'hospital': {'ach_debit': 0.60, 'wire_transfer': 0.35, 'card': 0.05},
    'clinic': {'ach_debit': 0.70, 'wire_transfer': 0.20, 'card': 0.10},
    'lab': {'ach_debit': 0.65, 'wire_transfer': 0.25, 'card': 0.10},
    'pharmacy': {'ach_debit': 0.50, 'wire_transfer': 0.15, 'card': 0.35}
}

# Initialize Faker and random seeds
fake = Faker()
fake.seed_instance(42)
random.seed(42)
np.random.seed(42)

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def generate_stripe_ids() -> Dict[str, str]:
    """Generate properly formatted Stripe IDs for B2B platform."""
    return {
        'customer': f"cus_{uuid.uuid4().hex[:14]}",
        'invoice': f"in_{uuid.uuid4().hex[:24]}",
        'payment': f"py_{uuid.uuid4().hex[:24]}",
        'quote': f"qt_{uuid.uuid4().hex[:24]}",
        'financing': f"cap_{uuid.uuid4().hex[:20]}"
    }

def get_lifecycle_stage(month: int) -> str:
    """Determine lifecycle stage based on month."""
    for stage, config in LIFECYCLE.items():
        if month in config['months']:
            return stage
    return 'mature'

def weighted_choice(choices: Dict[str, float]) -> str:
    """Make a weighted random choice from dictionary of choices."""
    total = sum(choices.values())
    r = random.uniform(0, total)
    cumulative = 0
    for choice, weight in choices.items():
        cumulative += weight
        if r <= cumulative:
            return choice
    return list(choices.keys())[-1]

def calculate_volume_discount(subtotal: int) -> int:
    """Calculate volume discount based on order size."""
    for tier in BUSINESS_CONFIG['volume_discounts']:
        if tier['min'] <= subtotal and (tier['max'] is None or subtotal < tier['max']):
            return int(subtotal * tier['discount'])
    return 0

def calculate_due_date(order_date: datetime, payment_terms: str) -> datetime:
    """Calculate invoice due date based on payment terms."""
    if payment_terms == 'net_30':
        return order_date + timedelta(days=30)
    elif payment_terms == 'net_60':
        return order_date + timedelta(days=60)
    elif payment_terms == 'net_90':
        return order_date + timedelta(days=90)
    else:
        return order_date + timedelta(days=30)  # Default

def calculate_late_fee(amount: int, days_late: int) -> int:
    """Calculate late payment fee."""
    months_late = max(1, days_late // 30)
    return int(amount * BUSINESS_CONFIG['late_payment_fee'] * months_late)

def calculate_monthly_payment(principal: int, annual_rate: float, months: int) -> int:
    """Calculate monthly payment for financing."""
    monthly_rate = annual_rate / 12
    if monthly_rate == 0:
        return principal // months
    return int(principal * (monthly_rate * (1 + monthly_rate)**months) / 
               ((1 + monthly_rate)**months - 1))

# =============================================================================
# B2B CUSTOMER GENERATION
# =============================================================================

def generate_medical_client(client_id: str, onboarding_date: datetime, 
                          client_type: str) -> Dict[str, Any]:
    """Generate B2B medical client with credit terms and business info."""
    stripe_ids = generate_stripe_ids()
    customer_config = CUSTOMER_TYPES[client_type]
    
    # Generate business name
    city = fake.city()
    business_name = f"{city} {random.choice(customer_config['name_suffix'])}"
    
    # Generate credit score and limit
    credit_score = random.randint(*customer_config['credit_score_range'])
    credit_limit_category = customer_config['credit_limit_category']
    base_credit_limit = BUSINESS_CONFIG['credit_limits'][credit_limit_category]
    
    # Adjust credit limit based on credit score
    if credit_score >= 800:
        credit_limit = int(base_credit_limit * 1.5)
    elif credit_score >= 750:
        credit_limit = base_credit_limit
    elif credit_score >= 700:
        credit_limit = int(base_credit_limit * 0.75)
    else:
        credit_limit = int(base_credit_limit * 0.5)
    
    # Assign payment terms (favor customer preference but allow variation)
    preferred_terms = customer_config['preferred_terms']
    if random.random() < 0.7:  # 70% get preferred terms
        payment_terms = preferred_terms
    else:
        payment_terms = weighted_choice(BUSINESS_CONFIG['payment_terms'])
    
    # Generate tax ID (EIN format)
    tax_id = f"{random.randint(10, 99)}-{random.randint(1000000, 9999999)}"
    
    return {
        "id": stripe_ids['customer'],
        "object": "customer",
        "created": int(onboarding_date.timestamp()),
        "name": business_name,
        "email": f"billing@{business_name.lower().replace(' ', '').replace('.', '')}.com",
        "phone": fake.phone_number(),
        "description": f"B2B Medical Equipment - {client_type.title()}",
        "address": {
            "line1": fake.street_address(),
            "city": city,
            "state": fake.state_abbr(),
            "postal_code": fake.zipcode(),
            "country": "US"
        },
        "shipping": {
            "name": business_name,
            "address": {
                "line1": fake.street_address(),
                "city": city,
                "state": fake.state_abbr(),
                "postal_code": fake.zipcode(),
                "country": "US"
            }
        },
        "metadata": {
            "client_id": client_id,
            "business_type": client_type,
            "tax_id": tax_id,
            "credit_limit_cents": credit_limit * 100,  # Convert to cents
            "credit_score": credit_score,
            "payment_terms": payment_terms,
            "client_since": onboarding_date.isoformat(),
            "annual_contract": random.choice([True, False]),
            "preferred_shipping": random.choice(['standard', 'express', 'white_glove']),
            "tax_exempt": customer_config['tax_exempt'],
            "account_manager": fake.name(),
            "industry_licenses": f"LIC-{random.randint(100000, 999999)}",
            "purchasing_contact": fake.name(),
            "purchasing_email": fake.email(),
            "billing_contact": fake.name(),
            "credit_limit_category": credit_limit_category,
            "order_frequency_per_month": customer_config['order_frequency'],
            "avg_order_size_cents": customer_config['avg_order_size'] * 100
        }
    }

# =============================================================================
# PURCHASE ORDER SYSTEM
# =============================================================================

def create_purchase_order(client: Dict[str, Any], order_date: datetime) -> Dict[str, Any]:
    """Create detailed purchase order with line items and pricing."""
    # Generate PO number
    po_number = f"PO-{order_date.strftime('%Y%m')}-{random.randint(1000, 9999)}"
    
    # Determine number of line items (1-20)
    num_items = random.choices(
        range(1, 21), 
        weights=[20, 15, 12, 10, 8, 6, 5, 4, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1]
    )[0]
    
    line_items = []
    
    for line_num in range(1, num_items + 1):
        # Select product category
        category_key = random.choice(list(MEDICAL_PRODUCTS.keys()))
        category = MEDICAL_PRODUCTS[category_key]
        
        # Select specific product
        product_name = random.choice(category['products'])
        
        # Generate pricing and quantity
        unit_price_range = category['unit_price_range']
        unit_price = random.randint(*unit_price_range)
        
        # Quantity based on product type
        base_qty = category['avg_quantity']
        quantity = max(1, int(random.gauss(base_qty, base_qty * 0.5)))
        
        # Product code
        product_code = f"MED-{category_key.upper()}-{random.randint(100, 999)}"
        
        # Calculate line total
        line_total = quantity * unit_price
        
        line_item = {
            "line_number": line_num,
            "product_code": product_code,
            "description": product_name,
            "category": category['category'],
            "quantity": quantity,
            "unit_price_cents": unit_price,
            "unit_price_dollars": unit_price / 100,
            "line_total_cents": line_total,
            "line_total_dollars": line_total / 100,
            "tax_rate": 0 if client['metadata']['tax_exempt'] else 0.08,
            "manufacturer": fake.company(),
            "model_number": f"MDL-{random.randint(1000, 9999)}",
            "warranty_months": random.choice([12, 24, 36, 60])
        }
        
        line_items.append(line_item)
    
    # Calculate totals
    subtotal = sum(item['line_total_cents'] for item in line_items)
    volume_discount = calculate_volume_discount(subtotal)
    
    # Calculate tax
    if client['metadata']['tax_exempt']:
        tax = 0
    else:
        taxable_items = [item for item in line_items if item['tax_rate'] > 0]
        tax = sum(int(item['line_total_cents'] * item['tax_rate']) for item in taxable_items)
    
    # Calculate shipping based on order size and preference
    shipping_method = client['metadata']['preferred_shipping']
    if shipping_method == 'standard':
        shipping = max(500, int(subtotal * 0.02))  # $5 or 2% of order
    elif shipping_method == 'express':
        shipping = max(1500, int(subtotal * 0.05))  # $15 or 5% of order
    else:  # white_glove
        shipping = max(5000, int(subtotal * 0.08))  # $50 or 8% of order
    
    total = subtotal - volume_discount + tax + shipping
    
    # Calculate due date
    due_date = calculate_due_date(order_date, client['metadata']['payment_terms'])
    
    return {
        "po_number": po_number,
        "client_id": client['id'],
        "client_name": client['name'],
        "order_date": order_date.isoformat(),
        "requested_delivery_date": (order_date + timedelta(days=random.randint(7, 30))).isoformat(),
        "line_items": line_items,
        "subtotal_cents": subtotal,
        "subtotal_dollars": subtotal / 100,
        "volume_discount_cents": volume_discount,
        "volume_discount_dollars": volume_discount / 100,
        "volume_discount_rate": volume_discount / subtotal if subtotal > 0 else 0,
        "tax_cents": tax,
        "tax_dollars": tax / 100,
        "shipping_cents": shipping,
        "shipping_dollars": shipping / 100,
        "shipping_method": shipping_method,
        "total_cents": total,
        "total_dollars": total / 100,
        "payment_terms": client['metadata']['payment_terms'],
        "due_date": due_date.isoformat(),
        "currency": "usd",
        "status": "pending_fulfillment",
        "metadata": {
            "account_manager": client['metadata']['account_manager'],
            "client_type": client['metadata']['business_type'],
            "tax_exempt": client['metadata']['tax_exempt'],
            "billing_contact": client['metadata']['billing_contact'],
            "purchasing_contact": client['metadata']['purchasing_contact'],
            "credit_limit_cents": client['metadata']['credit_limit_cents'],
            "order_priority": random.choice(['standard', 'rush', 'emergency']),
            "special_instructions": random.choice([
                None, "Deliver to loading dock", "Contact before delivery",
                "Requires refrigeration", "Fragile - handle with care"
            ])
        }
    }

# =============================================================================
# INVOICE AND PAYMENT PROCESSING
# =============================================================================

def generate_invoice(purchase_order: Dict[str, Any], 
                    client: Dict[str, Any]) -> Dict[str, Any]:
    """Generate Stripe invoice from purchase order."""
    stripe_ids = generate_stripe_ids()
    
    # Convert line items to Stripe invoice line format
    invoice_lines = []
    for item in purchase_order['line_items']:
        invoice_lines.append({
            "id": f"il_{uuid.uuid4().hex[:22]}",
            "object": "line_item",
            "amount": item['line_total_cents'],
            "currency": "usd",
            "description": f"{item['description']} (Qty: {item['quantity']})",
            "quantity": item['quantity'],
            "unit_amount": item['unit_price_cents'],
            "metadata": {
                "product_code": item['product_code'],
                "category": item['category'],
                "line_number": item['line_number']
            }
        })
    
    # Add discount line if applicable
    if purchase_order['volume_discount_cents'] > 0:
        invoice_lines.append({
            "id": f"il_{uuid.uuid4().hex[:22]}",
            "object": "line_item",
            "amount": -purchase_order['volume_discount_cents'],
            "currency": "usd",
            "description": f"Volume Discount ({purchase_order['volume_discount_rate']:.1%})",
            "quantity": 1,
            "unit_amount": -purchase_order['volume_discount_cents']
        })
    
    # Add shipping line
    if purchase_order['shipping_cents'] > 0:
        invoice_lines.append({
            "id": f"il_{uuid.uuid4().hex[:22]}",
            "object": "line_item",
            "amount": purchase_order['shipping_cents'],
            "currency": "usd",
            "description": f"Shipping ({purchase_order['shipping_method']})",
            "quantity": 1,
            "unit_amount": purchase_order['shipping_cents']
        })
    
    # Add tax line if applicable
    if purchase_order['tax_cents'] > 0:
        invoice_lines.append({
            "id": f"il_{uuid.uuid4().hex[:22]}",
            "object": "line_item",
            "amount": purchase_order['tax_cents'],
            "currency": "usd",
            "description": "Sales Tax (8%)",
            "quantity": 1,
            "unit_amount": purchase_order['tax_cents']
        })
    
    invoice = {
        "id": stripe_ids['invoice'],
        "object": "invoice",
        "customer": client['id'],
        "amount_due": purchase_order['total_cents'],
        "amount_paid": 0,
        "amount_remaining": purchase_order['total_cents'],
        "currency": "usd",
        "created": int(datetime.fromisoformat(purchase_order['order_date']).timestamp()),
        "due_date": int(datetime.fromisoformat(purchase_order['due_date']).timestamp()),
        "status": "open",
        "collection_method": "send_invoice",
        "description": f"Medical Equipment Order - {purchase_order['po_number']}",
        "lines": {
            "object": "list",
            "data": invoice_lines,
            "has_more": False,
            "total_count": len(invoice_lines)
        },
        "payment_settings": {
            "payment_method_types": ["ach_debit", "wire_transfer", "card"],
            "default_mandate": None
        },
        "footer": f"NET {client['metadata']['payment_terms'].split('_')[1]} payment terms. Late payments subject to 1.5% monthly fee.",
        "custom_fields": [
            {"name": "PO Number", "value": purchase_order['po_number']},
            {"name": "Account Manager", "value": client['metadata']['account_manager']},
            {"name": "Tax ID", "value": client['metadata']['tax_id']}
        ],
        "metadata": {
            "po_number": purchase_order['po_number'],
            "payment_terms": client['metadata']['payment_terms'],
            "client_type": client['metadata']['business_type'],
            "tax_exempt": str(client['metadata']['tax_exempt']),
            "credit_limit_cents": str(client['metadata']['credit_limit_cents']),
            "account_manager": client['metadata']['account_manager']
        }
    }
    
    return invoice

def determine_payment_timing(invoice: Dict[str, Any], client: Dict[str, Any], 
                           stage_config: Dict[str, Any]) -> str:
    """Determine when and how invoice will be paid."""
    late_payment_rate = stage_config['late_payment_rate']
    
    # Payment timing probabilities
    if random.random() < late_payment_rate:
        return random.choice(['late', 'partial'])
    else:
        return 'on_time'

def process_b2b_payment(invoice: Dict[str, Any], client: Dict[str, Any], 
                       payment_date: datetime, payment_timing: str) -> Dict[str, Any]:
    """Process B2B payment with appropriate method and timing."""
    stripe_ids = generate_stripe_ids()
    
    # Determine payment method based on client type
    client_type = client['metadata']['business_type']
    payment_method = weighted_choice(PAYMENT_METHODS[client_type])
    
    # Calculate payment amount
    if payment_timing == 'partial':
        payment_amount = int(invoice['amount_due'] * random.uniform(0.25, 0.75))
    else:
        payment_amount = invoice['amount_due']
    
    # Add late fees if applicable
    late_fee = 0
    if payment_timing == 'late':
        due_date = datetime.fromtimestamp(invoice['due_date'])
        days_late = max(1, (payment_date - due_date).days)
        late_fee = calculate_late_fee(invoice['amount_due'], days_late)
        payment_amount += late_fee
    
    # Generate payment object based on method
    if payment_method == 'ach_debit':
        payment = {
            "id": stripe_ids['payment'],
            "object": "payment_intent",
            "amount": payment_amount,
            "currency": "usd",
            "status": "succeeded",
            "customer": client['id'],
            "created": int(payment_date.timestamp()),
            "description": f"Payment for invoice {invoice['id']}",
            "payment_method": "ach_debit",
            "payment_method_types": ["ach_debit"],
            "processing_time_days": 3,
            "fees": {
                "amount": 500,  # $5.00 flat fee
                "currency": "usd",
                "description": "ACH processing fee"
            },
            "metadata": {
                "invoice_id": invoice['id'],
                "po_number": invoice['metadata']['po_number'],
                "payment_timing": payment_timing,
                "late_fee_cents": late_fee,
                "days_late": (payment_date - datetime.fromtimestamp(invoice['due_date'])).days if payment_timing == 'late' else 0
            }
        }
    elif payment_method == 'wire_transfer':
        payment = {
            "id": stripe_ids['payment'],
            "object": "payment_intent",
            "amount": payment_amount,
            "currency": "usd",
            "status": "succeeded",
            "customer": client['id'],
            "created": int(payment_date.timestamp()),
            "description": f"Wire payment for invoice {invoice['id']}",
            "payment_method": "wire_transfer",
            "payment_method_types": ["wire_transfer"],
            "processing_time_days": 1,
            "fees": {
                "amount": 2500,  # $25.00 flat fee
                "currency": "usd",
                "description": "Wire transfer fee"
            },
            "wire_details": {
                "reference": f"REF-{uuid.uuid4().hex[:12].upper()}",
                "originating_bank": fake.company() + " Bank",
                "originating_account": f"****{random.randint(1000, 9999)}"
            },
            "metadata": {
                "invoice_id": invoice['id'],
                "po_number": invoice['metadata']['po_number'],
                "payment_timing": payment_timing,
                "late_fee_cents": late_fee
            }
        }
    else:  # card payment
        payment = {
            "id": stripe_ids['payment'],
            "object": "payment_intent",
            "amount": payment_amount,
            "currency": "usd",
            "status": "succeeded",
            "customer": client['id'],
            "created": int(payment_date.timestamp()),
            "description": f"Card payment for invoice {invoice['id']}",
            "payment_method": "card",
            "payment_method_types": ["card"],
            "processing_time_days": 0,
            "fees": {
                "amount": int(payment_amount * 0.029 + 30),  # 2.9% + $0.30
                "currency": "usd",
                "description": "Card processing fee"
            },
            "charges": {
                "data": [{
                    "id": f"ch_{uuid.uuid4().hex[:24]}",
                    "amount": payment_amount,
                    "currency": "usd",
                    "paid": True,
                    "card": {
                        "brand": random.choice(["visa", "mastercard", "amex"]),
                        "last4": str(random.randint(1000, 9999)),
                        "funding": "credit"
                    }
                }]
            },
            "metadata": {
                "invoice_id": invoice['id'],
                "po_number": invoice['metadata']['po_number'],
                "payment_timing": payment_timing,
                "late_fee_cents": late_fee
            }
        }
    
    return payment

# =============================================================================
# FINANCING AND CREDIT
# =============================================================================

def offer_financing(client: Dict[str, Any], purchase_order: Dict[str, Any], 
                   stage_config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Generate Stripe Capital financing offer for large orders."""
    # Only offer financing for orders over $50K and good credit
    if (purchase_order['total_cents'] < 5000000 or  # $50K
        client['metadata']['credit_score'] < 700):
        return None
    
    # Check if client would be interested in financing
    financing_adoption = stage_config['financing_adoption']
    if random.random() > financing_adoption:
        return None
    
    stripe_ids = generate_stripe_ids()
    
    # Calculate financing terms
    order_amount = purchase_order['total_cents']
    credit_score = client['metadata']['credit_score']
    
    # Interest rate based on credit score
    if credit_score >= 800:
        interest_rate = 0.06  # 6% APR
    elif credit_score >= 750:
        interest_rate = 0.08  # 8% APR
    elif credit_score >= 700:
        interest_rate = 0.10  # 10% APR
    else:
        interest_rate = 0.12  # 12% APR
    
    # Term length based on order size
    if order_amount >= 50000000:  # $500K+
        term_months = 36
    elif order_amount >= 20000000:  # $200K+
        term_months = 24
    else:
        term_months = 12
    
    monthly_payment = calculate_monthly_payment(order_amount, interest_rate, term_months)
    
    # Determine if offer is accepted
    acceptance_probability = 0.6 if interest_rate <= 0.08 else 0.4
    status = 'accepted' if random.random() < acceptance_probability else 'declined'
    
    return {
        "id": stripe_ids['financing'],
        "object": "capital_offer",
        "type": "stripe_capital",
        "amount": order_amount,
        "currency": "usd",
        "customer": client['id'],
        "created": int(datetime.fromisoformat(purchase_order['order_date']).timestamp()),
        "term_length_months": term_months,
        "interest_rate": interest_rate,
        "monthly_payment_cents": monthly_payment,
        "monthly_payment_dollars": monthly_payment / 100,
        "total_repayment": monthly_payment * term_months,
        "total_interest": (monthly_payment * term_months) - order_amount,
        "status": status,
        "risk_assessment": {
            "credit_score": credit_score,
            "business_age_months": random.randint(12, 120),
            "revenue_verification": "verified",
            "risk_tier": "low" if credit_score >= 750 else "medium"
        },
        "metadata": {
            "po_number": purchase_order['po_number'],
            "client_id": client['id'],
            "client_type": client['metadata']['business_type'],
            "order_amount": order_amount,
            "credit_limit": client['metadata']['credit_limit_cents']
        }
    }

# =============================================================================
# MAIN DATA GENERATION
# =============================================================================

def generate_medsupply_data() -> Tuple[List[Dict], List[Dict], List[Dict], List[Dict], List[Dict]]:
    """Generate complete MedSupply Pro B2B data."""
    print("🏥 Generating MedSupply Pro B2B data...")
    
    all_clients = []
    all_purchase_orders = []
    all_invoices = []
    all_payments = []
    all_financing_offers = []
    
    # Start date for data generation
    start_date = datetime(2023, 1, 1)
    
    client_counter = 1
    
    # Generate data across 24 months
    for month in range(24):
        current_date = start_date + timedelta(days=30 * month)
        stage = get_lifecycle_stage(month)
        stage_config = LIFECYCLE[stage]
        
        print(f"📅 Processing month {month + 1}/24 ({stage} stage)...")
        
        # Generate new clients for this month (spread throughout lifecycle)
        new_clients_this_month = stage_config['clients'] // 12  # Monthly onboarding
        
        for _ in range(new_clients_this_month):
            # Select client type
            client_type = weighted_choice({
                'hospital': 0.25,
                'clinic': 0.40,
                'lab': 0.20,
                'pharmacy': 0.15
            })
            
            onboarding_date = current_date + timedelta(days=random.randint(0, 29))
            
            client = generate_medical_client(
                f"MED_{client_counter:06d}", 
                onboarding_date, 
                client_type
            )
            all_clients.append(client)
            client_counter += 1
        
        # Generate purchase orders for existing clients
        available_clients = [c for c in all_clients 
                           if c['created'] <= int(current_date.timestamp())]
        
        if not available_clients:
            continue
        
        # Calculate total orders needed this month based on stage volume
        monthly_volume_target = stage_config['monthly_volume'] * 100  # Convert to cents
        
        # Generate orders throughout the month
        for week in range(4):  # 4 weeks per month
            week_start = current_date + timedelta(days=week * 7)
            
            for client in available_clients:
                # Check if client should place an order this week
                monthly_frequency = client['metadata']['order_frequency_per_month']
                weekly_probability = monthly_frequency / 4.0
                
                if random.random() < weekly_probability:
                    order_date = week_start + timedelta(days=random.randint(0, 6))
                    
                    # Create purchase order
                    purchase_order = create_purchase_order(client, order_date)
                    all_purchase_orders.append(purchase_order)
                    
                    # Generate invoice
                    invoice = generate_invoice(purchase_order, client)
                    all_invoices.append(invoice)
                    
                    # Determine payment timing and process payment
                    payment_timing = determine_payment_timing(invoice, client, stage_config)
                    
                    if payment_timing == 'on_time':
                        payment_date = datetime.fromisoformat(purchase_order['due_date'])
                    elif payment_timing == 'late':
                        days_late = random.randint(1, 60)
                        payment_date = datetime.fromisoformat(purchase_order['due_date']) + timedelta(days=days_late)
                    else:  # partial
                        payment_date = datetime.fromisoformat(purchase_order['due_date']) + timedelta(days=random.randint(-5, 15))
                    
                    # Only process payment if it's within our timeframe
                    if payment_date <= datetime.now():
                        payment = process_b2b_payment(invoice, client, payment_date, payment_timing)
                        all_payments.append(payment)
                        
                        # Update invoice status
                        if payment_timing == 'partial':
                            invoice['status'] = 'partially_paid'
                            invoice['amount_paid'] = payment['amount'] - payment['metadata'].get('late_fee_cents', 0)
                        else:
                            invoice['status'] = 'paid'
                            invoice['amount_paid'] = invoice['amount_due']
                            invoice['paid_at'] = int(payment_date.timestamp())
                    
                    # Offer financing if applicable
                    financing_offer = offer_financing(client, purchase_order, stage_config)
                    if financing_offer:
                        all_financing_offers.append(financing_offer)
    
    print(f"✅ Generated {len(all_clients)} clients, {len(all_purchase_orders)} orders, {len(all_financing_offers)} financing offers")
    return all_clients, all_purchase_orders, all_invoices, all_payments, all_financing_offers

# =============================================================================
# METRICS AND AGING REPORTS
# =============================================================================

def calculate_b2b_metrics(clients: List[Dict], purchase_orders: List[Dict], 
                         invoices: List[Dict], payments: List[Dict], 
                         financing_offers: List[Dict]) -> Dict[str, Any]:
    """Calculate B2B medical equipment business metrics."""
    print("📊 Calculating MedSupply Pro metrics...")
    
    # Basic counts
    total_clients = len(clients)
    total_orders = len(purchase_orders)
    total_invoices = len(invoices)
    total_payments = len(payments)
    
    # Revenue calculations
    total_order_value = sum(po['total_cents'] for po in purchase_orders)
    paid_invoices = [inv for inv in invoices if inv['status'] in ['paid', 'partially_paid']]
    total_revenue = sum(inv['amount_paid'] for inv in paid_invoices)
    
    # Average order value
    avg_order_value = total_order_value / len(purchase_orders) if purchase_orders else 0
    
    # Payment terms analysis
    payment_terms_dist = {}
    for client in clients:
        terms = client['metadata']['payment_terms']
        payment_terms_dist[terms] = payment_terms_dist.get(terms, 0) + 1
    
    # Customer type distribution
    customer_type_dist = {}
    for client in clients:
        client_type = client['metadata']['business_type']
        customer_type_dist[client_type] = customer_type_dist.get(client_type, 0) + 1
    
    # Payment method analysis
    payment_method_dist = {}
    for payment in payments:
        method = payment['payment_method']
        payment_method_dist[method] = payment_method_dist.get(method, 0) + 1
    
    # Days Sales Outstanding (DSO) calculation
    open_invoices = [inv for inv in invoices if inv['status'] == 'open']
    if open_invoices:
        current_date = datetime.now()
        total_outstanding_days = 0
        total_outstanding_amount = 0
        
        for invoice in open_invoices:
            invoice_date = datetime.fromtimestamp(invoice['created'])
            days_outstanding = (current_date - invoice_date).days
            amount_outstanding = invoice['amount_remaining']
            
            total_outstanding_days += days_outstanding * amount_outstanding
            total_outstanding_amount += amount_outstanding
        
        dso = total_outstanding_days / total_outstanding_amount if total_outstanding_amount > 0 else 0
    else:
        dso = 0
    
    # Collection rate
    collection_rate = (len(paid_invoices) / len(invoices) * 100) if invoices else 0
    
    # Late payment analysis
    late_payments = [p for p in payments if p['metadata'].get('days_late', 0) > 0]
    late_payment_rate = (len(late_payments) / len(payments) * 100) if payments else 0
    
    # Volume discount analysis
    total_discounts = sum(po['volume_discount_cents'] for po in purchase_orders)
    discount_rate = (total_discounts / total_order_value * 100) if total_order_value > 0 else 0
    
    # Financing metrics
    financing_acceptance_rate = (len([f for f in financing_offers if f['status'] == 'accepted']) / 
                               len(financing_offers) * 100) if financing_offers else 0
    total_financing_offered = sum(f['amount'] for f in financing_offers)
    
    # Aging report
    aging_buckets = {'current': [], '1_30': [], '31_60': [], '61_90': [], '90_plus': []}
    current_date = datetime.now()
    
    for invoice in open_invoices:
        due_date = datetime.fromtimestamp(invoice['due_date'])
        days_overdue = (current_date - due_date).days
        
        if days_overdue <= 0:
            aging_buckets['current'].append(invoice)
        elif days_overdue <= 30:
            aging_buckets['1_30'].append(invoice)
        elif days_overdue <= 60:
            aging_buckets['31_60'].append(invoice)
        elif days_overdue <= 90:
            aging_buckets['61_90'].append(invoice)
        else:
            aging_buckets['90_plus'].append(invoice)
    
    aging_summary = {}
    for bucket, invoices_list in aging_buckets.items():
        aging_summary[bucket] = {
            'count': len(invoices_list),
            'amount_cents': sum(inv['amount_remaining'] for inv in invoices_list),
            'amount_dollars': sum(inv['amount_remaining'] for inv in invoices_list) / 100
        }
    
    return {
        "overview": {
            "total_clients": total_clients,
            "total_orders": total_orders,
            "total_invoices": total_invoices,
            "total_payments": total_payments,
            "collection_rate_percent": round(collection_rate, 2)
        },
        "financial_metrics": {
            "total_order_value_cents": total_order_value,
            "total_order_value_dollars": total_order_value / 100,
            "total_revenue_cents": total_revenue,
            "total_revenue_dollars": total_revenue / 100,
            "average_order_value_cents": int(avg_order_value),
            "average_order_value_dollars": avg_order_value / 100,
            "days_sales_outstanding": round(dso, 1),
            "total_volume_discounts_cents": total_discounts,
            "total_volume_discounts_dollars": total_discounts / 100,
            "discount_rate_percent": round(discount_rate, 2)
        },
        "payment_analysis": {
            "late_payment_rate_percent": round(late_payment_rate, 2),
            "payment_method_distribution": payment_method_dist,
            "payment_terms_distribution": payment_terms_dist
        },
        "customer_analysis": {
            "customer_type_distribution": customer_type_dist,
            "avg_credit_limit_by_type": {
                client_type: sum(c['metadata']['credit_limit_cents'] for c in clients 
                               if c['metadata']['business_type'] == client_type) / 
                           max(1, len([c for c in clients if c['metadata']['business_type'] == client_type])) / 100
                for client_type in customer_type_dist.keys()
            }
        },
        "financing_metrics": {
            "total_offers": len(financing_offers),
            "acceptance_rate_percent": round(financing_acceptance_rate, 2),
            "total_financing_offered_cents": total_financing_offered,
            "total_financing_offered_dollars": total_financing_offered / 100
        },
        "aging_report": aging_summary
    }

# =============================================================================
# OUTPUT GENERATION
# =============================================================================

def save_medsupply_data(clients: List[Dict], purchase_orders: List[Dict], 
                       invoices: List[Dict], payments: List[Dict], 
                       financing_offers: List[Dict], metrics: Dict[str, Any]) -> None:
    """Save all generated data to JSON files."""
    print("💾 Saving MedSupply Pro data to files...")
    
    output_dir = "b2b_data"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate aging report as separate detailed file
    current_date = datetime.now()
    aging_report = []
    
    for invoice in invoices:
        if invoice['status'] == 'open':
            due_date = datetime.fromtimestamp(invoice['due_date'])
            days_overdue = (current_date - due_date).days
            
            client = next(c for c in clients if c['id'] == invoice['customer'])
            
            aging_report.append({
                "invoice_id": invoice['id'],
                "customer_name": client['name'],
                "customer_type": client['metadata']['business_type'],
                "po_number": invoice['metadata']['po_number'],
                "invoice_date": datetime.fromtimestamp(invoice['created']).isoformat(),
                "due_date": due_date.isoformat(),
                "days_overdue": days_overdue,
                "amount_due_cents": invoice['amount_remaining'],
                "amount_due_dollars": invoice['amount_remaining'] / 100,
                "payment_terms": invoice['metadata']['payment_terms'],
                "aging_bucket": (
                    'current' if days_overdue <= 0 else
                    '1_30' if days_overdue <= 30 else
                    '31_60' if days_overdue <= 60 else
                    '61_90' if days_overdue <= 90 else
                    '90_plus'
                )
            })
    
    # Save main data files
    datasets = {
        "clients.json": clients,
        "purchase_orders.json": purchase_orders,
        "invoices.json": invoices,
        "payments.json": payments,
        "financing_offers.json": financing_offers,
        "aging_report.json": aging_report,
        "b2b_metrics.json": metrics
    }
    
    for filename, data in datasets.items():
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    print(f"📁 Data saved to {output_dir}/ directory")

def print_medsupply_summary(clients: List[Dict], purchase_orders: List[Dict], 
                          invoices: List[Dict], payments: List[Dict], 
                          financing_offers: List[Dict], metrics: Dict[str, Any]) -> None:
    """Print comprehensive MedSupply Pro generation summary."""
    print("\n" + "="*80)
    print("🏥 MEDSUPPLY PRO B2B DATA GENERATION COMPLETE")
    print("="*80)
    
    overview = metrics['overview']
    financial = metrics['financial_metrics']
    payment_analysis = metrics['payment_analysis']
    customer_analysis = metrics['customer_analysis']
    financing = metrics['financing_metrics']
    
    print(f"\n📊 GENERATION SUMMARY:")
    print(f"   Total B2B clients: {overview['total_clients']:,}")
    print(f"   Purchase orders: {overview['total_orders']:,}")
    print(f"   Invoices generated: {overview['total_invoices']:,}")
    print(f"   Payments processed: {overview['total_payments']:,}")
    print(f"   Collection rate: {overview['collection_rate_percent']:.1f}%")
    
    print(f"\n💰 FINANCIAL METRICS:")
    print(f"   Total order value: ${financial['total_order_value_dollars']:,.2f}")
    print(f"   Total revenue: ${financial['total_revenue_dollars']:,.2f}")
    print(f"   Average order value: ${financial['average_order_value_dollars']:,.2f}")
    print(f"   Days sales outstanding: {financial['days_sales_outstanding']:.1f} days")
    print(f"   Volume discounts: ${financial['total_volume_discounts_dollars']:,.2f} ({financial['discount_rate_percent']:.1f}%)")
    
    print(f"\n🏥 CUSTOMER ANALYSIS:")
    for customer_type, count in customer_analysis['customer_type_distribution'].items():
        avg_credit = customer_analysis['avg_credit_limit_by_type'][customer_type]
        print(f"   {customer_type.title()}s: {count} clients (avg credit: ${avg_credit:,.0f})")
    
    print(f"\n💳 PAYMENT ANALYSIS:")
    print(f"   Late payment rate: {payment_analysis['late_payment_rate_percent']:.1f}%")
    for method, count in payment_analysis['payment_method_distribution'].items():
        percentage = (count / overview['total_payments'] * 100) if overview['total_payments'] > 0 else 0
        print(f"   {method.replace('_', ' ').title()}: {count} ({percentage:.1f}%)")
    
    print(f"\n📋 PAYMENT TERMS:")
    for terms, count in payment_analysis['payment_terms_distribution'].items():
        percentage = (count / overview['total_clients'] * 100) if overview['total_clients'] > 0 else 0
        print(f"   {terms.replace('_', '-').upper()}: {count} clients ({percentage:.1f}%)")
    
    print(f"\n💵 FINANCING METRICS:")
    print(f"   Financing offers: {financing['total_offers']:,}")
    print(f"   Acceptance rate: {financing['acceptance_rate_percent']:.1f}%")
    print(f"   Total financing offered: ${financing['total_financing_offered_dollars']:,.2f}")
    
    print(f"\n📊 AGING REPORT:")
    aging = metrics['aging_report']
    total_outstanding = sum(bucket['amount_dollars'] for bucket in aging.values())
    for bucket_name, bucket_data in aging.items():
        percentage = (bucket_data['amount_dollars'] / total_outstanding * 100) if total_outstanding > 0 else 0
        bucket_display = bucket_name.replace('_', '-').title() if '_' in bucket_name else bucket_name.title()
        print(f"   {bucket_display}: ${bucket_data['amount_dollars']:,.2f} ({percentage:.1f}%)")
    
    print(f"\n📁 OUTPUT FILES:")
    print(f"   ✅ clients.json - B2B customer profiles with credit limits")
    print(f"   ✅ purchase_orders.json - Detailed POs with line items")
    print(f"   ✅ invoices.json - Stripe invoices with payment terms")
    print(f"   ✅ payments.json - ACH, wire, and card payments")
    print(f"   ✅ financing_offers.json - Stripe Capital offers")
    print(f"   ✅ aging_report.json - Accounts receivable aging")
    print(f"   ✅ b2b_metrics.json - Complete B2B analytics")
    
    print(f"\n🚀 Ready for B2B medical equipment platform prototyping!")
    print("="*80)

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("🏥 MedSupply Pro Synthetic B2B Data Generator")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        # Generate all data
        clients, purchase_orders, invoices, payments, financing_offers = generate_medsupply_data()
        
        # Calculate metrics
        metrics = calculate_b2b_metrics(clients, purchase_orders, invoices, payments, financing_offers)
        
        # Save data
        save_medsupply_data(clients, purchase_orders, invoices, payments, financing_offers, metrics)
        
        # Print summary
        print_medsupply_summary(clients, purchase_orders, invoices, payments, financing_offers, metrics)
        
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"\n⏱️ Total execution time: {execution_time:.1f} seconds")
        
    except Exception as e:
        print(f"\n❌ Error during generation: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
