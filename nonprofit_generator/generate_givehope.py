#!/usr/bin/env python3
"""
GiveHope Synthetic Stripe Non-Profit Data Generator

Generates realistic non-profit donation platform data with campaigns,
recurring donors, seasonal patterns, and employer matching.

Usage:
    python generate_givehope.py
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

# Non-profit donation configuration
DONATION_CONFIG = {
    'suggested_amounts': [25, 50, 100, 250, 500, 1000],  # Dollar amounts
    'recurring_frequencies': {
        'monthly': 0.6,      # 60% monthly recurring
        'quarterly': 0.2,    # 20% quarterly
        'annually': 0.2      # 20% annual
    },
    'campaign_types': [
        'disaster_relief',
        'education',
        'healthcare',
        'environment',
        'community'
    ],
    'employer_match_rate': 0.15,        # 15% of donations are matched
    'processing_fee_coverage': 0.30,    # 30% of donors cover fees
    'major_donor_threshold': 100000,    # $1,000+ for major donors
    'planned_giving_rate': 0.02         # 2% participate in planned giving
}

# Business lifecycle stages
LIFECYCLE = {
    'early': {
        'monthly_donations': 10000,    # $10K per month
        'donor_count': 200,
        'months': range(0, 8),
        'recurring_rate': 0.20,        # 20% become recurring
        'retention_rate': 0.65         # 65% donor retention
    },
    'growth': {
        'monthly_donations': 100000,   # $100K per month
        'donor_count': 2000,
        'months': range(8, 16),
        'recurring_rate': 0.35,        # 35% become recurring
        'retention_rate': 0.75         # 75% donor retention
    },
    'mature': {
        'monthly_donations': 1000000,  # $1M per month
        'donor_count': 20000,
        'months': range(16, 24),
        'recurring_rate': 0.50,        # 50% become recurring
        'retention_rate': 0.85         # 85% donor retention
    }
}

# Campaign types with specific characteristics
CAMPAIGN_DETAILS = {
    'disaster_relief': {
        'urgency': 'high',
        'goal_multiplier': 5.0,         # Larger goals for disasters
        'duration_days': (7, 30),       # Shorter campaigns
        'success_rate': 0.90,           # High success rate
        'donation_spike': 3.0           # 3x normal donation amount
    },
    'education': {
        'urgency': 'medium',
        'goal_multiplier': 1.5,
        'duration_days': (60, 120),
        'success_rate': 0.70,
        'donation_spike': 1.2
    },
    'healthcare': {
        'urgency': 'medium',
        'goal_multiplier': 2.0,
        'duration_days': (45, 90),
        'success_rate': 0.75,
        'donation_spike': 1.5
    },
    'environment': {
        'urgency': 'low',
        'goal_multiplier': 1.2,
        'duration_days': (90, 180),
        'success_rate': 0.60,
        'donation_spike': 1.0
    },
    'community': {
        'urgency': 'low',
        'goal_multiplier': 1.0,
        'duration_days': (30, 90),
        'success_rate': 0.65,
        'donation_spike': 1.1
    }
}

# Donor acquisition channels
ACQUISITION_CHANNELS = {
    'organic': 0.35,       # 35% organic (direct/referral)
    'email': 0.25,         # 25% email campaigns
    'social': 0.20,        # 20% social media
    'event': 0.15,         # 15% events/fundraisers
    'peer_to_peer': 0.05   # 5% peer-to-peer campaigns
}

# Seasonal giving patterns
SEASONAL_PATTERNS = {
    1: 1.2,   # January - New Year resolutions
    2: 0.9,   # February
    3: 1.0,   # March
    4: 1.1,   # April - Spring
    5: 1.0,   # May
    6: 0.8,   # June - Summer slump begins
    7: 0.7,   # July - Summer low
    8: 0.8,   # August
    9: 1.1,   # September - Back to school
    10: 1.3,  # October - Awareness campaigns
    11: 2.0,  # November - Giving Tuesday
    12: 2.8   # December - Year-end giving surge
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
    """Generate properly formatted Stripe IDs for nonprofit platform."""
    return {
        'customer': f"cus_{uuid.uuid4().hex[:14]}",
        'payment_intent': f"pi_{uuid.uuid4().hex[:24]}",
        'subscription': f"sub_{uuid.uuid4().hex[:21]}",
        'price': f"price_{uuid.uuid4().hex[:20]}",
        'checkout_session': f"cs_{uuid.uuid4().hex[:22]}",
        'payment_link': f"plink_{uuid.uuid4().hex[:18]}"
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

def get_giving_tuesday(year: int) -> int:
    """Calculate Giving Tuesday date (Tuesday after Thanksgiving)."""
    # Thanksgiving is 4th Thursday of November
    november_first = datetime(year, 11, 1)
    first_thursday = 3 - november_first.weekday() + 7 if november_first.weekday() > 3 else 3 - november_first.weekday()
    thanksgiving = november_first + timedelta(days=first_thursday + 21)  # 4th Thursday
    giving_tuesday = thanksgiving + timedelta(days=5)  # Tuesday after
    return giving_tuesday.day

def apply_seasonal_patterns(base_amount: int, date: datetime) -> int:
    """Apply seasonal giving patterns to donation amounts."""
    month = date.month
    multiplier = SEASONAL_PATTERNS.get(month, 1.0)
    
    # Special spike for Giving Tuesday
    if month == 11:
        giving_tuesday = get_giving_tuesday(date.year)
        if abs(date.day - giving_tuesday) <= 1:  # Tuesday or adjacent days
            multiplier *= 2.5  # Additional 150% spike on Giving Tuesday
    
    return int(base_amount * multiplier)

def generate_campaign_name(campaign_type: str) -> str:
    """Generate realistic campaign names based on type."""
    name_templates = {
        'disaster_relief': [
            "Emergency Relief Fund", "Disaster Response Initiative", 
            "Crisis Support Campaign", "Emergency Aid Drive"
        ],
        'education': [
            "Scholarships for Tomorrow", "Education Access Initiative",
            "Learning Opportunity Fund", "Student Success Campaign"
        ],
        'healthcare': [
            "Health Heroes Fund", "Medical Care Initiative",
            "Healing Hearts Campaign", "Healthcare Access Drive"
        ],
        'environment': [
            "Green Future Initiative", "Planet Protection Fund",
            "Environmental Action Campaign", "Climate Hope Project"
        ],
        'community': [
            "Community Strong Fund", "Neighborhood Impact Initiative",
            "Local Heroes Campaign", "Community Building Project"
        ]
    }
    
    base_name = random.choice(name_templates[campaign_type])
    
    # Add year or location sometimes
    if random.random() < 0.3:
        base_name += f" {random.randint(2023, 2024)}"
    elif random.random() < 0.2:
        base_name += f" - {fake.city()}"
    
    return base_name

# =============================================================================
# DONOR PROFILE GENERATION
# =============================================================================

def generate_donor(donor_id: str, first_donation_date: datetime) -> Dict[str, Any]:
    """Generate comprehensive donor profile with giving preferences."""
    stripe_ids = generate_stripe_ids()
    
    # Determine donor type (90% individual, 8% corporate, 2% foundation)
    donor_type = random.choices(
        ['individual', 'corporate', 'foundation'],
        weights=[90, 8, 2]
    )[0]
    
    # Generate basic information
    if donor_type == 'individual':
        name = fake.name()
        email = fake.email()
        is_major_donor = random.random() < 0.05  # 5% are major donors
    elif donor_type == 'corporate':
        name = fake.company()
        email = f"giving@{name.lower().replace(' ', '').replace(',', '').replace('.', '')}.com"
        is_major_donor = random.random() < 0.25  # 25% of corporate donors are major
    else:  # foundation
        name = f"{fake.last_name()} Foundation"
        email = f"grants@{name.lower().replace(' ', '').replace(',', '')}.org"
        is_major_donor = random.random() < 0.60  # 60% of foundations are major donors
    
    # Generate preferences
    preferred_causes = random.sample(DONATION_CONFIG['campaign_types'], k=random.randint(1, 3))
    
    return {
        "id": stripe_ids['customer'],
        "object": "customer",
        "created": int(first_donation_date.timestamp()),
        "name": name,
        "email": email,
        "description": f"GiveHope donor - {donor_type}",
        "address": {
            "line1": fake.street_address(),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "postal_code": fake.zipcode(),
            "country": "US"
        },
        "phone": fake.phone_number(),
        "metadata": {
            "donor_id": donor_id,
            "donor_type": donor_type,
            "first_donation": first_donation_date.isoformat(),
            "lifetime_value_cents": 0,
            "donation_count": 0,
            "preferred_causes": preferred_causes,
            "recurring_donor": False,
            "major_donor": is_major_donor,
            "acquisition_channel": weighted_choice(ACQUISITION_CHANNELS),
            "communication_preference": random.choice(['email', 'mail', 'both', 'none']),
            "tax_receipt_required": random.choice([True, False]) if donor_type == 'individual' else True,
            "anonymous": random.random() < 0.10,  # 10% prefer anonymity
            "employer": fake.company() if donor_type == 'individual' and random.random() < 0.7 else None,
            "age_group": random.choice(['18-25', '26-35', '36-50', '51-65', '65+']) if donor_type == 'individual' else None,
            "giving_capacity": random.choice(['low', 'medium', 'high', 'major']) if is_major_donor else random.choice(['low', 'medium', 'high']),
            "planned_giving_prospect": random.random() < DONATION_CONFIG['planned_giving_rate'],
            "volunteer": random.random() < 0.3,  # 30% also volunteer
            "event_attendee": random.random() < 0.4  # 40% attend events
        }
    }

# =============================================================================
# CAMPAIGN MANAGEMENT
# =============================================================================

def create_campaign(campaign_type: str, start_date: datetime, stage: str) -> Dict[str, Any]:
    """Create fundraising campaign with type-specific characteristics."""
    campaign_config = CAMPAIGN_DETAILS[campaign_type]
    stage_config = LIFECYCLE[stage]
    
    # Generate campaign details
    campaign_id = f"campaign_{uuid.uuid4().hex[:12]}"
    campaign_name = generate_campaign_name(campaign_type)
    
    # Calculate goal based on stage and campaign type
    base_goal = stage_config['monthly_donations'] * campaign_config['goal_multiplier']
    goal = int(base_goal + random.uniform(-0.3, 0.5) * base_goal)  # ±30% to +50% variation
    
    # Calculate duration
    min_days, max_days = campaign_config['duration_days']
    duration = random.randint(min_days, max_days)
    end_date = start_date + timedelta(days=duration)
    
    # Determine matching sponsor (20% chance)
    has_matching = random.random() < 0.2
    matching_sponsor = fake.company() if has_matching else None
    match_ratio = random.choice([0.5, 1.0, 2.0]) if has_matching else 0
    
    return {
        "id": campaign_id,
        "name": campaign_name,
        "type": campaign_type,
        "goal_cents": goal * 100,  # Convert to cents
        "goal_dollars": goal,
        "raised_cents": 0,
        "raised_dollars": 0,
        "donor_count": 0,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "duration_days": duration,
        "status": "active",
        "description": f"Help us make a difference with our {campaign_name} campaign.",
        "image_url": f"https://givehope.org/images/{campaign_type}_{random.randint(1, 5)}.jpg",
        "target_audience": random.choice(['general', 'major_donors', 'young_professionals', 'families']),
        "fundraising_team": [fake.name() for _ in range(random.randint(2, 5))],
        "metadata": {
            "urgency": campaign_config['urgency'],
            "success_rate": campaign_config['success_rate'],
            "donation_spike": campaign_config['donation_spike'],
            "matching_sponsor": matching_sponsor,
            "match_ratio": match_ratio,
            "match_cap_cents": int(goal * 0.5 * 100) if has_matching else 0,
            "peer_to_peer_enabled": random.choice([True, False]),
            "social_sharing_enabled": True,
            "thank_you_video": random.choice([True, False]),
            "update_frequency": random.choice(['daily', 'weekly', 'biweekly']),
            "geographic_focus": random.choice([None, fake.state(), fake.country()]),
            "beneficiary_stories": random.randint(3, 8),
            "media_coverage": random.choice([True, False])
        }
    }

# =============================================================================
# DONATION PROCESSING
# =============================================================================

def process_donation(donor: Dict[str, Any], campaign: Dict[str, Any], 
                    donation_date: datetime, is_recurring: bool = False) -> Tuple[Dict[str, Any], Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """Process donation with employer matching and tax receipt generation."""
    stripe_ids = generate_stripe_ids()
    
    # Determine donation amount
    if donor['metadata']['major_donor']:
        # Major donors: $1,000 - $25,000
        amount_cents = random.randint(100000, 2500000)
    elif donor['metadata']['giving_capacity'] == 'high':
        # High capacity: $500 - $2,000
        amount_cents = random.randint(50000, 200000)
    elif donor['metadata']['giving_capacity'] == 'medium':
        # Medium capacity: $100 - $500
        amount_cents = random.randint(10000, 50000)
    else:
        # Low capacity: suggested amounts
        amount_dollars = random.choice(DONATION_CONFIG['suggested_amounts'])
        amount_cents = amount_dollars * 100
    
    # Apply campaign-specific donation spike
    campaign_spike = campaign['metadata']['donation_spike']
    amount_cents = int(amount_cents * campaign_spike)
    
    # Apply seasonal patterns
    amount_cents = apply_seasonal_patterns(amount_cents, donation_date)
    
    # Add processing fee coverage (30% of donors)
    processing_fee = 0
    if random.random() < DONATION_CONFIG['processing_fee_coverage']:
        processing_fee = int(amount_cents * 0.029 + 30)  # 2.9% + $0.30
        total_amount = amount_cents + processing_fee
    else:
        total_amount = amount_cents
    
    # Determine payment success (96% success rate for donations)
    payment_succeeded = random.random() > 0.04
    
    # Generate dedication message (20% chance)
    dedication = None
    if random.random() < 0.2:
        dedication_types = [
            "In memory of {name}",
            "In honor of {name}",
            "In celebration of {name}",
            "In tribute to {name}"
        ]
        dedication = random.choice(dedication_types).format(name=fake.name())
    
    # Create payment intent
    payment_intent = {
        "id": stripe_ids['payment_intent'],
        "object": "payment_intent",
        "amount": total_amount,
        "currency": "usd",
        "status": "succeeded" if payment_succeeded else "requires_payment_method",
        "customer": donor['id'],
        "created": int(donation_date.timestamp()),
        "description": f"Donation to {campaign['name']}",
        "receipt_email": donor['email'] if not donor['metadata']['anonymous'] else None,
        "payment_method": f"pm_{uuid.uuid4().hex[:22]}",
        "payment_method_types": ["card"],
        "charges": {
            "object": "list",
            "data": [{
                "id": f"ch_{uuid.uuid4().hex[:24]}",
                "object": "charge",
                "amount": total_amount,
                "currency": "usd",
                "customer": donor['id'],
                "paid": payment_succeeded,
                "refunded": False,
                "disputed": False,
                "outcome": {
                    "network_status": "approved_by_network" if payment_succeeded else "declined_by_network",
                    "reason": None if payment_succeeded else "insufficient_funds",
                    "seller_message": "Payment complete." if payment_succeeded else "The card was declined.",
                    "type": "authorized" if payment_succeeded else "issuer_declined"
                }
            }]
        },
        "metadata": {
            "campaign_id": campaign['id'],
            "campaign_name": campaign['name'],
            "is_recurring": str(is_recurring),
            "covers_fees": str(processing_fee > 0),
            "processing_fee_cents": processing_fee,
            "donation_amount_cents": amount_cents,
            "tax_deductible": "true",
            "anonymous": str(donor['metadata']['anonymous']),
            "dedication": dedication,
            "donor_type": donor['metadata']['donor_type'],
            "acquisition_channel": donor['metadata']['acquisition_channel'],
            "giving_capacity": donor['metadata']['giving_capacity']
        }
    }
    
    # Handle employer matching (15% of donations)
    employer_match = None
    if (donor['metadata']['employer'] and 
        donor['metadata']['donor_type'] == 'individual' and
        random.random() < DONATION_CONFIG['employer_match_rate']):
        
        # Match typically 50-100% of donation, up to $5,000
        match_percentage = random.choice([0.5, 0.75, 1.0])
        match_amount = min(int(amount_cents * match_percentage), 500000)  # Cap at $5,000
        
        employer_match = {
            "id": stripe_ids['payment_intent'] + "_match",
            "object": "payment_intent",
            "amount": match_amount,
            "currency": "usd",
            "status": "succeeded",
            "customer": f"corp_{uuid.uuid4().hex[:12]}",  # Corporate customer
            "created": int((donation_date + timedelta(days=random.randint(1, 14))).timestamp()),
            "description": f"Employer match for donation to {campaign['name']}",
            "metadata": {
                "campaign_id": campaign['id'],
                "original_donation": payment_intent['id'],
                "original_donor": donor['id'],
                "employer": donor['metadata']['employer'],
                "match_percentage": match_percentage,
                "match_type": "employer_match",
                "tax_deductible": "true"
            }
        }
    
    # Generate tax receipt if required
    tax_receipt = None
    if (payment_succeeded and 
        donor['metadata']['tax_receipt_required'] and 
        amount_cents >= 2500):  # $25 minimum for receipt
        
        tax_receipt = {
            "id": f"receipt_{uuid.uuid4().hex[:16]}",
            "donation_id": payment_intent['id'],
            "donor_id": donor['id'],
            "donor_name": donor['name'] if not donor['metadata']['anonymous'] else "Anonymous",
            "donation_date": donation_date.isoformat(),
            "tax_year": donation_date.year,
            "deductible_amount_cents": amount_cents,  # Only donation, not fees
            "deductible_amount_dollars": amount_cents / 100,
            "organization_name": "GiveHope Foundation",
            "organization_ein": "12-3456789",
            "organization_address": "123 Giving Way, Hope City, HC 12345",
            "receipt_type": "donation",
            "goods_services_value": 0,  # Pure donation
            "description": f"Charitable contribution to {campaign['name']}",
            "dedication": dedication,
            "issued_date": donation_date.isoformat(),
            "metadata": {
                "campaign_id": campaign['id'],
                "campaign_type": campaign['type'],
                "employer_match_eligible": str(employer_match is not None)
            }
        }
    
    return payment_intent, employer_match, tax_receipt

# =============================================================================
# RECURRING DONATIONS
# =============================================================================

def setup_recurring_donation(donor: Dict[str, Any], campaign: Dict[str, Any], 
                            start_date: datetime) -> Dict[str, Any]:
    """Setup recurring donation subscription."""
    stripe_ids = generate_stripe_ids()
    
    # Determine frequency
    frequency = weighted_choice(DONATION_CONFIG['recurring_frequencies'])
    
    # Determine amount (usually smaller for recurring)
    if donor['metadata']['major_donor']:
        monthly_amount = random.randint(50000, 500000)  # $500-$5,000/month
    elif donor['metadata']['giving_capacity'] == 'high':
        monthly_amount = random.randint(10000, 100000)  # $100-$1,000/month
    elif donor['metadata']['giving_capacity'] == 'medium':
        monthly_amount = random.randint(2500, 25000)   # $25-$250/month
    else:
        monthly_amount = random.choice([2500, 5000, 10000])  # $25, $50, $100/month
    
    # Convert to appropriate interval amount
    if frequency == 'quarterly':
        interval_amount = monthly_amount * 3
        interval = 'month'
        interval_count = 3
    elif frequency == 'annually':
        interval_amount = monthly_amount * 12
        interval = 'year'
        interval_count = 1
    else:  # monthly
        interval_amount = monthly_amount
        interval = 'month'
        interval_count = 1
    
    # Generate subscription
    subscription = {
        "id": stripe_ids['subscription'],
        "object": "subscription",
        "customer": donor['id'],
        "status": "active",
        "created": int(start_date.timestamp()),
        "current_period_start": int(start_date.timestamp()),
        "current_period_end": int((start_date + timedelta(days=30 if frequency == 'monthly' else 90 if frequency == 'quarterly' else 365)).timestamp()),
        "cancel_at_period_end": False,
        "canceled_at": None,
        "collection_method": "charge_automatically",
        "items": {
            "object": "list",
            "data": [{
                "id": f"si_{uuid.uuid4().hex[:22]}",
                "object": "subscription_item",
                "price": {
                    "id": stripe_ids['price'],
                    "object": "price",
                    "active": True,
                    "currency": "usd",
                    "unit_amount": interval_amount,
                    "recurring": {
                        "interval": interval,
                        "interval_count": interval_count
                    },
                    "product": f"prod_recurring_donation_{frequency}"
                },
                "quantity": 1,
                "subscription": stripe_ids['subscription']
            }]
        },
        "default_payment_method": f"pm_{uuid.uuid4().hex[:22]}",
        "latest_invoice": f"in_{uuid.uuid4().hex[:24]}",
        "metadata": {
            "campaign_id": campaign['id'],
            "campaign_name": campaign['name'],
            "frequency": frequency,
            "monthly_equivalent_cents": monthly_amount,
            "monthly_equivalent_dollars": monthly_amount / 100,
            "dedication": random.choice([None, "In memory of...", "In honor of..."]),
            "send_updates": "true",
            "donor_type": donor['metadata']['donor_type'],
            "auto_increase": str(random.random() < 0.15),  # 15% opt for auto-increase
            "started_from_campaign": "true",
            "preferred_day_of_month": random.randint(1, 28) if frequency == 'monthly' else None
        }
    }
    
    return subscription

# =============================================================================
# MAIN DATA GENERATION
# =============================================================================

def generate_givehope_data() -> Tuple[List[Dict], List[Dict], List[Dict], List[Dict], List[Dict], List[Dict]]:
    """Generate complete GiveHope non-profit donation platform data."""
    print("❤️ Generating GiveHope non-profit donation data...")
    
    all_donors = []
    all_campaigns = []
    all_donations = []
    all_subscriptions = []
    all_employer_matches = []
    all_tax_receipts = []
    
    # Start date for data generation
    start_date = datetime(2023, 1, 1)
    
    donor_counter = 1
    
    # Track active campaigns by month
    active_campaigns = []
    
    # Generate data across 24 months
    for month in range(24):
        current_date = start_date + timedelta(days=30 * month)
        stage = get_lifecycle_stage(month)
        stage_config = LIFECYCLE[stage]
        
        print(f"📅 Processing month {month + 1}/24 ({stage} stage)...")
        
        # Generate new campaigns this month (1-3 campaigns per month)
        new_campaigns = random.randint(1, 3)
        for _ in range(new_campaigns):
            campaign_type = random.choice(DONATION_CONFIG['campaign_types'])
            campaign_start = current_date + timedelta(days=random.randint(0, 29))
            
            campaign = create_campaign(campaign_type, campaign_start, stage)
            all_campaigns.append(campaign)
            active_campaigns.append(campaign)
        
        # Remove expired campaigns
        active_campaigns = [c for c in active_campaigns 
                          if datetime.fromisoformat(c['end_date']) > current_date]
        
        # Generate new donors this month
        new_donors_this_month = stage_config['donor_count'] // 12  # Monthly donor acquisition
        
        for _ in range(new_donors_this_month):
            signup_date = current_date + timedelta(days=random.randint(0, 29))
            
            donor = generate_donor(f"DONOR_{donor_counter:06d}", signup_date)
            all_donors.append(donor)
            donor_counter += 1
        
        # Generate donations throughout the month
        target_monthly_volume = stage_config['monthly_donations'] * 100  # Convert to cents
        current_volume = 0
        
        # Get available donors for this month
        available_donors = [d for d in all_donors 
                          if d['created'] <= int(current_date.timestamp())]
        
        if not available_donors or not active_campaigns:
            continue
        
        # Generate donations until we reach target volume
        while current_volume < target_monthly_volume and len(available_donors) > 0:
            # Select random donor and campaign
            donor = random.choice(available_donors)
            campaign = random.choice(active_campaigns)
            
            # Check if donor aligns with campaign (preferred causes)
            if campaign['type'] in donor['metadata']['preferred_causes'] or random.random() < 0.3:
                donation_date = current_date + timedelta(
                    days=random.randint(0, 29),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
                
                # Process donation
                donation, employer_match, tax_receipt = process_donation(
                    donor, campaign, donation_date, is_recurring=False
                )
                
                if donation['status'] == 'succeeded':
                    all_donations.append(donation)
                    current_volume += donation['amount']
                    
                    # Update campaign raised amount
                    campaign['raised_cents'] += donation['metadata']['donation_amount_cents']
                    campaign['raised_dollars'] = campaign['raised_cents'] / 100
                    campaign['donor_count'] += 1
                    
                    # Update donor statistics
                    donor['metadata']['donation_count'] += 1
                    donor['metadata']['lifetime_value_cents'] += donation['metadata']['donation_amount_cents']
                    
                    # Add employer match if generated
                    if employer_match:
                        all_employer_matches.append(employer_match)
                        campaign['raised_cents'] += employer_match['amount']
                        campaign['raised_dollars'] = campaign['raised_cents'] / 100
                    
                    # Add tax receipt if generated
                    if tax_receipt:
                        all_tax_receipts.append(tax_receipt)
                    
                    # Setup recurring donation (based on stage recurring rate)
                    if (not donor['metadata']['recurring_donor'] and 
                        random.random() < stage_config['recurring_rate']):
                        
                        subscription = setup_recurring_donation(donor, campaign, donation_date)
                        all_subscriptions.append(subscription)
                        donor['metadata']['recurring_donor'] = True
        
        # Process existing recurring subscriptions (generate monthly charges)
        for subscription in all_subscriptions:
            if subscription['status'] == 'active':
                # Check if it's time for next charge
                last_charge = datetime.fromtimestamp(subscription['current_period_start'])
                frequency = subscription['metadata']['frequency']
                
                if frequency == 'monthly' and (current_date - last_charge).days >= 30:
                    # Generate recurring donation
                    donor = next(d for d in all_donors if d['id'] == subscription['customer'])
                    campaign = next(c for c in all_campaigns if c['id'] == subscription['metadata']['campaign_id'])
                    
                    recurring_donation, _, _ = process_donation(
                        donor, campaign, current_date, is_recurring=True
                    )
                    
                    if recurring_donation['status'] == 'succeeded':
                        all_donations.append(recurring_donation)
                        
                        # Update subscription period
                        subscription['current_period_start'] = int(current_date.timestamp())
                        subscription['current_period_end'] = int((current_date + timedelta(days=30)).timestamp())
    
    print(f"✅ Generated {len(all_donors)} donors, {len(all_campaigns)} campaigns, {len(all_donations)} donations")
    return all_donors, all_campaigns, all_donations, all_subscriptions, all_employer_matches, all_tax_receipts

# =============================================================================
# ANALYTICS AND REPORTING
# =============================================================================

def calculate_nonprofit_metrics(donors: List[Dict], campaigns: List[Dict], 
                               donations: List[Dict], subscriptions: List[Dict],
                               employer_matches: List[Dict]) -> Dict[str, Any]:
    """Calculate comprehensive non-profit analytics."""
    print("📊 Calculating GiveHope metrics...")
    
    # Basic counts
    total_donors = len(donors)
    total_campaigns = len(campaigns)
    total_donations = len([d for d in donations if d['status'] == 'succeeded'])
    recurring_donors = len([d for d in donors if d['metadata']['recurring_donor']])
    
    # Financial metrics
    successful_donations = [d for d in donations if d['status'] == 'succeeded']
    total_raised = sum(int(d['metadata']['donation_amount_cents']) for d in successful_donations)
    total_fees_covered = sum(int(d['metadata']['processing_fee_cents']) for d in successful_donations)
    
    # Average donation calculations
    avg_donation = total_raised / len(successful_donations) if successful_donations else 0
    avg_first_donation = sum(
        int(d['metadata']['donation_amount_cents']) for d in successful_donations 
        if donors[next(i for i, donor in enumerate(donors) if donor['id'] == d['customer'])]['metadata']['donation_count'] == 1
    ) / max(1, len([d for d in successful_donations if donors[next(i for i, donor in enumerate(donors) if donor['id'] == d['customer'])]['metadata']['donation_count'] == 1]))
    
    # Donor segmentation
    donor_segments = {
        'major_donors': len([d for d in donors if d['metadata']['major_donor']]),
        'recurring_donors': recurring_donors,
        'one_time_donors': total_donors - recurring_donors,
        'anonymous_donors': len([d for d in donors if d['metadata']['anonymous']])
    }
    
    # Campaign performance
    successful_campaigns = [c for c in campaigns if c['raised_cents'] >= c['goal_cents'] * 0.8]
    campaign_success_rate = (len(successful_campaigns) / len(campaigns) * 100) if campaigns else 0
    
    # Campaign type analysis
    campaign_performance = {}
    for campaign_type in DONATION_CONFIG['campaign_types']:
        type_campaigns = [c for c in campaigns if c['type'] == campaign_type]
        if type_campaigns:
            total_raised_type = sum(c['raised_cents'] for c in type_campaigns)
            avg_raised_type = total_raised_type / len(type_campaigns)
            campaign_performance[campaign_type] = {
                'count': len(type_campaigns),
                'total_raised_cents': total_raised_type,
                'total_raised_dollars': total_raised_type / 100,
                'avg_raised_cents': int(avg_raised_type),
                'avg_raised_dollars': avg_raised_type / 100,
                'success_rate': len([c for c in type_campaigns if c['raised_cents'] >= c['goal_cents'] * 0.8]) / len(type_campaigns) * 100
            }
    
    # Recurring donation metrics
    monthly_recurring_revenue = sum(
        int(sub['metadata']['monthly_equivalent_cents']) 
        for sub in subscriptions if sub['status'] == 'active'
    )
    
    # Seasonal analysis
    donations_by_month = defaultdict(list)
    for donation in successful_donations:
        month = datetime.fromtimestamp(donation['created']).month
        donations_by_month[month].append(int(donation['metadata']['donation_amount_cents']))
    
    seasonal_patterns = {}
    for month in range(1, 13):
        month_donations = donations_by_month[month]
        seasonal_patterns[month] = {
            'count': len(month_donations),
            'total_cents': sum(month_donations),
            'total_dollars': sum(month_donations) / 100,
            'avg_cents': sum(month_donations) / len(month_donations) if month_donations else 0,
            'avg_dollars': (sum(month_donations) / len(month_donations) / 100) if month_donations else 0
        }
    
    # Employer matching analysis
    total_employer_matches = len(employer_matches)
    total_match_amount = sum(match['amount'] for match in employer_matches)
    employer_match_rate = (total_employer_matches / total_donations * 100) if total_donations else 0
    
    # Acquisition channel analysis
    channel_performance = {}
    for channel in ACQUISITION_CHANNELS.keys():
        channel_donors = [d for d in donors if d['metadata']['acquisition_channel'] == channel]
        if channel_donors:
            total_ltv = sum(d['metadata']['lifetime_value_cents'] for d in channel_donors)
            channel_performance[channel] = {
                'donor_count': len(channel_donors),
                'total_ltv_cents': total_ltv,
                'total_ltv_dollars': total_ltv / 100,
                'avg_ltv_cents': total_ltv / len(channel_donors),
                'avg_ltv_dollars': (total_ltv / len(channel_donors)) / 100
            }
    
    return {
        "overview": {
            "total_donors": total_donors,
            "total_campaigns": total_campaigns,
            "total_donations": total_donations,
            "donation_success_rate": (total_donations / len(donations) * 100) if donations else 0,
            "campaign_success_rate": campaign_success_rate
        },
        "financial_metrics": {
            "total_raised_cents": total_raised,
            "total_raised_dollars": total_raised / 100,
            "total_fees_covered_cents": total_fees_covered,
            "total_fees_covered_dollars": total_fees_covered / 100,
            "average_donation_cents": int(avg_donation),
            "average_donation_dollars": avg_donation / 100,
            "average_first_donation_cents": int(avg_first_donation),
            "average_first_donation_dollars": avg_first_donation / 100,
            "monthly_recurring_revenue_cents": monthly_recurring_revenue,
            "monthly_recurring_revenue_dollars": monthly_recurring_revenue / 100
        },
        "donor_segments": donor_segments,
        "campaign_performance": campaign_performance,
        "seasonal_patterns": seasonal_patterns,
        "employer_matching": {
            "total_matches": total_employer_matches,
            "total_match_amount_cents": total_match_amount,
            "total_match_amount_dollars": total_match_amount / 100,
            "match_rate_percent": employer_match_rate
        },
        "acquisition_channels": channel_performance,
        "recurring_metrics": {
            "recurring_donor_count": recurring_donors,
            "recurring_rate_percent": (recurring_donors / total_donors * 100) if total_donors else 0,
            "active_subscriptions": len([s for s in subscriptions if s['status'] == 'active']),
            "monthly_revenue_cents": monthly_recurring_revenue,
            "monthly_revenue_dollars": monthly_recurring_revenue / 100
        }
    }

# =============================================================================
# OUTPUT GENERATION
# =============================================================================

def save_givehope_data(donors: List[Dict], campaigns: List[Dict], donations: List[Dict],
                      subscriptions: List[Dict], employer_matches: List[Dict], 
                      tax_receipts: List[Dict], metrics: Dict[str, Any]) -> None:
    """Save all generated data to JSON files."""
    print("💾 Saving GiveHope data to files...")
    
    output_dir = "nonprofit_data"
    os.makedirs(output_dir, exist_ok=True)
    
    # Campaign analytics (detailed breakdown)
    campaign_analytics = []
    for campaign in campaigns:
        campaign_donations = [d for d in donations if d['metadata']['campaign_id'] == campaign['id']]
        successful_donations = [d for d in campaign_donations if d['status'] == 'succeeded']
        
        analytics = {
            "campaign_id": campaign['id'],
            "campaign_name": campaign['name'],
            "campaign_type": campaign['type'],
            "goal_cents": campaign['goal_cents'],
            "raised_cents": campaign['raised_cents'],
            "goal_achievement_rate": (campaign['raised_cents'] / campaign['goal_cents'] * 100) if campaign['goal_cents'] > 0 else 0,
            "donor_count": len(set(d['customer'] for d in successful_donations)),
            "donation_count": len(successful_donations),
            "average_donation_cents": sum(int(d['metadata']['donation_amount_cents']) for d in successful_donations) / len(successful_donations) if successful_donations else 0,
            "duration_days": campaign['duration_days'],
            "start_date": campaign['start_date'],
            "end_date": campaign['end_date'],
            "matching_enabled": campaign['metadata']['match_ratio'] > 0,
            "urgency": campaign['metadata']['urgency']
        }
        campaign_analytics.append(analytics)
    
    # Donor analytics (segmentation and behavior)
    donor_analytics = []
    for donor in donors:
        donor_donations = [d for d in donations if d['customer'] == donor['id'] and d['status'] == 'succeeded']
        
        analytics = {
            "donor_id": donor['metadata']['donor_id'],
            "donor_type": donor['metadata']['donor_type'],
            "acquisition_channel": donor['metadata']['acquisition_channel'],
            "first_donation_date": donor['metadata']['first_donation'],
            "lifetime_value_cents": donor['metadata']['lifetime_value_cents'],
            "donation_count": len(donor_donations),
            "recurring_donor": donor['metadata']['recurring_donor'],
            "major_donor": donor['metadata']['major_donor'],
            "preferred_causes": donor['metadata']['preferred_causes'],
            "giving_capacity": donor['metadata']['giving_capacity'],
            "average_donation_cents": sum(int(d['metadata']['donation_amount_cents']) for d in donor_donations) / len(donor_donations) if donor_donations else 0,
            "months_active": len(set(datetime.fromtimestamp(d['created']).month for d in donor_donations)),
            "anonymous": donor['metadata']['anonymous'],
            "volunteer": donor['metadata']['volunteer']
        }
        donor_analytics.append(analytics)
    
    # Save main data files
    datasets = {
        "donors.json": donors,
        "campaigns.json": campaigns,
        "donations.json": donations,
        "subscriptions.json": subscriptions,
        "employer_matches.json": employer_matches,
        "tax_receipts.json": tax_receipts,
        "campaign_analytics.json": campaign_analytics,
        "donor_analytics.json": donor_analytics,
        "nonprofit_metrics.json": metrics
    }
    
    for filename, data in datasets.items():
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    print(f"📁 Data saved to {output_dir}/ directory")

def print_givehope_summary(donors: List[Dict], campaigns: List[Dict], donations: List[Dict],
                          subscriptions: List[Dict], employer_matches: List[Dict], 
                          metrics: Dict[str, Any]) -> None:
    """Print comprehensive GiveHope generation summary."""
    print("\n" + "="*80)
    print("❤️ GIVEHOPE NON-PROFIT DONATION PLATFORM DATA GENERATION COMPLETE")
    print("="*80)
    
    overview = metrics['overview']
    financial = metrics['financial_metrics']
    segments = metrics['donor_segments']
    recurring = metrics['recurring_metrics']
    employer = metrics['employer_matching']
    
    print(f"\n📊 GENERATION SUMMARY:")
    print(f"   Total donors: {overview['total_donors']:,}")
    print(f"   Active campaigns: {overview['total_campaigns']:,}")
    print(f"   Successful donations: {overview['total_donations']:,}")
    print(f"   Donation success rate: {overview['donation_success_rate']:.1f}%")
    print(f"   Campaign success rate: {overview['campaign_success_rate']:.1f}%")
    
    print(f"\n💰 FINANCIAL IMPACT:")
    print(f"   Total funds raised: ${financial['total_raised_dollars']:,.2f}")
    print(f"   Processing fees covered: ${financial['total_fees_covered_dollars']:,.2f}")
    print(f"   Average donation: ${financial['average_donation_dollars']:.2f}")
    print(f"   Monthly recurring revenue: ${financial['monthly_recurring_revenue_dollars']:,.2f}")
    
    print(f"\n👥 DONOR SEGMENTS:")
    print(f"   Major donors (>$1,000): {segments['major_donors']:,}")
    print(f"   Recurring donors: {segments['recurring_donors']:,} ({recurring['recurring_rate_percent']:.1f}%)")
    print(f"   One-time donors: {segments['one_time_donors']:,}")
    print(f"   Anonymous donors: {segments['anonymous_donors']:,}")
    
    print(f"\n🔄 RECURRING GIVING:")
    print(f"   Active subscriptions: {recurring['active_subscriptions']:,}")
    print(f"   Monthly recurring revenue: ${recurring['monthly_revenue_dollars']:,.2f}")
    print(f"   Recurring conversion rate: {recurring['recurring_rate_percent']:.1f}%")
    
    print(f"\n🏢 EMPLOYER MATCHING:")
    print(f"   Total matches: {employer['total_matches']:,}")
    print(f"   Match amount: ${employer['total_match_amount_dollars']:,.2f}")
    print(f"   Match rate: {employer['match_rate_percent']:.1f}%")
    
    print(f"\n📈 CAMPAIGN PERFORMANCE:")
    campaign_perf = metrics['campaign_performance']
    for campaign_type, stats in campaign_perf.items():
        print(f"   {campaign_type.replace('_', ' ').title()}: {stats['count']} campaigns, ${stats['total_raised_dollars']:,.0f} raised ({stats['success_rate']:.0f}% success)")
    
    print(f"\n🗓️ SEASONAL PATTERNS:")
    seasonal = metrics['seasonal_patterns']
    # Show peak months
    peak_months = sorted(seasonal.items(), key=lambda x: x[1]['total_dollars'], reverse=True)[:3]
    for month_num, data in peak_months:
        month_name = calendar.month_name[month_num]
        print(f"   {month_name}: ${data['total_dollars']:,.0f} ({data['count']} donations)")
    
    print(f"\n📁 OUTPUT FILES:")
    print(f"   ✅ donors.json - Donor profiles with giving history")
    print(f"   ✅ campaigns.json - Fundraising campaign details")
    print(f"   ✅ donations.json - All donation transactions")
    print(f"   ✅ subscriptions.json - Recurring donation setups")
    print(f"   ✅ employer_matches.json - Corporate matching gifts")
    print(f"   ✅ tax_receipts.json - Annual tax documentation")
    print(f"   ✅ campaign_analytics.json - Campaign performance data")
    print(f"   ✅ donor_analytics.json - Donor segmentation analysis")
    print(f"   ✅ nonprofit_metrics.json - Complete fundraising analytics")
    
    print(f"\n❤️ Ready for non-profit donation platform prototyping!")
    print("="*80)

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("❤️ GiveHope Synthetic Non-Profit Donation Data Generator")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        # Generate all data
        donors, campaigns, donations, subscriptions, employer_matches, tax_receipts = generate_givehope_data()
        
        # Calculate metrics
        metrics = calculate_nonprofit_metrics(donors, campaigns, donations, subscriptions, employer_matches)
        
        # Save data
        save_givehope_data(donors, campaigns, donations, subscriptions, employer_matches, tax_receipts, metrics)
        
        # Print summary
        print_givehope_summary(donors, campaigns, donations, subscriptions, employer_matches, metrics)
        
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"\n⏱️ Total execution time: {execution_time:.1f} seconds")
        
    except Exception as e:
        print(f"\n❌ Error during generation: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
