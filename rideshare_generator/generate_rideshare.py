#!/usr/bin/env python3
"""
RideShare Plus Synthetic Stripe Data Generator

Generates realistic on-demand transportation platform data with drivers,
dynamic pricing, fraud patterns, and Stripe Connect/Issuing integration.

Usage:
    python generate_rideshare.py
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

# Platform pricing configuration
PRICING_CONFIG = {
    'base_fare': 250,  # $2.50 in cents
    'per_mile': 150,   # $1.50 per mile
    'per_minute': 35,  # $0.35 per minute
    'minimum_fare': 500,  # $5.00 minimum
    'surge_multipliers': [1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0],
    'driver_take_rate': 0.75,  # Driver gets 75%
    'platform_fee': 0.25,     # Platform keeps 25%
    'instant_payout_fee': 50,  # $0.50 for instant payouts
    'booking_fee': 199,        # $1.99 booking fee
    'airport_surcharge': 350   # $3.50 airport fee
}

# Business lifecycle stages
LIFECYCLE = {
    'early': {
        'drivers': 50,  # Further reduced
        'rides_per_week': 150,  # Much smaller volume
        'cities': 1,
        'months': range(0, 8),
        'surge_frequency': 0.15,  # 15% of rides have surge
        'fraud_rate': 0.05        # 5% fraud attempts
    },
    'growth': {
        'drivers': 150,  # Further reduced
        'rides_per_week': 600,  # Much smaller volume
        'cities': 3,  # Reduced cities too
        'months': range(8, 16),
        'surge_frequency': 0.25,
        'fraud_rate': 0.03
    },
    'mature': {
        'drivers': 300,  # Further reduced
        'rides_per_week': 1200,  # Much smaller volume
        'cities': 5,  # Reduced cities
        'months': range(16, 24),
        'surge_frequency': 0.35,
        'fraud_rate': 0.02
    }
}

# Cities and their characteristics
CITIES = [
    {'name': 'San Francisco', 'population': 875000, 'density': 'high', 'airport': 'SFO'},
    {'name': 'Austin', 'population': 965000, 'density': 'medium', 'airport': 'AUS'},
    {'name': 'Miami', 'population': 470000, 'density': 'high', 'airport': 'MIA'},
    {'name': 'Denver', 'population': 715000, 'density': 'medium', 'airport': 'DEN'},
    {'name': 'Seattle', 'population': 750000, 'density': 'high', 'airport': 'SEA'},
    {'name': 'Nashville', 'population': 690000, 'density': 'medium', 'airport': 'BNA'},
    {'name': 'Phoenix', 'population': 1680000, 'density': 'low', 'airport': 'PHX'},
    {'name': 'Atlanta', 'population': 498000, 'density': 'medium', 'airport': 'ATL'},
    {'name': 'Boston', 'population': 695000, 'density': 'high', 'airport': 'BOS'},
    {'name': 'Las Vegas', 'population': 650000, 'density': 'medium', 'airport': 'LAS'},
    {'name': 'Portland', 'population': 650000, 'density': 'medium', 'airport': 'PDX'},
    {'name': 'Chicago', 'population': 2710000, 'density': 'high', 'airport': 'ORD'},
    {'name': 'Los Angeles', 'population': 4000000, 'density': 'high', 'airport': 'LAX'},
    {'name': 'New York', 'population': 8400000, 'density': 'very_high', 'airport': 'JFK'},
    {'name': 'Washington DC', 'population': 705000, 'density': 'high', 'airport': 'DCA'},
    {'name': 'Philadelphia', 'population': 1580000, 'density': 'high', 'airport': 'PHL'},
    {'name': 'San Diego', 'population': 1420000, 'density': 'medium', 'airport': 'SAN'},
    {'name': 'Dallas', 'population': 1340000, 'density': 'medium', 'airport': 'DFW'},
    {'name': 'Houston', 'population': 2320000, 'density': 'medium', 'airport': 'IAH'},
    {'name': 'Tampa', 'population': 385000, 'density': 'medium', 'airport': 'TPA'},
    {'name': 'Orlando', 'population': 310000, 'density': 'medium', 'airport': 'MCO'},
    {'name': 'Charlotte', 'population': 875000, 'density': 'medium', 'airport': 'CLT'},
    {'name': 'Minneapolis', 'population': 430000, 'density': 'medium', 'airport': 'MSP'},
    {'name': 'Detroit', 'population': 670000, 'density': 'medium', 'airport': 'DTW'},
    {'name': 'Salt Lake City', 'population': 200000, 'density': 'low', 'airport': 'SLC'}
]

# Vehicle types and their characteristics
VEHICLE_TYPES = {
    'standard': {
        'name': 'RideShare',
        'capacity': 4,
        'multiplier': 1.0,
        'distribution': 0.70
    },
    'premium': {
        'name': 'RideShare Premium',
        'capacity': 4,
        'multiplier': 1.5,
        'distribution': 0.20
    },
    'xl': {
        'name': 'RideShare XL',
        'capacity': 6,
        'multiplier': 1.8,
        'distribution': 0.10
    }
}

# Time-based surge patterns
SURGE_PATTERNS = {
    'rush_morning': {'hours': [7, 8, 9], 'multiplier_boost': 1.5},
    'rush_evening': {'hours': [17, 18, 19], 'multiplier_boost': 1.8},
    'late_night': {'hours': [23, 0, 1, 2], 'multiplier_boost': 1.3},
    'weekend_night': {'days': [5, 6], 'hours': [22, 23, 0, 1, 2], 'multiplier_boost': 2.0},
    'airport_peak': {'special': 'airport', 'multiplier_boost': 1.4}
}

# Fraud patterns
FRAUD_TYPES = {
    'fake_ride': {
        'probability': 0.4,
        'description': 'Driver and rider colluding for fake rides',
        'patterns': ['same_pickup_dropoff', 'unrealistic_gps', 'short_duration_high_fare']
    },
    'stolen_card': {
        'probability': 0.3,
        'description': 'Stolen payment method usage',
        'patterns': ['unusual_location', 'new_account_high_activity', 'multiple_failed_attempts']
    },
    'account_takeover': {
        'probability': 0.2,
        'description': 'Compromised rider account',
        'patterns': ['sudden_behavior_change', 'different_device', 'unusual_destinations']
    },
    'promo_abuse': {
        'probability': 0.1,
        'description': 'Multiple accounts for promotions',
        'patterns': ['similar_payment_methods', 'similar_pickup_locations', 'rapid_signups']
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
    """Generate properly formatted Stripe IDs for rideshare platform."""
    return {
        'account': f"acct_{uuid.uuid4().hex[:16]}",
        'customer': f"cus_{uuid.uuid4().hex[:14]}",
        'payment_intent': f"pi_{uuid.uuid4().hex[:24]}",
        'transfer': f"tr_{uuid.uuid4().hex[:24]}",
        'payout': f"po_{uuid.uuid4().hex[:24]}",
        'card': f"ic_{uuid.uuid4().hex[:24]}",
        'authorization': f"iauth_{uuid.uuid4().hex[:20]}",
        'charge': f"ch_{uuid.uuid4().hex[:24]}"
    }

def get_lifecycle_stage(month: int) -> str:
    """Determine lifecycle stage based on month."""
    for stage, config in LIFECYCLE.items():
        if month in config['months']:
            return stage
    return 'mature'

def calculate_distance(pickup_lat: float, pickup_lng: float, 
                      dropoff_lat: float, dropoff_lng: float) -> float:
    """Calculate approximate distance between two points (simplified)."""
    # Simplified distance calculation for demo purposes
    lat_diff = abs(pickup_lat - dropoff_lat)
    lng_diff = abs(pickup_lng - dropoff_lng)
    return math.sqrt(lat_diff**2 + lng_diff**2) * 69  # Approximate miles

def get_surge_multiplier(ride_time: datetime, location_type: str = 'standard') -> float:
    """Calculate surge multiplier based on time and location patterns."""
    base_multiplier = 1.0
    hour = ride_time.hour
    weekday = ride_time.weekday()
    
    # Check for surge patterns
    if hour in SURGE_PATTERNS['rush_morning']['hours']:
        base_multiplier *= SURGE_PATTERNS['rush_morning']['multiplier_boost']
    elif hour in SURGE_PATTERNS['rush_evening']['hours']:
        base_multiplier *= SURGE_PATTERNS['rush_evening']['multiplier_boost']
    elif hour in SURGE_PATTERNS['late_night']['hours']:
        base_multiplier *= SURGE_PATTERNS['late_night']['multiplier_boost']
    
    # Weekend night surge
    if (weekday in [5, 6] and 
        hour in SURGE_PATTERNS['weekend_night']['hours']):
        base_multiplier *= SURGE_PATTERNS['weekend_night']['multiplier_boost']
    
    # Airport surge
    if location_type == 'airport':
        base_multiplier *= SURGE_PATTERNS['airport_peak']['multiplier_boost']
    
    # Add randomness and select from available multipliers
    if base_multiplier > 1.0:
        available_multipliers = [m for m in PRICING_CONFIG['surge_multipliers'] 
                               if m >= base_multiplier]
        if available_multipliers:
            return random.choice(available_multipliers)
    
    return random.choice(PRICING_CONFIG['surge_multipliers'][:2])  # Default to 1.0 or 1.25

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
# DRIVER ACCOUNT MANAGEMENT
# =============================================================================

def create_driver_account(driver_id: str, onboarding_date: datetime, city: Dict[str, Any]) -> Dict[str, Any]:
    """Create Stripe Connect Express account for driver."""
    stripe_ids = generate_stripe_ids()
    
    # Driver demographics and vehicle info
    first_name = fake.first_name()
    last_name = fake.last_name()
    vehicle_type = weighted_choice({vtype: info['distribution'] 
                                   for vtype, info in VEHICLE_TYPES.items()})
    
    # Generate realistic driver metrics
    rating = max(3.0, min(5.0, random.gauss(4.7, 0.4)))
    acceptance_rate = max(0.5, min(1.0, random.gauss(0.85, 0.15)))
    completion_rate = max(0.7, min(1.0, random.gauss(0.94, 0.08)))
    
    # Payout preference (70% weekly, 30% instant)
    payout_preference = random.choice(['weekly'] * 7 + ['instant'] * 3)
    
    return {
        "id": stripe_ids['account'],
        "object": "account",
        "type": "express",
        "capabilities": {
            "transfers": {"status": "active"},
            "card_issuing": {"status": "active"}
        },
        "country": "US",
        "created": int(onboarding_date.timestamp()),
        "default_currency": "usd",
        "details_submitted": True,
        "payouts_enabled": True,
        "charges_enabled": True,
        "individual": {
            "id": f"person_{uuid.uuid4().hex[:16]}",
            "first_name": first_name,
            "last_name": last_name,
            "email": f"{first_name.lower()}.{last_name.lower()}@email.com",
            "phone": fake.phone_number(),
            "ssn_last_4": str(random.randint(1000, 9999)),
            "dob": {
                "day": random.randint(1, 28),
                "month": random.randint(1, 12),
                "year": random.randint(1970, 2000)
            },
            "address": {
                "line1": fake.street_address(),
                "city": city['name'],
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
            "mcc": "4121",  # Taxicabs and limousines
            "name": "RideShare Plus Driver",
            "product_description": "On-demand transportation services",
            "support_phone": "+1-555-RIDESHARE",
            "url": "https://ridesharplus.com"
        },
        "external_accounts": {
            "object": "list",
            "data": [{
                "id": f"ba_{uuid.uuid4().hex[:24]}",
                "object": "bank_account",
                "account_holder_type": "individual",
                "bank_name": random.choice(["Chase", "Bank of America", "Wells Fargo", "Citi"]),
                "country": "US",
                "currency": "usd",
                "last4": str(random.randint(1000, 9999)),
                "routing_number": f"{random.randint(100000000, 999999999)}",
                "status": "verified"
            }]
        },
        "metadata": {
            "driver_id": driver_id,
            "vehicle_type": vehicle_type,
            "vehicle_make": random.choice(["Toyota", "Honda", "Ford", "Chevrolet", "Nissan"]),
            "vehicle_model": random.choice(["Camry", "Accord", "Fusion", "Malibu", "Altima"]),
            "vehicle_year": str(random.randint(2015, 2023)),
            "license_plate": f"{fake.state_abbr()}{random.randint(100, 999)}{random.choice('ABCD')}",
            "rating": round(rating, 2),
            "acceptance_rate": round(acceptance_rate, 3),
            "completion_rate": round(completion_rate, 3),
            "city": city['name'],
            "onboarding_date": onboarding_date.isoformat(),
            "payout_preference": payout_preference,
            "background_check_status": "approved",
            "insurance_verified": True,
            "total_rides": 0,
            "total_earnings": 0
        },
        "tos_acceptance": {
            "date": int(onboarding_date.timestamp()),
            "ip": fake.ipv4(),
            "user_agent": fake.user_agent()
        }
    }

def create_driver_fuel_card(driver: Dict[str, Any]) -> Dict[str, Any]:
    """Create Stripe Issuing card for driver fuel and expenses."""
    stripe_ids = generate_stripe_ids()
    
    return {
        "id": stripe_ids['card'],
        "object": "issuing.card",
        "type": "virtual",
        "brand": "visa",
        "cardholder": {
            "id": f"ich_{uuid.uuid4().hex[:22]}",
            "name": f"{driver['individual']['first_name']} {driver['individual']['last_name']}",
            "type": "individual",
            "email": driver['individual']['email'],
            "phone_number": driver['individual']['phone'],
            "status": "active"
        },
        "created": driver['created'],
        "currency": "usd",
        "exp_month": random.randint(1, 12),
        "exp_year": random.randint(2025, 2029),
        "last4": str(random.randint(1000, 9999)),
        "spending_controls": {
            "spending_limits": [
                {
                    "amount": 20000,  # $200/day
                    "interval": "daily",
                    "categories": ["gas_stations"]
                },
                {
                    "amount": 100000,  # $1000/week
                    "interval": "weekly"
                }
            ],
            "allowed_categories": [
                "gas_stations",
                "parking_lots_garages",
                "tolls_bridge_fees",
                "automotive_parts_and_accessories",
                "automotive_tire_stores",
                "automotive_body_repair_shops"
            ],
            "blocked_categories": [
                "bars_cocktail_lounges",
                "gambling",
                "liquor_stores",
                "tobacco_stores"
            ]
        },
        "status": "active",
        "metadata": {
            "driver_account": driver['id'],
            "driver_id": driver['metadata']['driver_id'],
            "city": driver['metadata']['city'],
            "card_purpose": "fuel_and_maintenance"
        }
    }

# =============================================================================
# RIDE TRANSACTION PROCESSING
# =============================================================================

def generate_ride_locations(city: Dict[str, Any]) -> Tuple[Dict[str, float], Dict[str, float], str]:
    """Generate pickup and dropoff locations with realistic patterns."""
    # Base coordinates for cities (simplified)
    city_coords = {
        'San Francisco': {'lat': 37.7749, 'lng': -122.4194},
        'Austin': {'lat': 30.2672, 'lng': -97.7431},
        'Miami': {'lat': 25.7617, 'lng': -80.1918},
        'Denver': {'lat': 39.7392, 'lng': -104.9903},
        'Seattle': {'lat': 47.6062, 'lng': -122.3321},
        'New York': {'lat': 40.7128, 'lng': -74.0060},
        'Chicago': {'lat': 41.8781, 'lng': -87.6298},
        'Los Angeles': {'lat': 34.0522, 'lng': -118.2437}
    }
    
    base_coord = city_coords.get(city['name'], {'lat': 40.0, 'lng': -100.0})
    
    # Generate pickup location with some randomness
    pickup_lat = base_coord['lat'] + random.uniform(-0.1, 0.1)
    pickup_lng = base_coord['lng'] + random.uniform(-0.1, 0.1)
    
    # Generate dropoff location
    # 60% local rides, 30% medium distance, 10% airport/long distance
    ride_type = random.choices(['local', 'medium', 'airport'], weights=[60, 30, 10])[0]
    
    if ride_type == 'local':
        # Short ride within city
        dropoff_lat = pickup_lat + random.uniform(-0.02, 0.02)
        dropoff_lng = pickup_lng + random.uniform(-0.02, 0.02)
        location_type = 'standard'
    elif ride_type == 'medium':
        # Medium distance ride
        dropoff_lat = pickup_lat + random.uniform(-0.05, 0.05)
        dropoff_lng = pickup_lng + random.uniform(-0.05, 0.05)
        location_type = 'standard'
    else:  # airport
        # Airport ride
        airport_offset = random.choice([0.08, -0.08])
        dropoff_lat = pickup_lat + airport_offset + random.uniform(-0.01, 0.01)
        dropoff_lng = pickup_lng + airport_offset + random.uniform(-0.01, 0.01)
        location_type = 'airport'
    
    pickup = {'lat': pickup_lat, 'lng': pickup_lng}
    dropoff = {'lat': dropoff_lat, 'lng': dropoff_lng}
    
    return pickup, dropoff, location_type

def process_ride(ride_id: str, passenger: Dict[str, Any], driver: Dict[str, Any], 
                ride_time: datetime, city: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    """Process complete ride transaction with dynamic pricing."""
    stripe_ids = generate_stripe_ids()
    
    # Generate ride locations and calculate distance
    pickup, dropoff, location_type = generate_ride_locations(city)
    distance = calculate_distance(pickup['lat'], pickup['lng'], 
                                dropoff['lat'], dropoff['lng'])
    
    # Calculate ride duration (with traffic variability)
    base_duration = distance * random.uniform(2, 4)  # 2-4 minutes per mile
    duration = max(5, base_duration + random.uniform(-5, 15))  # Traffic variability
    
    # Calculate surge multiplier
    surge_multiplier = get_surge_multiplier(ride_time, location_type)
    
    # Calculate pricing
    vehicle_info = VEHICLE_TYPES[driver['metadata']['vehicle_type']]
    base_amount = PRICING_CONFIG['base_fare']
    distance_amount = int(distance * PRICING_CONFIG['per_mile'])
    time_amount = int(duration * PRICING_CONFIG['per_minute'])
    booking_fee = PRICING_CONFIG['booking_fee']
    
    # Apply vehicle type multiplier
    subtotal = (base_amount + distance_amount + time_amount) * vehicle_info['multiplier']
    
    # Add airport surcharge if applicable
    if location_type == 'airport':
        subtotal += PRICING_CONFIG['airport_surcharge']
    
    # Apply minimum fare
    subtotal = max(subtotal, PRICING_CONFIG['minimum_fare'])
    
    # Apply surge pricing
    surge_amount = int(subtotal * surge_multiplier)
    total_amount = surge_amount + booking_fee
    
    # Generate ride completion status (95% complete successfully)
    ride_status = random.choices(['completed', 'cancelled_by_driver', 'cancelled_by_rider'], 
                                weights=[95, 3, 2])[0]
    
    # Create payment intent
    payment_intent = {
        "id": stripe_ids['payment_intent'],
        "object": "payment_intent",
        "amount": total_amount if ride_status == 'completed' else 0,
        "currency": "usd",
        "status": "succeeded" if ride_status == 'completed' else "canceled",
        "customer": passenger['id'],
        "created": int(ride_time.timestamp()),
        "description": f"RideShare Plus ride from {city['name']}",
        "payment_method": f"pm_{uuid.uuid4().hex[:22]}",
        "payment_method_types": ["card"],
        "transfer_group": f"ride_{ride_id}",
        "charges": {
            "object": "list",
            "data": [{
                "id": stripe_ids['charge'],
                "object": "charge",
                "amount": total_amount if ride_status == 'completed' else 0,
                "currency": "usd",
                "customer": passenger['id'],
                "paid": ride_status == 'completed',
                "refunded": False,
                "disputed": False
            }] if ride_status == 'completed' else []
        },
        "metadata": {
            "ride_id": ride_id,
            "driver_account": driver['id'],
            "surge_multiplier": surge_multiplier,
            "distance_miles": round(distance, 2),
            "duration_minutes": round(duration, 1),
            "vehicle_type": driver['metadata']['vehicle_type'],
            "location_type": location_type,
            "city": city['name'],
            "ride_status": ride_status
        }
    }
    
    # Create driver transfer (only if ride completed)
    driver_transfer = None
    if ride_status == 'completed':
        driver_earnings = int(surge_amount * PRICING_CONFIG['driver_take_rate'])
        
        driver_transfer = {
            "id": stripe_ids['transfer'],
            "object": "transfer",
            "amount": driver_earnings,
            "currency": "usd",
            "destination": driver['id'],
            "created": int(ride_time.timestamp()),
            "transfer_group": f"ride_{ride_id}",
            "metadata": {
                "type": "ride_earnings",
                "ride_id": ride_id,
                "gross_fare": surge_amount,
                "platform_fee": surge_amount - driver_earnings,
                "driver_account": driver['id']
            }
        }
    
    # Create ride record
    ride_record = {
        "id": ride_id,
        "driver_account": driver['id'],
        "passenger_id": passenger['id'],
        "payment_intent": payment_intent['id'],
        "transfer_id": driver_transfer['id'] if driver_transfer else None,
        "status": ride_status,
        "requested_at": int(ride_time.timestamp()),
        "started_at": int((ride_time + timedelta(minutes=random.randint(2, 8))).timestamp()) if ride_status == 'completed' else None,
        "completed_at": int((ride_time + timedelta(minutes=duration + random.randint(2, 8))).timestamp()) if ride_status == 'completed' else None,
        "pickup_location": pickup,
        "dropoff_location": dropoff,
        "distance_miles": round(distance, 2),
        "duration_minutes": round(duration, 1) if ride_status == 'completed' else None,
        "vehicle_type": driver['metadata']['vehicle_type'],
        "pricing": {
            "base_fare": base_amount,
            "distance_fare": distance_amount,
            "time_fare": time_amount,
            "booking_fee": booking_fee,
            "surge_multiplier": surge_multiplier,
            "airport_surcharge": PRICING_CONFIG['airport_surcharge'] if location_type == 'airport' else 0,
            "subtotal": int(subtotal),
            "total": total_amount
        },
        "city": city['name'],
        "metadata": {
            "location_type": location_type,
            "pickup_address": f"{int(pickup['lat'] * 1000)} {fake.street_name()}, {city['name']}",
            "dropoff_address": f"{int(dropoff['lat'] * 1000)} {fake.street_name()}, {city['name']}",
            "rating_by_passenger": random.randint(4, 5) if ride_status == 'completed' else None,
            "rating_by_driver": random.randint(4, 5) if ride_status == 'completed' else None,
            "tip_amount": random.choice([0, 0, 0, 100, 200, 300, 500]) if ride_status == 'completed' else 0
        }
    }
    
    return ride_record, payment_intent, driver_transfer

# =============================================================================
# DRIVER PAYOUTS AND ISSUING
# =============================================================================

def handle_driver_payouts(driver: Dict[str, Any], earnings_this_period: int, 
                         payout_date: datetime) -> Dict[str, Any]:
    """Generate driver payout based on their preference."""
    stripe_ids = generate_stripe_ids()
    payout_preference = driver['metadata']['payout_preference']
    
    if payout_preference == 'instant':
        # Instant payout with fee
        net_amount = earnings_this_period - PRICING_CONFIG['instant_payout_fee']
        arrival_date = payout_date
        method = "instant"
        fee = PRICING_CONFIG['instant_payout_fee']
    else:  # weekly
        # Standard weekly payout
        net_amount = earnings_this_period
        # Next Monday
        days_ahead = 7 - payout_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        arrival_date = payout_date + timedelta(days=days_ahead)
        method = "standard"
        fee = 0
    
    # Only create payout if there are earnings
    if earnings_this_period <= 0:
        return None
    
    return {
        "id": stripe_ids['payout'],
        "object": "payout",
        "amount": net_amount,
        "currency": "usd",
        "created": int(payout_date.timestamp()),
        "arrival_date": int(arrival_date.timestamp()),
        "description": f"RideShare Plus driver earnings - {method} payout",
        "destination": driver['external_accounts']['data'][0]['id'],
        "method": method,
        "status": "paid",
        "type": "bank_account",
        "automatic": False,
        "failure_code": None,
        "failure_message": None,
        "metadata": {
            "driver_account": driver['id'],
            "driver_id": driver['metadata']['driver_id'],
            "gross_earnings": earnings_this_period,
            "payout_fee": fee,
            "payout_type": payout_preference,
            "period_start": (payout_date - timedelta(days=7)).isoformat(),
            "period_end": payout_date.isoformat()
        }
    }

def generate_fuel_purchases(driver_card: Dict[str, Any], week_start: datetime, 
                          rides_this_week: int) -> List[Dict[str, Any]]:
    """Generate realistic fuel purchases using driver's Issuing card."""
    authorizations = []
    
    # Estimate fuel purchases based on rides (roughly 1 fuel up per 15-25 rides)
    fuel_purchases = max(1, rides_this_week // random.randint(15, 25))
    
    for _ in range(fuel_purchases):
        stripe_ids = generate_stripe_ids()
        
        # Random day within the week
        purchase_date = week_start + timedelta(
            days=random.randint(0, 6),
            hours=random.randint(6, 22),
            minutes=random.randint(0, 59)
        )
        
        # Fuel purchase amount ($20-$80)
        amount = random.randint(2000, 8000)
        
        authorization = {
            "id": stripe_ids['authorization'],
            "object": "issuing.authorization",
            "amount": amount,
            "currency": "usd",
            "approved": True,
            "card": driver_card['id'],
            "cardholder": driver_card['cardholder']['id'],
            "created": int(purchase_date.timestamp()),
            "merchant_category_code": "5541",  # Gas stations
            "merchant_data": {
                "category": "gas_stations",
                "city": driver_card['metadata']['city'],
                "country": "US",
                "name": random.choice([
                    "Shell", "Chevron", "BP", "Exxon", "Mobil", 
                    "Texaco", "76", "Arco", "Valero", "Marathon"
                ]),
                "network_id": f"mcc_5541_{random.randint(1000, 9999)}",
                "postal_code": fake.zipcode(),
                "state": fake.state_abbr()
            },
            "pending_request": None,
            "request_history": [],
            "status": "closed",
            "transactions": [{
                "id": f"ipi_{uuid.uuid4().hex[:22]}",
                "amount": amount,
                "currency": "usd",
                "merchant_amount": amount,
                "merchant_currency": "usd"
            }],
            "verification_data": {
                "address_line1_check": "match",
                "address_postal_code_check": "match",
                "cvc_check": "match"
            },
            "metadata": {
                "driver_account": driver_card['metadata']['driver_account'],
                "driver_id": driver_card['metadata']['driver_id'],
                "purchase_type": "fuel",
                "gallons": round(amount / random.randint(350, 450), 1)  # Estimate gallons
            }
        }
        
        authorizations.append(authorization)
    
    return authorizations

# =============================================================================
# FRAUD DETECTION AND PATTERNS
# =============================================================================

def generate_fraud_scenarios(rides: List[Dict[str, Any]], 
                           stage_config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate realistic fraud scenarios based on rideshare patterns."""
    fraud_cases = []
    fraud_rate = stage_config['fraud_rate']
    
    # Select rides for fraud analysis
    num_fraud_cases = int(len(rides) * fraud_rate)
    fraud_rides = random.sample(rides, min(num_fraud_cases, len(rides)))
    
    for ride in fraud_rides:
        fraud_type = weighted_choice({ftype: fdata['probability'] 
                                    for ftype, fdata in FRAUD_TYPES.items()})
        fraud_info = FRAUD_TYPES[fraud_type]
        
        # Generate fraud-specific patterns
        patterns = []
        risk_score = random.uniform(0.6, 1.0)
        
        if fraud_type == 'fake_ride':
            patterns = [
                'GPS_ANOMALY: No movement detected during ride',
                'DURATION_MISMATCH: Ride completed in unrealistic time',
                'REPEAT_PATTERN: Same driver-rider pair multiple times',
                'LOCATION_SUSPICIOUS: Pickup and dropoff identical'
            ]
            # Override ride data to reflect fake patterns
            ride['distance_miles'] = 0.1
            ride['duration_minutes'] = 2.0
            risk_score = random.uniform(0.8, 1.0)
            
        elif fraud_type == 'stolen_card':
            patterns = [
                'VELOCITY_HIGH: Multiple rides in short timeframe',
                'LOCATION_INCONSISTENT: Rides from unexpected locations',
                'DEVICE_NEW: First-time device usage',
                'PAYMENT_PATTERN: Different from historical usage'
            ]
            risk_score = random.uniform(0.7, 0.95)
            
        elif fraud_type == 'account_takeover':
            patterns = [
                'BEHAVIOR_CHANGE: Sudden change in ride patterns',
                'DEVICE_SWITCH: Different device/IP than usual',
                'DESTINATION_UNUSUAL: Rides to unexpected locations',
                'TIME_ANOMALY: Rides at unusual hours for user'
            ]
            risk_score = random.uniform(0.65, 0.9)
            
        elif fraud_type == 'promo_abuse':
            patterns = [
                'ACCOUNT_SIMILARITY: Similar signup patterns detected',
                'PAYMENT_OVERLAP: Same payment method across accounts',
                'LOCATION_CLUSTERING: Multiple accounts from same location',
                'PROMO_PATTERN: Consistent promo code usage'
            ]
            risk_score = random.uniform(0.6, 0.85)
        
        fraud_case = {
            "id": f"fraud_{uuid.uuid4().hex[:16]}",
            "ride_id": ride['id'],
            "fraud_type": fraud_type,
            "description": fraud_info['description'],
            "risk_score": round(risk_score, 3),
            "detected_at": ride['requested_at'] + random.randint(300, 3600),  # 5min to 1hr after
            "patterns_detected": patterns,
            "status": random.choice(['investigating', 'confirmed', 'false_positive']),
            "action_taken": random.choice([
                'account_suspended', 
                'ride_refunded', 
                'additional_verification_required',
                'no_action',
                'escalated_to_law_enforcement'
            ]),
            "metadata": {
                "driver_account": ride['driver_account'],
                "passenger_id": ride['passenger_id'],
                "amount_at_risk": ride['pricing']['total'],
                "detection_method": random.choice(['ml_model', 'rule_based', 'manual_review']),
                "investigation_notes": f"Flagged for {fraud_type} - {random.choice(patterns)}"
            }
        }
        
        fraud_cases.append(fraud_case)
    
    return fraud_cases

# =============================================================================
# PASSENGER GENERATION
# =============================================================================

def generate_passenger(passenger_id: str, signup_date: datetime, city: Dict[str, Any]) -> Dict[str, Any]:
    """Generate passenger customer profile."""
    stripe_ids = generate_stripe_ids()
    
    # Passenger demographics
    is_business_account = random.random() < 0.15  # 15% business accounts
    
    passenger = {
        "id": stripe_ids['customer'],
        "object": "customer",
        "created": int(signup_date.timestamp()),
        "email": fake.email(),
        "name": fake.name() if not is_business_account else fake.company(),
        "phone": fake.phone_number(),
        "description": "RideShare Plus passenger",
        "address": {
            "line1": fake.street_address(),
            "city": city['name'],
            "state": fake.state_abbr(),
            "postal_code": fake.zipcode(),
            "country": "US"
        },
        "shipping": None,
        "default_source": f"card_{uuid.uuid4().hex[:22]}",
        "metadata": {
            "passenger_id": passenger_id,
            "account_type": "business" if is_business_account else "personal",
            "city": city['name'],
            "signup_channel": random.choice(['mobile_app', 'website', 'referral']),
            "preferred_vehicle": random.choice(['standard', 'premium', 'xl']),
            "average_rating": round(random.uniform(4.5, 5.0), 2),
            "total_rides": 0,
            "total_spent": 0
        }
    }
    
    return passenger

# =============================================================================
# MAIN DATA GENERATION
# =============================================================================

def generate_rideshare_data() -> Tuple[List[Dict], List[Dict], List[Dict], List[Dict], List[Dict], List[Dict], List[Dict]]:
    """Generate complete RideShare Plus platform data."""
    print("🚗 Generating RideShare Plus platform data...")
    
    all_drivers = []
    all_passengers = []
    all_rides = []
    all_payments = []
    all_payouts = []
    all_issuing_cards = []
    all_issuing_authorizations = []
    all_fraud_cases = []
    
    # Start date for data generation
    start_date = datetime(2023, 1, 1)
    
    driver_counter = 1
    passenger_counter = 1
    ride_counter = 1
    
    # Track driver earnings for payouts
    driver_earnings = defaultdict(int)
    
    # Generate data across 24 months
    for month in range(24):
        current_date = start_date + timedelta(days=30 * month)
        stage = get_lifecycle_stage(month)
        stage_config = LIFECYCLE[stage]
        
        print(f"📅 Processing month {month + 1}/24 ({stage} stage) - {stage_config['cities']} cities...")
        
        # Select cities for this stage
        active_cities = CITIES[:stage_config['cities']]
        
        # Generate new drivers for this month (20% of total target per month)
        new_drivers_this_month = stage_config['drivers'] // 12  # Monthly onboarding
        
        for _ in range(new_drivers_this_month):
            city = random.choice(active_cities)
            onboarding_date = current_date + timedelta(days=random.randint(0, 29))
            
            # Create driver account
            driver = create_driver_account(f"DRIVER_{driver_counter:06d}", onboarding_date, city)
            all_drivers.append(driver)
            
            # Create fuel card for driver
            fuel_card = create_driver_fuel_card(driver)
            all_issuing_cards.append(fuel_card)
            
            driver_counter += 1
        
        # Generate passengers (more passengers than drivers)
        passengers_this_month = int(new_drivers_this_month * 3.5)  # 3.5x passenger to driver ratio
        
        for _ in range(passengers_this_month):
            city = random.choice(active_cities)
            signup_date = current_date + timedelta(days=random.randint(0, 29))
            
            passenger = generate_passenger(f"PASS_{passenger_counter:06d}", signup_date, city)
            all_passengers.append(passenger)
            passenger_counter += 1
        
        # Generate rides for this month
        weekly_rides = stage_config['rides_per_week']
        monthly_rides = weekly_rides * 4
        
        # Distribute rides throughout the month
        for _ in range(monthly_rides):
            # Select random day/time within month
            ride_date = current_date + timedelta(
                days=random.randint(0, 29),
                hours=random.randint(5, 23),
                minutes=random.randint(0, 59)
            )
            
            # Select city, driver, and passenger
            city = random.choice(active_cities)
            
            # Available drivers in this city
            city_drivers = [d for d in all_drivers 
                          if d['metadata']['city'] == city['name'] 
                          and d['created'] <= int(ride_date.timestamp())]
            
            # Available passengers
            available_passengers = [p for p in all_passengers 
                                  if p['created'] <= int(ride_date.timestamp())]
            
            if not city_drivers or not available_passengers:
                continue
            
            driver = random.choice(city_drivers)
            passenger = random.choice(available_passengers)
            
            # Process ride
            ride_record, payment_intent, driver_transfer = process_ride(
                f"RIDE_{ride_counter:08d}", passenger, driver, ride_date, city
            )
            
            all_rides.append(ride_record)
            all_payments.append(payment_intent)
            
            if driver_transfer:
                driver_earnings[driver['id']] += driver_transfer['amount']
            
            ride_counter += 1
        
        # Generate weekly payouts for drivers (every 4th week)
        if month % 1 == 0:  # Monthly payout processing
            payout_date = current_date + timedelta(days=28)
            
            for driver in all_drivers:
                if driver['id'] in driver_earnings and driver_earnings[driver['id']] > 0:
                    payout = handle_driver_payouts(driver, driver_earnings[driver['id']], payout_date)
                    if payout:
                        all_payouts.append(payout)
                    
                    # Generate fuel purchases for drivers with earnings
                    driver_cards = [c for c in all_issuing_cards 
                                  if c['metadata']['driver_account'] == driver['id']]
                    if driver_cards:
                        fuel_card = driver_cards[0]
                        # Estimate rides this week
                        driver_rides_this_month = len([r for r in all_rides 
                                                     if r['driver_account'] == driver['id']])
                        
                        weekly_auths = generate_fuel_purchases(
                            fuel_card, current_date, driver_rides_this_month
                        )
                        all_issuing_authorizations.extend(weekly_auths)
                    
                    # Reset driver earnings
                    driver_earnings[driver['id']] = 0
    
    # Generate fraud cases
    print("🔍 Generating fraud detection scenarios...")
    for stage, config in LIFECYCLE.items():
        stage_rides = [r for r in all_rides 
                      if get_lifecycle_stage(
                          (datetime.fromtimestamp(r['requested_at']) - start_date).days // 30
                      ) == stage]
        
        fraud_cases = generate_fraud_scenarios(stage_rides, config)
        all_fraud_cases.extend(fraud_cases)
    
    print(f"✅ Generated {len(all_drivers)} drivers, {len(all_rides)} rides, {len(all_fraud_cases)} fraud cases")
    return (all_drivers, all_passengers, all_rides, all_payments, 
            all_payouts, all_issuing_cards, all_issuing_authorizations, all_fraud_cases)

# =============================================================================
# METRICS CALCULATION
# =============================================================================

def calculate_platform_metrics(drivers: List[Dict], rides: List[Dict], payments: List[Dict],
                              payouts: List[Dict], fraud_cases: List[Dict]) -> Dict[str, Any]:
    """Calculate rideshare platform metrics."""
    print("📊 Calculating RideShare Plus metrics...")
    
    # Basic counts
    total_drivers = len(drivers)
    active_drivers = len([d for d in drivers if any(r['driver_account'] == d['id'] for r in rides)])
    total_rides = len(rides)
    completed_rides = len([r for r in rides if r['status'] == 'completed'])
    
    # Revenue calculations
    successful_payments = [p for p in payments if p['status'] == 'succeeded']
    gross_bookings = sum(p['amount'] for p in successful_payments)
    
    # Platform revenue (keep 25% of fare)
    platform_revenue = sum(
        int(p['amount'] * PRICING_CONFIG['platform_fee']) + PRICING_CONFIG['booking_fee']
        for p in successful_payments
    )
    
    # Driver earnings
    total_driver_earnings = sum(po['amount'] for po in payouts)
    
    # Average metrics
    avg_fare = (gross_bookings / len(successful_payments)) if successful_payments else 0
    avg_distance = sum(r['distance_miles'] for r in rides if r['distance_miles']) / max(1, len(rides))
    avg_duration = sum(r['duration_minutes'] for r in rides if r['duration_minutes']) / max(1, completed_rides)
    
    # Utilization metrics
    avg_rides_per_driver = total_rides / max(1, active_drivers)
    completion_rate = (completed_rides / total_rides * 100) if total_rides > 0 else 0
    
    # Surge pricing analysis
    surge_rides = [r for r in rides if r['pricing']['surge_multiplier'] > 1.0]
    surge_frequency = (len(surge_rides) / total_rides * 100) if total_rides > 0 else 0
    avg_surge_multiplier = (sum(r['pricing']['surge_multiplier'] for r in surge_rides) / 
                           len(surge_rides)) if surge_rides else 1.0
    
    # Fraud metrics
    fraud_rate = (len(fraud_cases) / total_rides * 100) if total_rides > 0 else 0
    fraud_by_type = {}
    for fraud_type in FRAUD_TYPES.keys():
        type_cases = [f for f in fraud_cases if f['fraud_type'] == fraud_type]
        fraud_by_type[fraud_type] = {
            'count': len(type_cases),
            'percentage': (len(type_cases) / len(fraud_cases) * 100) if fraud_cases else 0
        }
    
    # Vehicle type distribution
    vehicle_distribution = {}
    for vehicle_type in VEHICLE_TYPES.keys():
        type_rides = [r for r in rides if r['vehicle_type'] == vehicle_type]
        vehicle_distribution[vehicle_type] = {
            'rides': len(type_rides),
            'percentage': (len(type_rides) / total_rides * 100) if total_rides > 0 else 0
        }
    
    # City performance
    city_metrics = {}
    for city in set(r['city'] for r in rides):
        city_rides = [r for r in rides if r['city'] == city]
        city_revenue = sum(r['pricing']['total'] for r in city_rides if r['status'] == 'completed')
        city_metrics[city] = {
            'rides': len(city_rides),
            'revenue': city_revenue,
            'avg_fare': (city_revenue / len(city_rides)) if city_rides else 0
        }
    
    return {
        "overview": {
            "total_drivers": total_drivers,
            "active_drivers": active_drivers,
            "total_rides": total_rides,
            "completed_rides": completed_rides,
            "completion_rate": round(completion_rate, 2)
        },
        "financial_metrics": {
            "gross_bookings_cents": gross_bookings,
            "gross_bookings_dollars": gross_bookings / 100,
            "platform_revenue_cents": platform_revenue,
            "platform_revenue_dollars": platform_revenue / 100,
            "driver_earnings_cents": total_driver_earnings,
            "driver_earnings_dollars": total_driver_earnings / 100,
            "take_rate_percent": round((platform_revenue / gross_bookings * 100) if gross_bookings > 0 else 0, 2)
        },
        "ride_metrics": {
            "average_fare_dollars": round(avg_fare / 100, 2),
            "average_distance_miles": round(avg_distance, 2),
            "average_duration_minutes": round(avg_duration, 1),
            "rides_per_active_driver": round(avg_rides_per_driver, 1)
        },
        "surge_pricing": {
            "surge_rides": len(surge_rides),
            "surge_frequency_percent": round(surge_frequency, 2),
            "average_surge_multiplier": round(avg_surge_multiplier, 2)
        },
        "fraud_detection": {
            "total_fraud_cases": len(fraud_cases),
            "fraud_rate_percent": round(fraud_rate, 3),
            "fraud_by_type": fraud_by_type
        },
        "vehicle_distribution": vehicle_distribution,
        "city_performance": city_metrics
    }

# =============================================================================
# OUTPUT GENERATION
# =============================================================================

def save_rideshare_data(drivers: List[Dict], passengers: List[Dict], rides: List[Dict],
                       payments: List[Dict], payouts: List[Dict], cards: List[Dict],
                       authorizations: List[Dict], fraud_cases: List[Dict], 
                       metrics: Dict[str, Any]) -> None:
    """Save all generated data to JSON files."""
    print("💾 Saving RideShare Plus data to files...")
    
    output_dir = "rideshare_data"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save main data files
    datasets = {
        "drivers.json": drivers,
        "passengers.json": passengers,
        "rides.json": rides,
        "payments.json": payments,
        "payouts.json": payouts,
        "issuing_cards.json": cards,
        "issuing_authorizations.json": authorizations,
        "fraud_cases.json": fraud_cases,
        "platform_metrics.json": metrics
    }
    
    for filename, data in datasets.items():
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    print(f"📁 Data saved to {output_dir}/ directory")

def print_rideshare_summary(drivers: List[Dict], rides: List[Dict], payments: List[Dict],
                          fraud_cases: List[Dict], metrics: Dict[str, Any]) -> None:
    """Print comprehensive RideShare Plus generation summary."""
    print("\n" + "="*80)
    print("🚗 RIDESHARE PLUS PLATFORM DATA GENERATION COMPLETE")
    print("="*80)
    
    overview = metrics['overview']
    financial = metrics['financial_metrics']
    ride_metrics = metrics['ride_metrics']
    surge = metrics['surge_pricing']
    fraud = metrics['fraud_detection']
    
    print(f"\n📊 GENERATION SUMMARY:")
    print(f"   Total drivers onboarded: {overview['total_drivers']:,}")
    print(f"   Active drivers: {overview['active_drivers']:,}")
    print(f"   Total rides: {overview['total_rides']:,}")
    print(f"   Completed rides: {overview['completed_rides']:,}")
    print(f"   Completion rate: {overview['completion_rate']:.1f}%")
    
    print(f"\n💰 FINANCIAL METRICS:")
    print(f"   Gross bookings: ${financial['gross_bookings_dollars']:,.2f}")
    print(f"   Platform revenue: ${financial['platform_revenue_dollars']:,.2f}")
    print(f"   Driver earnings: ${financial['driver_earnings_dollars']:,.2f}")
    print(f"   Platform take rate: {financial['take_rate_percent']:.1f}%")
    
    print(f"\n🚗 RIDE PERFORMANCE:")
    print(f"   Average fare: ${ride_metrics['average_fare_dollars']:.2f}")
    print(f"   Average distance: {ride_metrics['average_distance_miles']:.1f} miles")
    print(f"   Average duration: {ride_metrics['average_duration_minutes']:.1f} minutes")
    print(f"   Rides per active driver: {ride_metrics['rides_per_active_driver']:.1f}")
    
    print(f"\n📈 SURGE PRICING:")
    print(f"   Surge rides: {surge['surge_rides']:,}")
    print(f"   Surge frequency: {surge['surge_frequency_percent']:.1f}%")
    print(f"   Average surge multiplier: {surge['average_surge_multiplier']:.1f}x")
    
    print(f"\n🔍 FRAUD DETECTION:")
    print(f"   Fraud cases detected: {fraud['total_fraud_cases']:,}")
    print(f"   Fraud rate: {fraud['fraud_rate_percent']:.2f}%")
    for fraud_type, stats in fraud['fraud_by_type'].items():
        print(f"   {fraud_type.replace('_', ' ').title()}: {stats['count']} ({stats['percentage']:.1f}%)")
    
    print(f"\n🏙️ CITY PERFORMANCE:")
    city_performance = metrics['city_performance']
    top_cities = sorted(city_performance.items(), key=lambda x: x[1]['rides'], reverse=True)[:5]
    for city, stats in top_cities:
        print(f"   {city}: {stats['rides']:,} rides, ${stats['revenue']/100:,.0f} revenue")
    
    print(f"\n📁 OUTPUT FILES:")
    print(f"   ✅ drivers.json - Driver Connect accounts with ratings")
    print(f"   ✅ passengers.json - Customer profiles and preferences")
    print(f"   ✅ rides.json - Complete ride records with pricing")
    print(f"   ✅ payments.json - Ride payments with surge pricing")
    print(f"   ✅ payouts.json - Driver earnings and transfers")
    print(f"   ✅ issuing_cards.json - Driver fuel and expense cards")
    print(f"   ✅ issuing_authorizations.json - Fuel purchase transactions")
    print(f"   ✅ fraud_cases.json - Suspicious activity detection")
    print(f"   ✅ platform_metrics.json - Complete platform analytics")
    
    print(f"\n🚀 Ready for transportation platform prototyping!")
    print("="*80)

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("🚗 RideShare Plus Synthetic Platform Data Generator")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        # Generate all data
        (drivers, passengers, rides, payments, payouts, 
         cards, authorizations, fraud_cases) = generate_rideshare_data()
        
        # Calculate metrics
        metrics = calculate_platform_metrics(drivers, rides, payments, payouts, fraud_cases)
        
        # Save data
        save_rideshare_data(drivers, passengers, rides, payments, payouts, 
                           cards, authorizations, fraud_cases, metrics)
        
        # Print summary
        print_rideshare_summary(drivers, rides, payments, fraud_cases, metrics)
        
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"\n⏱️ Total execution time: {execution_time:.1f} seconds")
        
    except Exception as e:
        print(f"\n❌ Error during generation: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
