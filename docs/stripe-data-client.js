/**
 * Stripe Synthetic Data Client
 * Independent data client for prototype bases to consume personas
 * Version: 1.0.0
 */

class StripeDataClient {
  constructor(options = {}) {
    this.baseUrl = options.baseUrl || 'https://raw.githubusercontent.com/swanson-stripe/synthetic-dataset/main/api/v1';
    this.currentPersona = options.defaultPersona || 'techstyle';
    this.cache = new Map();
    this.subscribers = [];
    this.retryAttempts = options.retryAttempts || 3;
    this.retryDelay = options.retryDelay || 1000;
    
    // Initialize
    this.init();
  }

  async init() {
    // For demo purposes, always use fallback data to ensure immediate loading
    console.log('🚀 Initializing Stripe Synthetic Dataset Demo');
    console.log('📊 Loading comprehensive demo data for all personas...');
    
    this.useFallbackData();
    
    // Debug: Verify data loaded
    const debugMetrics = this.calculateMetrics();
    console.log('✅ Demo data loaded:', {
      currentPersona: this.currentPersona,
      availablePersonas: Object.keys(this.availablePersonas),
      currentDataKeys: Object.keys(this.currentData || {}),
      metricsExample: debugMetrics,
      fullDataMetrics: this.currentData?._fullDatasetMetrics
    });
    
    // Extra debug for metrics calculation
    console.log('🔍 Raw metrics calculation result:', debugMetrics);
    if (debugMetrics && debugMetrics.length > 0) {
      debugMetrics.forEach((metric, i) => {
        console.log(`  ${i}: ${metric.label} = ${metric.value} (raw: ${metric.rawValue})`);
      });
    }
    
    // Optionally try to load from API in background (but don't wait)
    this.loadPersonas().then(() => {
      console.log('🌐 API data available, but using fallback for demo consistency');
    }).catch(() => {
      console.log('📡 API not available, continuing with fallback data (this is expected)');
    });
  }

  // Fallback data for demo when API is not available
  useFallbackData() {
    console.log('Using comprehensive fallback data for demo with all personas');
    
    // Create complete personas matching the real API structure
    this.availablePersonas = {
      techstyle: {
        id: 'techstyle',
        name: 'TechStyle Fashion Retailer',
        business_model: 'ecommerce',
        description: 'E-commerce fashion retailer with global payment processing',
        complexity: 'medium',
        data_scale: 'large',
        stripe_products: ['Payments', 'Checkout', 'Subscriptions', 'Radar'],
        endpoints: {}
      },
      edutech: {
        id: 'edutech', 
        name: 'EduTech Academy',
        business_model: 'education_marketplace',
        description: 'Online education marketplace with instructor payouts',
        complexity: 'high',
        data_scale: 'large',
        stripe_products: ['Payments', 'Connect', 'Subscriptions', 'Tax'],
        endpoints: {}
      },
      propertyflow: {
        id: 'propertyflow',
        name: 'PropertyFlow Property Management',
        business_model: 'property_management',
        description: 'Property management platform with rent collection',
        complexity: 'medium',
        data_scale: 'medium',
        stripe_products: ['Payments', 'Connect', 'ACH', 'Invoicing'],
        endpoints: {}
      },
      fitstream: {
        id: 'fitstream',
        name: 'FitStream Fitness Platform',
        business_model: 'subscription',
        description: 'Subscription fitness platform with trials and engagement',
        complexity: 'medium',
        data_scale: 'large',
        stripe_products: ['Subscriptions', 'Payments', 'Billing', 'Revenue Recognition'],
        endpoints: {}
      },
      creatorhub: {
        id: 'creatorhub',
        name: 'CreatorHub Content Platform',
        business_model: 'creator_economy',
        description: 'Content monetization platform with creator payouts',
        complexity: 'high',
        data_scale: 'large',
        stripe_products: ['Connect', 'Subscriptions', 'Payments', 'Identity'],
        endpoints: {}
      },
      givehope: {
        id: 'givehope',
        name: 'GiveHope Non-Profit Platform',
        business_model: 'nonprofit',
        description: 'Non-profit donation platform with campaigns and recurring donors',
        complexity: 'medium',
        data_scale: 'large',
        stripe_products: ['Payments', 'Checkout', 'Tax', 'Sigma'],
        endpoints: {}
      },
      medsupply: {
        id: 'medsupply',
        name: 'MedSupply Pro B2B Platform',
        business_model: 'b2b_wholesale',
        description: 'B2B medical equipment wholesaler with net terms',
        complexity: 'high',
        data_scale: 'large',
        stripe_products: ['Payments', 'Invoicing', 'Treasury', 'Capital'],
        endpoints: {}
      },
      cloudflow: {
        id: 'cloudflow',
        name: 'CloudFlow SaaS Platform',
        business_model: 'saas',
        description: 'B2B SaaS platform with subscription management',
        complexity: 'high',
        data_scale: 'large',
        stripe_products: ['Subscriptions', 'Billing', 'Revenue Recognition', 'Tax'],
        endpoints: {}
      },
      localbites: {
        id: 'localbites',
        name: 'LocalBites Food Delivery',
        business_model: 'marketplace',
        description: 'Food delivery marketplace with restaurant and driver management',
        complexity: 'high',
        data_scale: 'very_large',
        stripe_products: ['Connect', 'Payments', 'Issuing', 'Terminal'],
        endpoints: {}
      }
    };

    // Support lifecycle stages
    this.lifecycleStages = {
      early: { name: 'Early Stage', description: 'Months 1-8: Startup phase' },
      growth: { name: 'Growth Stage', description: 'Months 9-16: Expansion phase' },
      mature: { name: 'Mature Stage', description: 'Months 17-24: Established business' }
    };

    this.currentStage = 'growth'; // Default stage
    this.currentData = this.generateFallbackData(this.currentPersona, this.currentStage);
    this.notifySubscribers(this.currentData, this.currentPersona);
  }

  // Helper methods for generating realistic Stripe data
  generateId() {
    return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
  }
  
  randomStatus(statuses, weights) {
    const random = Math.random();
    let sum = 0;
    for (let i = 0; i < weights.length; i++) {
      sum += weights[i];
      if (random <= sum) return statuses[i];
    }
    return statuses[0];
  }
  
  randomPaymentMethod() {
    const methods = [
      { type: 'card', card: { brand: 'visa', last4: Math.floor(Math.random() * 9999).toString().padStart(4, '0') } },
      { type: 'card', card: { brand: 'mastercard', last4: Math.floor(Math.random() * 9999).toString().padStart(4, '0') } },
      { type: 'card', card: { brand: 'amex', last4: Math.floor(Math.random() * 9999).toString().padStart(4, '0') } },
      { type: 'ach_debit', ach_debit: { bank_name: 'Chase', last4: Math.floor(Math.random() * 9999).toString().padStart(4, '0') } },
      { type: 'sepa_debit', sepa_debit: { bank_code: 'DEUTDEFF', last4: Math.floor(Math.random() * 9999).toString().padStart(4, '0') } }
    ];
    return methods[Math.floor(Math.random() * methods.length)];
  }
  
  generateCustomerName() {
    const firstNames = ['John', 'Jane', 'Mike', 'Sarah', 'David', 'Emily', 'Chris', 'Jessica', 'Ryan', 'Amanda'];
    const lastNames = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez'];
    return `${firstNames[Math.floor(Math.random() * firstNames.length)]} ${lastNames[Math.floor(Math.random() * lastNames.length)]}`;
  }
  
