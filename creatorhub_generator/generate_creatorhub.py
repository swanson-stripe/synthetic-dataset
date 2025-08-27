#!/usr/bin/env python3
"""
CreatorHub Synthetic Stripe Connect Data Generator

Generates realistic content monetization platform data with creators,
fan subscriptions, content sales, tips, and fraud prevention.

Usage:
    python generate_creatorhub.py
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
import math

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

# Creator platform configuration
PLATFORM_CONFIG = {
    'platform_take_rate': 0.20,  # Platform keeps 20% of content sales
    'tip_take_rate': 0.10,       # Lower rate for tips (10%)
    'creator_tiers': {
        'starter': {'take_rate': 0.30, 'min_followers': 0, 'max_followers': 999},
        'growth': {'take_rate': 0.25, 'min_followers': 1000, 'max_followers': 9999},
        'established': {'take_rate': 0.20, 'min_followers': 10000, 'max_followers': 99999},
        'premium': {'take_rate': 0.15, 'min_followers': 100000, 'max_followers': None}
    },
    'content_types': [
        'video_course',
        'ebook',
        'membership',
        'coaching',
        'digital_download'
    ],
    'subscription_tiers': [499, 999, 1999, 4999],  # $4.99 to $49.99
    'content_prices': {
        'video_course': (1999, 19999),   # $19.99 - $199.99
        'ebook': (999, 4999),           # $9.99 - $49.99
        'membership': (999, 9999),      # $9.99 - $99.99
        'coaching': (9999, 49999),      # $99.99 - $499.99
        'digital_download': (199, 1999) # $1.99 - $19.99
    }
}

# Business lifecycle stages
LIFECYCLE = {
    'early': {
        'creators': 50,
        'monthly_gmv': 50000,     # $50K GMV
        'months': range(0, 8),
        'avg_fans_per_creator': 20,
        'content_items_per_creator': 3
    },
    'growth': {
        'creators': 500,
        'monthly_gmv': 500000,    # $500K GMV
        'months': range(8, 16),
        'avg_fans_per_creator': 100,
        'content_items_per_creator': 8
    },
    'mature': {
        'creators': 2000,         # Reduced from 5000 for performance
        'monthly_gmv': 2000000,   # $2M GMV
        'months': range(16, 24),
        'avg_fans_per_creator': 500,
        'content_items_per_creator': 15
    }
}

# Creator categories and niches
CREATOR_CATEGORIES = {
    'education': {
        'content_types': ['video_course', 'ebook', 'coaching'],
        'avg_price_multiplier': 1.5,
        'primary_platforms': ['youtube', 'udemy', 'linkedin']
    },
    'entertainment': {
        'content_types': ['membership', 'digital_download', 'video_course'],
        'avg_price_multiplier': 1.0,
        'primary_platforms': ['youtube', 'twitch', 'tiktok']
    },
    'lifestyle': {
        'content_types': ['ebook', 'coaching', 'membership'],
        'avg_price_multiplier': 1.2,
        'primary_platforms': ['instagram', 'youtube', 'tiktok']
    },
    'tech': {
        'content_types': ['video_course', 'ebook', 'coaching'],
        'avg_price_multiplier': 1.8,
        'primary_platforms': ['youtube', 'github', 'twitter']
    },
    'business': {
        'content_types': ['coaching', 'video_course', 'ebook'],
        'avg_price_multiplier': 2.0,
        'primary_platforms': ['linkedin', 'youtube', 'twitter']
    }
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
    """Generate properly formatted Stripe IDs for creator platform."""
    return {
        'account': f"acct_{uuid.uuid4().hex[:16]}",
        'customer': f"cus_{uuid.uuid4().hex[:14]}",
        'payment_intent': f"pi_{uuid.uuid4().hex[:24]}",
        'subscription': f"sub_{uuid.uuid4().hex[:21]}",
        'transfer': f"tr_{uuid.uuid4().hex[:24]}",
        'payout': f"po_{uuid.uuid4().hex[:24]}",
        'price': f"price_{uuid.uuid4().hex[:20]}",
        'product': f"prod_{uuid.uuid4().hex[:20]}"
    }

def get_lifecycle_stage(month: int) -> str:
    """Determine lifecycle stage based on month."""
    for stage, config in LIFECYCLE.items():
        if month in config['months']:
            return stage
    return 'mature'

def determine_creator_tier(follower_count: int) -> str:
    """Determine creator tier based on follower count."""
    for tier, config in PLATFORM_CONFIG['creator_tiers'].items():
        if follower_count >= config['min_followers']:
            if config['max_followers'] is None or follower_count <= config['max_followers']:
                return tier
    return 'starter'

def generate_follower_count() -> int:
    """Generate realistic follower count using log-normal distribution."""
    # Log-normal distribution skewed toward smaller creators
    return max(1, int(np.random.lognormal(mean=7, sigma=2)))

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

def get_tier_name(price_cents: int) -> str:
    """Get subscription tier name based on price."""
    tier_names = {
        499: "Supporter",
        999: "Fan",
        1999: "Super Fan",
        4999: "VIP"
    }
    return tier_names.get(price_cents, "Custom")

def get_tier_perks(price_cents: int) -> List[str]:
    """Get subscription tier perks based on price."""
    perks_by_tier = {
        499: ["Early access to content", "Discord access"],
        999: ["Early access", "Discord access", "Monthly livestream"],
        1999: ["All Fan perks", "Exclusive content", "1-on-1 Q&A monthly"],
        4999: ["All perks", "Personal consultation", "Custom content requests"]
    }
    return perks_by_tier.get(price_cents, ["Basic access"])

# =============================================================================
# CREATOR ACCOUNT MANAGEMENT
# =============================================================================

def create_creator_account(creator_id: str, onboarding_date: datetime) -> Dict[str, Any]:
    """Create Stripe Connect Express account for creator."""
    stripe_ids = generate_stripe_ids()
    
    # Generate creator profile
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = f"{first_name.lower()}{random.randint(10, 99)}"
    
    # Generate follower count and determine tier
    follower_count = generate_follower_count()
    tier = determine_creator_tier(follower_count)
    
    # Select creator category
    category = random.choice(list(CREATOR_CATEGORIES.keys()))
    category_config = CREATOR_CATEGORIES[category]
    
    # Generate engagement metrics
    engagement_rate = max(0.01, min(0.20, random.gauss(0.05, 0.03)))
    
    return {
        "id": stripe_ids['account'],
        "object": "account",
        "type": "express",
        "country": "US",
        "created": int(onboarding_date.timestamp()),
        "business_type": "individual",
        "individual": {
            "id": f"person_{uuid.uuid4().hex[:16]}",
            "first_name": first_name,
            "last_name": last_name,
            "email": f"{username}@email.com",
            "phone": fake.phone_number(),
            "dob": {
                "day": random.randint(1, 28),
                "month": random.randint(1, 12),
                "year": random.randint(1985, 2000)
            },
            "address": {
                "line1": fake.street_address(),
                "city": fake.city(),
                "state": fake.state_abbr(),
                "postal_code": fake.zipcode(),
                "country": "US"
            },
            "verification": {
                "status": "verified",
                "document": {
                    "back": f"file_{uuid.uuid4().hex[:24]}",
                    "front": f"file_{uuid.uuid4().hex[:24]}"
                }
            }
        },
        "business_profile": {
            "mcc": "5815",  # Digital goods and services
            "name": f"{username} Creative",
            "product_description": f"{category.title()} content creator",
            "support_phone": fake.phone_number(),
            "url": f"https://creatorhub.com/{username}"
        },
        "capabilities": {
            "card_payments": {"status": "active"},
            "transfers": {"status": "active"},
            "tax_reporting_us_1099_k": {"status": "active"}
        },
        "charges_enabled": True,
        "payouts_enabled": True,
        "details_submitted": True,
        "external_accounts": {
            "object": "list",
            "data": [{
                "id": f"ba_{uuid.uuid4().hex[:24]}",
                "object": "bank_account",
                "account_holder_type": "individual",
                "bank_name": random.choice(["Chase", "Bank of America", "Wells Fargo"]),
                "country": "US",
                "currency": "usd",
                "last4": str(random.randint(1000, 9999)),
                "routing_number": f"{random.randint(100000000, 999999999)}",
                "status": "verified"
            }]
        },
        "metadata": {
            "creator_id": creator_id,
            "username": username,
            "category": category,
            "content_focus": random.choice(category_config['content_types']),
            "tier": tier,
            "follower_count": str(follower_count),
            "engagement_rate": f"{engagement_rate:.3f}",
            "primary_platform": random.choice(category_config['primary_platforms']),
            "onboarding_date": onboarding_date.isoformat(),
            "content_published": "0",
            "total_earnings": "0",
            "fan_count": "0",
            "verification_status": "verified",
            "content_rating": "general",  # general, teen, mature
            "languages": random.choice(["en", "en,es", "en,fr", "en,de"])
        },
        "tos_acceptance": {
            "date": int(onboarding_date.timestamp()),
            "ip": fake.ipv4(),
            "user_agent": fake.user_agent()
        }
    }

def create_content_item(creator: Dict[str, Any], content_type: str) -> Dict[str, Any]:
    """Create a content item for sale."""
    category = creator['metadata']['category']
    category_config = CREATOR_CATEGORIES[category]
    
    # Get price range for content type
    price_range = PLATFORM_CONFIG['content_prices'][content_type]
    base_price = random.randint(*price_range)
    
    # Apply category multiplier
    final_price = int(base_price * category_config['avg_price_multiplier'])
    
    # Generate content metadata
    content_titles = {
        'video_course': [
            "Complete {category} Masterclass",
            "Advanced {category} Techniques",
            "Beginner's Guide to {category}",
            "{category} Fundamentals"
        ],
        'ebook': [
            "The Ultimate {category} Guide",
            "{category} Secrets Revealed",
            "Mastering {category} in 30 Days",
            "{category} Handbook"
        ],
        'membership': [
            "VIP {category} Community",
            "Premium {category} Access",
            "Elite {category} Membership",
            "Exclusive {category} Circle"
        ],
        'coaching': [
            "1-on-1 {category} Coaching",
            "Personal {category} Mentorship",
            "{category} Success Coaching",
            "Private {category} Sessions"
        ],
        'digital_download': [
            "{category} Templates Pack",
            "Premium {category} Resources",
            "{category} Toolkit",
            "Essential {category} Assets"
        ]
    }
    
    title_template = random.choice(content_titles[content_type])
    title = title_template.format(category=category.title())
    
    return {
        "id": f"content_{uuid.uuid4().hex[:16]}",
        "creator_id": creator['metadata']['creator_id'],
        "creator_account": creator['id'],
        "title": title,
        "type": content_type,
        "category": category,
        "price_cents": final_price,
        "price_dollars": final_price / 100,
        "description": f"High-quality {category} content by {creator['metadata']['username']}",
        "created": int(datetime.now().timestamp()),
        "status": "published",
        "download_count": 0,
        "rating": round(random.uniform(4.0, 5.0), 1),
        "review_count": random.randint(0, 50),
        "metadata": {
            "duration_minutes": random.randint(30, 480) if content_type == 'video_course' else None,
            "pages": random.randint(20, 200) if content_type == 'ebook' else None,
            "session_count": random.randint(1, 10) if content_type == 'coaching' else None,
            "file_format": random.choice(['PDF', 'MP4', 'ZIP', 'EPUB']) if content_type == 'digital_download' else None,
            "difficulty": random.choice(['beginner', 'intermediate', 'advanced']),
            "tags": [f"{category}_content", content_type, random.choice(['premium', 'bestseller', 'new'])]
        }
    }

# =============================================================================
# FAN CUSTOMER GENERATION
# =============================================================================

def generate_fan_customer(fan_id: str, signup_date: datetime) -> Dict[str, Any]:
    """Generate fan customer profile."""
    stripe_ids = generate_stripe_ids()
    
    # Fan demographics and preferences
    age_group = random.choice(['18-24', '25-34', '35-44', '45-54', '55+'])
    spending_tier = random.choices(
        ['low', 'medium', 'high', 'premium'],
        weights=[40, 35, 20, 5]
    )[0]
    
    return {
        "id": stripe_ids['customer'],
        "object": "customer",
        "created": int(signup_date.timestamp()),
        "email": fake.email(),
        "name": fake.name(),
        "phone": fake.phone_number(),
        "description": "CreatorHub fan",
        "address": {
            "line1": fake.street_address(),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "postal_code": fake.zipcode(),
            "country": "US"
        },
        "default_source": f"card_{uuid.uuid4().hex[:22]}",
        "metadata": {
            "fan_id": fan_id,
            "signup_date": signup_date.isoformat(),
            "age_group": age_group,
            "spending_tier": spending_tier,
            "preferred_categories": random.sample(list(CREATOR_CATEGORIES.keys()), k=random.randint(1, 3)),
            "subscription_count": "0",
            "total_spent_cents": "0",
            "favorite_creators": "[]",
            "engagement_level": random.choice(['low', 'medium', 'high']),
            "platform_referrer": random.choice(['organic', 'social', 'creator_referral', 'paid_ads']),
            "notification_preferences": random.choice(['all', 'creators_only', 'minimal', 'none'])
        }
    }

# =============================================================================
# SUBSCRIPTION MANAGEMENT
# =============================================================================

def create_fan_subscription(fan: Dict[str, Any], creator: Dict[str, Any], 
                           start_date: datetime) -> Dict[str, Any]:
    """Create fan subscription to creator."""
    stripe_ids = generate_stripe_ids()
    
    # Select subscription tier based on fan spending level
    spending_tier = fan['metadata']['spending_tier']
    if spending_tier == 'premium':
        tier_price = random.choice([1999, 4999])
    elif spending_tier == 'high':
        tier_price = random.choice([999, 1999])
    elif spending_tier == 'medium':
        tier_price = random.choice([499, 999])
    else:  # low
        tier_price = 499
    
    # Get creator's take rate based on their tier
    creator_tier = creator['metadata']['tier']
    platform_fee_rate = PLATFORM_CONFIG['creator_tiers'][creator_tier]['take_rate']
    
    return {
        "id": stripe_ids['subscription'],
        "object": "subscription",
        "customer": fan['id'],
        "status": "active",
        "created": int(start_date.timestamp()),
        "current_period_start": int(start_date.timestamp()),
        "current_period_end": int((start_date + timedelta(days=30)).timestamp()),
        "cancel_at_period_end": False,
        "canceled_at": None,
        "collection_method": "charge_automatically",
        "application_fee_percent": platform_fee_rate * 100,
        "transfer_data": {
            "destination": creator['id']
        },
        "items": {
            "object": "list",
            "data": [{
                "id": stripe_ids['subscription'] + "_item",
                "object": "subscription_item",
                "price": {
                    "id": stripe_ids['price'],
                    "object": "price",
                    "active": True,
                    "currency": "usd",
                    "unit_amount": tier_price,
                    "recurring": {
                        "interval": "month",
                        "interval_count": 1
                    },
                    "product": stripe_ids['product']
                },
                "quantity": 1,
                "subscription": stripe_ids['subscription']
            }]
        },
        "default_payment_method": f"pm_{uuid.uuid4().hex[:22]}",
        "latest_invoice": f"in_{uuid.uuid4().hex[:24]}",
        "metadata": {
            "creator_id": creator['metadata']['creator_id'],
            "creator_username": creator['metadata']['username'],
            "tier_name": get_tier_name(tier_price),
            "tier_price_cents": str(tier_price),
            "tier_price_dollars": str(tier_price / 100),
            "perks": ','.join(get_tier_perks(tier_price)),
            "auto_renew": "true",
            "gift_subscription": str(random.random() < 0.05),  # 5% are gifts
            "referral_code": f"REF{random.randint(1000, 9999)}" if random.random() < 0.1 else None
        }
    }

# =============================================================================
# CONTENT SALES PROCESSING
# =============================================================================

def process_content_purchase(buyer: Dict[str, Any], creator: Dict[str, Any], 
                           content_item: Dict[str, Any], purchase_date: datetime) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Process one-time content purchase."""
    stripe_ids = generate_stripe_ids()
    
    amount = content_item['price_cents']
    platform_fee = int(amount * PLATFORM_CONFIG['platform_take_rate'])
    creator_payout = amount - platform_fee
    
    # Create payment intent
    payment_intent = {
        "id": stripe_ids['payment_intent'],
        "object": "payment_intent",
        "amount": amount,
        "currency": "usd",
        "status": "succeeded" if random.random() > 0.02 else "requires_payment_method",
        "customer": buyer['id'],
        "created": int(purchase_date.timestamp()),
        "description": f"Purchase: {content_item['title']}",
        "application_fee_amount": platform_fee,
        "transfer_data": {
            "destination": creator['id']
        },
        "charges": {
            "object": "list",
            "data": [{
                "id": f"ch_{uuid.uuid4().hex[:24]}",
                "object": "charge",
                "amount": amount,
                "currency": "usd",
                "customer": buyer['id'],
                "paid": True,
                "refunded": False,
                "disputed": False
            }]
        },
        "metadata": {
            "content_id": content_item['id'],
            "content_title": content_item['title'],
            "content_type": content_item['type'],
            "creator_id": creator['metadata']['creator_id'],
            "creator_username": creator['metadata']['username'],
            "downloadable": str(content_item['type'] in ['ebook', 'digital_download']),
            "purchase_type": "content_sale",
            "category": content_item['category']
        }
    }
    
    # Create transfer to creator
    transfer = {
        "id": stripe_ids['transfer'],
        "object": "transfer",
        "amount": creator_payout,
        "currency": "usd",
        "destination": creator['id'],
        "created": int(purchase_date.timestamp()),
        "source_transaction": payment_intent['id'],
        "metadata": {
            "content_id": content_item['id'],
            "content_sale": "true",
            "creator_id": creator['metadata']['creator_id'],
            "platform_fee_cents": str(platform_fee),
            "creator_payout_cents": str(creator_payout)
        }
    }
    
    return payment_intent, transfer

