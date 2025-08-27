#!/usr/bin/env python3
"""
PropertyFlow Property Management Platform - Synthetic Data Generator

Generates realistic Stripe payment data for a property management platform
including rent collection, security deposits, maintenance, and landlord payouts.

Author: Stripe Synthetic Data Team
Created: 2024
"""

import json
import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import pandas as pd
import numpy as np
from faker import Faker

# Initialize Faker
faker = Faker()
faker.seed_instance(42)
random.seed(42)
np.random.seed(42)

# =============================================================================
# CONFIGURATION
# =============================================================================

PROPERTY_CONFIG = {
    'rent_collection': {
        'ach_debit': 0.70,  # 70% use bank debits
        'card': 0.25,       # 25% use cards
        'wire': 0.05        # 5% use wire
    },
    'fees': {
        'management_fee': 0.08,  # 8% of rent
        'late_fee': 50.00,       # $50 flat
        'nsf_fee': 35.00,        # $35 for bounced payment
        'maintenance_markup': 0.10  # 10% on maintenance
    },
    'payment_timing': {
        'on_time': 0.85,
        'late': 0.12,
        'nsf': 0.03
    }
}

LIFECYCLE = {
    'early': {
        'properties': 50,
        'landlords': 10,
        'months': range(0, 8),
        'late_rate': 0.15,
        'nsf_rate': 0.08
    },
    'growth': {
        'properties': 500,
        'landlords': 100,
        'months': range(8, 16),
        'late_rate': 0.08,
        'nsf_rate': 0.04
    },
    'mature': {
        'properties': 5000,
        'landlords': 1000,
        'months': range(16, 24),
        'late_rate': 0.04,
        'nsf_rate': 0.02
    }
}

PROPERTY_TYPES = {
    'apartment': {'min_rent': 1200, 'max_rent': 3500, 'weight': 0.4},
    'house': {'min_rent': 1800, 'max_rent': 5000, 'weight': 0.3},
    'condo': {'min_rent': 1500, 'max_rent': 4000, 'weight': 0.2},
    'townhouse': {'min_rent': 1600, 'max_rent': 4500, 'weight': 0.1}
}

MAINTENANCE_TYPES = {
    'plumbing': {'min_cost': 150, 'max_cost': 800, 'frequency': 0.15},
    'electrical': {'min_cost': 200, 'max_cost': 1200, 'frequency': 0.10},
    'hvac': {'min_cost': 300, 'max_cost': 2000, 'frequency': 0.20},
    'appliance': {'min_cost': 100, 'max_cost': 600, 'frequency': 0.12},
    'cleaning': {'min_cost': 50, 'max_cost': 300, 'frequency': 0.25},
    'landscaping': {'min_cost': 75, 'max_cost': 400, 'frequency': 0.08},
    'damage_repair': {'min_cost': 200, 'max_cost': 1500, 'frequency': 0.10}
}

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def generate_id() -> str:
    """Generate a unique identifier."""
    return str(uuid.uuid4()).replace('-', '')[:16]

def get_stage_config(month: int) -> Tuple[str, Dict]:
    """Get lifecycle stage configuration for a given month."""
    for stage, config in LIFECYCLE.items():
        if month in config['months']:
            return stage, config
    return 'mature', LIFECYCLE['mature']

def calculate_monthly_date(start_date: datetime, month_offset: int) -> datetime:
    """Calculate date for a specific month offset."""
    year = start_date.year + (start_date.month + month_offset - 1) // 12
    month = (start_date.month + month_offset - 1) % 12 + 1
    day = min(start_date.day, [31,28,31,30,31,30,31,31,30,31,30,31][month-1])
    return datetime(year, month, day)

def determine_payment_outcome(credit_score: int, late_rate: float, nsf_rate: float) -> str:
    """Determine payment outcome based on credit score and stage rates."""
    # Higher credit score = lower chance of issues
    credit_factor = max(0.5, (credit_score - 500) / 350)
    
    adjusted_late_rate = late_rate * (1 - credit_factor * 0.5)
    adjusted_nsf_rate = nsf_rate * (1 - credit_factor * 0.7)
    
    rand = random.random()
    if rand < adjusted_nsf_rate:
        return 'nsf'
    elif rand < adjusted_nsf_rate + adjusted_late_rate:
        return 'late'
    else:
        return 'on_time'