  generateProductName(category) {
    const products = {
      fashion: ['Premium Cotton T-Shirt', 'Designer Jeans', 'Leather Jacket', 'Running Shoes', 'Winter Coat'],
      education: ['Advanced Mathematics Course', 'Python Programming', 'Digital Marketing', 'Data Science Bootcamp', 'Creative Writing'],
      fitness: ['Premium Membership', 'Personal Training', 'Nutrition Plan', 'Yoga Classes', 'CrossFit Program'],
      property: ['Monthly Rent', 'Security Deposit', 'Maintenance Fee', 'Parking Spot', 'Storage Unit'],
      creator: ['Digital Art Commission', 'Video Tutorial', 'Stock Photo Pack', 'Music Track License', 'Design Template'],
      nonprofit: ['General Donation', 'Education Fund', 'Emergency Relief', 'Healthcare Support', 'Environmental Initiative'],
      b2b: ['Medical Equipment', 'Surgical Supplies', 'Diagnostic Tools', 'Safety Equipment', 'Laboratory Supplies'],
      saas: ['Basic Plan', 'Professional Plan', 'Enterprise Plan', 'API Access', 'Premium Support'],
      marketplace: ['Food Delivery', 'Restaurant Commission', 'Driver Earnings', 'Service Fee', 'Delivery Fee']
    };
    const categoryProducts = products[category] || products.fashion;
    return categoryProducts[Math.floor(Math.random() * categoryProducts.length)];
  }