# =============================================================================
# TIPS AND DONATIONS
# =============================================================================

def process_tip(fan: Dict[str, Any], creator: Dict[str, Any], 
               tip_date: datetime) -> Dict[str, Any]:
    """Process tip/donation to creator."""
    stripe_ids = generate_stripe_ids()
    
    # Tip amounts based on fan spending tier
    spending_tier = fan['metadata']['spending_tier']
    tip_amounts = {
        'low': [100, 200, 500],      # $1-$5
        'medium': [500, 1000, 2000], # $5-$20
        'high': [1000, 2500, 5000],  # $10-$50
        'premium': [2500, 5000, 10000] # $25-$100
    }
    
    amount = random.choice(tip_amounts[spending_tier])
    platform_fee = int(amount * PLATFORM_CONFIG['tip_take_rate'])  # Lower fee for tips
    
    # Generate optional tip message
    tip_messages = [
        "Keep up the great work!",
        "Love your content!",
        "Thanks for the inspiration!",
        "You're amazing!",
        "More content please!",
        ""  # Empty message
    ]
    
    return {
        "id": stripe_ids['payment_intent'],
        "object": "payment_intent",
        "amount": amount,
        "currency": "usd",
        "status": "succeeded",
        "customer": fan['id'],
        "created": int(tip_date.timestamp()),
        "description": f"Tip for {creator['metadata']['username']}",
        "application_fee_amount": platform_fee,
        "transfer_data": {
            "destination": creator['id']
        },
        "charges": {
            "object": "list",
            "data": [{
                "id": f"ch_{uuid.uuid4().hex[:24]}",
                "object": "charge",
                "amount": amount,
                "currency": "usd",
                "customer": fan['id'],
                "paid": True,
                "refunded": False,
                "disputed": False
            }]
        },
        "metadata": {
            "type": "tip",
            "creator_id": creator['metadata']['creator_id'],
            "creator_username": creator['metadata']['username'],
            "tip_amount_cents": str(amount),
            "tip_amount_dollars": str(amount / 100),
            "platform_fee_cents": str(platform_fee),
            "creator_payout_cents": str(amount - platform_fee),
            "message": random.choice(tip_messages),
            "anonymous": str(random.random() < 0.2)  # 20% anonymous tips
        }
    }