# =============================================================================
# LANDLORD ACCOUNT MANAGEMENT
# =============================================================================

def create_landlord_account(landlord_id: str, onboarding_date: datetime) -> Dict:
    """Create a Stripe Connect account for a landlord."""
    property_count = random.randint(1, 20)
    business_type = random.choice(["individual", "company"])
    
    account = {
        "id": f"acct_LANDLORD_{landlord_id}",
        "object": "account",
        "type": "custom",
        "business_type": business_type,
        "country": "US",
        "created": int(onboarding_date.timestamp()),
        "default_currency": "usd",
        "details_submitted": True,
        "email": faker.email(),
        "charges_enabled": True,
        "payouts_enabled": True,
        "capabilities": {
            "transfers": {"status": "active"},
            "tax_reporting_us_1099_k": {"status": "active"},
            "tax_reporting_us_1099_misc": {"status": "active"}
        },
        "business_profile": {
            "name": f"{faker.company()} Properties" if business_type == "company" else f"{faker.name()} Real Estate",
            "mcc": "6513",  # Real estate agents and managers
            "url": faker.url(),
            "product_description": "Residential property management and rental services"
        },
        "metadata": {
            "landlord_id": str(landlord_id),
            "property_count": str(property_count),
            "portfolio_value": str(property_count * random.randint(150000, 500000)),
            "management_type": random.choice(["self_managed", "full_service"]),
            "payout_schedule": random.choice(["daily", "weekly", "monthly"]),
            "years_experience": str(random.randint(1, 25))
        },
        "tos_acceptance": {
            "date": int(onboarding_date.timestamp()),
            "ip": faker.ipv4(),
            "user_agent": "PropertyFlow/1.0"
        }
    }
    
    if business_type == "individual":
        account["individual"] = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": account["email"],
            "phone": faker.phone_number(),
            "ssn_last_4": f"{random.randint(1000, 9999)}",
            "address": {
                "line1": faker.street_address(),
                "city": faker.city(),
                "state": faker.state_abbr(),
                "postal_code": faker.zipcode(),
                "country": "US"
            }
        }
    else:
        account["company"] = {
            "name": account["business_profile"]["name"],
            "tax_id": f"{random.randint(10, 99)}-{random.randint(1000000, 9999999)}",
            "phone": faker.phone_number(),
            "address": {
                "line1": faker.street_address(),
                "city": faker.city(),
                "state": faker.state_abbr(),
                "postal_code": faker.zipcode(),
                "country": "US"
            }
        }
    
    return account

# =============================================================================
# PROPERTY AND TENANT MANAGEMENT
# =============================================================================

def generate_tenant() -> Dict:
    """Generate a tenant customer profile."""
    return {
        "id": f"cus_TENANT_{generate_id()}",
        "object": "customer",
        "created": int(faker.date_time_between(start_date='-1y').timestamp()),
        "email": faker.email(),
        "name": faker.name(),
        "phone": faker.phone_number(),
        "description": "Property tenant",
        "metadata": {
            "tenant_type": "residential",
            "payment_method": random.choice(["ach_debit", "card"]),
            "autopay_enabled": str(random.random() > 0.2),  # 80% use autopay
            "credit_score": str(random.randint(550, 850)),
            "employment_verified": str(random.random() > 0.1),
            "income_to_rent_ratio": f"{random.uniform(2.5, 6.0):.1f}",
            "previous_landlord_rating": f"{random.uniform(3.0, 5.0):.1f}"
        }
    }

