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
    try {
      await this.loadPersonas();
      await this.loadPersona(this.currentPersona);
    } catch (error) {
      console.error('Failed to initialize StripeDataClient:', error);
      // Use fallback data for demo purposes
      this.useFallbackData();
    }
  }

  // Fallback data for demo when API is not available
  useFallbackData() {
    console.log('Using fallback data for demo');
    
    this.availablePersonas = {
      techstyle: {
        id: 'techstyle',
        name: 'TechStyle Fashion Retailer',
        business_model: 'ecommerce',
        description: 'E-commerce fashion retailer with global payment processing',
        endpoints: {}
      },
      edutech: {
        id: 'edutech', 
        name: 'EduTech Academy',
        business_model: 'education_marketplace',
        description: 'Online education marketplace with instructor payouts',
        endpoints: {}
      },
      propertyflow: {
        id: 'propertyflow',
        name: 'PropertyFlow Property Management',
        business_model: 'property_management',
        description: 'Property management platform with rent collection',
        endpoints: {}
      },
      fitstream: {
        id: 'fitstream',
        name: 'FitStream Fitness Platform',
        business_model: 'subscription',
        description: 'Subscription fitness platform with trials and engagement',
        endpoints: {}
      },
      creatorhub: {
        id: 'creatorhub',
        name: 'CreatorHub Content Platform',
        business_model: 'creator_economy',
        description: 'Content monetization platform with creator payouts',
        endpoints: {}
      }
    };

    this.currentData = this.generateFallbackData(this.currentPersona);
    this.notifySubscribers(this.currentData, this.currentPersona);
  }

  // Generate realistic fallback data
  generateFallbackData(personaId) {
    const baseAmount = Math.floor(Math.random() * 10000) + 5000;
    
    switch (personaId) {
      case 'techstyle':
        return {
          payments: Array.from({length: 50}, (_, i) => ({
            id: `pi_demo_${i.toString().padStart(6, '0')}`,
            amount: Math.floor(Math.random() * 20000) + 1000,
            currency: 'usd',
            status: Math.random() > 0.05 ? 'succeeded' : 'failed',
            customer: `cus_demo_${i.toString().padStart(6, '0')}`,
            created: Date.now() - Math.random() * 86400000 * 30
          })),
          customers: Array.from({length: 30}, (_, i) => ({
            id: `cus_demo_${i.toString().padStart(6, '0')}`,
            email: `customer${i}@example.com`,
            created: Date.now() - Math.random() * 86400000 * 90,
            metadata: { country: ['US', 'CA', 'GB', 'AU'][Math.floor(Math.random() * 4)] }
          })),
          summary: {
            revenue_metrics: {
              total_revenue: baseAmount * 100,
              current_mrr: baseAmount
            }
          }
        };
        
      case 'edutech':
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
          students: Array.from({length: 100}, (_, i) => ({
            id: `cus_demo_${i.toString().padStart(6, '0')}`,
            email: `student${i}@university.edu`,
            created: Date.now() - Math.random() * 86400000 * 90
          })),
          enrollments: Array.from({length: 40}, (_, i) => ({
            id: `enroll_demo_${i.toString().padStart(6, '0')}`,
            amount: Math.floor(Math.random() * 50000) + 10000,
            status: 'succeeded',
            customer: `cus_demo_${i.toString().padStart(6, '0')}`,
            course_id: `course_${Math.floor(Math.random() * 20)}`
          }))
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
          }))
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
          }))
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
    if (!data) return {};

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
      default:
        return this.calculateGenericMetrics(data);
    }
  }

  calculateEcommerceMetrics(data) {
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