  // Generate realistic fallback data that reflects full synthetic dataset scale
  generateFallbackData(personaId, stage = 'growth') {
    // Scale data based on business stage
    const stageMultipliers = {
      early: 0.3,   // 30% of growth stage
      growth: 1.0,  // Base scale
      mature: 2.5   // 250% of growth stage
    };
    
    const stageMultiplier = stageMultipliers[stage] || 1.0;
    const baseAmount = Math.floor((Math.floor(Math.random() * 50000) + 25000) * stageMultiplier);
    
    switch (personaId) {
      case 'techstyle':
        // TechStyle: E-commerce with subscriptions and one-time payments
        return {
          payments: Array.from({length: 50}, (_, i) => ({
            id: `pi_${this.generateId()}`,
            amount: Math.floor(Math.random() * 25000) + 1500,
            currency: ['usd', 'eur', 'gbp'][Math.floor(Math.random() * 3)],
            status: this.randomStatus(['succeeded', 'failed', 'requires_action'], [0.95, 0.03, 0.02]),
            customer: `cus_${this.generateId()}`,
            created: Date.now() - Math.random() * 86400000 * 30,
            payment_method: this.randomPaymentMethod(),
            metadata: {
              order_id: `order_${this.generateId()}`,
              product_category: ['apparel', 'accessories', 'footwear', 'activewear'][Math.floor(Math.random() * 4)],
              discount_code: Math.random() > 0.7 ? ['SAVE20', 'WELCOME10', 'FASHION15'][Math.floor(Math.random() * 3)] : null,
              shipping_method: ['standard', 'express', 'overnight'][Math.floor(Math.random() * 3)],
              gift_message: Math.random() > 0.9 ? 'Happy Birthday!' : null
            },
            description: `TechStyle Fashion Purchase`,
            receipt_email: `customer${i}@example.com`
          })),
          
          customers: Array.from({length: 30}, (_, i) => ({
            id: `cus_${this.generateId()}`,
            email: `customer${i}@example.com`,
            name: this.generateCustomerName(),
            created: Date.now() - Math.random() * 86400000 * 365,
            metadata: {
              total_spend: Math.floor(Math.random() * 500000) + 5000,
              lifetime_orders: Math.floor(Math.random() * 50) + 1,
              preferred_size: ['XS', 'S', 'M', 'L', 'XL'][Math.floor(Math.random() * 5)],
              style_preference: ['casual', 'formal', 'athletic', 'trendy'][Math.floor(Math.random() * 4)],
              acquisition_channel: ['organic', 'social', 'email', 'paid_ads'][Math.floor(Math.random() * 4)],
              vip_tier: Math.random() > 0.8 ? ['silver', 'gold', 'platinum'][Math.floor(Math.random() * 3)] : null
            },
            address: {
              country: ['US', 'CA', 'GB', 'AU', 'DE'][Math.floor(Math.random() * 5)],
              state: 'CA',
              city: 'San Francisco'
            }
          })),
          
          products: Array.from({length: 20}, (_, i) => ({
            id: `prod_${this.generateId()}`,
            name: this.generateProductName('fashion'),
            description: `Premium fashion item from TechStyle collection`,
            active: Math.random() > 0.1,
            metadata: {
              category: ['apparel', 'accessories', 'footwear'][Math.floor(Math.random() * 3)],
              brand: ['TechStyle', 'Urban Elite', 'Style Pro'][Math.floor(Math.random() * 3)],
              season: ['spring', 'summer', 'fall', 'winter'][Math.floor(Math.random() * 4)],
              material: ['cotton', 'polyester', 'wool', 'silk'][Math.floor(Math.random() * 4)]
            },
            images: [`https://example.com/products/img_${i}.jpg`],
            created: Date.now() - Math.random() * 86400000 * 180
          })),
          
          subscriptions: Array.from({length: 15}, (_, i) => ({
            id: `sub_${this.generateId()}`,
            customer: `cus_${this.generateId()}`,
            status: this.randomStatus(['active', 'canceled', 'past_due'], [0.85, 0.10, 0.05]),
            current_period_start: Date.now() - Math.random() * 86400000 * 30,
            current_period_end: Date.now() + Math.random() * 86400000 * 30,
            created: Date.now() - Math.random() * 86400000 * 180,
            metadata: {
              plan_name: ['Style Box Monthly', 'Fashion Weekly', 'Trend Quarterly'][Math.floor(Math.random() * 3)],
              box_size: ['small', 'medium', 'large'][Math.floor(Math.random() * 3)],
              style_profile: ['casual', 'professional', 'trendy'][Math.floor(Math.random() * 3)]
            }
          })),
          
          transfers: Array.from({length: 10}, (_, i) => ({
            id: `tr_${this.generateId()}`,
            amount: Math.floor(Math.random() * 100000) + 5000,
            currency: 'usd',
            created: Date.now() - Math.random() * 86400000 * 7,
            description: 'TechStyle supplier payment',
            metadata: {
              supplier_id: `supplier_${Math.floor(Math.random() * 5)}`,
              payment_type: 'supplier_payment',
              invoice_id: `inv_${this.generateId()}`
            }
          })),
          
          balances: [{
            available: [{amount: Math.floor(Math.random() * 10000000) + 100000, currency: 'usd'}],
            pending: [{amount: Math.floor(Math.random() * 500000), currency: 'usd'}],
            connect_reserved: [{amount: Math.floor(Math.random() * 50000), currency: 'usd'}]
          }],
          // Full dataset metrics (not just the 50 sample payments)
          _fullDatasetMetrics: {
            totalPayments: Math.floor(149847 * stageMultiplier),
            totalCustomers: Math.floor(74892 * stageMultiplier),
            totalRevenue: Math.floor(18473628900 * stageMultiplier), // $184.7M in cents
            successfulPayments: Math.floor(146923 * stageMultiplier),
            stage: stage
          },
          summary: {
            revenue_metrics: {
              total_revenue: 18500000000, // Full dataset revenue
              current_mrr: baseAmount
            }
          }
        };
        
      case 'edutech':
        // EduTech: Education marketplace with instructor payouts
        return {
          payments: Array.from({length: 50}, (_, i) => ({
            id: `pi_${this.generateId()}`,
            amount: Math.floor(Math.random() * 50000) + 5000, // $50-$500 courses
            currency: 'usd',
            status: this.randomStatus(['succeeded', 'failed', 'requires_action'], [0.97, 0.02, 0.01]),
            customer: `cus_${this.generateId()}`,
            created: Date.now() - Math.random() * 86400000 * 60,
            payment_method: this.randomPaymentMethod(),
            metadata: {
              course_id: `course_${this.generateId()}`,
              instructor_id: `acct_${this.generateId()}`,
              enrollment_type: ['individual', 'corporate', 'bulk'][Math.floor(Math.random() * 3)],
              course_category: ['programming', 'business', 'design', 'marketing', 'data_science'][Math.floor(Math.random() * 5)],
              completion_certificate: Math.random() > 0.3,
              payment_plan: Math.random() > 0.8 ? 'installment' : 'full'
            },
            description: 'Course enrollment payment',
            application_fee_amount: Math.floor(Math.random() * 5000) + 500 // Platform commission
          })),
          
          customers: Array.from({length: 40}, (_, i) => ({
            id: `cus_${this.generateId()}`,
            email: `student${i}@university.edu`,
            name: this.generateCustomerName(),
            created: Date.now() - Math.random() * 86400000 * 365,
            metadata: {
              total_spend: Math.floor(Math.random() * 200000) + 2000,
              courses_completed: Math.floor(Math.random() * 20),
              student_level: ['beginner', 'intermediate', 'advanced'][Math.floor(Math.random() * 3)],
              learning_goals: ['career_change', 'skill_upgrade', 'certification', 'hobby'][Math.floor(Math.random() * 4)],
              referral_source: ['organic', 'social', 'colleague', 'advertisement'][Math.floor(Math.random() * 4)]
            },
            address: {
              country: ['US', 'CA', 'GB', 'AU', 'IN'][Math.floor(Math.random() * 5)]
            }
          })),
          
          connected_accounts: Array.from({length: 25}, (_, i) => ({
            id: `acct_${this.generateId()}`,
            type: 'express',
            business_profile: { 
              name: `Dr. ${this.generateCustomerName()}`,
              url: `https://instructor${i}.edutech.com`
            },
            created: Date.now() - Math.random() * 86400000 * 180,
            metadata: {
              expertise: ['Computer Science', 'Mathematics', 'Physics', 'Chemistry', 'Biology', 'Economics'][Math.floor(Math.random() * 6)],
              rating: (4.0 + Math.random()).toFixed(1),
              total_students: Math.floor(Math.random() * 5000) + 50,
              course_count: Math.floor(Math.random() * 15) + 1,
              teaching_experience: Math.floor(Math.random() * 20) + 1,
              qualification: ['PhD', 'Masters', 'Industry Expert'][Math.floor(Math.random() * 3)]
            },
            capabilities: {
              transfers: 'requested'
            }
          })),
          
          products: Array.from({length: 30}, (_, i) => ({
            id: `prod_${this.generateId()}`,
            name: this.generateProductName('education'),
            description: `Comprehensive online course with certification`,
            active: Math.random() > 0.05,
            metadata: {
              category: ['programming', 'business', 'design', 'marketing', 'data_science'][Math.floor(Math.random() * 5)],
              difficulty: ['beginner', 'intermediate', 'advanced'][Math.floor(Math.random() * 3)],
              duration_hours: Math.floor(Math.random() * 40) + 5,
              instructor_id: `acct_${this.generateId()}`,
              certification: Math.random() > 0.3
            },
            created: Date.now() - Math.random() * 86400000 * 90
          })),
          
          transfers: Array.from({length: 35}, (_, i) => ({
            id: `tr_${this.generateId()}`,
            amount: Math.floor(Math.random() * 40000) + 2000, // Instructor payout (80% of course fee)
            currency: 'usd',
            destination: `acct_${this.generateId()}`,
            created: Date.now() - Math.random() * 86400000 * 30,
            description: 'Instructor course revenue payout',
            metadata: {
              course_id: `course_${this.generateId()}`,
              payout_period: 'weekly',
              student_enrollments: Math.floor(Math.random() * 50) + 1
            }
          })),
          
          invoices: Array.from({length: 20}, (_, i) => ({
            id: `in_${this.generateId()}`,
            customer: `cus_${this.generateId()}`,
            amount_due: Math.floor(Math.random() * 100000) + 10000, // Corporate training
            currency: 'usd',
            status: this.randomStatus(['paid', 'open', 'draft'], [0.8, 0.15, 0.05]),
            created: Date.now() - Math.random() * 86400000 * 90,
            metadata: {
              invoice_type: 'corporate_training',
              employee_count: Math.floor(Math.random() * 100) + 5,
              training_program: ['leadership', 'technical', 'compliance'][Math.floor(Math.random() * 3)]
            }
          })),
          
          balances: [{
            available: [{amount: Math.floor(Math.random() * 5000000) + 500000, currency: 'usd'}],
            pending: [{amount: Math.floor(Math.random() * 200000), currency: 'usd'}]
          }],
          // Full dataset metrics
          _fullDatasetMetrics: {
            totalStudents: Math.floor(72847 * stageMultiplier),
            totalInstructors: Math.floor(73 * stageMultiplier),
            totalCourses: Math.floor(217 * stageMultiplier),
            totalEnrollments: Math.floor(11934 * stageMultiplier),
            totalRevenue: Math.floor(20087642300 * stageMultiplier), // $200.9M in cents
            stage: stage
          }
        };
        
      case 'propertyflow':
        return {
          payments: Array.from({length: 60}, (_, i) => ({
            id: `pi_${this.generateId()}`,
            amount: Math.floor(Math.random() * 400000) + 100000, // $1K-$4K rent
            currency: 'usd',
            status: this.randomStatus(['succeeded', 'failed', 'requires_action'], [0.95, 0.03, 0.02]),
            customer: `cus_${this.generateId()}`,
            created: Date.now() - Math.random() * 86400000 * 90,
            payment_method: this.randomPaymentMethod(),
            metadata: {
              property_id: `prop_${this.generateId()}`,
              landlord_id: `acct_${this.generateId()}`,
              payment_type: ['rent', 'security_deposit', 'maintenance_fee', 'late_fee'][Math.floor(Math.random() * 4)],
              property_type: ['apartment', 'house', 'condo', 'townhouse'][Math.floor(Math.random() * 4)],
              lease_term: ['month_to_month', '6_month', '12_month', '24_month'][Math.floor(Math.random() * 4)],
              unit_number: Math.random() > 0.5 ? `Unit ${Math.floor(Math.random() * 50) + 1}` : null
            },
            description: 'Property rental payment',
            application_fee_amount: Math.floor(Math.random() * 10000) + 1000 // Platform fee
          })),
          
          customers: Array.from({length: 45}, (_, i) => ({
            id: `cus_${this.generateId()}`,
            email: `tenant${i}@example.com`,
            name: this.generateCustomerName(),
            created: Date.now() - Math.random() * 86400000 * 730, // Up to 2 years
            metadata: {
              total_spend: Math.floor(Math.random() * 1000000) + 50000,
              lease_start_date: new Date(Date.now() - Math.random() * 86400000 * 365).toISOString(),
              tenant_type: ['individual', 'family', 'corporate', 'student'][Math.floor(Math.random() * 4)],
              credit_score: Math.floor(Math.random() * 300) + 500,
              pets: Math.random() > 0.6 ? ['cat', 'dog', 'none'][Math.floor(Math.random() * 3)] : 'none',
              lease_status: ['active', 'ending_soon', 'month_to_month'][Math.floor(Math.random() * 3)]
            },
            address: {
              country: 'US',
              state: ['CA', 'NY', 'TX', 'FL'][Math.floor(Math.random() * 4)]
            }
          })),
          
          connected_accounts: Array.from({length: 20}, (_, i) => ({
            id: `acct_${this.generateId()}`,
            type: 'express',
            business_profile: { 
              name: `${this.generateCustomerName()} Properties LLC`,
              url: `https://landlord${i}.propertyflow.com`
            },
            created: Date.now() - Math.random() * 86400000 * 365,
            metadata: {
              account_type: 'landlord',
              properties_count: Math.floor(Math.random() * 20) + 1,
              property_types: ['residential', 'commercial', 'mixed'][Math.floor(Math.random() * 3)],
              years_experience: Math.floor(Math.random() * 30) + 1,
              portfolio_value: Math.floor(Math.random() * 50000000) + 1000000
            },
            capabilities: {
              transfers: 'requested'
            }
          })),
          
          products: Array.from({length: 25}, (_, i) => ({
            id: `prod_${this.generateId()}`,
            name: this.generateProductName('property'),
            description: `Rental property unit`,
            active: Math.random() > 0.1,
            metadata: {
              property_type: ['apartment', 'house', 'condo', 'townhouse'][Math.floor(Math.random() * 4)],
              bedrooms: Math.floor(Math.random() * 5) + 1,
              bathrooms: Math.floor(Math.random() * 3) + 1,
              square_feet: Math.floor(Math.random() * 2000) + 500,
              amenities: ['pool', 'gym', 'parking', 'laundry', 'pets_allowed'][Math.floor(Math.random() * 5)],
              landlord_id: `acct_${this.generateId()}`
            },
            created: Date.now() - Math.random() * 86400000 * 180
          })),
          
          transfers: Array.from({length: 40}, (_, i) => ({
            id: `tr_${this.generateId()}`,
            amount: Math.floor(Math.random() * 350000) + 80000, // Landlord payout (85% of rent)
            currency: 'usd',
            destination: `acct_${this.generateId()}`,
            created: Date.now() - Math.random() * 86400000 * 30,
            description: 'Landlord rental income payout',
            metadata: {
              property_id: `prop_${this.generateId()}`,
              payout_period: 'monthly',
              rent_collected: Math.floor(Math.random() * 400000) + 100000
            }
          })),
          
          invoices: Array.from({length: 15}, (_, i) => ({
            id: `in_${this.generateId()}`,
            customer: `cus_${this.generateId()}`,
            amount_due: Math.floor(Math.random() * 300000) + 100000,
            currency: 'usd',
            status: this.randomStatus(['paid', 'open', 'overdue'], [0.85, 0.10, 0.05]),
            created: Date.now() - Math.random() * 86400000 * 60,
            metadata: {
              invoice_type: 'monthly_rent',
              property_id: `prop_${this.generateId()}`,
              due_date: new Date(Date.now() + Math.random() * 86400000 * 30).toISOString()
            }
          })),
          
          balances: [{
            available: [{amount: Math.floor(Math.random() * 20000000) + 2000000, currency: 'usd'}],
            pending: [{amount: Math.floor(Math.random() * 1000000), currency: 'usd'}]
          }],
          // Full dataset metrics - PropertyFlow: 25K properties, $2.8B volume
          _fullDatasetMetrics: {
            totalProperties: Math.floor(24789 * stageMultiplier),
            totalLandlords: Math.floor(8463 * stageMultiplier),
            totalPayments: Math.floor(348521 * stageMultiplier),
            totalVolume: Math.floor(279842719600 * stageMultiplier), // $2.798B in cents
            successfulPayments: Math.floor(341067 * stageMultiplier),
            stage: stage
          }
        };

      case 'fitstream':
        return {
          subscriptions: Array.from({length: 35}, (_, i) => ({
            id: `sub_demo_${i.toString().padStart(6, '0')}`,
            plan: ['Basic', 'Unlimited', 'Family'][Math.floor(Math.random() * 3)],
            status: Math.random() > 0.1 ? 'active' : 'canceled',
            current_period_start: Date.now() - Math.random() * 86400000 * 30,
            mrr: [999, 1999, 3999][Math.floor(Math.random() * 3)]
          })),
          customers: Array.from({length: 50}, (_, i) => ({
            id: `cus_demo_${i.toString().padStart(6, '0')}`,
            email: `member${i}@fitstream.com`,
            plan: ['Basic', 'Unlimited', 'Family'][Math.floor(Math.random() * 3)],
            engagement_score: Math.floor(Math.random() * 100),
            ltv: Math.floor(Math.random() * 50000) + 5000,
            status: 'active'
          })),
          summary: {
            revenue_metrics: {
              current_mrr: baseAmount * 2,
              total_revenue: baseAmount * 24
            }
          },
          // Full dataset metrics - FitStream: 85K subscribers, $98M ARR
          _fullDatasetMetrics: {
            totalSubscribers: Math.floor(84672 * stageMultiplier),
            totalCustomers: Math.floor(119483 * stageMultiplier),
            totalMRR: Math.floor(816847200 * stageMultiplier), // $8.168M MRR in cents
            totalARR: Math.floor(9802166400 * stageMultiplier), // $98.02M ARR in cents
            activeSubscriptions: Math.floor(77854 * stageMultiplier),
            stage: stage
          }
        };

      case 'creatorhub':
        return {
          creators: Array.from({length: 30}, (_, i) => ({
            id: `acct_demo_${i.toString().padStart(6, '0')}`,
            business_profile: { name: `Creator ${i + 1}` },
            category: ['Art', 'Music', 'Video', 'Writing', 'Photography'][Math.floor(Math.random() * 5)],
            followers: Math.floor(Math.random() * 50000) + 1000,
            revenue: Math.floor(Math.random() * 100000) + 5000,
            content_count: Math.floor(Math.random() * 50) + 10
          })),
          fans: Array.from({length: 80}, (_, i) => ({
            id: `cus_demo_${i.toString().padStart(6, '0')}`,
            email: `fan${i}@example.com`,
            total_spent: Math.floor(Math.random() * 10000) + 500,
            favorite_creators: Math.floor(Math.random() * 5) + 1
          })),
          content_sales: Array.from({length: 60}, (_, i) => ({
            id: `sale_demo_${i.toString().padStart(6, '0')}`,
            amount: Math.floor(Math.random() * 5000) + 500,
            content_title: `Content Item ${i + 1}`,
            creator: `Creator ${Math.floor(Math.random() * 30) + 1}`,
            fan: `Fan ${Math.floor(Math.random() * 80) + 1}`
          })),
          // Full dataset metrics - CreatorHub: 35K creators, $67M volume
          _fullDatasetMetrics: {
            totalCreators: Math.floor(34827 * stageMultiplier),
            totalFans: Math.floor(849642 * stageMultiplier),
            totalSales: Math.floor(418739 * stageMultiplier),
            totalVolume: Math.floor(6691847300 * stageMultiplier), // $66.92M in cents
            topCreators: Math.floor(2783 * stageMultiplier),
            stage: stage
          }
        };

      case 'givehope':
        // GiveHope: 15K donors, $17.5M total raised, 55 campaigns
        return {
          donors: Array.from({length: 25}, (_, i) => ({
            id: `cus_demo_${i.toString().padStart(6, '0')}`,
            email: `donor${i}@example.com`,
            total_donated: Math.floor(Math.random() * 10000) + 500,
            donor_type: ['individual', 'corporate', 'foundation'][Math.floor(Math.random() * 3)],
            created: Date.now() - Math.random() * 86400000 * 365
          })),
          campaigns: Array.from({length: 15}, (_, i) => ({
            id: `camp_demo_${i.toString().padStart(6, '0')}`,
            name: `Campaign ${i + 1}`,
            cause: ['Disaster Relief', 'Education', 'Healthcare', 'Environment'][Math.floor(Math.random() * 4)],
            goal: Math.floor(Math.random() * 500000) + 50000,
            raised: Math.floor(Math.random() * 400000) + 20000,
            status: 'active'
          })),
          donations: Array.from({length: 30}, (_, i) => ({
            id: `don_demo_${i.toString().padStart(6, '0')}`,
            amount: Math.floor(Math.random() * 50000) + 2500,
            donor: `Donor ${i + 1}`,
            campaign: `Campaign ${Math.floor(Math.random() * 15) + 1}`,
            recurring: Math.random() > 0.7
          })),
          // Full dataset metrics
          _fullDatasetMetrics: {
            totalDonors: Math.floor(14893 * stageMultiplier),
            totalCampaigns: Math.floor(54 * stageMultiplier),
            totalRaised: Math.floor(1748623750 * stageMultiplier), // $17.49M in cents
            totalDonations: Math.floor(124672 * stageMultiplier),
            recurringDonors: Math.floor(1487 * stageMultiplier),
            stage: stage
          }
        };

      case 'medsupply':
        return {
          clients: Array.from({length: 25}, (_, i) => ({
            id: `cli_demo_${i.toString().padStart(6, '0')}`,
            name: `Medical Facility ${i + 1}`,
            type: ['Hospital', 'Clinic', 'Laboratory', 'Pharmacy'][Math.floor(Math.random() * 4)],
            credit_limit: [25000, 100000, 500000][Math.floor(Math.random() * 3)],
            outstanding_balance: Math.floor(Math.random() * 50000)
          })),
          purchase_orders: Array.from({length: 30}, (_, i) => ({
            id: `po_demo_${i.toString().padStart(6, '0')}`,
            client: `Client ${Math.floor(Math.random() * 25) + 1}`,
            amount: Math.floor(Math.random() * 200000) + 50000,
            items: Math.floor(Math.random() * 20) + 5,
            status: ['pending', 'approved', 'fulfilled'][Math.floor(Math.random() * 3)]
          })),
          invoices: Array.from({length: 35}, (_, i) => ({
            id: `inv_demo_${i.toString().padStart(6, '0')}`,
            client: `Client ${Math.floor(Math.random() * 25) + 1}`,
            amount: Math.floor(Math.random() * 200000) + 50000,
            due_date: Date.now() + Math.random() * 86400000 * 90,
            status: Math.random() > 0.2 ? 'paid' : 'outstanding'
          })),
          // Full dataset metrics - MedSupply: 2.5K clients, $125M volume
          _fullDatasetMetrics: {
            totalClients: Math.floor(2487 * stageMultiplier),
            totalOrders: Math.floor(14923 * stageMultiplier),
            totalVolume: Math.floor(12487364200 * stageMultiplier), // $124.87M in cents
            totalInvoices: Math.floor(17894 * stageMultiplier),
            paidInvoices: Math.floor(16429 * stageMultiplier),
            stage: stage
          }
        };

      case 'cloudflow':
        return {
          customers: Array.from({length: 40}, (_, i) => ({
            id: `cus_demo_${i.toString().padStart(6, '0')}`,
            company: `Company ${i + 1}`,
            plan: ['Starter', 'Professional', 'Enterprise'][Math.floor(Math.random() * 3)],
            mrr: [99, 299, 999][Math.floor(Math.random() * 3)],
            employees: Math.floor(Math.random() * 1000) + 10
          })),
          subscriptions: Array.from({length: 38}, (_, i) => ({
            id: `sub_demo_${i.toString().padStart(6, '0')}`,
            customer: `Company ${Math.floor(Math.random() * 40) + 1}`,
            plan: ['Starter', 'Professional', 'Enterprise'][Math.floor(Math.random() * 3)],
            status: Math.random() > 0.1 ? 'active' : 'canceled',
            current_period_start: Date.now() - Math.random() * 86400000 * 30
          })),
          invoices: Array.from({length: 50}, (_, i) => ({
            id: `in_demo_${i.toString().padStart(6, '0')}`,
            customer: `Company ${Math.floor(Math.random() * 40) + 1}`,
            amount: [9900, 29900, 99900][Math.floor(Math.random() * 3)],
            status: Math.random() > 0.05 ? 'paid' : 'open',
            due_date: Date.now() + Math.random() * 86400000 * 30
          })),
          // Full dataset metrics - CloudFlow: 50K customers, $240M ARR
          _fullDatasetMetrics: {
            totalCustomers: Math.floor(49821 * stageMultiplier),
            totalSubscriptions: Math.floor(46739 * stageMultiplier),
            totalMRR: Math.floor(1998473600 * stageMultiplier), // $19.98M MRR in cents
            totalARR: Math.floor(23981683200 * stageMultiplier), // $239.82M ARR in cents
            activeSubscriptions: Math.floor(43892 * stageMultiplier),
            stage: stage
          }
        };

      case 'localbites':
        return {
          orders: Array.from({length: 70}, (_, i) => ({
            id: `ord_demo_${i.toString().padStart(6, '0')}`,
            restaurant: `Restaurant ${Math.floor(Math.random() * 20) + 1}`,
            driver: `Driver ${Math.floor(Math.random() * 15) + 1}`,
            customer: `Customer ${Math.floor(Math.random() * 100) + 1}`,
            total: Math.floor(Math.random() * 8000) + 1500,
            delivery_fee: Math.floor(Math.random() * 500) + 200,
            status: ['delivered', 'in_transit', 'preparing'][Math.floor(Math.random() * 3)]
          })),
          connected_accounts: Array.from({length: 35}, (_, i) => ({
            id: `acct_demo_${i.toString().padStart(6, '0')}`,
            business_profile: { 
              name: i < 20 ? `Restaurant ${i + 1}` : `Driver ${i - 19}`
            },
            type: i < 20 ? 'restaurant' : 'driver',
            total_payouts: Math.floor(Math.random() * 50000) + 5000,
            rating: (4.0 + Math.random()).toFixed(1)
          })),
          payments: Array.from({length: 65}, (_, i) => ({
            id: `pi_demo_${i.toString().padStart(6, '0')}`,
            amount: Math.floor(Math.random() * 8000) + 1500,
            application_fee: Math.floor(Math.random() * 800) + 150,
            status: Math.random() > 0.03 ? 'succeeded' : 'failed',
            customer: `Customer ${Math.floor(Math.random() * 100) + 1}`
          })),
          // Full dataset metrics - LocalBites: 600K orders, $95M volume
          _fullDatasetMetrics: {
            totalOrders: Math.floor(598473 * stageMultiplier),
            totalRestaurants: Math.floor(8467 * stageMultiplier),
            totalDrivers: Math.floor(11934 * stageMultiplier),
            totalVolume: Math.floor(9487364700 * stageMultiplier), // $94.87M in cents
            totalPayments: Math.floor(583621 * stageMultiplier),
            stage: stage
          }
        };
        
      default:
        return {
          data: Array.from({length: 10}, (_, i) => ({
            id: i,
            value: Math.random() * 1000,
            status: 'active'
          }))
        };
    }
  }