def create_property(property_id: str, landlord: Dict) -> Dict:
    """Create a property with tenant."""
    property_type = random.choices(
        list(PROPERTY_TYPES.keys()),
        weights=[config['weight'] for config in PROPERTY_TYPES.values()]
    )[0]
    
    type_config = PROPERTY_TYPES[property_type]
    rent_amount = random.randint(type_config['min_rent'], type_config['max_rent']) * 100  # Convert to cents
    
    now = datetime.now()
    lease_start = faker.date_time_between(start_date=now - timedelta(days=730), end_date=now)
    lease_end = faker.date_time_between(start_date=now, end_date=now + timedelta(days=730))
    
    property_data = {
        "id": f"prop_{property_id}",
        "landlord_id": landlord['metadata']['landlord_id'],
        "landlord_account": landlord['id'],
        "address": {
            "line1": faker.street_address(),
            "city": faker.city(),
            "state": faker.state_abbr(),
            "postal_code": faker.zipcode(),
            "country": "US"
        },
        "unit_number": random.choice([None, f"#{random.randint(1, 50)}", f"Unit {random.randint(1, 25)}"]),
        "property_type": property_type,
        "bedrooms": random.randint(0, 4),
        "bathrooms": random.uniform(1, 3.5),
        "square_feet": random.randint(500, 3000),
        "rent_amount": rent_amount,
        "security_deposit": rent_amount,  # Typically one month's rent
        "lease_start": lease_start.isoformat(),
        "lease_end": lease_end.isoformat(),
        "tenant": generate_tenant(),
        "amenities": random.sample([
            "parking", "laundry", "dishwasher", "air_conditioning", 
            "heating", "balcony", "gym", "pool", "pet_friendly"
        ], k=random.randint(2, 6)),
        "occupied": True,
        "last_inspection": faker.date_time_between(start_date=datetime.now() - timedelta(days=180), end_date=datetime.now()).isoformat()
    }
    
    return property_data

# =============================================================================
# RENT COLLECTION
# =============================================================================

def collect_monthly_rent(property_data: Dict, collection_date: datetime, stage_config: Dict) -> Dict:
    """Process monthly rent collection for a property."""
    rent_amount = property_data['rent_amount']
    tenant = property_data['tenant']
    credit_score = int(tenant['metadata']['credit_score'])
    
    # Determine payment outcome
    payment_outcome = determine_payment_outcome(
        credit_score, 
        stage_config['late_rate'], 
        stage_config['nsf_rate']
    )
    
    # Base payment object
    payment = {
        "id": f"pi_RENT_{generate_id()}",
        "object": "payment_intent",
        "currency": "usd",
        "customer": tenant['id'],
        "created": int(collection_date.timestamp()),
        "description": f"Monthly rent - {property_data['address']['line1']}",
        "payment_method_types": [tenant['metadata']['payment_method']],
        "transfer_group": f"rent_{property_data['id']}_{collection_date.strftime('%Y%m')}",
        "metadata": {
            "property_id": property_data['id'],
            "landlord_id": property_data['landlord_id'],
            "month": collection_date.strftime('%Y-%m'),
            "payment_type": "rent",
            "rent_amount": str(rent_amount)
        }
    }
    
    if payment_outcome == 'on_time':
        payment.update({
            "amount": rent_amount,
            "status": "succeeded",
            "charges": {
                "data": [{
                    "id": f"ch_{generate_id()}",
                    "amount": rent_amount,
                    "currency": "usd",
                    "paid": True,
                    "refunded": False,
                    "disputed": False,
                    "failure_code": None,
                    "failure_message": None,
                    "outcome": {
                        "network_status": "approved_by_network",
                        "reason": None,
                        "risk_level": "normal",
                        "seller_message": "Payment complete.",
                        "type": "authorized"
                    }
                }]
            }
        })
        
    elif payment_outcome == 'late':
        days_late = random.randint(1, 15)
        late_fee = int(PROPERTY_CONFIG['fees']['late_fee'] * 100)  # Convert to cents
        total_amount = rent_amount + late_fee
        
        payment.update({
            "amount": total_amount,
            "status": "succeeded",
            "description": f"Monthly rent + late fee - {property_data['address']['line1']}",
            "metadata": {
                **payment["metadata"],
                "days_late": str(days_late),
                "late_fee": str(late_fee),
                "late_fee_reason": "payment_after_due_date"
            },
            "charges": {
                "data": [{
                    "id": f"ch_{generate_id()}",
                    "amount": total_amount,
                    "currency": "usd",
                    "paid": True,
                    "refunded": False,
                    "disputed": False,
                    "failure_code": None,
                    "failure_message": None
                }]
            }
        })
        
    else:  # NSF (Non-sufficient funds)
        nsf_fee = int(PROPERTY_CONFIG['fees']['nsf_fee'] * 100)
        
        payment.update({
            "amount": rent_amount,
            "status": "failed",
            "last_payment_error": {
                "code": "insufficient_funds",
                "doc_url": "https://stripe.com/docs/error-codes/insufficient-funds",
                "message": "Your bank account has insufficient funds.",
                "type": "card_error"
            },
            "charges": {
                "data": [{
                    "id": f"ch_{generate_id()}",
                    "amount": rent_amount,
                    "currency": "usd",
                    "paid": False,
                    "refunded": False,
                    "disputed": False,
                    "failure_code": "insufficient_funds",
                    "failure_message": "Your bank account has insufficient funds.",
                    "outcome": {
                        "network_status": "declined_by_network",
                        "reason": "insufficient_funds",
                        "risk_level": "normal",
                        "seller_message": "The bank account has insufficient funds.",
                        "type": "issuer_declined"
                    }
                }]
            },
            "metadata": {
                **payment["metadata"],
                "nsf_fee": str(nsf_fee),
                "retry_attempt": "1"
            }
        })
    
    return payment

