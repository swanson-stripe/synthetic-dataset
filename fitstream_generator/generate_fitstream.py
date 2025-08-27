#!/usr/bin/env python3
"""
FitStream Synthetic Stripe Subscription Data Generator

Generates realistic subscription data for a fitness streaming platform with
trials, churn patterns, add-ons, and fitness-specific behaviors.

Usage:
    python generate_fitstream.py
"""

import json
import random
import uuid
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import os
import sys
from collections import defaultdict

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

# Subscription plans configuration
SUBSCRIPTION_PLANS = {
    'basic': {'price': 999, 'name': 'Basic', 'classes_per_month': 10},
    'unlimited': {'price': 1999, 'name': 'Unlimited', 'classes_per_month': 999},
    'family': {'price': 3999, 'name': 'Family', 'users': 5}
}

# Add-on services
ADD_ONS = {
    'personal_training': 4999,  # One-time sessions
    'nutrition_plan': 1499,     # Monthly add-on
    'equipment_rental': 2999    # Monthly
}

# Business lifecycle stages
LIFECYCLE = {
    'early': {
        'months': range(0, 8),
        'subscribers': 250,  # Reduced from 500
        'churn_rate': 0.10,  # 10% monthly churn
        'trial_conversion': 0.15,
        'failed_payment_rate': 0.06
    },
    'growth': {
        'months': range(8, 16),
        'subscribers': 1500,  # Reduced from 5000
        'churn_rate': 0.05,
        'trial_conversion': 0.25,
        'failed_payment_rate': 0.04
    },
    'mature': {
        'months': range(16, 24),
        'subscribers': 5000,  # Reduced from 50000
        'churn_rate': 0.02,
        'trial_conversion': 0.35,
        'failed_payment_rate': 0.02
    }
}

# Trial period options
TRIAL_PERIODS = [7, 14, 30]  # days

# Plan distribution by lifecycle stage
PLAN_DISTRIBUTION = {
    'early': {'basic': 0.60, 'unlimited': 0.35, 'family': 0.05},
    'growth': {'basic': 0.45, 'unlimited': 0.40, 'family': 0.15},
    'mature': {'basic': 0.35, 'unlimited': 0.45, 'family': 0.20}
}

# Acquisition channels
ACQUISITION_CHANNELS = {
    'organic': 0.25,
    'paid_social': 0.30,
    'referral': 0.20,
    'influencer': 0.15,
    'corporate': 0.10
}

# Device preferences
DEVICE_TYPES = ['ios', 'android', 'web', 'roku', 'apple_tv', 'smart_tv']

# Payment failure patterns
FAILURE_REASONS = {
    'card_expired': 0.40,
    'insufficient_funds': 0.35,
    'card_declined': 0.25
}

# Recovery success rates by attempt
RECOVERY_RATES = {
    1: 0.30,  # First retry
    2: 0.20,  # Second retry
    3: 0.10   # Third retry
}