  // Load available personas
  async loadPersonas() {
    try {
      const response = await this.fetchWithRetry(`${this.baseUrl}/personas.json`);
      this.availablePersonas = response.personas;
      return this.availablePersonas;
    } catch (error) {
      console.error('Failed to load personas:', error);
      throw error;
    }
  }

  // Load data for a specific persona
  async loadPersona(personaId) {
    if (!this.availablePersonas || !this.availablePersonas[personaId]) {
      throw new Error(`Persona '${personaId}' not found. Available: ${Object.keys(this.availablePersonas || {}).join(', ')}`);
    }

    const persona = this.availablePersonas[personaId];
    const endpoints = persona.endpoints?.combined || persona.endpoints;
    
    try {
      // Load main data endpoints
      const dataPromises = Object.entries(endpoints).map(async ([key, endpoint]) => {
        try {
        const url = `${this.baseUrl}${endpoint}`;
        const data = await this.fetchWithRetry(url);
        return [key, data];
        } catch (error) {
          console.warn(`Failed to load ${key} for ${personaId}:`, error.message);
          return [key, []]; // Return empty array as fallback
        }
      });

      const results = await Promise.all(dataPromises);
      const personaData = Object.fromEntries(results);

      // Cache the data
      this.cache.set(personaId, personaData);
      this.currentPersona = personaId;
      this.currentData = personaData;

      // Notify subscribers
      this.notifySubscribers(personaData, personaId);
      
      return personaData;
    } catch (error) {
      console.error(`Failed to load persona '${personaId}':`, error);
      throw error;
    }
  }

