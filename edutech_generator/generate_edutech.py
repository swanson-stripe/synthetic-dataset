#!/usr/bin/env python3
"""
EduTech Academy Online Education Marketplace - Synthetic Data Generator

Generates realistic Stripe payment data for an online education platform
with instructor payouts, student financing, and corporate training.

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

PLATFORM_CONFIG = {
    'revenue_share': {
        'instructor': 0.70,  # Instructor gets 70%
        'platform': 0.30     # Platform gets 30%
    },
    'course_pricing': {
        'mini': range(900, 2900),      # $9-29
        'standard': range(4900, 9900),  # $49-99
        'comprehensive': range(19900, 49900),  # $199-499
        'bootcamp': range(99900, 299900)  # $999-2999
    },
    'refund_window': 30,  # 30-day guarantee
    'payment_plans': {
        'enabled': True,
        'installments': [2, 3, 4, 6],
        'apr': 0.0  # 0% interest educational financing
    },
    'corporate_discounts': {
        'small': {'employees': range(10, 50), 'discount': 0.10},     # 10%
        'medium': {'employees': range(50, 200), 'discount': 0.20},   # 20%
        'large': {'employees': range(200, 1000), 'discount': 0.30}   # 30%
    }
}

LIFECYCLE = {
    'early': {
        'courses': 100,
        'students': 1000,
        'instructors': 20,
        'months': range(0, 8),
        'refund_rate': 0.08,
        'corporate_rate': 0.05
    },
    'growth': {
        'courses': 1000,
        'students': 20000,
        'instructors': 200,
        'months': range(8, 16),
        'refund_rate': 0.05,
        'corporate_rate': 0.15
    },
    'mature': {
        'courses': 10000,
        'students': 200000,
        'instructors': 2000,
        'months': range(16, 24),
        'refund_rate': 0.03,
        'corporate_rate': 0.25
    }
}

COURSE_CATEGORIES = {
    'technology': {
        'courses': ['Python Programming', 'Web Development', 'Data Science', 'Machine Learning', 'DevOps', 'Cybersecurity'],
        'weight': 0.35
    },
    'business': {
        'courses': ['Digital Marketing', 'Project Management', 'Finance', 'Leadership', 'Entrepreneurship', 'Sales'],
        'weight': 0.25
    },
    'design': {
        'courses': ['UI/UX Design', 'Graphic Design', 'Video Editing', 'Animation', 'Photography', 'Illustration'],
        'weight': 0.20
    },
    'languages': {
        'courses': ['Spanish', 'French', 'Mandarin', 'German', 'Japanese', 'English'],
        'weight': 0.10
    },
    'arts': {
        'courses': ['Music Production', 'Creative Writing', 'Drawing', 'Painting', 'Sculpture', 'Digital Art'],
        'weight': 0.10
    }
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

def generate_course_title(category: str) -> str:
    """Generate a realistic course title."""
    courses = COURSE_CATEGORIES[category]['courses']
    base_course = random.choice(courses)
    
    modifiers = [
        "Complete", "Advanced", "Beginner's", "Mastery", "Fundamentals of",
        "Professional", "Comprehensive", "Ultimate", "Modern", "Practical"
    ]
    
    formats = [
        "Bootcamp", "Masterclass", "Course", "Tutorial", "Workshop", 
        "Training", "Academy", "Intensive", "Crash Course"
    ]
    
    if random.random() < 0.7:
        return f"{random.choice(modifiers)} {base_course} {random.choice(formats)}"
    else:
        return f"{base_course} for {random.choice(['Beginners', 'Professionals', 'Everyone'])}"

def get_course_duration(course_type: str) -> int:
    """Get course duration in hours based on type."""
    durations = {
        'mini': random.randint(1, 5),
        'standard': random.randint(8, 25),
        'comprehensive': random.randint(40, 100),
        'bootcamp': random.randint(120, 300)
    }
    return durations[course_type]

# =============================================================================
# INSTRUCTOR MANAGEMENT
# =============================================================================

def create_instructor_account(instructor_id: str, onboarding_date: datetime) -> Dict:
    """Create a Stripe Express account for an instructor."""
    category = random.choices(
        list(COURSE_CATEGORIES.keys()),
        weights=[cat['weight'] for cat in COURSE_CATEGORIES.values()]
    )[0]
    
    account = {
        "id": f"acct_INSTRUCTOR_{instructor_id}",
        "object": "account",
        "type": "express",
        "business_type": "individual",
        "country": "US",
        "created": int(onboarding_date.timestamp()),
        "default_currency": "usd",
        "details_submitted": True,
        "email": faker.email(),
        "charges_enabled": True,
        "payouts_enabled": True,
        "capabilities": {
            "card_payments": {"status": "active"},
            "transfers": {"status": "active"},
            "tax_reporting_us_1099_k": {"status": "active"}
        },
        "individual": {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": faker.email(),
            "phone": faker.phone_number(),
            "address": {
                "line1": faker.street_address(),
                "city": faker.city(),
                "state": faker.state_abbr(),
                "postal_code": faker.zipcode(),
                "country": "US"
            }
        },
        "business_profile": {
            "name": f"{faker.name()} Education",
            "product_description": f"{category.title()} Online Courses",
            "mcc": "8299",  # Educational services
            "url": f"https://edutech.academy/instructor/{instructor_id}",
            "support_email": faker.email()
        },
        "metadata": {
            "instructor_id": str(instructor_id),
            "expertise": category,
            "rating": f"{random.uniform(4.0, 5.0):.1f}",
            "total_students": str(random.randint(10, 10000)),
            "course_count": str(random.randint(1, 20)),
            "credentials": random.choice(["PhD", "Masters", "Professional", "Industry Expert"]),
            "years_teaching": str(random.randint(1, 15)),
            "completion_rate": f"{random.uniform(0.6, 0.95):.2f}"
        },
        "tos_acceptance": {
            "date": int(onboarding_date.timestamp()),
            "ip": faker.ipv4(),
            "user_agent": "EduTechAcademy/1.0"
        }
    }
    
    return account

# =============================================================================
# COURSE CREATION
# =============================================================================

def create_course(instructor: Dict, course_id: str) -> Dict:
    """Create a course listing."""
    category = instructor['metadata']['expertise']
    course_type = random.choices(
        ['mini', 'standard', 'comprehensive', 'bootcamp'],
        weights=[0.3, 0.4, 0.25, 0.05]  # Most courses are mini/standard
    )[0]
    
    price_range = PLATFORM_CONFIG['course_pricing'][course_type]
    price = random.choice(range(price_range.start, price_range.stop, 100))
    
    course = {
        "id": f"course_{course_id}",
        "instructor_id": instructor['metadata']['instructor_id'],
        "instructor_account": instructor['id'],
        "title": generate_course_title(category),
        "price": price,
        "type": course_type,
        "category": category,
        "level": random.choice(["beginner", "intermediate", "advanced"]),
        "duration_hours": get_course_duration(course_type),
        "enrolled_students": 0,
        "completion_rate": random.uniform(0.4, 0.9),
        "rating": random.uniform(3.5, 5.0),
        "created": faker.date_time_between(start_date='-1y').isoformat(),
        "published": True,
        "metadata": {
            "certificate_offered": str(course_type in ['comprehensive', 'bootcamp']),
            "accredited": str(random.random() < 0.2),
            "corporate_eligible": str(course_type != 'mini'),
            "prerequisites": str(random.random() < 0.3),
            "language": "English",
            "closed_captions": str(random.random() > 0.2)
        }
    }
    
    return course

# =============================================================================
# STUDENT MANAGEMENT
# =============================================================================

def generate_student() -> Dict:
    """Generate a student customer profile."""
    student_type = random.choices(
        ['individual', 'student', 'professional'],
        weights=[0.5, 0.3, 0.2]
    )[0]
    
    return {
        "id": f"cus_STUDENT_{generate_id()}",
        "object": "customer",
        "created": int(faker.date_time_between(start_date='-2y').timestamp()),
        "email": faker.email(),
        "name": faker.name(),
        "phone": faker.phone_number(),
        "description": f"EduTech Academy {student_type}",
        "metadata": {
            "student_type": student_type,
            "preferred_language": "English",
            "courses_completed": str(random.randint(0, 10)),
            "avg_course_rating": f"{random.uniform(3.0, 5.0):.1f}",
            "learning_path": random.choice(['career_change', 'skill_upgrade', 'hobby', 'certification']),
            "payment_preference": random.choice(['one_time', 'installments']),
            "corporate_sponsored": str(random.random() < 0.15)  # 15% corporate sponsored
        }
    }

# =============================================================================
# ENROLLMENT AND PAYMENTS
# =============================================================================

def process_enrollment(student: Dict, course: Dict, enrollment_date: datetime) -> Tuple[Dict, Optional[Dict], Optional[Dict]]:
    """Process student enrollment with payment or financing."""
    # Determine if student uses payment plan
    use_payment_plan = (
        course['price'] > 50000 and  # Expensive courses
        random.random() < 0.4 and    # 40% chance
        student['metadata']['payment_preference'] == 'installments'
    )
    
    if use_payment_plan:
        return create_payment_plan(student, course, enrollment_date)
    else:
        return create_one_time_payment(student, course, enrollment_date)

def create_one_time_payment(student: Dict, course: Dict, enrollment_date: datetime) -> Tuple[Dict, Dict, None]:
    """Create one-time payment for course enrollment."""
    payment_intent = {
        "id": f"pi_COURSE_{generate_id()}",
        "object": "payment_intent",
        "amount": course['price'],
        "currency": "usd",
        "customer": student['id'],
        "created": int(enrollment_date.timestamp()),
        "description": f"Enrollment: {course['title']}",
        "status": "succeeded" if random.random() > 0.02 else "failed",  # 2% failure rate
        "payment_method_types": ["card"],
        "charges": {
            "data": [{
                "id": f"ch_{generate_id()}",
                "amount": course['price'],
                "currency": "usd",
                "paid": random.random() > 0.02,
                "refunded": False,
                "disputed": False
            }]
        },
        "metadata": {
            "course_id": course['id'],
            "instructor_id": course['instructor_id'],
            "enrollment_date": enrollment_date.isoformat(),
            "eligible_for_refund_until": (enrollment_date + timedelta(days=30)).isoformat(),
            "course_type": course['type'],
            "student_type": student['metadata']['student_type']
        }
    }
    
    # Create instructor payout (if payment succeeded)
    transfer = None
    if payment_intent['status'] == 'succeeded':
        instructor_amount = int(course['price'] * PLATFORM_CONFIG['revenue_share']['instructor'])
        platform_fee = course['price'] - instructor_amount
        
        transfer = {
            "id": f"tr_INSTRUCTOR_{generate_id()}",
            "object": "transfer",
            "amount": instructor_amount,
            "currency": "usd",
            "created": int(enrollment_date.timestamp()),
            "destination": course['instructor_account'],
            "source_transaction": payment_intent['id'],
            "metadata": {
                "course_id": course['id'],
                "student_id": student['id'],
                "platform_fee": str(platform_fee),
                "revenue_share": str(PLATFORM_CONFIG['revenue_share']['instructor'])
            }
        }
    
    return payment_intent, transfer, None

def create_payment_plan(student: Dict, course: Dict, enrollment_date: datetime) -> Tuple[Dict, None, Dict]:
    """Create payment plan for course enrollment."""
    installments = random.choice(PLATFORM_CONFIG['payment_plans']['installments'])
    installment_amount = course['price'] // installments
    
    # Create Stripe Capital offer for student financing
    financing = {
        "id": f"cap_EDU_{generate_id()}",
        "object": "capital_financing_offer",
        "type": "student_financing",
        "total_amount": course['price'],
        "currency": "usd",
        "created": int(enrollment_date.timestamp()),
        "term_length": installments,
        "installment_amount": installment_amount,
        "apr": PLATFORM_CONFIG['payment_plans']['apr'],
        "status": "accepted",
        "metadata": {
            "course_id": course['id'],
            "student_id": student['id'],
            "instructor_id": course['instructor_id'],
            "financing_type": "education"
        }
    }
    
    # Create subscription for installment payments
    subscription = {
        "id": f"sub_PAYMENT_PLAN_{generate_id()}",
        "object": "subscription",
        "customer": student['id'],
        "created": int(enrollment_date.timestamp()),
        "status": "active",
        "current_period_start": int(enrollment_date.timestamp()),
        "current_period_end": int((enrollment_date + timedelta(days=30)).timestamp()),
        "items": {
            "data": [{
                "id": f"si_{generate_id()}",
                "price": {
                    "id": f"price_INSTALLMENT_{course['id']}",
                    "recurring": {
                        "interval": "month",
                        "interval_count": 1
                    },
                    "unit_amount": installment_amount,
                    "currency": "usd"
                },
                "quantity": 1
            }]
        },
        "metadata": {
            "course_id": course['id'],
            "total_installments": str(installments),
            "financing_id": financing['id'],
            "remaining_installments": str(installments)
        }
    }
    
    return financing, None, subscription

# =============================================================================
# REFUND PROCESSING
# =============================================================================

def process_refund_request(payment: Dict, course: Dict, request_date: datetime) -> Tuple[Optional[Dict], Optional[Dict]]:
    """Process refund request within refund window."""
    enrollment_date = datetime.fromisoformat(payment['metadata']['enrollment_date'])
    days_since_enrollment = (request_date - enrollment_date).days
    
    if days_since_enrollment <= PLATFORM_CONFIG['refund_window']:
        refund = {
            "id": f"re_EDU_{generate_id()}",
            "object": "refund",
            "payment_intent": payment['id'],
            "amount": payment['amount'],
            "currency": "usd",
            "created": int(request_date.timestamp()),
            "reason": random.choice(["requested_by_customer", "duplicate", "fraudulent"]),
            "status": "succeeded",
            "metadata": {
                "course_id": payment['metadata']['course_id'],
                "days_since_enrollment": str(days_since_enrollment),
                "refund_type": "full",
                "refund_reason": random.choice([
                    "course_quality", "technical_issues", "not_as_described", 
                    "schedule_conflict", "duplicate_purchase"
                ])
            }
        }
        
        # Reverse instructor payout
        instructor_amount = int(payment['amount'] * PLATFORM_CONFIG['revenue_share']['instructor'])
        reverse_transfer = {
            "id": f"trr_INSTRUCTOR_{generate_id()}",
            "object": "transfer_reversal",
            "amount": instructor_amount,
            "currency": "usd",
            "created": int(request_date.timestamp()),
            "metadata": {
                "original_payment": payment['id'],
                "reason": "student_refund",
                "course_id": payment['metadata']['course_id']
            }
        }
        
        return refund, reverse_transfer
    
    return None, None

# =============================================================================
# CORPORATE TRAINING
# =============================================================================

def create_corporate_account() -> Dict:
    """Create a corporate training customer account."""
    company_name = faker.company()
    employee_count = random.randint(10, 1000)
    
    # Determine discount tier
    if employee_count < 50:
        discount = PLATFORM_CONFIG['corporate_discounts']['small']['discount']
    elif employee_count < 200:
        discount = PLATFORM_CONFIG['corporate_discounts']['medium']['discount']
    else:
        discount = PLATFORM_CONFIG['corporate_discounts']['large']['discount']
    
    return {
        "id": f"cus_CORP_{generate_id()}",
        "object": "customer",
        "email": f"training@{company_name.lower().replace(' ', '').replace(',', '')}.com",
        "name": f"{company_name} - Training Department",
        "created": int(faker.date_time_between(start_date='-1y').timestamp()),
        "description": f"{company_name} - Corporate Training",
        "metadata": {
            "type": "corporate",
            "company_name": company_name,
            "employee_count": str(employee_count),
            "bulk_discount": f"{discount:.2f}",
            "invoice_payment": "true",
            "net_terms": "net_30",
            "industry": random.choice(['Technology', 'Healthcare', 'Finance', 'Manufacturing', 'Retail']),
            "training_budget": str(random.randint(10000, 500000))
        }
    }

def process_bulk_enrollment(corporate_account: Dict, course: Dict, employee_count: int, enrollment_date: datetime) -> Dict:
    """Process bulk enrollment for corporate training."""
    base_amount = course['price'] * employee_count
    discount = float(corporate_account['metadata']['bulk_discount'])
    discount_amount = int(base_amount * discount)
    final_amount = base_amount - discount_amount
    
    due_date = enrollment_date + timedelta(days=30)  # Net 30 terms
    
    # Create invoice for corporate billing
    invoice = {
        "id": f"in_CORP_{generate_id()}",
        "object": "invoice",
        "customer": corporate_account['id'],
        "amount_due": final_amount,
        "amount_paid": final_amount,
        "currency": "usd",
        "created": int(enrollment_date.timestamp()),
        "due_date": int(due_date.timestamp()),
        "description": f"Corporate Training: {course['title']} for {employee_count} employees",
        "status": "paid",
        "collection_method": "send_invoice",
        "lines": {
            "data": [{
                "id": f"il_{generate_id()}",
                "amount": base_amount,
                "currency": "usd",
                "description": f"{course['title']} - {employee_count} seats",
                "quantity": employee_count,
                "unit_amount": course['price']
            }, {
                "id": f"il_{generate_id()}",
                "amount": -discount_amount,
                "currency": "usd",
                "description": f"Corporate discount ({discount*100:.0f}%)",
                "quantity": 1,
                "unit_amount": -discount_amount
            }]
        },
        "metadata": {
            "course_id": course['id'],
            "instructor_id": course['instructor_id'],
            "employee_count": str(employee_count),
            "discount_rate": f"{discount:.2f}",
            "training_type": "corporate_bulk",
            "training_coordinator": faker.email()
        }
    }
    
    return invoice

# =============================================================================
# LEARNING ANALYTICS
# =============================================================================

def generate_student_progress(student: Dict, course: Dict, enrollment_date: datetime) -> Dict:
    """Generate student learning progress data."""
    progress_percentage = random.uniform(0, 100)
    completed = progress_percentage > 70
    
    last_accessed = enrollment_date + timedelta(days=random.randint(0, 90))
    time_spent = random.randint(0, course['duration_hours'] * 60)
    
    return {
        "student_id": student['id'],
        "course_id": course['id'],
        "enrollment_date": enrollment_date.isoformat(),
        "progress_percentage": progress_percentage,
        "last_accessed": last_accessed.isoformat(),
        "time_spent_minutes": time_spent,
        "assignments_completed": random.randint(0, 20),
        "quiz_scores": [random.uniform(60, 100) for _ in range(random.randint(0, 10))],
        "certificate_earned": completed and course['metadata']['certificate_offered'] == 'True',
        "completion_date": (enrollment_date + timedelta(days=random.randint(7, 60))).isoformat() if completed else None,
        "satisfaction_rating": random.uniform(3.0, 5.0) if completed else None
    }

def calculate_instructor_metrics(instructor: Dict, enrollments: List[Dict], refunds: List[Dict]) -> Dict:
    """Calculate performance metrics for an instructor."""
    instructor_id = instructor['metadata']['instructor_id']
    
    # Filter enrollments for this instructor
    instructor_enrollments = [
        e for e in enrollments 
        if (isinstance(e, dict) and 
            e.get('metadata', {}).get('instructor_id') == instructor_id)
    ]
    
    instructor_refunds = [
        r for r in refunds
        if r.get('metadata', {}).get('course_id') in [
            e.get('metadata', {}).get('course_id') for e in instructor_enrollments
        ]
    ]
    
    total_revenue = sum(
        e.get('amount', 0) for e in instructor_enrollments 
        if e.get('status') == 'succeeded'
    )
    
    instructor_earnings = int(total_revenue * PLATFORM_CONFIG['revenue_share']['instructor'])
    refund_amount = sum(r.get('amount', 0) for r in instructor_refunds)
    
    return {
        "instructor_id": instructor_id,
        "total_students": len(instructor_enrollments),
        "total_revenue": total_revenue,
        "instructor_earnings": instructor_earnings,
        "platform_earnings": total_revenue - instructor_earnings,
        "refund_rate": len(instructor_refunds) / len(instructor_enrollments) if instructor_enrollments else 0,
        "refund_amount": refund_amount,
        "average_rating": float(instructor['metadata']['rating']),
        "completion_rate": random.uniform(0.4, 0.9),
        "student_satisfaction": random.uniform(0.7, 0.95),
        "courses_published": int(instructor['metadata']['course_count'])
    }

# =============================================================================
# TAX COMPLIANCE
# =============================================================================

def generate_tax_documents(instructor: Dict, year: int, annual_earnings: float) -> Dict:
    """Generate tax documents for instructors."""
    instructor_id = instructor['metadata']['instructor_id']
    country = instructor.get('country', 'US')
    
    if country == 'US' and annual_earnings > 600:  # IRS threshold for 1099-K
        return {
            "id": f"tax_1099_{year}_{instructor_id}",
            "object": "tax_document",
            "type": "1099-K",
            "year": year,
            "instructor_id": instructor_id,
            "gross_amount": int(annual_earnings),
            "currency": "usd",
            "created": int(datetime(year + 1, 1, 31).timestamp()),
            "tax_id": f"XXX-XX-{random.randint(1000, 9999)}",
            "metadata": {
                "form_delivered": "electronic",
                "delivery_date": f"{year + 1}-01-31",
                "payment_transactions": random.randint(1, 200),
                "gross_payment_amount": int(annual_earnings)
            }
        }
    else:
        # International tax reporting
        return {
            "id": f"tax_intl_{year}_{instructor_id}",
            "object": "tax_document", 
            "type": "international_reporting",
            "year": year,
            "instructor_id": instructor_id,
            "gross_amount": int(annual_earnings),
            "currency": "usd",
            "country": country,
            "tax_treaty": random.choice([True, False]),
            "withholding_rate": random.choice([0.0, 0.15, 0.30]) if country != 'US' else 0.0,
            "metadata": {
                "delivery_method": "electronic",
                "compliance_status": "compliant"
            }
        }

# =============================================================================
# MAIN DATA GENERATION
# =============================================================================

def generate_edutech_data() -> Tuple[List[Dict], List[Dict], List[Dict], List[Dict], List[Dict], List[Dict], List[Dict], List[Dict], List[Dict], List[Dict]]:
    """Generate complete EduTech Academy education marketplace data."""
    print("🎓 Generating EduTech Academy education marketplace data...")
    
    all_instructors = []
    all_students = []
    all_courses = []
    all_enrollments = []
    all_transfers = []
    all_refunds = []
    all_corporate_accounts = []
    all_financing = []
    all_student_progress = []
    all_tax_documents = []
    
    # Start date for data generation
    start_date = datetime(2022, 1, 1)
    
    # Generate instructors and courses per stage
    instructor_counter = 1
    course_counter = 1
    student_counter = 1
    
    for month in range(24):  # 24 months of data
        current_date = calculate_monthly_date(start_date, month)
        stage_name, stage_config = get_stage_config(month)
        
        print(f"📅 Processing month {month + 1}/24 ({stage_name} stage)...")
        
        # Add new instructors (front-loaded)
        if month < 12:  # Add instructors in first year
            new_instructors_count = max(1, stage_config['instructors'] // 12)
            
            for _ in range(new_instructors_count):
                onboarding_date = current_date + timedelta(days=random.randint(0, 29))
                
                instructor = create_instructor_account(f"INST{instructor_counter:04d}", onboarding_date)
                all_instructors.append(instructor)
                
                # Create courses for this instructor
                courses_per_instructor = random.randint(1, 5)
                
                for _ in range(courses_per_instructor):
                    course = create_course(instructor, f"C{course_counter:06d}")
                    all_courses.append(course)
                    course_counter += 1
                
                instructor_counter += 1
        
        # Add new students
        new_students_count = max(10, stage_config['students'] // 24)  # Spread over 24 months
        
        for _ in range(new_students_count):
            student = generate_student()
            all_students.append(student)
            student_counter += 1
        
        # Process enrollments for existing students
        active_students = all_students[-min(len(all_students), stage_config['students']):]  # Recent students
        active_courses = all_courses
        
        # Regular individual enrollments
        enrollment_rate = random.uniform(0.02, 0.05)  # 2-5% of students enroll per month
        students_to_enroll = random.sample(
            active_students,
            min(int(len(active_students) * enrollment_rate), len(active_students))
        )
        
        for student in students_to_enroll:
            if active_courses:
                course = random.choice(active_courses)
                enrollment_date = current_date + timedelta(days=random.randint(0, 29))
                
                payment, transfer, financing = process_enrollment(student, course, enrollment_date)
                
                enrollment_record = {
                    "student_id": student['id'],
                    "course_id": course['id'],
                    "enrollment_date": enrollment_date.isoformat(),
                    "payment_id": payment['id'] if payment else None,
                    "financing_id": financing['id'] if financing else None,
                    "enrollment_type": "individual"
                }
                
                all_enrollments.append(enrollment_record)
                
                if payment:
                    all_enrollments.append(payment)
                if transfer:
                    all_transfers.append(transfer)
                if financing:
                    all_financing.append(financing)
        
        # Corporate enrollments
        corporate_enrollment_rate = stage_config['corporate_rate']
        if random.random() < corporate_enrollment_rate:
            if not all_corporate_accounts or random.random() < 0.3:  # 30% chance of new corporate account
                corporate_account = create_corporate_account()
                all_corporate_accounts.append(corporate_account)
            else:
                corporate_account = random.choice(all_corporate_accounts)
            
            # Corporate bulk enrollment
            if active_courses:
                course = random.choice([c for c in active_courses if c['metadata']['corporate_eligible'] == 'True'])
                if course:
                    employee_count = random.randint(5, 50)
                    enrollment_date = current_date + timedelta(days=random.randint(0, 29))
                    
                    invoice = process_bulk_enrollment(corporate_account, course, employee_count, enrollment_date)
                    all_enrollments.append(invoice)
        
        # Process refunds (within refund window)
        refund_rate = stage_config['refund_rate']
        eligible_payments = [
            p for p in all_enrollments 
            if (isinstance(p, dict) and 
                p.get('object') == 'payment_intent' and 
                p.get('status') == 'succeeded' and
                'enrollment_date' in p.get('metadata', {}))
        ]
        
        refunds_to_process = random.sample(
            eligible_payments,
            min(int(len(eligible_payments) * refund_rate), len(eligible_payments))
        )
        
        for payment in refunds_to_process:
            course = next((c for c in all_courses if c['id'] == payment['metadata']['course_id']), None)
            if course:
                refund_date = current_date + timedelta(days=random.randint(0, 29))
                refund, reverse_transfer = process_refund_request(payment, course, refund_date)
                
                if refund:
                    all_refunds.append(refund)
                    if reverse_transfer:
                        all_transfers.append(reverse_transfer)
    
    # Generate student progress data
    print("📚 Generating student progress data...")
    individual_payments = [e for e in all_enrollments if e.get('object') == 'payment_intent' and e.get('status') == 'succeeded']
    
    for payment in random.sample(individual_payments, min(len(individual_payments), 1000)):  # Sample for performance
        if 'course_id' in payment.get('metadata', {}):
            course = next((c for c in all_courses if c['id'] == payment['metadata']['course_id']), None)
            student = next((s for s in all_students if s['id'] == payment['customer']), None)
            
            if course and student:
                enrollment_date = datetime.fromisoformat(payment['metadata']['enrollment_date'])
                progress = generate_student_progress(student, course, enrollment_date)
                all_student_progress.append(progress)
    
    # Generate tax documents for 2023
    print("📋 Generating tax documents...")
    for instructor in all_instructors:
        instructor_id = instructor['metadata']['instructor_id']
        
        # Calculate 2023 earnings
        instructor_transfers = [
            t for t in all_transfers 
            if (t.get('destination') == instructor['id'] and 
                datetime.fromtimestamp(t.get('created', 0)).year == 2023)
        ]
        
        annual_earnings = sum(t.get('amount', 0) for t in instructor_transfers)
        
        if annual_earnings > 0:
            tax_doc = generate_tax_documents(instructor, 2023, annual_earnings)
            all_tax_documents.append(tax_doc)
    
    print(f"✅ Generated {len(all_instructors)} instructors, {len(all_courses)} courses, {len(all_students)} students")
    return (all_instructors, all_students, all_courses, all_enrollments, 
            all_transfers, all_refunds, all_corporate_accounts, all_financing,
            all_student_progress, all_tax_documents)

# =============================================================================
# ANALYTICS AND METRICS
# =============================================================================

def calculate_education_metrics(instructors: List[Dict], students: List[Dict], courses: List[Dict],
                               enrollments: List[Dict], transfers: List[Dict], refunds: List[Dict],
                               corporate_accounts: List[Dict], financing: List[Dict],
                               student_progress: List[Dict], tax_documents: List[Dict]) -> Dict:
    """Calculate comprehensive education marketplace metrics."""
    print("📊 Calculating education marketplace metrics...")
    
    # Filter different types of enrollment records
    individual_payments = [e for e in enrollments if e.get('object') == 'payment_intent']
    corporate_invoices = [e for e in enrollments if e.get('object') == 'invoice']
    student_enrollments = [e for e in enrollments if 'enrollment_date' in e and 'student_id' in e]
    
    # Revenue analysis
    individual_revenue = sum(p['amount'] for p in individual_payments if p.get('status') == 'succeeded')
    corporate_revenue = sum(i['amount_paid'] for i in corporate_invoices)
    total_revenue = individual_revenue + corporate_revenue
    
    # Platform vs instructor revenue
    platform_revenue = total_revenue * PLATFORM_CONFIG['revenue_share']['platform']
    instructor_revenue = total_revenue * PLATFORM_CONFIG['revenue_share']['instructor']
    
    # Refund analysis
    total_refunds = sum(r['amount'] for r in refunds)
    refund_rate = len(refunds) / len(individual_payments) if individual_payments else 0
    
    # Course analysis
    course_categories = {}
    for course in courses:
        category = course['category']
        course_categories[category] = course_categories.get(category, 0) + 1
    
    # Student analysis
    student_types = {}
    for student in students:
        student_type = student['metadata']['student_type']
        student_types[student_type] = student_types.get(student_type, 0) + 1
    
    # Average course price by type
    course_prices = {}
    for course in courses:
        course_type = course['type']
        if course_type not in course_prices:
            course_prices[course_type] = []
        course_prices[course_type].append(course['price'])
    
    avg_prices = {
        course_type: sum(prices) / len(prices) if prices else 0
        for course_type, prices in course_prices.items()
    }
    
    # Learning analytics
    completed_courses = len([p for p in student_progress if p.get('completion_date')])
    avg_completion_rate = completed_courses / len(student_progress) if student_progress else 0
    avg_satisfaction = sum(p.get('satisfaction_rating', 0) for p in student_progress if p.get('satisfaction_rating')) / max(1, len([p for p in student_progress if p.get('satisfaction_rating')]))
    
    # Tax compliance
    tax_documents_issued = len(tax_documents)
    
    return {
        "total_instructors": len(instructors),
        "total_students": len(students),
        "total_courses": len(courses),
        "individual_enrollments": len(student_enrollments),
        "corporate_accounts": len(corporate_accounts),
        "total_revenue": total_revenue,
        "individual_revenue": individual_revenue,
        "corporate_revenue": corporate_revenue,
        "platform_revenue": platform_revenue,
        "instructor_revenue": instructor_revenue,
        "total_refunds": total_refunds,
        "refund_rate": refund_rate,
        "payment_plan_usage": len([f for f in financing]),
        "course_distribution": course_categories,
        "student_distribution": student_types,
        "average_course_prices": avg_prices,
        "learning_analytics": {
            "total_progress_records": len(student_progress),
            "course_completion_rate": avg_completion_rate,
            "average_satisfaction": avg_satisfaction,
            "certificates_earned": len([p for p in student_progress if p.get('certificate_earned')])
        },
        "tax_compliance": {
            "tax_documents_issued": tax_documents_issued,
            "instructors_with_tax_docs": len(set(t['instructor_id'] for t in tax_documents)),
            "total_taxable_earnings": sum(t.get('gross_amount', 0) for t in tax_documents)
        },
        "marketplace_metrics": {
            "revenue_per_student": total_revenue / len(students) if students else 0,
            "revenue_per_instructor": instructor_revenue / len(instructors) if instructors else 0,
            "courses_per_instructor": len(courses) / len(instructors) if instructors else 0,
            "corporate_penetration": len(corporate_accounts) / (len(corporate_accounts) + len(students)) if (corporate_accounts or students) else 0,
            "platform_take_rate": PLATFORM_CONFIG['revenue_share']['platform'],
            "payment_plan_adoption": len(financing) / len([e for e in enrollments if e.get('object') == 'payment_intent']) if enrollments else 0
        }
    }

# =============================================================================
# FILE OUTPUT
# =============================================================================

def save_edutech_data(instructors: List[Dict], students: List[Dict], courses: List[Dict],
                     enrollments: List[Dict], transfers: List[Dict], refunds: List[Dict],
                     corporate_accounts: List[Dict], financing: List[Dict], 
                     student_progress: List[Dict], tax_documents: List[Dict], metrics: Dict) -> None:
    """Save all EduTech Academy data to JSON files."""
    print("💾 Saving EduTech Academy data to files...")
    
    output_dir = "education_data"
    
    # Ensure output directory exists
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    files_to_save = {
        "instructors.json": instructors,
        "students.json": students,
        "courses.json": courses,
        "enrollments.json": enrollments,
        "instructor_transfers.json": transfers,
        "refunds.json": refunds,
        "corporate_accounts.json": corporate_accounts,
        "student_financing.json": financing,
        "student_progress.json": student_progress,
        "tax_documents.json": tax_documents,
        "education_metrics.json": metrics
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
    print("🎓 EDUTECH ACADEMY ONLINE EDUCATION MARKETPLACE DATA GENERATOR")
    print("="*80)
    
    try:
        # Generate all data
        start_time = datetime.now()
        
        (instructors, students, courses, enrollments, transfers, refunds, 
         corporate_accounts, financing, student_progress, tax_documents) = generate_edutech_data()
        
        # Calculate metrics
        metrics = calculate_education_metrics(
            instructors, students, courses, enrollments, transfers, refunds, 
            corporate_accounts, financing, student_progress, tax_documents
        )
        
        # Save data
        save_edutech_data(
            instructors, students, courses, enrollments, transfers, refunds, 
            corporate_accounts, financing, student_progress, tax_documents, metrics
        )
        
        # Print summary
        execution_time = datetime.now() - start_time
        
        print("\n" + "="*80)
        print("🎓 EDUTECH ACADEMY EDUCATION MARKETPLACE DATA GENERATION COMPLETE")
        print("="*80)
        
        print(f"\n📊 GENERATION SUMMARY:")
        print(f"   Total instructors: {metrics['total_instructors']:,}")
        print(f"   Total students: {metrics['total_students']:,}")
        print(f"   Total courses: {metrics['total_courses']:,}")
        print(f"   Individual enrollments: {metrics['individual_enrollments']:,}")
        print(f"   Corporate accounts: {metrics['corporate_accounts']:,}")
        
        print(f"\n💰 REVENUE METRICS:")
        print(f"   Total marketplace revenue: ${metrics['total_revenue']:,.2f}")
        print(f"   Individual student revenue: ${metrics['individual_revenue']:,.2f}")
        print(f"   Corporate training revenue: ${metrics['corporate_revenue']:,.2f}")
        print(f"   Platform revenue (30%): ${metrics['platform_revenue']:,.2f}")
        print(f"   Instructor earnings (70%): ${metrics['instructor_revenue']:,.2f}")
        
        print(f"\n📈 STUDENT METRICS:")
        print(f"   Revenue per student: ${metrics['marketplace_metrics']['revenue_per_student']:,.2f}")
        print(f"   Payment plan usage: {metrics['payment_plan_usage']:,} financing agreements")
        print(f"   Refund rate: {metrics['refund_rate']:.1%}")
        print(f"   Total refunds processed: ${metrics['total_refunds']:,.2f}")
        
        print(f"\n👨‍🏫 INSTRUCTOR METRICS:")
        print(f"   Revenue per instructor: ${metrics['marketplace_metrics']['revenue_per_instructor']:,.2f}")
        print(f"   Courses per instructor: {metrics['marketplace_metrics']['courses_per_instructor']:.1f}")
        print(f"   Course distribution:")
        for category, count in metrics['course_distribution'].items():
            print(f"     {category.title()}: {count:,}")
        
        print(f"\n🏢 CORPORATE TRAINING:")
        print(f"   Corporate penetration: {metrics['marketplace_metrics']['corporate_penetration']:.1%}")
        print(f"   Payment plan adoption: {metrics['marketplace_metrics']['payment_plan_adoption']:.1%}")
        print(f"   Student type distribution:")
        for student_type, count in metrics['student_distribution'].items():
            print(f"     {student_type.title()}: {count:,}")
        
        print(f"\n📚 LEARNING ANALYTICS:")
        print(f"   Course completion rate: {metrics['learning_analytics']['course_completion_rate']:.1%}")
        print(f"   Average satisfaction: {metrics['learning_analytics']['average_satisfaction']:.1f}/5.0")
        print(f"   Certificates earned: {metrics['learning_analytics']['certificates_earned']:,}")
        print(f"   Progress records: {metrics['learning_analytics']['total_progress_records']:,}")
        
        print(f"\n📋 TAX COMPLIANCE:")
        print(f"   Tax documents issued: {metrics['tax_compliance']['tax_documents_issued']:,}")
        print(f"   Instructors with tax docs: {metrics['tax_compliance']['instructors_with_tax_docs']:,}")
        print(f"   Total taxable earnings: ${metrics['tax_compliance']['total_taxable_earnings']:,.2f}")
        
        print(f"\n💳 COURSE PRICING:")
        for course_type, avg_price in metrics['average_course_prices'].items():
            print(f"   {course_type.title()}: ${avg_price:,.2f}")
        
        print(f"\n📁 OUTPUT FILES:")
        print(f"   ✅ instructors.json - Instructor Express accounts")
        print(f"   ✅ students.json - Student customer profiles")
        print(f"   ✅ courses.json - Course catalog with pricing")
        print(f"   ✅ enrollments.json - Student enrollments and payments")
        print(f"   ✅ instructor_transfers.json - Instructor revenue payouts")
        print(f"   ✅ refunds.json - Student refund processing")
        print(f"   ✅ corporate_accounts.json - Corporate training customers")
        print(f"   ✅ student_financing.json - Payment plan agreements")
        print(f"   ✅ student_progress.json - Learning analytics and completion")
        print(f"   ✅ tax_documents.json - 1099-K and international tax forms")
        print(f"   ✅ education_metrics.json - Complete marketplace analytics")
        
        print(f"\n🚀 Ready for education marketplace prototyping!")
        print("="*80)
        print(f"\n⏱️ Total execution time: {execution_time.total_seconds():.1f} seconds")
        
    except Exception as e:
        print(f"\n❌ Error during generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