# Seasonal multipliers for new subscriptions
SEASONAL_PATTERNS = {
    1: 2.5,   # January - New Year resolution spike
    2: 1.8,   # February
    3: 1.4,   # March - Spring prep
    4: 1.2,   # April
    5: 1.6,   # May - Summer prep
    6: 1.3,   # June
    7: 0.9,   # July - Summer vacation
    8: 0.8,   # August
    9: 1.1,   # September - Back to routine
    10: 1.0,  # October
    11: 0.7,  # November - Holidays
    12: 0.6   # December - Holidays
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
    """Generate properly formatted Stripe IDs for fitness platform."""
    return {
        'subscription': f"sub_FIT{uuid.uuid4().hex[:21]}",
        'customer': f"cus_{uuid.uuid4().hex[:14]}",
        'payment_intent': f"pi_{uuid.uuid4().hex[:24]}",
        'invoice': f"in_{uuid.uuid4().hex[:24]}",
        'price': f"price_{uuid.uuid4().hex[:20]}",
        'subscription_item': f"si_{uuid.uuid4().hex[:22]}",
        'payment_method': f"pm_{uuid.uuid4().hex[:22]}"
    }

def get_lifecycle_stage(month: int) -> str:
    """Determine lifecycle stage based on month."""
    for stage, config in LIFECYCLE.items():
        if month in config['months']:
            return stage
    return 'mature'

def apply_seasonal_pattern(base_count: int, month: int) -> int:
    """Apply seasonal patterns to subscription counts."""
    multiplier = SEASONAL_PATTERNS.get(month, 1.0)
    return int(base_count * multiplier * random.uniform(0.8, 1.2))

def calculate_churn_risk(engagement_score: float, payment_failures: int = 0) -> float:
    """Calculate churn risk score based on engagement and payment issues."""
    base_risk = max(0, (100 - engagement_score) / 100)
    payment_risk = min(0.5, payment_failures * 0.15)
    return min(1.0, base_risk + payment_risk)

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

# =============================================================================
# CUSTOMER GENERATION
# =============================================================================

def generate_customer_profile(customer_id: str, created_date: datetime) -> Dict[str, Any]:
    """Generate detailed customer profile with fitness-specific attributes."""
    engagement_score = max(10, min(100, random.gauss(65, 20)))
    workout_frequency = max(0, int(random.gauss(12, 8)))  # workouts per month
    
    # Generate fitness preferences
    workout_types = ['strength', 'cardio', 'yoga', 'pilates', 'hiit', 'dance', 'meditation']
    preferred_types = random.sample(workout_types, random.randint(1, 4))
    
    # Instructor preferences (synthetic names)
    instructors = ['Sarah M.', 'Mike T.', 'Jessica L.', 'David R.', 'Emma K.', 'Alex P.']
    preferred_instructors = random.sample(instructors, random.randint(0, 3))
    
    return {
        "id": customer_id,
        "object": "customer",
        "email": fake.email(),
        "name": fake.name(),
        "phone": fake.phone_number(),
        "created": int(created_date.timestamp()),
        "address": {
            "line1": fake.street_address(),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "postal_code": fake.zipcode(),
            "country": "US"
        },
        "metadata": {
            "acquisition_channel": weighted_choice(ACQUISITION_CHANNELS),
            "engagement_score": round(engagement_score, 1),
            "workout_frequency": workout_frequency,
            "preferred_workout_types": preferred_types,
            "preferred_instructors": preferred_instructors,
            "device_preferences": random.sample(DEVICE_TYPES, random.randint(1, 3)),
            "referral_count": random.randint(0, 5) if random.random() < 0.3 else 0,
            "corporate_account": random.random() < 0.15,
            "family_admin": False,  # Will be set for family plan admins
            "churn_risk_score": 0.0,  # Will be calculated later
            "lifetime_workouts": 0,
            "total_workout_minutes": 0
        }
    }

# =============================================================================
# SUBSCRIPTION GENERATION
# =============================================================================

def generate_fitness_subscription(customer: Dict[str, Any], start_date: datetime, stage: str) -> Dict[str, Any]:
    """Generate fitness subscription with trial and lifecycle patterns."""
    stripe_ids = generate_stripe_ids()
    stage_config = LIFECYCLE[stage]
    
    # Select plan based on stage distribution
    plan_key = weighted_choice(PLAN_DISTRIBUTION[stage])
    plan = SUBSCRIPTION_PLANS[plan_key]
    
    # Determine trial period
    trial_days = random.choice(TRIAL_PERIODS)
    trial_end = start_date + timedelta(days=trial_days)
    
    # Initial status (most start as trialing)
    status = "trialing" if random.random() < 0.85 else "active"
    
    # Calculate current period end
    if status == "trialing":
        current_period_start = int(trial_end.timestamp())
        current_period_end = int((trial_end + timedelta(days=30)).timestamp())
    else:
        current_period_start = int(start_date.timestamp())
        current_period_end = int((start_date + timedelta(days=30)).timestamp())
    
    # Generate add-ons (20% chance for basic plans, 40% for unlimited, 60% for family)
    addon_probability = {'basic': 0.20, 'unlimited': 0.40, 'family': 0.60}[plan_key]
    selected_addons = []
    
    if random.random() < addon_probability:
        num_addons = random.choices([1, 2, 3], weights=[70, 25, 5])[0]
        available_addons = list(ADD_ONS.keys())
        selected_addons = random.sample(available_addons, min(num_addons, len(available_addons)))
    
    # Build subscription items
    items = [{
        "id": stripe_ids['subscription_item'],
        "object": "subscription_item",
        "price": {
            "id": stripe_ids['price'],
            "object": "price",
            "active": True,
            "currency": "usd",
            "unit_amount": plan['price'],
            "recurring": {
                "interval": "month",
                "interval_count": 1
            },
            "product": f"prod_fitstream_{plan_key}"
        },
        "quantity": 1,
        "subscription": stripe_ids['subscription']
    }]
    
    # Add addon items
    for addon in selected_addons:
        addon_item_id = generate_stripe_ids()['subscription_item']
        items.append({
            "id": addon_item_id,
            "object": "subscription_item",
            "price": {
                "id": generate_stripe_ids()['price'],
                "object": "price",
                "active": True,
                "currency": "usd",
                "unit_amount": ADD_ONS[addon],
                "recurring": {
                    "interval": "month",
                    "interval_count": 1
                },
                "product": f"prod_fitstream_{addon}"
            },
            "quantity": 1,
            "subscription": stripe_ids['subscription']
        })
    
    # Family plan metadata
    family_members = []
    if plan_key == 'family':
        customer["metadata"]["family_admin"] = True
        # Generate family member emails
        for i in range(random.randint(2, 5)):
            family_members.append({
                "email": fake.email(),
                "name": fake.name(),
                "relation": random.choice(['spouse', 'child', 'parent', 'sibling']),
                "age_group": random.choice(['adult', 'teen', 'child'])
            })
    
    return {
        "id": stripe_ids['subscription'],
        "object": "subscription",
        "customer": customer['id'],
        "status": status,
        "created": int(start_date.timestamp()),
        "current_period_start": current_period_start,
        "current_period_end": current_period_end,
        "trial_start": int(start_date.timestamp()) if status == "trialing" else None,
        "trial_end": int(trial_end.timestamp()) if status == "trialing" else None,
        "cancel_at_period_end": False,
        "canceled_at": None,
        "pause_collection": None,  # For vacation holds
        "items": {
            "object": "list",
            "data": items,
            "has_more": False,
            "total_count": len(items)
        },
        "metadata": {
            "plan_type": plan_key,
            "signup_source": customer["metadata"]["acquisition_channel"],
            "trial_days": trial_days,
            "device_signup": random.choice(DEVICE_TYPES),
            "referral_code": f"REF{random.randint(1000, 9999)}" if random.random() < 0.25 else None,
            "corporate_discount": customer["metadata"]["corporate_account"],
            "family_members": len(family_members) if family_members else 0,
            "selected_addons": selected_addons,
            "engagement_tier": "new",  # Will evolve: new -> engaged -> champion -> at_risk
            "workout_streak": 0,
            "last_workout_date": None,
            "favorite_workout_type": random.choice(['strength', 'cardio', 'yoga', 'hiit']),
            "total_classes_booked": 0,
            "no_show_count": 0
        },
        "family_members": family_members if family_members else []
    }

def handle_subscription_lifecycle(subscription: Dict[str, Any], current_date: datetime, 
                                customer: Dict[str, Any], stage: str) -> Tuple[Dict[str, Any], Dict[str, Any], List[Dict]]:
    """Process subscription lifecycle events including trials, churn, and engagement."""
    stage_config = LIFECYCLE[stage]
    events = []
    
    # Handle trial conversion
    if subscription['status'] == 'trialing' and subscription['trial_end']:
        trial_end_date = datetime.fromtimestamp(subscription['trial_end'])
        if current_date >= trial_end_date:
            # Determine conversion based on engagement and stage
            base_conversion = stage_config['trial_conversion']
            engagement_factor = customer["metadata"]["engagement_score"] / 100
            conversion_rate = base_conversion * (0.5 + engagement_factor)
            
            if random.random() < conversion_rate:
                subscription['status'] = 'active'
                subscription['trial_end'] = None
                events.append({
                    "type": "trial_converted",
                    "date": current_date.isoformat(),
                    "subscription_id": subscription['id'],
                    "customer_id": customer['id']
                })
            else:
                subscription['status'] = 'canceled'
                subscription['canceled_at'] = int(current_date.timestamp())
                events.append({
                    "type": "trial_expired",
                    "date": current_date.isoformat(),
                    "subscription_id": subscription['id'],
                    "customer_id": customer['id']
                })
    
    # Handle active subscription churn
    elif subscription['status'] == 'active':
        monthly_churn_rate = stage_config['churn_rate']
        
        # Adjust churn rate based on engagement
        engagement_score = customer["metadata"]["engagement_score"]
        if engagement_score > 80:
            churn_multiplier = 0.3  # Highly engaged users churn 70% less
        elif engagement_score > 60:
            churn_multiplier = 0.6
        elif engagement_score > 40:
            churn_multiplier = 1.0
        else:
            churn_multiplier = 2.0  # Low engagement users churn 2x more
        
        adjusted_churn_rate = monthly_churn_rate * churn_multiplier
        
        # Check for voluntary churn
        if random.random() < adjusted_churn_rate / 30:  # Daily churn probability
            # Determine churn type
            churn_reasons = {
                'cost': 0.35,
                'content_dissatisfaction': 0.25,
                'technical_issues': 0.15,
                'life_change': 0.15,
                'competitor': 0.10
            }
            churn_reason = weighted_choice(churn_reasons)
            
            # 60% cancel immediately, 40% at period end
            if random.random() < 0.6:
                subscription['status'] = 'canceled'
                subscription['canceled_at'] = int(current_date.timestamp())
            else:
                subscription['cancel_at_period_end'] = True
            
            events.append({
                "type": "voluntary_churn",
                "date": current_date.isoformat(),
                "subscription_id": subscription['id'],
                "customer_id": customer['id'],
                "reason": churn_reason,
                "immediate": subscription['status'] == 'canceled'
            })
        
        # Handle payment failures leading to involuntary churn
        elif random.random() < stage_config['failed_payment_rate'] / 30:
            subscription['status'] = 'past_due'
            failure_reason = weighted_choice(FAILURE_REASONS)
            
            events.append({
                "type": "payment_failed",
                "date": current_date.isoformat(),
                "subscription_id": subscription['id'],
                "customer_id": customer['id'],
                "failure_reason": failure_reason,
                "attempt": 1
            })
        
        # Handle vacation pause (5% chance for active subscribers in summer months)
        elif current_date.month in [6, 7, 8] and random.random() < 0.05:
            subscription['pause_collection'] = {
                "behavior": "void",
                "resumes_at": int((current_date + timedelta(days=random.randint(14, 60))).timestamp())
            }
            events.append({
                "type": "subscription_paused",
                "date": current_date.isoformat(),
                "subscription_id": subscription['id'],
                "customer_id": customer['id'],
                "reason": "vacation"
            })
    
    # Handle past due recovery attempts
    elif subscription['status'] == 'past_due':
        # Simulate retry attempts (typically 3 attempts over 2 weeks)
        attempt_number = random.randint(1, 3)
        recovery_rate = RECOVERY_RATES.get(attempt_number, 0.05)
        
        if random.random() < recovery_rate:
            subscription['status'] = 'active'
            events.append({
                "type": "payment_recovered",
                "date": current_date.isoformat(),
                "subscription_id": subscription['id'],
                "customer_id": customer['id'],
                "recovery_attempt": attempt_number
            })
        elif attempt_number >= 3:
            subscription['status'] = 'canceled'
            subscription['canceled_at'] = int(current_date.timestamp())
            events.append({
                "type": "involuntary_churn",
                "date": current_date.isoformat(),
                "subscription_id": subscription['id'],
                "customer_id": customer['id'],
                "final_attempt": attempt_number
            })
    
    # Handle subscription resume from pause
    if subscription.get('pause_collection') and subscription['pause_collection'].get('resumes_at'):
        resume_date = datetime.fromtimestamp(subscription['pause_collection']['resumes_at'])
        if current_date >= resume_date:
            subscription['pause_collection'] = None
            events.append({
                "type": "subscription_resumed",
                "date": current_date.isoformat(),
                "subscription_id": subscription['id'],
                "customer_id": customer['id']
            })
    
    # Update engagement tier based on activity
    engagement_score = customer["metadata"]["engagement_score"]
    if engagement_score > 85:
        subscription["metadata"]["engagement_tier"] = "champion"
    elif engagement_score > 65:
        subscription["metadata"]["engagement_tier"] = "engaged"
    elif engagement_score > 35:
        subscription["metadata"]["engagement_tier"] = "casual"
    else:
        subscription["metadata"]["engagement_tier"] = "at_risk"
    
    # Update churn risk score
    customer["metadata"]["churn_risk_score"] = calculate_churn_risk(
        engagement_score, 
        1 if subscription['status'] == 'past_due' else 0
    )
    
    return subscription, customer, events

# =============================================================================
# PAYMENT GENERATION
# =============================================================================

def generate_subscription_payments(subscription: Dict[str, Any], billing_period_start: datetime,
                                 billing_period_end: datetime, stage: str) -> List[Dict[str, Any]]:
    """Generate subscription payments with fitness industry patterns."""
    payments = []
    stage_config = LIFECYCLE[stage]
    
    # Only generate payments for active or past_due subscriptions
    if subscription['status'] not in ['active', 'past_due']:
        return payments
    
    # Calculate total amount from subscription items
    total_amount = sum(item['price']['unit_amount'] * item['quantity'] 
                      for item in subscription['items']['data'])
    
    # Determine payment success based on subscription status and stage
    if subscription['status'] == 'active':
        success_rate = 1.0 - stage_config['failed_payment_rate']
    else:  # past_due
        success_rate = 0.3  # Lower success rate for retry attempts
    
    # Generate payment attempt
    payment_ids = generate_stripe_ids()
    payment_date = billing_period_start + timedelta(days=random.randint(0, 5))
    
    payment_succeeded = random.random() < success_rate
    
    payment = {
        "id": payment_ids['payment_intent'],
        "object": "payment_intent",
        "amount": total_amount,
        "currency": "usd",
        "status": "succeeded" if payment_succeeded else "requires_payment_method",
        "customer": subscription['customer'],
        "created": int(payment_date.timestamp()),
        "description": f"Subscription update for FitStream {subscription['metadata']['plan_type']} plan",
        "invoice": f"in_{uuid.uuid4().hex[:24]}",
        "payment_method": payment_ids['payment_method'],
        "payment_method_types": ["card"],
        "receipt_email": None,
        "charges": {
            "object": "list",
            "data": [{
                "id": f"ch_{uuid.uuid4().hex[:24]}",
                "object": "charge",
                "amount": total_amount,
                "currency": "usd",
                "customer": subscription['customer'],
                "paid": payment_succeeded,
                "refunded": False,
                "disputed": False,
                "failure_code": None if payment_succeeded else weighted_choice(FAILURE_REASONS),
                "failure_message": None if payment_succeeded else "Your card was declined.",
                "outcome": {
                    "network_status": "approved_by_network" if payment_succeeded else "declined_by_network",
                    "reason": None if payment_succeeded else "generic_decline",
                    "seller_message": "Payment complete." if payment_succeeded else "The bank declined the payment.",
                    "type": "authorized" if payment_succeeded else "issuer_declined"
                }
            }]
        },
        "metadata": {
            "subscription_id": subscription['id'],
            "billing_period_start": billing_period_start.isoformat(),
            "billing_period_end": billing_period_end.isoformat(),
            "plan_type": subscription['metadata']['plan_type'],
            "add_ons": ','.join(subscription['metadata']['selected_addons']),
            "payment_type": "recurring_subscription"
        }
    }
    
    payments.append(payment)
    
    # Generate one-time payments for personal training sessions (15% chance)
    if random.random() < 0.15 and subscription['status'] == 'active':
        pt_payment_date = billing_period_start + timedelta(days=random.randint(1, 28))
        pt_sessions = random.randint(1, 4)
        pt_amount = ADD_ONS['personal_training'] * pt_sessions
        
        pt_payment = {
            "id": generate_stripe_ids()['payment_intent'],
            "object": "payment_intent",
            "amount": pt_amount,
            "currency": "usd",
            "status": "succeeded",
            "customer": subscription['customer'],
            "created": int(pt_payment_date.timestamp()),
            "description": f"Personal training sessions ({pt_sessions}x)",
            "payment_method": payment_ids['payment_method'],
            "payment_method_types": ["card"],
            "charges": {
                "object": "list",
                "data": [{
                    "id": f"ch_{uuid.uuid4().hex[:24]}",
                    "object": "charge",
                    "amount": pt_amount,
                    "currency": "usd",
                    "customer": subscription['customer'],
                    "paid": True,
                    "refunded": False,
                    "disputed": False
                }]
            },
            "metadata": {
                "subscription_id": subscription['id'],
                "payment_type": "one_time_personal_training",
                "sessions_count": pt_sessions
            }
        }
        payments.append(pt_payment)
    
    return payments

# =============================================================================
# MAIN DATA GENERATION
# =============================================================================

def generate_fitstream_data() -> Tuple[List[Dict], List[Dict], List[Dict], List[Dict], List[Dict]]:
    """Generate complete FitStream subscription ecosystem data."""
    print("🏋️ Generating FitStream subscription data...")
    
    all_customers = []
    all_subscriptions = []
    all_payments = []
    all_trials = []
    all_events = []
    
    # Start date for data generation
    start_date = datetime(2023, 1, 1)
    
    customer_counter = 1
    subscription_counter = 1
    
    # Generate data across 24 months
    for month in range(24):
        current_date = start_date + timedelta(days=30 * month)
        stage = get_lifecycle_stage(month)
        stage_config = LIFECYCLE[stage]
        
        print(f"📅 Processing month {month + 1}/24 ({stage} stage)...")
        
        # Calculate new subscribers for this month
        base_subscribers = stage_config['subscribers'] // 12  # Monthly target
        seasonal_subscribers = apply_seasonal_pattern(base_subscribers, current_date.month)
        
        # Generate new customers and subscriptions for this month
        for _ in range(seasonal_subscribers):
            # Create customer
            signup_date = current_date + timedelta(days=random.randint(0, 29))
            customer_id = generate_stripe_ids()['customer']
            
            customer = generate_customer_profile(customer_id, signup_date)
            all_customers.append(customer)
            
            # Create subscription
            subscription = generate_fitness_subscription(customer, signup_date, stage)
            all_subscriptions.append(subscription)
            
            # Track trial if applicable
            if subscription['status'] == 'trialing':
                trial_record = {
                    "subscription_id": subscription['id'],
                    "customer_id": customer['id'],
                    "trial_start": subscription['trial_start'],
                    "trial_end": subscription['trial_end'],
                    "trial_days": subscription['metadata']['trial_days'],
                    "plan_type": subscription['metadata']['plan_type'],
                    "acquisition_channel": customer['metadata']['acquisition_channel'],
                    "converted": False,  # Will be updated later
                    "conversion_date": None
                }
                all_trials.append(trial_record)
        
        # Process existing subscriptions for lifecycle events
        for i, subscription in enumerate(all_subscriptions):
            if subscription['created'] <= int(current_date.timestamp()):
                customer = next(c for c in all_customers if c['id'] == subscription['customer'])
                
                # Update subscription lifecycle
                updated_sub, updated_customer, events = handle_subscription_lifecycle(
                    subscription, current_date, customer, stage
                )
                all_subscriptions[i] = updated_sub
                all_events.extend(events)
                
                # Update customer in list
                customer_idx = next(i for i, c in enumerate(all_customers) if c['id'] == customer['id'])
                all_customers[customer_idx] = updated_customer
                
                # Update trial records for conversions
                for trial in all_trials:
                    if (trial['subscription_id'] == subscription['id'] and 
                        not trial['converted'] and 
                        subscription['status'] == 'active'):
                        trial['converted'] = True
                        trial['conversion_date'] = int(current_date.timestamp())
                
                # Generate payments for active subscriptions
                if subscription['status'] in ['active', 'past_due']:
                    billing_start = current_date.replace(day=1)
                    billing_end = billing_start + timedelta(days=30)
                    
                    payments = generate_subscription_payments(
                        subscription, billing_start, billing_end, stage
                    )
                    all_payments.extend(payments)
    
    print(f"✅ Generated {len(all_customers)} customers, {len(all_subscriptions)} subscriptions")
    return all_customers, all_subscriptions, all_payments, all_trials, all_events

# =============================================================================
# METRICS CALCULATION
# =============================================================================

def calculate_fitness_metrics(customers: List[Dict], subscriptions: List[Dict], 
                            payments: List[Dict], trials: List[Dict]) -> Dict[str, Any]:
    """Calculate fitness industry specific metrics."""
    print("📊 Calculating FitStream metrics...")
    
    # Basic counts
    total_customers = len(customers)
    total_subscriptions = len(subscriptions)
    active_subscriptions = len([s for s in subscriptions if s['status'] == 'active'])
    
    # Plan distribution
    plan_distribution = {}
    for plan in SUBSCRIPTION_PLANS.keys():
        plan_subs = [s for s in subscriptions if s['metadata']['plan_type'] == plan]
        plan_distribution[plan] = {
            'count': len(plan_subs),
            'active': len([s for s in plan_subs if s['status'] == 'active']),
            'percentage': (len(plan_subs) / total_subscriptions * 100) if total_subscriptions > 0 else 0
        }
    
    # Trial conversion metrics
    total_trials = len(trials)
    converted_trials = len([t for t in trials if t['converted']])
    trial_conversion_rate = (converted_trials / total_trials * 100) if total_trials > 0 else 0
    
    # Churn analysis
    canceled_subscriptions = [s for s in subscriptions if s['status'] == 'canceled']
    total_churn_count = len(canceled_subscriptions)
    churn_rate = (total_churn_count / total_subscriptions * 100) if total_subscriptions > 0 else 0
    
    # Revenue calculations
    successful_payments = [p for p in payments if p['status'] == 'succeeded']
    total_revenue = sum(p['amount'] for p in successful_payments)
    
    # Calculate MRR from active subscriptions
    current_mrr = 0
    for subscription in subscriptions:
        if subscription['status'] == 'active':
            monthly_amount = sum(item['price']['unit_amount'] for item in subscription['items']['data'])
            current_mrr += monthly_amount
    
    arr = current_mrr * 12
    
    # Payment success rate
    total_payment_attempts = len(payments)
    successful_payment_attempts = len(successful_payments)
    payment_success_rate = (successful_payment_attempts / total_payment_attempts * 100) if total_payment_attempts > 0 else 0
    
    # Customer Lifetime Value by plan
    ltv_by_plan = {}
    for plan in SUBSCRIPTION_PLANS.keys():
        plan_customers = [c for c in customers if any(
            s['metadata']['plan_type'] == plan and s['customer'] == c['id'] 
            for s in subscriptions
        )]
        if plan_customers:
            avg_engagement = sum(c['metadata']['engagement_score'] for c in plan_customers) / len(plan_customers)
            # Simplified LTV calculation based on engagement and plan price
            avg_monthly_revenue = SUBSCRIPTION_PLANS[plan]['price']
            estimated_months = max(12, avg_engagement * 0.3)  # Higher engagement = longer retention
            ltv_by_plan[plan] = avg_monthly_revenue * estimated_months / 100  # Convert to dollars
    
    # Engagement metrics
    avg_engagement = sum(c['metadata']['engagement_score'] for c in customers) / len(customers) if customers else 0
    high_engagement_customers = len([c for c in customers if c['metadata']['engagement_score'] > 80])
    at_risk_customers = len([c for c in customers if c['metadata']['churn_risk_score'] > 0.7])
    
    # Add-on attachment rate
    subscriptions_with_addons = [s for s in subscriptions if s['metadata']['selected_addons']]
    addon_attachment_rate = (len(subscriptions_with_addons) / total_subscriptions * 100) if total_subscriptions > 0 else 0
    
    # Family plan metrics
    family_subscriptions = [s for s in subscriptions if s['metadata']['plan_type'] == 'family']
    avg_family_size = (sum(s['metadata']['family_members'] for s in family_subscriptions) / 
                      len(family_subscriptions)) if family_subscriptions else 0
    
    return {
        "overview": {
            "total_customers": total_customers,
            "total_subscriptions": total_subscriptions,
            "active_subscriptions": active_subscriptions,
            "subscription_penetration": (total_subscriptions / total_customers * 100) if total_customers > 0 else 0
        },
        "revenue_metrics": {
            "total_revenue_cents": total_revenue,
            "total_revenue_dollars": total_revenue / 100,
            "current_mrr_cents": current_mrr,
            "current_mrr_dollars": current_mrr / 100,
            "estimated_arr_cents": arr,
            "estimated_arr_dollars": arr / 100,
            "arpu_dollars": (current_mrr / active_subscriptions / 100) if active_subscriptions > 0 else 0
        },
        "plan_distribution": plan_distribution,
        "trial_metrics": {
            "total_trials": total_trials,
            "converted_trials": converted_trials,
            "trial_conversion_rate": trial_conversion_rate
        },
        "churn_metrics": {
            "total_churned": total_churn_count,
            "churn_rate_percent": churn_rate,
            "at_risk_customers": at_risk_customers
        },
        "payment_metrics": {
            "total_payment_attempts": total_payment_attempts,
            "successful_payments": successful_payment_attempts,
            "payment_success_rate": payment_success_rate
        },
        "engagement_metrics": {
            "average_engagement_score": avg_engagement,
            "high_engagement_customers": high_engagement_customers,
            "addon_attachment_rate": addon_attachment_rate
        },
        "customer_lifetime_value": ltv_by_plan,
        "family_plan_metrics": {
            "family_subscriptions": len(family_subscriptions),
            "average_family_size": avg_family_size
        }
    }

# =============================================================================
# OUTPUT GENERATION
# =============================================================================

def save_fitstream_data(customers: List[Dict], subscriptions: List[Dict], payments: List[Dict],
                       trials: List[Dict], events: List[Dict], metrics: Dict[str, Any]) -> None:
    """Save all generated data to JSON files."""
    print("💾 Saving FitStream data to files...")
    
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save main data files
    datasets = {
        "customers.json": customers,
        "subscriptions.json": subscriptions,
        "payments.json": payments,
        "trials.json": trials,
        "churn_analysis.json": events,
        "fitness_metrics.json": metrics
    }
    
    for filename, data in datasets.items():
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    # Generate engagement correlation data
    engagement_data = []
    for customer in customers:
        customer_subs = [s for s in subscriptions if s['customer'] == customer['id']]
        if customer_subs:
            latest_sub = max(customer_subs, key=lambda x: x['created'])
            engagement_data.append({
                "customer_id": customer['id'],
                "engagement_score": customer['metadata']['engagement_score'],
                "subscription_status": latest_sub['status'],
                "plan_type": latest_sub['metadata']['plan_type'],
                "workout_frequency": customer['metadata']['workout_frequency'],
                "churn_risk_score": customer['metadata']['churn_risk_score'],
                "has_addons": len(latest_sub['metadata']['selected_addons']) > 0,
                "acquisition_channel": customer['metadata']['acquisition_channel']
            })
    
    with open(os.path.join(output_dir, "engagement_metrics.json"), 'w') as f:
        json.dump(engagement_data, f, indent=2)
    
    print(f"📁 Data saved to {output_dir}/ directory")

def print_fitstream_summary(customers: List[Dict], subscriptions: List[Dict], 
                          payments: List[Dict], trials: List[Dict], metrics: Dict[str, Any]) -> None:
    """Print comprehensive FitStream generation summary."""
    print("\n" + "="*80)
    print("🏋️ FITSTREAM SUBSCRIPTION DATA GENERATION COMPLETE")
    print("="*80)
    
    overview = metrics['overview']
    revenue = metrics['revenue_metrics']
    trial_metrics = metrics['trial_metrics']
    churn = metrics['churn_metrics']
    payment_metrics = metrics['payment_metrics']
    
    print(f"\n📊 GENERATION SUMMARY:")
    print(f"   Total customers generated: {overview['total_customers']:,}")
    print(f"   Total subscriptions: {overview['total_subscriptions']:,}")
    print(f"   Active subscriptions: {overview['active_subscriptions']:,}")
    print(f"   Payment records: {len(payments):,}")
    
    print(f"\n💰 REVENUE METRICS:")
    print(f"   Current MRR: ${revenue['current_mrr_dollars']:,.2f}")
    print(f"   Estimated ARR: ${revenue['estimated_arr_dollars']:,.2f}")
    print(f"   Total revenue: ${revenue['total_revenue_dollars']:,.2f}")
    print(f"   ARPU: ${revenue['arpu_dollars']:.2f}")
    
    print(f"\n🔄 SUBSCRIPTION HEALTH:")
    print(f"   Trial conversion rate: {trial_metrics['trial_conversion_rate']:.1f}%")
    print(f"   Churn rate: {churn['churn_rate_percent']:.1f}%")
    print(f"   Payment success rate: {payment_metrics['payment_success_rate']:.1f}%")
    print(f"   At-risk customers: {churn['at_risk_customers']:,}")
    
    print(f"\n📋 PLAN DISTRIBUTION:")
    for plan, stats in metrics['plan_distribution'].items():
        print(f"   {plan.title()}: {stats['active']} active ({stats['percentage']:.1f}%)")
    
    print(f"\n🏆 ENGAGEMENT METRICS:")
    engagement = metrics['engagement_metrics']
    print(f"   Average engagement score: {engagement['average_engagement_score']:.1f}/100")
    print(f"   High engagement customers: {engagement['high_engagement_customers']:,}")
    print(f"   Add-on attachment rate: {engagement['addon_attachment_rate']:.1f}%")
    
    print(f"\n📁 OUTPUT FILES:")
    print(f"   ✅ customers.json - Customer profiles with fitness preferences")
    print(f"   ✅ subscriptions.json - Subscription lifecycle data")
    print(f"   ✅ payments.json - Recurring and one-time payments")
    print(f"   ✅ trials.json - Trial tracking and conversion")
    print(f"   ✅ churn_analysis.json - Churn events and patterns")
    print(f"   ✅ engagement_metrics.json - Engagement correlation data")
    print(f"   ✅ fitness_metrics.json - Complete fitness industry KPIs")
    
    print(f"\n🚀 Ready for fitness platform prototyping and analytics!")
    print("="*80)

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("🏋️ FitStream Synthetic Subscription Data Generator")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        # Generate all data
        customers, subscriptions, payments, trials, events = generate_fitstream_data()
        
        # Calculate metrics
        metrics = calculate_fitness_metrics(customers, subscriptions, payments, trials)
        
        # Save data
        save_fitstream_data(customers, subscriptions, payments, trials, events, metrics)
        
        # Print summary
        print_fitstream_summary(customers, subscriptions, payments, trials, metrics)
        
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"\n⏱️ Total execution time: {execution_time:.1f} seconds")
        
    except Exception as e:
        print(f"\n❌ Error during generation: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
