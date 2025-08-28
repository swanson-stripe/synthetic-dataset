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
        endpoints: {}
      },
      edutech: {
        id: 'edutech', 
        name: 'EduTech Academy',
        business_model: 'education_marketplace',
        description: 'Online education marketplace with instructor payouts',
        complexity: 'high',
        data_scale: 'large',
        endpoints: {}
      },
      propertyflow: {
        id: 'propertyflow',
        name: 'PropertyFlow Property Management',
        business_model: 'property_management',
        description: 'Property management platform with rent collection',
        complexity: 'medium',
        data_scale: 'medium',
        endpoints: {}
      },
      fitstream: {
        id: 'fitstream',
        name: 'FitStream Fitness Platform',
        business_model: 'subscription',
        description: 'Subscription fitness platform with trials and engagement',
        complexity: 'medium',
        data_scale: 'large',
        endpoints: {}
      },
      creatorhub: {
        id: 'creatorhub',
        name: 'CreatorHub Content Platform',
        business_model: 'creator_economy',
        description: 'Content monetization platform with creator payouts',
        complexity: 'high',
        data_scale: 'large',
        endpoints: {}
      },
      givehope: {
        id: 'givehope',
        name: 'GiveHope Non-Profit Platform',
        business_model: 'nonprofit',
        description: 'Non-profit donation platform with campaigns and recurring donors',
        complexity: 'medium',
        data_scale: 'large',
        endpoints: {}
      },
      medsupply: {
        id: 'medsupply',
        name: 'MedSupply Pro B2B Platform',
        business_model: 'b2b_wholesale',
        description: 'B2B medical equipment wholesaler with net terms',
        complexity: 'high',
        data_scale: 'large',
        endpoints: {}
      },
      cloudflow: {
        id: 'cloudflow',
        name: 'CloudFlow SaaS Platform',
        business_model: 'saas',
        description: 'B2B SaaS platform with subscription management',
        complexity: 'high',
        data_scale: 'large',
        endpoints: {}
      },
      localbites: {
        id: 'localbites',
        name: 'LocalBites Food Delivery',
        business_model: 'marketplace',
        description: 'Food delivery marketplace with restaurant and driver management',
        complexity: 'high',
        data_scale: 'very_large',
        endpoints: {}
      }
    };

    // Support lifecycle stages
    this.lifecycleStages = {
      early: { name: 'Early Stage', description: 'Months 1-8: Startup phase' },
      growth: { name: 'Growth Stage', description: 'Months 9-16: Expansion phase' },
      mature: { name: 'Mature Stage', description: 'Months 17-24: Established business' }
    };

    this.currentData = this.generateFallbackData(this.currentPersona);
    this.notifySubscribers(this.currentData, this.currentPersona);
  }

  // Generate realistic fallback data that reflects full synthetic dataset scale
  generateFallbackData(personaId) {
    // Base amounts for massive scale datasets
    const baseAmount = Math.floor(Math.random() * 50000) + 25000;
    
    switch (personaId) {
      case 'techstyle':
        // TechStyle: 150K payments, 75K customers (full synthetic dataset scale)
        const techstylePayments = Array.from({length: 50}, (_, i) => ({
          id: `pi_demo_${i.toString().padStart(6, '0')}`,
          amount: Math.floor(Math.random() * 20000) + 1000,
          currency: 'usd',
          status: Math.random() > 0.05 ? 'succeeded' : 'failed',
          customer: `cus_demo_${i.toString().padStart(6, '0')}`,
          created: Date.now() - Math.random() * 86400000 * 30
        }));
        
        return {
          payments: techstylePayments,
                     customers: Array.from({length: 30}, (_, i) => ({
             id: `cus_demo_${i.toString().padStart(6, '0')}`,
             email: `customer${i}@example.com`,
             country: ['US', 'CA', 'GB', 'AU'][Math.floor(Math.random() * 4)],
             created: Date.now() - Math.random() * 86400000 * 90,
             metadata: { country: ['US', 'CA', 'GB', 'AU'][Math.floor(Math.random() * 4)] }
           })),
          // Full dataset metrics (not just the 50 sample payments)
          _fullDatasetMetrics: {
            totalPayments: 150000,
            totalCustomers: 75000,
            totalRevenue: 18500000000, // $185M in cents
            successfulPayments: 147000
          },
          summary: {
            revenue_metrics: {
              total_revenue: 18500000000, // Full dataset revenue
              current_mrr: baseAmount
            }
          }
        };
        
      case 'edutech':
        // EduTech: 73K students, 218 courses, $201M in transactions
        return {
          instructors: Array.from({length: 20}, (_, i) => ({
            id: `acct_demo_${i.toString().padStart(6, '0')}`,
            business_profile: { name: `Dr. Instructor ${i + 1}` },
            metadata: {
              expertise: ['Computer Science', 'Mathematics', 'Physics', 'Chemistry', 'Biology', 'Economics'][Math.floor(Math.random() * 6)],
              rating: (4.0 + Math.random()).toFixed(1),
              total_students: Math.floor(Math.random() * 500) + 50,
              course_count: Math.floor(Math.random() * 10) + 1
            }
          })),
          students: Array.from({length: 30}, (_, i) => ({
            id: `cus_demo_${i.toString().padStart(6, '0')}`,
            email: `student${i}@university.edu`,
            created: Date.now() - Math.random() * 86400000 * 90
          })),
          enrollments: Array.from({length: 25}, (_, i) => ({
            id: `enroll_demo_${i.toString().padStart(6, '0')}`,
            amount: Math.floor(Math.random() * 50000) + 10000,
            status: 'succeeded',
            customer: `cus_demo_${i.toString().padStart(6, '0')}`,
            course_id: `course_${Math.floor(Math.random() * 20)}`
          })),
          // Full dataset metrics
          _fullDatasetMetrics: {
            totalStudents: 73000,
            totalInstructors: 72,
            totalCourses: 218,
            totalEnrollments: 12000,
            totalRevenue: 20100000000 // $201M in cents
          }
        };
        
      case 'propertyflow':
        return {
          properties: Array.from({length: 25}, (_, i) => ({
            id: `prop_demo_${i.toString().padStart(6, '0')}`,
            address: `${100 + i} Demo Street, City ${Math.floor(i/5) + 1}`,
            type: ['apartment', 'house', 'condo', 'townhouse'][Math.floor(Math.random() * 4)],
            rent_amount: Math.floor(Math.random() * 200000) + 100000,
            tenant_id: `tenant_${i}`
          })),
          landlords: Array.from({length: 15}, (_, i) => ({
            id: `acct_demo_${i.toString().padStart(6, '0')}`,
            business_profile: { name: `Landlord ${i + 1}` },
            properties_count: Math.floor(Math.random() * 5) + 1
          })),
          rent_payments: Array.from({length: 35}, (_, i) => ({
            id: `rent_demo_${i.toString().padStart(6, '0')}`,
            amount: Math.floor(Math.random() * 200000) + 100000,
            status: Math.random() > 0.05 ? 'succeeded' : 'failed',
            property_id: `prop_demo_${Math.floor(Math.random() * 25).toString().padStart(6, '0')}`,
            tenant: `Tenant ${i + 1}`
          })),
          // Full dataset metrics - PropertyFlow: 25K properties, $2.8B volume
          _fullDatasetMetrics: {
            totalProperties: 25000,
            totalLandlords: 8500,
            totalPayments: 350000,
            totalVolume: 280000000000, // $2.8B in cents
            successfulPayments: 342000
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
            totalSubscribers: 85000,
            totalCustomers: 120000,
            totalMRR: 817000000, // $8.17M MRR in cents
            totalARR: 9800000000, // $98M ARR in cents
            activeSubscriptions: 78000
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
            totalCreators: 35000,
            totalFans: 850000,
            totalSales: 420000,
            totalVolume: 6700000000, // $67M in cents
            topCreators: 2800
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
            totalDonors: 15000,
            totalCampaigns: 55,
            totalRaised: 1750000000, // $17.5M in cents
            totalDonations: 125000,
            recurringDonors: 1500
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
            totalClients: 2500,
            totalOrders: 15000,
            totalVolume: 12500000000, // $125M in cents
            totalInvoices: 18000,
            paidInvoices: 16500
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
            totalCustomers: 50000,
            totalSubscriptions: 47000,
            totalMRR: 2000000000, // $20M MRR in cents
            totalARR: 24000000000, // $240M ARR in cents
            activeSubscriptions: 44000
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
            totalOrders: 600000,
            totalRestaurants: 8500,
            totalDrivers: 12000,
            totalVolume: 9500000000, // $95M in cents
            totalPayments: 585000
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

  // Switch to a different persona
  async switchPersona(personaId) {
    if (personaId === this.currentPersona) {
      return this.currentData;
    }

    // Check cache first
    if (this.cache.has(personaId)) {
      this.currentPersona = personaId;
      this.currentData = this.cache.get(personaId);
      this.notifySubscribers(this.currentData, personaId);
      return this.currentData;
    }

    // Try to load from API, fall back to generated data
    try {
    return await this.loadPersona(personaId);
    } catch (error) {
      console.warn(`Failed to load ${personaId}, using fallback data:`, error.message);
      this.currentPersona = personaId;
      this.currentData = this.generateFallbackData(personaId);
      this.cache.set(personaId, this.currentData);
      this.notifySubscribers(this.currentData, personaId);
      return this.currentData;
    }
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
