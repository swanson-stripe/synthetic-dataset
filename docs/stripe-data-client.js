/**
 * Stripe Synthetic Data Client
 * Independent data client for prototype bases to consume personas
 * Version: 1.0.0
 */

class StripeDataClient {
  constructor(options = {}) {
    this.baseUrl = options.baseUrl || 'https://swanson-stripe.github.io/synthetic-dataset/api/v1';
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
    const endpoints = persona.endpoints;
    
    try {
      // Load all endpoints in parallel
      const dataPromises = Object.entries(endpoints).map(async ([key, endpoint]) => {
        const url = `${this.baseUrl}${endpoint}`;
        const data = await this.fetchWithRetry(url);
        return [key, data];
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

    // Load new persona
    return await this.loadPersona(personaId);
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