# =============================================================================
# SECURITY DEPOSIT MANAGEMENT (ESCROW)
# =============================================================================

def handle_security_deposit(property_data: Dict, tenant: Dict, move_in_date: datetime) -> Tuple[Dict, Optional[Dict]]:
    """Handle security deposit escrow and potential refund."""
    deposit_amount = property_data['security_deposit']
    
    # Create Treasury account for escrow
    escrow_account = {
        "id": f"treasury_ESCROW_{property_data['id']}",
        "object": "treasury.financial_account",
        "balance": {
            "cash": {"usd": deposit_amount},
            "inbound_pending": {"usd": 0},
            "outbound_pending": {"usd": 0}
        },
        "country": "US",
        "created": int(move_in_date.timestamp()),
        "currency": "usd",
        "financial_addresses": [{
            "type": "ach",
            "ach": {
                "account_number": f"{random.randint(100000000, 999999999)}",
                "routing_number": "110000000"
            }
        }],
        "platform_restrictions": {
            "inbound_flows": "restricted",
            "outbound_flows": "restricted"
        },
        "status": "open",
        "supported_currencies": ["usd"],
        "metadata": {
            "property_id": property_data['id'],
            "tenant_id": tenant['id'],
            "landlord_id": property_data['landlord_id'],
            "deposit_date": move_in_date.isoformat(),
            "deposit_amount": str(deposit_amount)
        }
    }
    
    # Simulate move-out and deposit refund (for some properties)
    refund = None
    if random.random() > 0.7:  # 30% have moved out and processed refunds
        move_out_date = move_in_date + timedelta(days=random.randint(365, 730))  # 1-2 years later
        
        if random.random() > 0.3:  # 70% get full refund
            refund_amount = deposit_amount
            deduction_reason = None
            deduction_amount = 0
        else:  # 30% have deductions
            deduction_amount = random.randint(5000, deposit_amount // 2)  # $50 to half deposit
            refund_amount = deposit_amount - deduction_amount
            deduction_reason = random.choice([
                "carpet_cleaning", "wall_damage", "unpaid_utilities", 
                "missing_items", "excessive_wear", "cleaning_required"
            ])
        
        refund = {
            "id": f"treasury_refund_{generate_id()}",
            "object": "treasury.outbound_transfer",
            "amount": refund_amount,
            "currency": "usd",
            "created": int(move_out_date.timestamp()),
            "description": f"Security deposit refund - {property_data['address']['line1']}",
            "destination_payment_method": tenant['id'],
            "financial_account": escrow_account['id'],
            "status": "posted",
            "metadata": {
                "property_id": property_data['id'],
                "tenant_id": tenant['id'],
                "move_out_date": move_out_date.isoformat(),
                "original_deposit": str(deposit_amount),
                "refund_amount": str(refund_amount),
                "deduction_amount": str(deduction_amount),
                "deduction_reason": deduction_reason or "none"
            }
        }
        
        # Update escrow account balance
        escrow_account["balance"]["cash"]["usd"] = 0
        escrow_account["status"] = "closed"
    
    return escrow_account, refund

# =============================================================================
# MAINTENANCE MANAGEMENT
# =============================================================================

def process_maintenance_request(property_data: Dict, request_date: datetime) -> Tuple[Dict, Optional[Dict]]:
    """Process a maintenance request with vendor payment and potential tenant charge."""
    issue_type = random.choices(
        list(MAINTENANCE_TYPES.keys()),
        weights=[config['frequency'] for config in MAINTENANCE_TYPES.values()]
    )[0]
    
    type_config = MAINTENANCE_TYPES[issue_type]
    cost = random.randint(type_config['min_cost'], type_config['max_cost']) * 100  # Convert to cents
    markup = int(cost * PROPERTY_CONFIG['fees']['maintenance_markup'])
    
    vendor_name = f"{faker.company()} {issue_type.replace('_', ' ').title()} Services"
    
    # Vendor payment
    vendor_payment = {
        "id": f"pi_VENDOR_{generate_id()}",
        "object": "payment_intent",
        "amount": cost,
        "currency": "usd",
        "created": int(request_date.timestamp()),
        "description": f"Maintenance: {issue_type.replace('_', ' ')} - {property_data['address']['line1']}",
        "status": "succeeded",
        "charges": {
            "data": [{
                "id": f"ch_{generate_id()}",
                "amount": cost,
                "currency": "usd",
                "paid": True,
                "refunded": False,
                "disputed": False
            }]
        },
        "metadata": {
            "property_id": property_data['id'],
            "landlord_id": property_data['landlord_id'],
            "vendor": vendor_name,
            "issue_type": issue_type,
            "maintenance_type": "vendor_payment",
            "urgency": random.choice(["low", "medium", "high", "emergency"])
        }
    }
    
    # Tenant charge (if tenant-caused damage)
    tenant_charge = None
    if issue_type in ['damage_repair'] or random.random() < 0.2:  # 20% of maintenance charged to tenant
        tenant_charge = {
            "id": f"pi_MAINTENANCE_{generate_id()}",
            "object": "payment_intent",
            "amount": cost + markup,
            "currency": "usd",
            "customer": property_data['tenant']['id'],
            "created": int(request_date.timestamp()),
            "description": f"Maintenance charge: {issue_type.replace('_', ' ')}",
            "status": "succeeded" if random.random() > 0.1 else "failed",
            "charges": {
                "data": [{
                    "id": f"ch_{generate_id()}",
                    "amount": cost + markup,
                    "currency": "usd",
                    "paid": random.random() > 0.1,
                    "refunded": False,
                    "disputed": False
                }]
            },
            "metadata": {
                "property_id": property_data['id'],
                "related_vendor_payment": vendor_payment['id'],
                "maintenance_cost": str(cost),
                "markup": str(markup),
                "charge_reason": "tenant_responsibility"
            }
        }
    
    return vendor_payment, tenant_charge

# =============================================================================
# LANDLORD PAYOUTS
# =============================================================================

def process_landlord_payout(landlord: Dict, collected_rents: List[Dict], 
                          maintenance_costs: List[Dict], payout_date: datetime) -> Dict:
    """Process net income payout to landlord after fees and expenses."""
    # Calculate gross collected rent
    total_collected = sum(
        rent['amount'] for rent in collected_rents 
        if rent['status'] == 'succeeded'
    )
    
    # Calculate maintenance expenses
    total_maintenance = sum(
        cost['amount'] for cost in maintenance_costs
        if cost['metadata']['maintenance_type'] == 'vendor_payment'
    )
    
    # Calculate management fee
    management_fee = int(total_collected * PROPERTY_CONFIG['fees']['management_fee'])
    
    # Net payout amount
    net_payout = total_collected - management_fee - total_maintenance
    
    payout_schedule = landlord['metadata']['payout_schedule']
    
    transfer = {
        "id": f"tr_LANDLORD_{generate_id()}",
        "object": "transfer",
        "amount": max(0, net_payout),  # Ensure non-negative
        "currency": "usd",
        "created": int(payout_date.timestamp()),
        "destination": landlord['id'],
        "description": f"Rental income payout - {payout_schedule}",
        "metadata": {
            "landlord_id": landlord['metadata']['landlord_id'],
            "payout_period": payout_date.strftime('%Y-%m'),
            "payout_schedule": payout_schedule,
            "gross_collected": str(total_collected),
            "management_fee": str(management_fee),
            "maintenance_expenses": str(total_maintenance),
            "net_payout": str(net_payout),
            "property_count": str(len([r for r in collected_rents if r['status'] == 'succeeded'])),
            "management_fee_rate": str(PROPERTY_CONFIG['fees']['management_fee'])
        }
    }
    
    return transfer

# =============================================================================
# MAIN DATA GENERATION
# =============================================================================

def generate_propertyflow_data() -> Tuple[List[Dict], List[Dict], List[Dict], List[Dict], List[Dict], List[Dict], List[Dict]]:
    """Generate complete PropertyFlow property management platform data."""
    print("🏠 Generating PropertyFlow property management data...")
    
    all_landlords = []
    all_properties = []
    all_rent_payments = []
    all_security_deposits = []
    all_maintenance_payments = []
    all_landlord_payouts = []
    all_late_payments = []
    
    # Start date for data generation
    start_date = datetime(2022, 1, 1)
    
    # Generate landlords and properties per stage
    landlord_counter = 1
    property_counter = 1
    
    for month in range(24):  # 24 months of data
        current_date = calculate_monthly_date(start_date, month)
        stage_name, stage_config = get_stage_config(month)
        
        print(f"📅 Processing month {month + 1}/24 ({stage_name} stage)...")
        
        # Add new landlords this month (front-loaded)
        if month < 12:  # Add landlords in first year
            new_landlords_count = max(1, stage_config['landlords'] // 12)
            
            for _ in range(new_landlords_count):
                onboarding_date = current_date + timedelta(days=random.randint(0, 29))
                
                landlord = create_landlord_account(f"LL{landlord_counter:04d}", onboarding_date)
                all_landlords.append(landlord)
                
                # Create properties for this landlord
                properties_for_landlord = random.randint(1, min(10, stage_config['properties'] // stage_config['landlords']))
                
                for _ in range(properties_for_landlord):
                    property_data = create_property(f"P{property_counter:06d}", landlord)
                    all_properties.append(property_data)
                    
                    # Handle security deposit for new property
                    move_in_date = faker.date_time_between(start_date=start_date, end_date=current_date)
                    escrow_account, refund = handle_security_deposit(property_data, property_data['tenant'], move_in_date)
                    
                    all_security_deposits.append({
                        "escrow_account": escrow_account,
                        "refund": refund
                    })
                    
                    property_counter += 1
                
                landlord_counter += 1
        
        # Process monthly operations for existing properties
        active_properties = [p for p in all_properties]
        active_landlords = [l for l in all_landlords]
        
        monthly_rent_payments = []
        monthly_maintenance = []
        
        # Collect rent for all properties
        for property_data in active_properties:
            rent_payment = collect_monthly_rent(property_data, current_date, stage_config)
            all_rent_payments.append(rent_payment)
            monthly_rent_payments.append(rent_payment)
            
            # Track late payments separately
            if 'late_fee' in rent_payment.get('metadata', {}):
                all_late_payments.append(rent_payment)
        
        # Generate maintenance requests (5-15% of properties per month)
        maintenance_rate = random.uniform(0.05, 0.15)
        properties_needing_maintenance = random.sample(
            active_properties,
            min(int(len(active_properties) * maintenance_rate), len(active_properties))
        )
        
        for property_data in properties_needing_maintenance:
            maintenance_date = current_date + timedelta(days=random.randint(0, 29))
            vendor_payment, tenant_charge = process_maintenance_request(property_data, maintenance_date)
            
            all_maintenance_payments.append(vendor_payment)
            monthly_maintenance.append(vendor_payment)
            
            if tenant_charge:
                all_maintenance_payments.append(tenant_charge)
        
        # Process landlord payouts (monthly for now, could be adjusted based on schedule)
        for landlord in active_landlords:
            landlord_properties = [p for p in active_properties if p['landlord_id'] == landlord['metadata']['landlord_id']]
            landlord_rents = [r for r in monthly_rent_payments if r['metadata']['landlord_id'] == landlord['metadata']['landlord_id']]
            landlord_maintenance = [m for m in monthly_maintenance if m['metadata'].get('landlord_id') == landlord['metadata']['landlord_id']]
            
            if landlord_rents:  # Only create payout if there were rent collections
                payout_date = current_date + timedelta(days=random.randint(25, 30))
                payout = process_landlord_payout(landlord, landlord_rents, landlord_maintenance, payout_date)
                all_landlord_payouts.append(payout)
    
    print(f"✅ Generated {len(all_properties)} properties, {len(all_landlords)} landlords, {len(all_rent_payments)} rent payments")
    return (all_landlords, all_properties, all_rent_payments, all_security_deposits, 
            all_maintenance_payments, all_landlord_payouts, all_late_payments)

# =============================================================================
# ANALYTICS AND METRICS
# =============================================================================

def calculate_property_metrics(landlords: List[Dict], properties: List[Dict], 
                             rent_payments: List[Dict], late_payments: List[Dict],
                             maintenance_payments: List[Dict], payouts: List[Dict]) -> Dict:
    """Calculate comprehensive property management metrics."""
    print("📊 Calculating property management metrics...")
    
    # Convert to DataFrames for analysis
    rent_df = pd.DataFrame(rent_payments)
    late_df = pd.DataFrame(late_payments)
    
    # Basic counts
    total_properties = len(properties)
    total_landlords = len(landlords)
    total_rent_payments = len(rent_payments)
    
    # Revenue analysis
    successful_rents = rent_df[rent_df['status'] == 'succeeded']
    total_rent_collected = successful_rents['amount'].sum() if not successful_rents.empty else 0
    
    # Collection rates
    collection_rate = len(successful_rents) / len(rent_df) if len(rent_df) > 0 else 0
    late_payment_rate = len(late_df) / len(rent_df) if len(rent_df) > 0 else 0
    
    # NSF analysis
    nsf_payments = rent_df[rent_df['status'] == 'failed']
    nsf_rate = len(nsf_payments) / len(rent_df) if len(rent_df) > 0 else 0
    
    # Maintenance analysis
    maintenance_df = pd.DataFrame(maintenance_payments)
    vendor_payments = maintenance_df[maintenance_df['metadata'].apply(lambda x: x.get('maintenance_type') == 'vendor_payment')]
    total_maintenance_costs = vendor_payments['amount'].sum() if not vendor_payments.empty else 0
    
    # Payout analysis
    payout_df = pd.DataFrame(payouts)
    total_payouts = payout_df['amount'].sum() if not payout_df.empty else 0
    
    # Calculate average rent
    if properties:
        average_rent = sum(p['rent_amount'] for p in properties) / len(properties)
    else:
        average_rent = 0
    
    # Security deposit analysis
    total_deposits_held = sum(p['security_deposit'] for p in properties)
    
    return {
        "total_properties": total_properties,
        "total_landlords": total_landlords,
        "occupied_properties": len([p for p in properties if p['occupied']]),
        "occupancy_rate": len([p for p in properties if p['occupied']]) / total_properties if total_properties > 0 else 0,
        "total_rent_payments": total_rent_payments,
        "successful_payments": len(successful_rents),
        "collection_rate": collection_rate,
        "late_payment_rate": late_payment_rate,
        "nsf_rate": nsf_rate,
        "total_rent_collected": total_rent_collected,
        "average_rent_amount": average_rent,
        "total_maintenance_costs": total_maintenance_costs,
        "maintenance_requests_per_property": len(maintenance_payments) / total_properties if total_properties > 0 else 0,
        "total_landlord_payouts": total_payouts,
        "total_security_deposits_held": total_deposits_held,
        "management_fee_revenue": total_rent_collected * PROPERTY_CONFIG['fees']['management_fee'],
        "platform_metrics": {
            "properties_by_type": {ptype: len([p for p in properties if p['property_type'] == ptype]) for ptype in PROPERTY_TYPES.keys()},
            "avg_properties_per_landlord": total_properties / total_landlords if total_landlords > 0 else 0,
            "monthly_recurring_revenue": total_rent_collected / 24,  # Average monthly rent
            "net_platform_revenue": total_rent_collected * PROPERTY_CONFIG['fees']['management_fee']
        }
    }

# =============================================================================
# FILE OUTPUT
# =============================================================================

def save_propertyflow_data(landlords: List[Dict], properties: List[Dict], 
                          rent_payments: List[Dict], security_deposits: List[Dict],
                          maintenance_payments: List[Dict], landlord_payouts: List[Dict],
                          late_payments: List[Dict], metrics: Dict) -> None:
    """Save all PropertyFlow data to JSON files."""
    print("💾 Saving PropertyFlow data to files...")
    
    output_dir = "property_data"
    
    # Ensure output directory exists
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    files_to_save = {
        "landlords.json": landlords,
        "properties.json": properties,
        "rent_payments.json": rent_payments,
        "security_deposits.json": security_deposits,
        "maintenance_payments.json": maintenance_payments,
        "landlord_payouts.json": landlord_payouts,
        "late_payments.json": late_payments,
        "property_metrics.json": metrics
    }
    
    for filename, data in files_to_save.items():
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    print(f"📁 Data saved to {output_dir}/ directory")

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution function."""
    print("\n" + "="*80)
    print("🏠 PROPERTYFLOW PROPERTY MANAGEMENT PLATFORM DATA GENERATOR")
    print("="*80)
    
    try:
        # Generate all data
        start_time = datetime.now()
        
        landlords, properties, rent_payments, security_deposits, maintenance_payments, landlord_payouts, late_payments = generate_propertyflow_data()
        
        # Calculate metrics
        metrics = calculate_property_metrics(
            landlords, properties, rent_payments, late_payments,
            maintenance_payments, landlord_payouts
        )
        
        # Save data
        save_propertyflow_data(
            landlords, properties, rent_payments, security_deposits,
            maintenance_payments, landlord_payouts, late_payments, metrics
        )
        
        # Print summary
        execution_time = datetime.now() - start_time
        
        print("\n" + "="*80)
        print("🏠 PROPERTYFLOW PROPERTY MANAGEMENT DATA GENERATION COMPLETE")
        print("="*80)
        
        print(f"\n📊 GENERATION SUMMARY:")
        print(f"   Total properties: {metrics['total_properties']:,}")
        print(f"   Active landlords: {metrics['total_landlords']:,}")
        print(f"   Occupancy rate: {metrics['occupancy_rate']:.1%}")
        print(f"   Rent payments processed: {metrics['total_rent_payments']:,}")
        
        print(f"\n💰 FINANCIAL METRICS:")
        print(f"   Total rent collected: ${metrics['total_rent_collected']:,.2f}")
        print(f"   Collection rate: {metrics['collection_rate']:.1%}")
        print(f"   Late payment rate: {metrics['late_payment_rate']:.1%}")
        print(f"   NSF rate: {metrics['nsf_rate']:.1%}")
        print(f"   Average rent: ${metrics['average_rent_amount']:,.2f}")
        
        print(f"\n🔧 OPERATIONS METRICS:")
        print(f"   Maintenance costs: ${metrics['total_maintenance_costs']:,.2f}")
        print(f"   Maintenance requests per property: {metrics['maintenance_requests_per_property']:.1f}")
        print(f"   Security deposits held: ${metrics['total_security_deposits_held']:,.2f}")
        print(f"   Total landlord payouts: ${metrics['total_landlord_payouts']:,.2f}")
        
        print(f"\n🏢 PLATFORM METRICS:")
        print(f"   Management fee revenue: ${metrics['management_fee_revenue']:,.2f}")
        print(f"   Properties by type:")
        for ptype, count in metrics['platform_metrics']['properties_by_type'].items():
            print(f"     {ptype.title()}: {count:,}")
        print(f"   Avg properties per landlord: {metrics['platform_metrics']['avg_properties_per_landlord']:.1f}")
        
        print(f"\n📁 OUTPUT FILES:")
        print(f"   ✅ landlords.json - Landlord Connect accounts")
        print(f"   ✅ properties.json - Property details with tenants")
        print(f"   ✅ rent_payments.json - Monthly rent collections")
        print(f"   ✅ security_deposits.json - Escrow accounts and refunds")
        print(f"   ✅ maintenance_payments.json - Vendor and tenant charges")
        print(f"   ✅ landlord_payouts.json - Net income transfers")
        print(f"   ✅ late_payments.json - Late fees and penalties")
        print(f"   ✅ property_metrics.json - Complete platform analytics")
        
        print(f"\n🚀 Ready for property management platform prototyping!")
        print("="*80)
        print(f"\n⏱️ Total execution time: {execution_time.total_seconds():.1f} seconds")
        
    except Exception as e:
        print(f"\n❌ Error during generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