  // Update business stage and regenerate data
  updateStage(stage) {
    this.currentStage = stage;
    console.log(`🔄 Updating stage to ${stage} and regenerating data`);
    
    // Regenerate data for current persona with new stage
    this.currentData = this.generateFallbackData(this.currentPersona, stage);
    this.cache.set(`${this.currentPersona}_${stage}`, this.currentData);
    this.notifySubscribers(this.currentData, this.currentPersona);
    return this.currentData;
  }

  // Switch to a different persona
  async switchPersona(personaId) {
    if (personaId === this.currentPersona) {
      return this.currentData;
    }

    // Check cache first (including stage)
    const cacheKey = `${personaId}_${this.currentStage || 'growth'}`;
    if (this.cache.has(cacheKey)) {
      this.currentPersona = personaId;
      this.currentData = this.cache.get(cacheKey);
      this.notifySubscribers(this.currentData, personaId);
      return this.currentData;
    }

    // For demo consistency, always use fallback data with full dataset metrics
    console.log(`🔄 Switching to ${personaId} using fallback data for demo consistency`);
    this.currentPersona = personaId;
    this.currentStage = this.currentStage || 'growth'; // Use current stage or default
    this.currentData = this.generateFallbackData(personaId, this.currentStage);
    this.cache.set(`${personaId}_${this.currentStage}`, this.currentData);
    this.notifySubscribers(this.currentData, personaId);
    return this.currentData;
  }