# =============================================================================
# FRAUD DETECTION
# =============================================================================

def detect_fraudulent_activity(transactions: List[Dict[str, Any]], 
                              customers: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Detect various fraud patterns in transactions."""
    
    # Card testing detection
    card_testing = []
    customer_transactions = defaultdict(list)
    for transaction in transactions:
        customer_transactions[transaction['customer']].append(transaction)
    
    for customer_id, txns in customer_transactions.items():
        # Multiple failed transactions in short time = card testing
        failed_txns = [t for t in txns if t['status'] != 'succeeded']
        if len(failed_txns) >= 3:
            time_span = max(t['created'] for t in failed_txns) - min(t['created'] for t in failed_txns)
            if time_span < 3600:  # Within 1 hour
                card_testing.append({
                    "customer_id": customer_id,
                    "failed_attempts": len(failed_txns),
                    "time_span_seconds": time_span,
                    "risk_level": "high"
                })
    
    # Account sharing detection (unusual access patterns)
    account_sharing = []
    for customer in customers:
        customer_txns = [t for t in transactions if t['customer'] == customer['id']]
        if len(customer_txns) > 20:  # High transaction volume
            # Check for different creators being accessed rapidly
            creator_times = defaultdict(list)
            for txn in customer_txns:
                if 'creator_id' in txn['metadata']:
                    creator_times[txn['metadata']['creator_id']].append(txn['created'])
            
            if len(creator_times) > 10:  # Accessing many creators
                account_sharing.append({
                    "customer_id": customer['id'],
                    "creators_accessed": len(creator_times),
                    "total_transactions": len(customer_txns),
                    "risk_level": "medium"
                })
    
    # Suspicious purchase patterns
    suspicious_purchases = []
    for customer_id, txns in customer_transactions.items():
        content_purchases = [t for t in txns if t['metadata'].get('purchase_type') == 'content_sale']
        if len(content_purchases) > 5:
            # Check for rapid bulk purchases
            purchase_times = sorted([t['created'] for t in content_purchases])
            rapid_purchases = 0
            for i in range(1, len(purchase_times)):
                if purchase_times[i] - purchase_times[i-1] < 300:  # Within 5 minutes
                    rapid_purchases += 1
            
            if rapid_purchases > 3:
                suspicious_purchases.append({
                    "customer_id": customer_id,
                    "rapid_purchases": rapid_purchases,
                    "total_content_purchases": len(content_purchases),
                    "risk_level": "medium"
                })
    
    return {
        "card_testing_attempts": card_testing,
        "suspected_account_sharing": account_sharing,
        "suspicious_purchases": suspicious_purchases,
        "total_blocked": len(card_testing) + len(suspicious_purchases),
        "fraud_rate_percent": ((len(card_testing) + len(suspicious_purchases)) / len(customers) * 100) if customers else 0
    }

# =============================================================================
# MAIN DATA GENERATION
# =============================================================================

def generate_creatorhub_data() -> Tuple[List[Dict], List[Dict], List[Dict], List[Dict], List[Dict], List[Dict], List[Dict]]:
    """Generate complete CreatorHub content monetization platform data."""
    print("🎨 Generating CreatorHub content monetization data...")
    
    all_creators = []
    all_fans = []
    all_content_items = []
    all_subscriptions = []
    all_content_sales = []
    all_tips = []
    all_transfers = []
    
    # Start date for data generation
    start_date = datetime(2023, 1, 1)
    
    creator_counter = 1
    fan_counter = 1
    
    # Generate data across 24 months
    for month in range(24):
        current_date = start_date + timedelta(days=30 * month)
        stage = get_lifecycle_stage(month)
        stage_config = LIFECYCLE[stage]
        
        print(f"📅 Processing month {month + 1}/24 ({stage} stage)...")
        
        # Generate new creators this month
        new_creators_this_month = stage_config['creators'] // 12  # Monthly onboarding
        
        for _ in range(new_creators_this_month):
            onboarding_date = current_date + timedelta(days=random.randint(0, 29))
            
            creator = create_creator_account(f"CREATOR_{creator_counter:06d}", onboarding_date)
            all_creators.append(creator)
            
            # Generate content items for new creator
            content_count = random.randint(1, stage_config['content_items_per_creator'])
            category = creator['metadata']['category']
            category_config = CREATOR_CATEGORIES[category]
            
            for _ in range(content_count):
                # Select content type from category's allowed types
                content_type = random.choice(category_config['content_types'])
                content_item = create_content_item(creator, content_type)
                all_content_items.append(content_item)
            
            creator_counter += 1
        
        # Generate new fans this month
        total_creators = len(all_creators)
        if total_creators > 0:
            new_fans_this_month = total_creators * stage_config['avg_fans_per_creator'] // 12
            
            for _ in range(min(new_fans_this_month, 500)):  # Cap for performance
                signup_date = current_date + timedelta(days=random.randint(0, 29))
                
                fan = generate_fan_customer(f"FAN_{fan_counter:06d}", signup_date)
                all_fans.append(fan)
                fan_counter += 1
        
        # Generate subscriptions and content sales
        active_creators = [c for c in all_creators 
                          if c['created'] <= int(current_date.timestamp())]
        active_fans = [f for f in all_fans 
                      if f['created'] <= int(current_date.timestamp())]
        
        if not active_creators or not active_fans:
            continue
        
        # Generate subscriptions (30% of fans subscribe each month)
        subscription_rate = 0.30
        fans_to_subscribe = random.sample(
            active_fans, 
            min(int(len(active_fans) * subscription_rate), len(active_fans))
        )
        
        for fan in fans_to_subscribe:
            # Select random creator to subscribe to
            creator = random.choice(active_creators)
            subscription_date = current_date + timedelta(days=random.randint(0, 29))
            
            subscription = create_fan_subscription(fan, creator, subscription_date)
            all_subscriptions.append(subscription)
        
        # Generate content sales (25% of fans buy content each month)
        content_sale_rate = 0.25
        fans_to_buy = random.sample(
            active_fans,
            min(int(len(active_fans) * content_sale_rate), len(active_fans))
        )
        
        # Only include content from active creators
        available_content = [c for c in all_content_items 
                           if any(ac['metadata']['creator_id'] == c['creator_id'] for ac in active_creators)]
        
        for fan in fans_to_buy:
            if available_content:
                content_item = random.choice(available_content)
                try:
                    creator = next(c for c in active_creators 
                                 if c['metadata']['creator_id'] == content_item['creator_id'])
                    
                    purchase_date = current_date + timedelta(days=random.randint(0, 29))
                    
                    payment, transfer = process_content_purchase(fan, creator, content_item, purchase_date)
                    
                    if payment['status'] == 'succeeded':
                        all_content_sales.append(payment)
                        all_transfers.append(transfer)
                        content_item['download_count'] += 1
                except StopIteration:
                    # Creator not found, skip this sale
                    continue
        
        # Generate tips (10% of fans tip each month)
        tip_rate = 0.10
        fans_to_tip = random.sample(
            active_fans,
            min(int(len(active_fans) * tip_rate), len(active_fans))
        )
        
        for fan in fans_to_tip:
            creator = random.choice(active_creators)
            tip_date = current_date + timedelta(days=random.randint(0, 29))
            
            tip = process_tip(fan, creator, tip_date)
            all_tips.append(tip)
    
    print(f"✅ Generated {len(all_creators)} creators, {len(all_fans)} fans, {len(all_content_sales)} content sales")
    return all_creators, all_fans, all_content_items, all_subscriptions, all_content_sales, all_tips, all_transfers

# =============================================================================
# ANALYTICS AND METRICS
# =============================================================================

def calculate_creator_analytics(creators: List[Dict], subscriptions: List[Dict], 
                               content_sales: List[Dict], tips: List[Dict]) -> List[Dict]:
    """Calculate detailed analytics for each creator."""
    print("📊 Calculating creator analytics...")
    
    creator_analytics = []
    
    for creator in creators:
        creator_id = creator['metadata']['creator_id']
        
        # Get creator's transactions
        creator_subscriptions = [s for s in subscriptions 
                                if s['metadata']['creator_id'] == creator_id]
        creator_sales = [s for s in content_sales 
                        if s['metadata']['creator_id'] == creator_id]
        creator_tips = [t for t in tips 
                       if t['metadata']['creator_id'] == creator_id]
        
        # Calculate MRR from subscriptions
        monthly_revenue = sum(
            s['items']['data'][0]['price']['unit_amount'] 
            for s in creator_subscriptions if s['status'] == 'active'
        )
        
        # Platform fees calculation
        creator_tier = creator['metadata']['tier']
        subscription_fee_rate = PLATFORM_CONFIG['creator_tiers'][creator_tier]['take_rate']
        content_fee_rate = PLATFORM_CONFIG['platform_take_rate']
        tip_fee_rate = PLATFORM_CONFIG['tip_take_rate']
        
        # Revenue breakdown
        subscription_revenue = sum(s['items']['data'][0]['price']['unit_amount'] for s in creator_subscriptions)
        content_revenue = sum(s['amount'] for s in creator_sales)
        tip_revenue = sum(t['amount'] for t in creator_tips)
        
        # Net earnings after platform fees
        net_subscription = int(subscription_revenue * (1 - subscription_fee_rate))
        net_content = int(content_revenue * (1 - content_fee_rate))
        net_tips = int(tip_revenue * (1 - tip_fee_rate))
        
        total_earnings = net_subscription + net_content + net_tips
        
        analytics = {
            "creator_id": creator_id,
            "username": creator['metadata']['username'],
            "category": creator['metadata']['category'],
            "tier": creator['metadata']['tier'],
            "follower_count": int(creator['metadata']['follower_count']),
            "fan_count": len(set(s['customer'] for s in creator_subscriptions)),
            "subscription_count": len(creator_subscriptions),
            "content_sales_count": len(creator_sales),
            "tips_count": len(creator_tips),
            "monthly_recurring_revenue_cents": monthly_revenue,
            "monthly_recurring_revenue_dollars": monthly_revenue / 100,
            "total_revenue_cents": subscription_revenue + content_revenue + tip_revenue,
            "total_revenue_dollars": (subscription_revenue + content_revenue + tip_revenue) / 100,
            "total_earnings_cents": total_earnings,
            "total_earnings_dollars": total_earnings / 100,
            "revenue_breakdown": {
                "subscriptions_cents": subscription_revenue,
                "content_sales_cents": content_revenue,
                "tips_cents": tip_revenue,
                "subscriptions_percent": (subscription_revenue / max(1, subscription_revenue + content_revenue + tip_revenue) * 100),
                "content_sales_percent": (content_revenue / max(1, subscription_revenue + content_revenue + tip_revenue) * 100),
                "tips_percent": (tip_revenue / max(1, subscription_revenue + content_revenue + tip_revenue) * 100)
            },
            "average_revenue_per_fan": total_earnings / max(1, len(set(s['customer'] for s in creator_subscriptions))),
            "engagement_rate": float(creator['metadata']['engagement_rate']),
            "primary_platform": creator['metadata']['primary_platform']
        }
        
        creator_analytics.append(analytics)
    
    return creator_analytics

def calculate_platform_metrics(creators: List[Dict], fans: List[Dict], subscriptions: List[Dict],
                              content_sales: List[Dict], tips: List[Dict], transfers: List[Dict]) -> Dict[str, Any]:
    """Calculate overall platform metrics."""
    print("📈 Calculating platform metrics...")
    
    # Basic counts
    total_creators = len(creators)
    total_fans = len(fans)
    active_subscriptions = len([s for s in subscriptions if s['status'] == 'active'])
    
    # Revenue calculations
    subscription_gmv = sum(s['items']['data'][0]['price']['unit_amount'] for s in subscriptions)
    content_gmv = sum(s['amount'] for s in content_sales if s['status'] == 'succeeded')
    tip_gmv = sum(t['amount'] for t in tips)
    total_gmv = subscription_gmv + content_gmv + tip_gmv
    
    # Platform revenue (fees collected)
    subscription_fees = sum(
        int(s['items']['data'][0]['price']['unit_amount'] * s['application_fee_percent'] / 100)
        for s in subscriptions
    )
    content_fees = sum(int(s['application_fee_amount']) for s in content_sales if s.get('application_fee_amount'))
    tip_fees = sum(int(t['application_fee_amount']) for t in tips if t.get('application_fee_amount'))
    total_platform_revenue = subscription_fees + content_fees + tip_fees
    
    # Creator tiers distribution
    tier_distribution = defaultdict(int)
    for creator in creators:
        tier_distribution[creator['metadata']['tier']] += 1
    
    # Category distribution
    category_distribution = defaultdict(int)
    for creator in creators:
        category_distribution[creator['metadata']['category']] += 1
    
    # Fan spending analysis
    fan_spending = defaultdict(int)
    for fan in fans:
        spending_tier = fan['metadata']['spending_tier']
        fan_spending[spending_tier] += 1
    
    # Monthly recurring revenue
    mrr = sum(s['items']['data'][0]['price']['unit_amount'] for s in subscriptions if s['status'] == 'active')
    
    return {
        "overview": {
            "total_creators": total_creators,
            "total_fans": total_fans,
            "active_subscriptions": active_subscriptions,
            "total_content_sales": len(content_sales),
            "total_tips": len(tips)
        },
        "revenue_metrics": {
            "total_gmv_cents": total_gmv,
            "total_gmv_dollars": total_gmv / 100,
            "platform_revenue_cents": total_platform_revenue,
            "platform_revenue_dollars": total_platform_revenue / 100,
            "take_rate_percent": (total_platform_revenue / total_gmv * 100) if total_gmv > 0 else 0,
            "mrr_cents": mrr,
            "mrr_dollars": mrr / 100,
            "arr_cents": mrr * 12,
            "arr_dollars": (mrr * 12) / 100
        },
        "revenue_breakdown": {
            "subscriptions_gmv_cents": subscription_gmv,
            "subscriptions_gmv_dollars": subscription_gmv / 100,
            "content_sales_gmv_cents": content_gmv,
            "content_sales_gmv_dollars": content_gmv / 100,
            "tips_gmv_cents": tip_gmv,
            "tips_gmv_dollars": tip_gmv / 100,
            "subscription_percentage": (subscription_gmv / total_gmv * 100) if total_gmv > 0 else 0,
            "content_sales_percentage": (content_gmv / total_gmv * 100) if total_gmv > 0 else 0,
            "tips_percentage": (tip_gmv / total_gmv * 100) if total_gmv > 0 else 0
        },
        "creator_distribution": {
            "by_tier": dict(tier_distribution),
            "by_category": dict(category_distribution)
        },
        "fan_distribution": {
            "by_spending_tier": dict(fan_spending)
        }
    }

# =============================================================================
# OUTPUT GENERATION
# =============================================================================

def save_creatorhub_data(creators: List[Dict], fans: List[Dict], content_items: List[Dict],
                        subscriptions: List[Dict], content_sales: List[Dict], tips: List[Dict],
                        transfers: List[Dict], creator_analytics: List[Dict], 
                        platform_metrics: Dict[str, Any]) -> None:
    """Save all generated data to JSON files."""
    print("💾 Saving CreatorHub data to files...")
    
    output_dir = "creator_data"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate fraud prevention data
    fraud_data = detect_fraudulent_activity(content_sales + tips, fans)
    
    # Generate payout data
    payouts = []
    for transfer in transfers:
        payout = {
            "id": f"po_{uuid.uuid4().hex[:24]}",
            "amount": transfer['amount'],
            "currency": "usd",
            "created": transfer['created'],
            "arrival_date": transfer['created'] + 86400,  # Next day
            "description": f"CreatorHub earnings payout",
            "destination": transfer['destination'],
            "method": "standard",
            "status": "paid",
            "type": "bank_account",
            "metadata": {
                "creator_payout": "true",
                "period": "weekly"
            }
        }
        payouts.append(payout)
    
    # Save main data files
    datasets = {
        "creators.json": creators,
        "fans.json": fans,
        "content_items.json": content_items,
        "subscriptions.json": subscriptions,
        "content_sales.json": content_sales,
        "tips.json": tips,
        "payouts.json": payouts,
        "fraud_prevention.json": fraud_data,
        "creator_analytics.json": creator_analytics,
        "platform_metrics.json": platform_metrics
    }
    
    for filename, data in datasets.items():
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    print(f"📁 Data saved to {output_dir}/ directory")

def print_creatorhub_summary(creators: List[Dict], fans: List[Dict], subscriptions: List[Dict],
                            content_sales: List[Dict], tips: List[Dict], 
                            platform_metrics: Dict[str, Any]) -> None:
    """Print comprehensive CreatorHub generation summary."""
    print("\n" + "="*80)
    print("🎨 CREATORHUB CONTENT MONETIZATION PLATFORM DATA GENERATION COMPLETE")
    print("="*80)
    
    overview = platform_metrics['overview']
    revenue = platform_metrics['revenue_metrics']
    breakdown = platform_metrics['revenue_breakdown']
    creator_dist = platform_metrics['creator_distribution']
    
    print(f"\n📊 GENERATION SUMMARY:")
    print(f"   Active creators: {overview['total_creators']:,}")
    print(f"   Total fans: {overview['total_fans']:,}")
    print(f"   Active subscriptions: {overview['active_subscriptions']:,}")
    print(f"   Content sales: {overview['total_content_sales']:,}")
    print(f"   Tips sent: {overview['total_tips']:,}")
    
    print(f"\n💰 REVENUE METRICS:")
    print(f"   Total GMV: ${revenue['total_gmv_dollars']:,.2f}")
    print(f"   Platform revenue: ${revenue['platform_revenue_dollars']:,.2f}")
    print(f"   Platform take rate: {revenue['take_rate_percent']:.1f}%")
    print(f"   Monthly recurring revenue: ${revenue['mrr_dollars']:,.2f}")
    print(f"   Estimated ARR: ${revenue['arr_dollars']:,.2f}")
    
    print(f"\n📈 REVENUE BREAKDOWN:")
    print(f"   Subscriptions: ${breakdown['subscriptions_gmv_dollars']:,.2f} ({breakdown['subscription_percentage']:.1f}%)")
    print(f"   Content sales: ${breakdown['content_sales_gmv_dollars']:,.2f} ({breakdown['content_sales_percentage']:.1f}%)")
    print(f"   Tips: ${breakdown['tips_gmv_dollars']:,.2f} ({breakdown['tips_percentage']:.1f}%)")
    
    print(f"\n🎯 CREATOR DISTRIBUTION:")
    print(f"   By tier:")
    for tier, count in creator_dist['by_tier'].items():
        percentage = (count / overview['total_creators'] * 100) if overview['total_creators'] > 0 else 0
        print(f"     {tier.title()}: {count} ({percentage:.1f}%)")
    
    print(f"   By category:")
    for category, count in creator_dist['by_category'].items():
        percentage = (count / overview['total_creators'] * 100) if overview['total_creators'] > 0 else 0
        print(f"     {category.title()}: {count} ({percentage:.1f}%)")
    
    print(f"\n📁 OUTPUT FILES:")
    print(f"   ✅ creators.json - Creator Connect accounts with analytics")
    print(f"   ✅ fans.json - Fan customer profiles and preferences")
    print(f"   ✅ content_items.json - Digital content catalog")
    print(f"   ✅ subscriptions.json - Fan subscription management")
    print(f"   ✅ content_sales.json - One-time content purchases")
    print(f"   ✅ tips.json - Creator tip transactions")
    print(f"   ✅ payouts.json - Creator earnings transfers")
    print(f"   ✅ fraud_prevention.json - Security and fraud detection")
    print(f"   ✅ creator_analytics.json - Individual creator performance")
    print(f"   ✅ platform_metrics.json - Complete platform analytics")
    
    print(f"\n🚀 Ready for content monetization platform prototyping!")
    print("="*80)

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("🎨 CreatorHub Synthetic Content Monetization Data Generator")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        # Generate all data
        creators, fans, content_items, subscriptions, content_sales, tips, transfers = generate_creatorhub_data()
        
        # Calculate analytics
        creator_analytics = calculate_creator_analytics(creators, subscriptions, content_sales, tips)
        platform_metrics = calculate_platform_metrics(creators, fans, subscriptions, content_sales, tips, transfers)
        
        # Save data
        save_creatorhub_data(creators, fans, content_items, subscriptions, content_sales, 
                            tips, transfers, creator_analytics, platform_metrics)
        
        # Print summary
        print_creatorhub_summary(creators, fans, subscriptions, content_sales, tips, platform_metrics)
        
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"\n⏱️ Total execution time: {execution_time:.1f} seconds")
        
    except Exception as e:
        print(f"\n❌ Error during generation: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