  // Get current persona info
  getCurrentPersona() {
    return {
      id: this.currentPersona,
      info: this.availablePersonas?.[this.currentPersona],
      data: this.currentData
    };
  }

  // Get list of available personas
  getAvailablePersonas() {
    return this.availablePersonas;
  }

  // Subscribe to data changes
  subscribe(callback) {
    this.subscribers.push(callback);
    
    // Return unsubscribe function
    return () => {
      const index = this.subscribers.indexOf(callback);
      if (index > -1) {
        this.subscribers.splice(index, 1);
      }
    };
  }

  // Notify all subscribers of data changes
  notifySubscribers(data, personaId) {
    this.subscribers.forEach(callback => {
      try {
        callback(data, personaId);
      } catch (error) {
        console.error('Subscriber callback error:', error);
      }
    });
  }

  // Get specific data type from current persona
  getData(type) {
    if (!this.currentData) {
      throw new Error('No persona data loaded. Call loadPersona() first.');
    }
    return this.currentData[type];
  }

  // Get metrics for current persona
  getMetrics() {
    return this.getData('metrics');
  }

  // Get summary for current persona
  getSummary() {
    return this.getData('summary');
  }

  // Fetch with retry logic
  async fetchWithRetry(url, attempt = 1) {
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      if (attempt < this.retryAttempts) {
        console.warn(`Fetch attempt ${attempt} failed, retrying in ${this.retryDelay}ms:`, error.message);
        await new Promise(resolve => setTimeout(resolve, this.retryDelay));
        return this.fetchWithRetry(url, attempt + 1);
      }
      throw error;
    }
  }

  // Calculate business-specific metrics
  calculateMetrics(personaId = this.currentPersona) {
    const data = this.currentData;
    console.log(`🧮 calculateMetrics called for persona: ${personaId}, data available:`, !!data);
    
    if (!data) {
      console.warn('❌ No data available for metrics calculation');
      return [];
    }

    console.log(`🧮 Calculating metrics for ${personaId}, data keys:`, Object.keys(data));

    switch (personaId) {
      case 'techstyle':
        return this.calculateEcommerceMetrics(data);
      case 'edutech':
        return this.calculateEducationMetrics(data);
      case 'propertyflow':
        return this.calculatePropertyMetrics(data);
      case 'fitstream':
        return this.calculateFitnessMetrics(data);
      case 'creatorhub':
        return this.calculateCreatorMetrics(data);
      case 'givehope':
        return this.calculateNonprofitMetrics(data);
      case 'medsupply':
        return this.calculateB2BMetrics(data);
      case 'cloudflow':
        return this.calculateSaaSMetrics(data);
      case 'localbites':
        return this.calculateMarketplaceMetrics(data);
      default:
        return this.calculateGenericMetrics(data);
    }
  }

  calculateEcommerceMetrics(data) {
    // Use full dataset metrics if available, otherwise calculate from sample
    const fullMetrics = data._fullDatasetMetrics;
    
    if (fullMetrics) {
      const successRate = fullMetrics.successfulPayments / fullMetrics.totalPayments;
      const avgOrder = fullMetrics.totalRevenue / fullMetrics.totalPayments;
      
      return [
        { 
          label: 'Total Revenue', 
          value: this.formatCurrency(fullMetrics.totalRevenue),
          rawValue: fullMetrics.totalRevenue
        },
        { 
          label: 'Success Rate', 
          value: this.formatPercent(successRate),
          rawValue: successRate
        },
        { 
          label: 'Customers', 
          value: fullMetrics.totalCustomers.toLocaleString(),
          rawValue: fullMetrics.totalCustomers
        },
        { 
          label: 'Avg Order', 
          value: this.formatCurrency(avgOrder),
          rawValue: avgOrder
        }
      ];
    }
    
    // Fallback to sample calculation
    const payments = data.payments || [];
    const customers = data.customers || [];
    
    const totalRevenue = payments
      .filter(p => p.status === 'succeeded')
      .reduce((sum, p) => sum + p.amount, 0);
    
    const successRate = payments.length > 0 
      ? payments.filter(p => p.status === 'succeeded').length / payments.length 
      : 0;

    return [
      { 
        label: 'Total Revenue', 
        value: this.formatCurrency(totalRevenue),
        rawValue: totalRevenue
      },
      { 
        label: 'Success Rate', 
        value: this.formatPercent(successRate),
        rawValue: successRate
      },
      { 
        label: 'Customers', 
        value: customers.length.toLocaleString(),
        rawValue: customers.length
      },
      { 
        label: 'Avg Order', 
        value: payments.length > 0 ? this.formatCurrency(totalRevenue / payments.length) : '$0',
        rawValue: payments.length > 0 ? totalRevenue / payments.length : 0
      }
    ];
  }

  calculateEducationMetrics(data) {
    // Use full dataset metrics if available
    const fullMetrics = data._fullDatasetMetrics;
    console.log('🎓 EduTech calculateEducationMetrics called with data:', data);
    console.log('🎓 EduTech fullMetrics:', fullMetrics);
    console.log('🎓 EduTech data._fullDatasetMetrics:', data._fullDatasetMetrics);
    
    if (fullMetrics) {
      return [
        { 
          label: 'Students', 
          value: fullMetrics.totalStudents.toLocaleString(),
          rawValue: fullMetrics.totalStudents
        },
        { 
          label: 'Course Revenue', 
          value: this.formatCurrency(fullMetrics.totalRevenue),
          rawValue: fullMetrics.totalRevenue
        },
        { 
          label: 'Instructors', 
          value: fullMetrics.totalInstructors.toString(),
          rawValue: fullMetrics.totalInstructors
        },
        { 
          label: 'Enrollments', 
          value: fullMetrics.totalEnrollments.toLocaleString(),
          rawValue: fullMetrics.totalEnrollments
        }
      ];
    }
    
    // Fallback to sample calculation
    const instructors = data.instructors || [];
    const students = data.students || [];
    const enrollments = data.enrollments || [];
    
    const totalRevenue = enrollments
      .filter(e => e.status === 'succeeded' || e.paid === true)
      .reduce((sum, e) => sum + (e.amount || e.amount_paid || 0), 0);

    return [
      { 
        label: 'Students', 
        value: students.length.toLocaleString(),
        rawValue: students.length
      },
      { 
        label: 'Course Revenue', 
        value: this.formatCurrency(totalRevenue),
        rawValue: totalRevenue
      },
      { 
        label: 'Instructors', 
        value: instructors.length.toString(),
        rawValue: instructors.length
      },
      { 
        label: 'Enrollments', 
        value: enrollments.length.toLocaleString(),
        rawValue: enrollments.length
      }
    ];
  }

  calculatePropertyMetrics(data) {
    // Use full dataset metrics if available
    const fullMetrics = data._fullDatasetMetrics;
    console.log('🏠 PropertyFlow calculatePropertyMetrics called with data:', data);
    console.log('🏠 PropertyFlow fullMetrics:', fullMetrics);
    
    if (fullMetrics) {
      const successRate = fullMetrics.successfulPayments / fullMetrics.totalPayments;
      
      return [
        { 
          label: 'Properties', 
          value: fullMetrics.totalProperties.toLocaleString(),
          rawValue: fullMetrics.totalProperties
        },
        { 
          label: 'Rent Collected', 
          value: this.formatCurrency(fullMetrics.totalVolume),
          rawValue: fullMetrics.totalVolume
        },
        { 
          label: 'Landlords', 
          value: fullMetrics.totalLandlords.toLocaleString(),
          rawValue: fullMetrics.totalLandlords
        },
        { 
          label: 'Success Rate', 
          value: this.formatPercent(successRate),
          rawValue: successRate
        }
      ];
    }
    
    // Fallback to sample calculation
    const properties = data.properties || [];
    const rentPayments = data.rent_payments || [];
    const landlords = data.landlords || [];
    
    const totalRent = rentPayments
      .filter(p => p.status === 'succeeded')
      .reduce((sum, p) => sum + p.amount, 0);

    return [
      { 
        label: 'Properties', 
        value: properties.length.toLocaleString(),
        rawValue: properties.length
      },
      { 
        label: 'Rent Collected', 
        value: this.formatCurrency(totalRent),
        rawValue: totalRent
      },
      { 
        label: 'Landlords', 
        value: landlords.length.toString(),
        rawValue: landlords.length
      },
      { 
        label: 'Collection Rate', 
        value: '98.3%',
        rawValue: 0.983
      }
    ];
  }

  calculateFitnessMetrics(data) {
    // Use full dataset metrics if available
    const fullMetrics = data._fullDatasetMetrics;
    console.log('💪 FitStream calculateFitnessMetrics called with data:', data);
    console.log('💪 FitStream fullMetrics:', fullMetrics);
    
    if (fullMetrics) {
      const churnRate = (fullMetrics.totalSubscribers - fullMetrics.activeSubscriptions) / fullMetrics.totalSubscribers;
      
      return [
        { 
          label: 'Subscribers', 
          value: fullMetrics.totalCustomers.toLocaleString(),
          rawValue: fullMetrics.totalCustomers
        },
        { 
          label: 'Active Subs', 
          value: fullMetrics.activeSubscriptions.toLocaleString(),
          rawValue: fullMetrics.activeSubscriptions
        },
        { 
          label: 'MRR', 
          value: this.formatCurrency(fullMetrics.totalMRR),
          rawValue: fullMetrics.totalMRR
        },
        { 
          label: 'Annual ARR', 
          value: this.formatCurrency(fullMetrics.totalARR),
          rawValue: fullMetrics.totalARR
        }
      ];
    }
    
    // Fallback to sample calculation
    const subscriptions = data.subscriptions || [];
    const customers = data.customers || [];
    
    const activeSubscriptions = subscriptions.filter(s => s.status === 'active');
    const totalRevenue = (data.summary?.revenue_metrics?.total_revenue || 0);

    return [
      { 
        label: 'Subscribers', 
        value: customers.length.toLocaleString(),
        rawValue: customers.length
      },
      { 
        label: 'Active Subs', 
        value: activeSubscriptions.length.toLocaleString(),
        rawValue: activeSubscriptions.length
      },
      { 
        label: 'MRR', 
        value: this.formatCurrency((data.summary?.revenue_metrics?.current_mrr || 0) * 100),
        rawValue: (data.summary?.revenue_metrics?.current_mrr || 0) * 100
      },
      { 
        label: 'Churn Rate', 
        value: '4.9%',
        rawValue: 0.049
      }
    ];
  }

  calculateCreatorMetrics(data) {
    // Use full dataset metrics if available
    const fullMetrics = data._fullDatasetMetrics;
    console.log('🎨 CreatorHub calculateCreatorMetrics called with data:', data);
    console.log('🎨 CreatorHub fullMetrics:', fullMetrics);
    
    if (fullMetrics) {
      return [
        { 
          label: 'Creators', 
          value: fullMetrics.totalCreators.toLocaleString(),
          rawValue: fullMetrics.totalCreators
        },
        { 
          label: 'Fans', 
          value: fullMetrics.totalFans.toLocaleString(),
          rawValue: fullMetrics.totalFans
        },
        { 
          label: 'GMV', 
          value: this.formatCurrency(fullMetrics.totalVolume),
          rawValue: fullMetrics.totalVolume
        },
        { 
          label: 'Content Sales', 
          value: fullMetrics.totalSales.toLocaleString(),
          rawValue: fullMetrics.totalSales
        }
      ];
    }
    
    // Fallback to sample calculation
    const creators = data.creators || [];
    const fans = data.fans || [];
    const contentSales = data.content_sales || [];
    
    const totalGMV = contentSales.reduce((sum, s) => sum + (s.amount || 0), 0);

    return [
      { 
        label: 'Creators', 
        value: creators.length.toLocaleString(),
        rawValue: creators.length
      },
      { 
        label: 'Fans', 
        value: fans.length.toLocaleString(),
        rawValue: fans.length
      },
      { 
        label: 'GMV', 
        value: this.formatCurrency(totalGMV),
        rawValue: totalGMV
      },
      { 
        label: 'Content Sales', 
        value: contentSales.length.toLocaleString(),
        rawValue: contentSales.length
      }
    ];
  }

  calculateGenericMetrics(data) {
    // Fallback for unknown personas
    const allKeys = Object.keys(data);
    return allKeys.slice(0, 4).map(key => ({
      label: key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()),
      value: Array.isArray(data[key]) ? data[key].length.toLocaleString() : 'N/A',
      rawValue: Array.isArray(data[key]) ? data[key].length : 0
    }));
  }

  calculateNonprofitMetrics(data) {
    // Use full dataset metrics if available
    const fullMetrics = data._fullDatasetMetrics;
    
    if (fullMetrics) {
      return [
        { 
          label: 'Total Donors', 
          value: fullMetrics.totalDonors.toLocaleString(),
          rawValue: fullMetrics.totalDonors
        },
        { 
          label: 'Total Raised', 
          value: this.formatCurrency(fullMetrics.totalRaised),
          rawValue: fullMetrics.totalRaised
        },
        { 
          label: 'Active Campaigns', 
          value: fullMetrics.totalCampaigns.toString(),
          rawValue: fullMetrics.totalCampaigns
        },
        { 
          label: 'Donations', 
          value: fullMetrics.totalDonations.toLocaleString(),
          rawValue: fullMetrics.totalDonations
        }
      ];
    }
    
    // Fallback to sample calculation
    const donors = data.donors || [];
    const campaigns = data.campaigns || [];
    const donations = data.donations || [];
    
    const totalRaised = donations.reduce((sum, d) => sum + (d.amount || 0), 0);
    const activeCampaigns = campaigns.filter(c => c.status === 'active').length;

    return [
      { 
        label: 'Total Donors', 
        value: donors.length.toLocaleString(),
        rawValue: donors.length
      },
      { 
        label: 'Total Raised', 
        value: this.formatCurrency(totalRaised),
        rawValue: totalRaised
      },
      { 
        label: 'Active Campaigns', 
        value: activeCampaigns.toString(),
        rawValue: activeCampaigns
      },
      { 
        label: 'Donations', 
        value: donations.length.toLocaleString(),
        rawValue: donations.length
      }
    ];
  }

  calculateB2BMetrics(data) {
    // Use full dataset metrics if available
    const fullMetrics = data._fullDatasetMetrics;
    
    if (fullMetrics) {
      const collectionRate = fullMetrics.paidInvoices / fullMetrics.totalInvoices;
      
      return [
        { 
          label: 'B2B Clients', 
          value: fullMetrics.totalClients.toLocaleString(),
          rawValue: fullMetrics.totalClients
        },
        { 
          label: 'Purchase Volume', 
          value: this.formatCurrency(fullMetrics.totalVolume),
          rawValue: fullMetrics.totalVolume
        },
        { 
          label: 'Purchase Orders', 
          value: fullMetrics.totalOrders.toLocaleString(),
          rawValue: fullMetrics.totalOrders
        },
        { 
          label: 'Collection Rate', 
          value: this.formatPercent(collectionRate),
          rawValue: collectionRate
        }
      ];
    }
    
    // Fallback to sample calculation
    const clients = data.clients || [];
    const purchaseOrders = data.purchase_orders || [];
    const invoices = data.invoices || [];
    
    const totalVolume = purchaseOrders.reduce((sum, po) => sum + (po.amount || 0), 0);
    const paidInvoices = invoices.filter(inv => inv.status === 'paid').length;
    const collectionRate = invoices.length > 0 ? paidInvoices / invoices.length : 0;

    return [
      { 
        label: 'B2B Clients', 
        value: clients.length.toLocaleString(),
        rawValue: clients.length
      },
      { 
        label: 'Purchase Volume', 
        value: this.formatCurrency(totalVolume),
        rawValue: totalVolume
      },
      { 
        label: 'Purchase Orders', 
        value: purchaseOrders.length.toLocaleString(),
        rawValue: purchaseOrders.length
      },
      { 
        label: 'Collection Rate', 
        value: this.formatPercent(collectionRate),
        rawValue: collectionRate
      }
    ];
  }

  calculateSaaSMetrics(data) {
    // Use full dataset metrics if available
    const fullMetrics = data._fullDatasetMetrics;
    
    if (fullMetrics) {
      const churnRate = (fullMetrics.totalSubscriptions - fullMetrics.activeSubscriptions) / fullMetrics.totalSubscriptions;
      
      return [
        { 
          label: 'SaaS Customers', 
          value: fullMetrics.totalCustomers.toLocaleString(),
          rawValue: fullMetrics.totalCustomers
        },
        { 
          label: 'Monthly MRR', 
          value: this.formatCurrency(fullMetrics.totalMRR),
          rawValue: fullMetrics.totalMRR
        },
        { 
          label: 'Active Subs', 
          value: fullMetrics.activeSubscriptions.toLocaleString(),
          rawValue: fullMetrics.activeSubscriptions
        },
        { 
          label: 'Annual ARR', 
          value: this.formatCurrency(fullMetrics.totalARR),
          rawValue: fullMetrics.totalARR
        }
      ];
    }
    
    // Fallback to sample calculation
    const customers = data.customers || [];
    const subscriptions = data.subscriptions || [];
    const invoices = data.invoices || [];
    
    const totalMRR = customers.reduce((sum, c) => sum + (c.mrr || 0), 0);
    const activeSubscriptions = subscriptions.filter(s => s.status === 'active').length;
    const churnRate = subscriptions.length > 0 ? 
      (subscriptions.length - activeSubscriptions) / subscriptions.length : 0;

    return [
      { 
        label: 'SaaS Customers', 
        value: customers.length.toLocaleString(),
        rawValue: customers.length
      },
      { 
        label: 'Monthly MRR', 
        value: this.formatCurrency(totalMRR * 100),
        rawValue: totalMRR * 100
      },
      { 
        label: 'Active Subs', 
        value: activeSubscriptions.toLocaleString(),
        rawValue: activeSubscriptions
      },
      { 
        label: 'Churn Rate', 
        value: this.formatPercent(churnRate),
        rawValue: churnRate
      }
    ];
  }

  calculateMarketplaceMetrics(data) {
    // Use full dataset metrics if available
    const fullMetrics = data._fullDatasetMetrics;
    
    if (fullMetrics) {
      return [
        { 
          label: 'Total Orders', 
          value: fullMetrics.totalOrders.toLocaleString(),
          rawValue: fullMetrics.totalOrders
        },
        { 
          label: 'GMV', 
          value: this.formatCurrency(fullMetrics.totalVolume),
          rawValue: fullMetrics.totalVolume
        },
        { 
          label: 'Restaurants', 
          value: fullMetrics.totalRestaurants.toLocaleString(),
          rawValue: fullMetrics.totalRestaurants
        },
        { 
          label: 'Drivers', 
          value: fullMetrics.totalDrivers.toLocaleString(),
          rawValue: fullMetrics.totalDrivers
        }
      ];
    }
    
    // Fallback to sample calculation
    const orders = data.orders || [];
    const connectedAccounts = data.connected_accounts || [];
    const payments = data.payments || [];
    
    const totalGMV = orders.reduce((sum, o) => sum + (o.total || 0), 0);
    const deliveredOrders = orders.filter(o => o.status === 'delivered').length;
    const restaurants = connectedAccounts.filter(acc => acc.type === 'restaurant').length;
    const drivers = connectedAccounts.filter(acc => acc.type === 'driver').length;

    return [
      { 
        label: 'Total Orders', 
        value: orders.length.toLocaleString(),
        rawValue: orders.length
      },
      { 
        label: 'GMV', 
        value: this.formatCurrency(totalGMV),
        rawValue: totalGMV
      },
      { 
        label: 'Restaurants', 
        value: restaurants.toString(),
        rawValue: restaurants
      },
      { 
        label: 'Drivers', 
        value: drivers.toString(),
        rawValue: drivers
      }
    ];
  }

  // Utility functions
  formatCurrency(cents) {
    const dollars = cents / 100;
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(dollars);
  }

  formatPercent(value) {
    return new Intl.NumberFormat('en-US', {
      style: 'percent',
      minimumFractionDigits: 1,
      maximumFractionDigits: 1
    }).format(value);
  }

  formatNumber(value) {
    return new Intl.NumberFormat('en-US').format(value);
  }

  // Health check
  async healthCheck() {
    try {
      const response = await this.fetchWithRetry(`${this.baseUrl}/health.json`);
      return response;
    } catch (error) {
      console.error('Health check failed:', error);
      return { status: 'error', error: error.message };
    }
  }
}

// Export for both CommonJS and ES6 modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = StripeDataClient;
}
if (typeof window !== 'undefined') {
  window.StripeDataClient = StripeDataClient;
}
