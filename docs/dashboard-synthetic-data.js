/**
 * Dashboard Synthetic Data Kit
 * Complete integration package for business persona data and UI components
 * Version: 1.0.0
 */

(function() {
  'use strict';

  // Auto-inject CSS styles
  const injectCSS = () => {
    if (document.getElementById('dashboard-synthetic-data-styles')) return;
    
    const css = `
      /* Dashboard Synthetic Data Kit Styles */
      
      /* Persona Selector */
      .persona-selector-container {
        position: relative;
        display: inline-block;
        min-width: 240px;
      }
      
      .persona-selector-button {
        display: flex;
        align-items: center;
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 12px 16px;
        cursor: pointer;
        transition: all 0.2s ease;
        width: 100%;
        min-width: 0;
      }
      
      .persona-selector-button:hover {
        background: #f8f9fa;
        border-color: #d0d7de;
      }
      
      .persona-logo {
        width: 32px;
        height: 32px;
        border-radius: 6px;
        object-fit: cover;
        flex-shrink: 0;
        margin-right: 16px;
      }
      
      .persona-selector-text {
        flex: 1;
        text-align: left;
        min-width: 0;
      }
      
      .persona-name {
        font-size: 15px;
        font-weight: 500;
        color: #1a1a1a;
        margin: 0;
        line-height: 1.2;
      }
      
      .dropdown-arrow {
        width: 12px;
        height: 12px;
        color: #666;
        transition: transform 0.15s ease;
        margin-left: 16px;
        flex-shrink: 0;
      }
      
      .persona-selector-button.open .dropdown-arrow {
        transform: rotate(180deg);
      }
      
      /* Popover Styles */
      .persona-popover {
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: white;
        border-radius: 16px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        z-index: 1000;
        margin-top: 8px;
        display: none;
        border: 1px solid #f0f0f0;
      }
      
      .persona-popover.show {
        display: block;
      }
      
      .popover-content {
        text-align: center;
      }
      
      .popover-logo-section {
        padding: 24px 24px 0;
        margin-bottom: 12px;
        text-align: center;
      }
      
      .popover-persona-logo {
        width: 48px;
        height: 48px;
        border-radius: 6px;
        object-fit: cover;
        display: block;
        margin: 0 auto;
      }
      
      .popover-title {
        font-size: 18px;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 8px;
        line-height: 1.2;
        padding: 0 24px;
      }
      
      .popover-description {
        font-size: 14px;
        color: #666;
        line-height: 1.3;
        margin-bottom: 16px;
        padding: 0 24px;
      }
      
      .stage-section {
        text-align: left;
        padding: 8px;
      }
      
      .stage-label {
        font-size: 14px;
        font-weight: 600;
        color: #666;
        margin-bottom: 12px;
      }
      
      .stage-options {
        display: flex;
        flex-direction: column;
        gap: 0;
      }
      
      .stage-option {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 4px;
        cursor: pointer;
        font-size: 16px;
        color: #1a1a1a;
        transition: all 0.2s ease;
        border-bottom: none;
        border-radius: 6px;
      }
      
      .stage-option:hover {
        background: #F5F6F8;
      }
      
      .stage-text {
        font-weight: 400;
        font-size: 14px;
      }
      
      .stage-check {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: #666;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: 600;
      }
      
      .stage-option:not(.selected) .stage-check {
        display: none;
      }
      
      .change-persona-btn {
        background: none;
        border: none;
        color: #1a1a1a;
        text-decoration: underline;
        cursor: pointer;
        font-size: 14px;
        margin-bottom: 16px;
        padding: 0;
        font-weight: 400;
      }
      
      .change-persona-btn:hover {
        color: #666;
      }
      
      .popover-divider {
        height: 1px;
        background: #e0e0e0;
        margin: 0;
      }
      
      /* Modal Styles */
      .persona-modal {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        z-index: 2000;
        align-items: center;
        justify-content: center;
      }
      
      .persona-modal.show {
        display: flex;
      }
      
      .modal-content {
        background: white;
        border-radius: 12px;
        max-width: 800px;
        width: 90%;
        max-height: 80vh;
        overflow: hidden;
        position: relative;
        display: flex;
        padding: 0;
        flex-direction: row;
        height: 80vh;
      }
      
      .persona-list-panel {
        width: 50%;
        padding: 2rem;
        border-right: 1px solid #e5e7eb;
        display: flex;
        flex-direction: column;
        height: 100%;
      }
      
      .persona-details-panel {
        width: 50%;
        padding: 2rem;
        overflow-y: auto;
        height: 100%;
      }
      
      .modal-header {
        margin-bottom: 1.5rem;
      }
      
      .modal-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
        color: #111827;
      }
      
      .modal-description {
        color: #6b7280;
        margin: 0;
        font-size: 1rem;
        line-height: 1.5;
      }
      
      .personas-list {
        flex: 1;
        overflow-y: auto;
        margin-bottom: 1.5rem;
      }
      
      .persona-option {
        display: flex;
        align-items: center;
        padding: 8px;
        border: 2px solid transparent;
        border-radius: 8px;
        cursor: pointer;
        margin-bottom: 8px;
        transition: all 0.2s ease;
      }
      
      .persona-option:hover {
        background: #f9fafb;
      }
      
      .persona-option.selected {
        border-color: #8b5cf6;
        background: #f3f4f6;
      }
      
      .persona-option-logo {
        width: 40px;
        height: 40px;
        border-radius: 6px;
        object-fit: cover;
        margin-right: 12px;
        flex-shrink: 0;
      }
      
      .persona-option-info {
        flex: 1;
        min-width: 0;
      }
      
      .persona-option-name {
        font-size: 16px;
        font-weight: 500;
        color: #111827;
        margin: 0 0 4px 0;
        line-height: 1.2;
      }
      
      .persona-option-type {
        font-size: 14px;
        color: #6b7280;
        margin: 0;
        line-height: 1.2;
      }
      
      .modal-footer-left {
        margin-top: auto;
      }
      
      .modal-footer-left .btn {
        padding: 12px 24px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        text-decoration: none;
        display: inline-block;
        text-align: center;
        width: 100%;
        background: white;
        color: #374151;
        border: 1px solid #d1d5db;
      }
      
      .modal-footer-left .btn:hover {
        background: #f9fafb;
      }
      
      .persona-details-title {
        font-size: 1.25rem;
        font-weight: 600;
        margin: 0 0 1rem 0;
        color: #111827;
      }
      
      .persona-details-description {
        color: #6b7280;
        margin: 0 0 2rem 0;
        font-size: 1.125rem;
        line-height: 1.6;
      }
      
      .products-section {
        margin-top: 2rem;
      }
      
      .products-title {
        font-size: 1.125rem;
        font-weight: 600;
        margin: 0 0 1rem 0;
        color: #111827;
      }
      
      .products-list {
        list-style: none;
        padding: 0;
        margin: 0;
      }
      
      .products-list li {
        color: #6b7280;
        margin-bottom: 0.5rem;
        font-size: 1.125rem;
        line-height: 1.5;
      }
      
      .products-list li:before {
        content: "• ";
        color: #9ca3af;
        margin-right: 0.5rem;
      }
      
      /* Custom scrollbar styling */
      .personas-list::-webkit-scrollbar,
      .persona-details-panel::-webkit-scrollbar {
        width: 8px;
      }
      
      .personas-list::-webkit-scrollbar-track,
      .persona-details-panel::-webkit-scrollbar-track {
        background: transparent;
      }
      
      .personas-list::-webkit-scrollbar-thumb,
      .persona-details-panel::-webkit-scrollbar-thumb {
        background: #e5e7eb;
        border-radius: 4px;
      }
      
      .personas-list::-webkit-scrollbar-thumb:hover,
      .persona-details-panel::-webkit-scrollbar-thumb:hover {
        background: #d1d5db;
      }
    `;
    
    const style = document.createElement('style');
    style.id = 'dashboard-synthetic-data-styles';
    style.textContent = css;
    document.head.appendChild(style);
  };

  // Data Client Class (consolidated from stripe-data-client.js)
  class DataClient {
    constructor(options = {}) {
      this.baseUrl = options.baseUrl || 'https://raw.githubusercontent.com/swanson-stripe/synthetic-dataset/main/api/v1';
      this.currentPersona = options.defaultPersona || 'modaic';
      this.currentStage = options.defaultStage || 'growth';
      this.cache = new Map();
      this.subscribers = [];
      this.retryAttempts = options.retryAttempts || 3;
      this.retryDelay = options.retryDelay || 1000;
      
      // Initialize synchronously for immediate data availability
      this.initSync();
    }

    initSync() {
      console.log('🚀 Initializing Dashboard Synthetic Dataset');
      this.useFallbackData();
      
      // Debug: Verify data loaded
      const debugMetrics = this.calculateMetrics();
      console.log('✅ Demo data loaded:', {
        currentPersona: this.currentPersona,
        availablePersonas: Object.keys(this.availablePersonas),
        currentDataKeys: Object.keys(this.currentData || {}),
        metricsExample: debugMetrics
      });
    }

    // Fallback data for demo when API is not available
    useFallbackData() {
      // Create complete personas matching the real API structure
      this.availablePersonas = {
        modaic: {
          id: 'modaic',
          name: 'Modaic',
          business_model: 'ecommerce',
          description: 'E-commerce fashion retailer with global payment processing',
          complexity: 'medium',
          data_scale: 'large',
          products: ['Payments', 'Checkout', 'Subscriptions', 'Radar'],
          endpoints: {}
        },
        mindora: {
          id: 'mindora', 
          name: 'Mindora',
          business_model: 'education_marketplace',
          description: 'Online education marketplace with instructor payouts',
          complexity: 'high',
          data_scale: 'large',
          products: ['Payments', 'Connect', 'Subscriptions', 'Tax'],
          endpoints: {}
        },
        keynest: {
          id: 'keynest',
          name: 'Keynest',
          business_model: 'property_management',
          description: 'Property management platform with rent collection',
          complexity: 'medium',
          data_scale: 'medium',
          products: ['Payments', 'Connect', 'ACH', 'Invoicing'],
          endpoints: {}
        },
        pulseon: {
          id: 'pulseon',
          name: 'Pulseon',
          business_model: 'subscription',
          description: 'Subscription fitness platform with trials and engagement',
          complexity: 'medium',
          data_scale: 'large',
          products: ['Subscriptions', 'Payments', 'Billing', 'Revenue Recognition'],
          endpoints: {}
        },
        fluxly: {
          id: 'fluxly',
          name: 'Fluxly',
          business_model: 'creator_economy',
          description: 'Content monetization platform with creator payouts',
          complexity: 'high',
          data_scale: 'large',
          products: ['Payments', 'Connect', 'Subscriptions', 'Tax'],
          endpoints: {}
        },
        brightfund: {
          id: 'brightfund',
          name: 'Brightfund',
          business_model: 'non_profit',
          description: 'Non-profit fundraising with donor management',
          complexity: 'medium',
          data_scale: 'medium',
          products: ['Payments', 'Checkout', 'Subscriptions', 'Tax'],
          endpoints: {}
        },
        procura: {
          id: 'procura',
          name: 'Procura',
          business_model: 'b2b_marketplace',
          description: 'B2B medical supply marketplace with financing',
          complexity: 'high',
          data_scale: 'large',
          products: ['Payments', 'Connect', 'Invoicing', 'Capital'],
          endpoints: {}
        },
        stratus: {
          id: 'stratus',
          name: 'Stratus',
          business_model: 'saas',
          description: 'Cloud infrastructure SaaS with usage-based billing',
          complexity: 'high',
          data_scale: 'large',
          products: ['Billing', 'Subscriptions', 'Invoicing', 'Revenue Recognition'],
          endpoints: {}
        },
        forksy: {
          id: 'forksy',
          name: 'Forksy',
          business_model: 'marketplace',
          description: 'Food delivery marketplace with restaurant payouts',
          complexity: 'high',
          data_scale: 'large',
          products: ['Payments', 'Connect', 'Issuing', 'Treasury'],
          endpoints: {}
        }
      };

      // Generate fallback data for current persona
      this.generateFallbackData(this.currentPersona);
    }

    generateFallbackData(personaId) {
      const stageMultipliers = {
        early: 0.3,
        growth: 1.0,
        mature: 2.8
      };
      
      const multiplier = stageMultipliers[this.currentStage] || 1.0;
      
      // Generate realistic sample data
      this.currentData = {
        payments: this.generatePayments(personaId, multiplier),
        customers: this.generateCustomers(personaId, multiplier),
        connected_accounts: this.generateConnectedAccounts(personaId, multiplier),
        transfers: this.generateTransfers(personaId, multiplier),
        balances: this.generateBalances(personaId, multiplier),
        _fullDatasetMetrics: this.generateFullDatasetMetrics(personaId, multiplier)
      };

      // Add persona-specific objects
      switch (personaId) {
        case 'mindora':
          this.currentData.invoices = this.generateInvoices(personaId, multiplier);
          break;
        case 'pulseon':
          this.currentData.subscriptions = this.generateSubscriptions(personaId, multiplier);
          break;
        case 'stratus':
          this.currentData.subscriptions = this.generateSubscriptions(personaId, multiplier);
          this.currentData.invoices = this.generateInvoices(personaId, multiplier);
          break;
        case 'forksy':
          this.currentData.issuing_cards = this.generateIssuingCards(personaId, multiplier);
          break;
      }

      // Update cache
      const cacheKey = `${personaId}_${this.currentStage}`;
      this.cache.set(cacheKey, this.currentData);
    }

    generatePayments(personaId, multiplier) {
      const payments = [];
      const count = Math.floor(10 * multiplier);
      
      for (let i = 0; i < count; i++) {
        const amount = Math.floor(Math.random() * 50000 + 1000) * multiplier;
        payments.push({
          id: `py_${Math.random().toString(36).substr(2, 14)}`,
          amount: Math.floor(amount * 100), // amount in cents
          currency: 'usd',
          status: this.getRandomStatus(['succeeded', 'succeeded', 'succeeded', 'pending', 'failed']),
          created: Date.now() - Math.floor(Math.random() * 86400000 * 30), // last 30 days
          description: this.getPaymentDescription(personaId),
          customer: `cus_${Math.random().toString(36).substr(2, 14)}`,
          metadata: this.getPaymentMetadata(personaId)
        });
      }
      
      return payments;
    }

    generateCustomers(personaId, multiplier) {
      const customers = [];
      const count = Math.floor(10 * multiplier);
      
      for (let i = 0; i < count; i++) {
        customers.push({
          id: `cus_${Math.random().toString(36).substr(2, 14)}`,
          email: `customer${i}@example.com`,
          name: `Customer ${i + 1}`,
          created: Date.now() - Math.floor(Math.random() * 86400000 * 90), // last 90 days
          metadata: this.getCustomerMetadata(personaId)
        });
      }
      
      return customers;
    }

    generateConnectedAccounts(personaId, multiplier) {
      if (!this.requiresConnect(personaId)) return [];
      
      const accounts = [];
      const count = Math.floor(5 * multiplier);
      
      for (let i = 0; i < count; i++) {
        accounts.push({
          id: `acct_${Math.random().toString(36).substr(2, 14)}`,
          type: 'express',
          country: 'US',
          email: `account${i}@example.com`,
          created: Date.now() - Math.floor(Math.random() * 86400000 * 60), // last 60 days
          metadata: this.getAccountMetadata(personaId)
        });
      }
      
      return accounts;
    }

    generateTransfers(personaId, multiplier) {
      const transfers = [];
      const count = Math.floor(8 * multiplier);
      
      for (let i = 0; i < count; i++) {
        const amount = Math.floor(Math.random() * 30000 + 500) * multiplier;
        transfers.push({
          id: `tr_${Math.random().toString(36).substr(2, 14)}`,
          amount: Math.floor(amount * 100), // amount in cents
          currency: 'usd',
          created: Date.now() - Math.floor(Math.random() * 86400000 * 30), // last 30 days
          destination: this.requiresConnect(personaId) ? `acct_${Math.random().toString(36).substr(2, 14)}` : null,
          metadata: this.getTransferMetadata(personaId)
        });
      }
      
      return transfers;
    }

    generateBalances(personaId, multiplier) {
      return {
        available: [{
          amount: Math.floor(Math.random() * 100000 + 10000) * multiplier * 100,
          currency: 'usd'
        }],
        pending: [{
          amount: Math.floor(Math.random() * 20000 + 1000) * multiplier * 100,
          currency: 'usd'
        }]
      };
    }

    generateInvoices(personaId, multiplier) {
      const invoices = [];
      const count = Math.floor(6 * multiplier);
      
      for (let i = 0; i < count; i++) {
        const amount = Math.floor(Math.random() * 80000 + 2000) * multiplier;
        invoices.push({
          id: `in_${Math.random().toString(36).substr(2, 14)}`,
          amount_paid: Math.floor(amount * 100),
          currency: 'usd',
          status: this.getRandomStatus(['paid', 'paid', 'open', 'draft']),
          created: Date.now() - Math.floor(Math.random() * 86400000 * 45), // last 45 days
          customer: `cus_${Math.random().toString(36).substr(2, 14)}`,
          metadata: this.getInvoiceMetadata(personaId)
        });
      }
      
      return invoices;
    }

    generateSubscriptions(personaId, multiplier) {
      const subscriptions = [];
      const count = Math.floor(7 * multiplier);
      
      for (let i = 0; i < count; i++) {
        subscriptions.push({
          id: `sub_${Math.random().toString(36).substr(2, 14)}`,
          status: this.getRandomStatus(['active', 'active', 'active', 'trialing', 'canceled']),
          current_period_start: Date.now() - Math.floor(Math.random() * 86400000 * 30),
          current_period_end: Date.now() + Math.floor(Math.random() * 86400000 * 30),
          customer: `cus_${Math.random().toString(36).substr(2, 14)}`,
          metadata: this.getSubscriptionMetadata(personaId)
        });
      }
      
      return subscriptions;
    }

    generateIssuingCards(personaId, multiplier) {
      const cards = [];
      const count = Math.floor(4 * multiplier);
      
      for (let i = 0; i < count; i++) {
        cards.push({
          id: `ic_${Math.random().toString(36).substr(2, 14)}`,
          status: this.getRandomStatus(['active', 'active', 'inactive', 'canceled']),
          type: 'virtual',
          brand: 'visa',
          created: Date.now() - Math.floor(Math.random() * 86400000 * 60),
          metadata: this.getCardMetadata(personaId)
        });
      }
      
      return cards;
    }

    generateFullDatasetMetrics(personaId, multiplier) {
      // Generate large-scale metrics for the full dataset
      const baseMetrics = {
        totalTransactions: Math.floor((Math.random() * 500000 + 100000) * multiplier),
        totalCustomers: Math.floor((Math.random() * 50000 + 10000) * multiplier),
        totalRevenue: Math.floor((Math.random() * 10000000 + 2000000) * multiplier * 100), // in cents
        averageOrderValue: Math.floor((Math.random() * 20000 + 5000) * multiplier), // in cents
      };

      // Add persona-specific metrics
      switch (personaId) {
        case 'modaic':
          baseMetrics.conversionRate = (Math.random() * 0.05 + 0.02) * multiplier;
          baseMetrics.newCustomers = Math.floor(baseMetrics.totalCustomers * 0.15);
          break;
        case 'mindora':
          baseMetrics.retentionRate = (Math.random() * 0.3 + 0.7) * multiplier;
          baseMetrics.totalPayments = baseMetrics.totalTransactions;
          break;
        case 'keynest':
          baseMetrics.connectedAccounts = Math.floor((Math.random() * 1000 + 200) * multiplier);
          break;
        case 'pulseon':
          baseMetrics.activeSubscribers = Math.floor(baseMetrics.totalCustomers * 0.6);
          baseMetrics.churnRate = Math.random() * 0.08 + 0.02;
          break;
        case 'fluxly':
          baseMetrics.grossVolume = baseMetrics.totalRevenue;
          baseMetrics.trialConversionRate = Math.random() * 0.2 + 0.1;
          break;
        case 'brightfund':
          baseMetrics.grossVolume = baseMetrics.totalRevenue;
          baseMetrics.customers = baseMetrics.totalCustomers;
          baseMetrics.retentionRate = Math.random() * 0.4 + 0.6;
          baseMetrics.paymentAcceptanceRate = Math.random() * 0.05 + 0.94;
          break;
        case 'procura':
          baseMetrics.grossVolume = baseMetrics.totalRevenue;
          baseMetrics.customers = baseMetrics.totalCustomers;
          baseMetrics.invoicePaymentRate = Math.random() * 0.1 + 0.85;
          baseMetrics.invoiceCollectionTime = Math.floor(Math.random() * 20 + 25); // days
          break;
        case 'stratus':
          baseMetrics.activeSubscribers = Math.floor(baseMetrics.totalCustomers * 0.8);
          baseMetrics.grossRevenue = baseMetrics.totalRevenue;
          baseMetrics.netRevenueRetention = Math.random() * 0.3 + 1.0;
          baseMetrics.churnRate = Math.random() * 0.05 + 0.02;
          break;
        case 'forksy':
          baseMetrics.netVolumeFromSales = Math.floor(baseMetrics.totalRevenue * 0.85);
          baseMetrics.connectedAccounts = Math.floor((Math.random() * 2000 + 500) * multiplier);
          baseMetrics.blockedPaymentsRate = Math.random() * 0.02 + 0.005;
          baseMetrics.cardSpendVolume = Math.floor(baseMetrics.totalRevenue * 0.3);
          break;
      }

      return baseMetrics;
    }

    // Helper methods for generating realistic data
    getRandomStatus(options) {
      return options[Math.floor(Math.random() * options.length)];
    }

    requiresConnect(personaId) {
      return ['mindora', 'keynest', 'fluxly', 'procura', 'forksy'].includes(personaId);
    }

    getPaymentDescription(personaId) {
      const descriptions = {
        modaic: 'Fashion purchase',
        mindora: 'Course enrollment',
        keynest: 'Rent payment',
        pulseon: 'Subscription payment',
        fluxly: 'Content purchase',
        brightfund: 'Donation',
        procura: 'Medical supplies',
        stratus: 'Platform usage',
        forksy: 'Food order'
      };
      return descriptions[personaId] || 'Payment';
    }

    getPaymentMetadata(personaId) {
      const metadataOptions = {
        modaic: { product_category: 'clothing', size: 'M', color: 'blue' },
        mindora: { course_id: 'course_123', instructor: 'instructor_456' },
        keynest: { property_id: 'prop_789', unit: '2A' },
        pulseon: { plan: 'premium', billing_cycle: 'monthly' },
        fluxly: { content_type: 'video', creator_id: 'creator_123' },
        brightfund: { campaign_id: 'camp_456', donor_type: 'individual' },
        procura: { product_sku: 'MED-789', category: 'supplies' },
        stratus: { usage_type: 'compute', region: 'us-east-1' },
        forksy: { restaurant_id: 'rest_123', delivery_zone: 'zone_A' }
      };
      return metadataOptions[personaId] || {};
    }

    getCustomerMetadata(personaId) {
      const metadataOptions = {
        modaic: { customer_segment: 'premium', preferred_size: 'M' },
        mindora: { student_level: 'intermediate', enrollment_date: '2024-01-15' },
        keynest: { tenant_type: 'residential', lease_start: '2024-01-01' },
        pulseon: { fitness_level: 'beginner', goals: 'weight_loss' },
        fluxly: { fan_tier: 'supporter', join_date: '2024-02-01' },
        brightfund: { donor_category: 'major', first_donation: '2024-01-10' },
        procura: { business_size: 'medium', industry: 'healthcare' },
        stratus: { plan_tier: 'enterprise', onboarding_date: '2024-01-20' },
        forksy: { delivery_preference: 'contactless', dietary_restrictions: 'none' }
      };
      return metadataOptions[personaId] || {};
    }

    getAccountMetadata(personaId) {
      const metadataOptions = {
        mindora: { instructor_specialty: 'data_science', experience_years: '5' },
        keynest: { property_manager: 'true', properties_managed: '12' },
        fluxly: { creator_category: 'video', follower_count: '10000' },
        procura: { supplier_category: 'medical_devices', certification: 'FDA' },
        forksy: { restaurant_type: 'casual_dining', cuisine: 'american' }
      };
      return metadataOptions[personaId] || {};
    }

    getTransferMetadata(personaId) {
      const metadataOptions = {
        mindora: { transfer_type: 'instructor_payout', course_earnings: 'true' },
        keynest: { transfer_type: 'rent_collection', property: 'prop_123' },
        fluxly: { transfer_type: 'creator_payout', content_earnings: 'true' },
        procura: { transfer_type: 'supplier_payment', order_id: 'ord_456' },
        forksy: { transfer_type: 'restaurant_payout', order_batch: 'batch_789' }
      };
      return metadataOptions[personaId] || {};
    }

    getInvoiceMetadata(personaId) {
      const metadataOptions = {
        mindora: { invoice_type: 'course_fee', semester: 'spring_2024' },
        stratus: { invoice_type: 'usage_billing', billing_period: 'march_2024' },
        procura: { invoice_type: 'bulk_order', net_terms: '30' }
      };
      return metadataOptions[personaId] || {};
    }

    getSubscriptionMetadata(personaId) {
      const metadataOptions = {
        pulseon: { plan_name: 'premium', features: 'unlimited_classes' },
        stratus: { plan_tier: 'enterprise', compute_hours: '1000' }
      };
      return metadataOptions[personaId] || {};
    }

    getCardMetadata(personaId) {
      const metadataOptions = {
        forksy: { card_purpose: 'delivery_payments', driver_id: 'driver_123' }
      };
      return metadataOptions[personaId] || {};
    }

    // Public API methods
    calculateMetrics() {
      const data = this.currentData;
      const fullMetrics = data._fullDatasetMetrics;
      const personaId = this.currentPersona;

      if (!fullMetrics) return [];

      // Return persona-specific metrics
      switch (personaId) {
        case 'modaic':
          return [
            { label: 'Total Revenue', value: this.formatCurrency(fullMetrics.totalRevenue), rawValue: fullMetrics.totalRevenue },
            { label: 'New Customers', value: this.formatNumber(fullMetrics.newCustomers), rawValue: fullMetrics.newCustomers },
            { label: 'Average Order Value', value: this.formatCurrency(fullMetrics.averageOrderValue), rawValue: fullMetrics.averageOrderValue },
            { label: 'Conversion Rate', value: this.formatPercentage(fullMetrics.conversionRate), rawValue: fullMetrics.conversionRate }
          ];
        case 'mindora':
          return [
            { label: 'Gross Volume', value: this.formatCurrency(fullMetrics.totalRevenue), rawValue: fullMetrics.totalRevenue },
            { label: 'Total Payments', value: this.formatNumber(fullMetrics.totalPayments), rawValue: fullMetrics.totalPayments },
            { label: 'Total Customers', value: this.formatNumber(fullMetrics.totalCustomers), rawValue: fullMetrics.totalCustomers },
            { label: 'Retention Rate', value: this.formatPercentage(fullMetrics.retentionRate), rawValue: fullMetrics.retentionRate }
          ];
        case 'keynest':
          return [
            { label: 'Total Revenue', value: this.formatCurrency(fullMetrics.totalRevenue), rawValue: fullMetrics.totalRevenue },
            { label: 'Connected Accounts', value: this.formatNumber(fullMetrics.connectedAccounts), rawValue: fullMetrics.connectedAccounts },
            { label: 'Total Customers', value: this.formatNumber(fullMetrics.totalCustomers), rawValue: fullMetrics.totalCustomers },
            { label: 'Average Order Value', value: this.formatCurrency(fullMetrics.averageOrderValue), rawValue: fullMetrics.averageOrderValue }
          ];
        case 'pulseon':
          return [
            { label: 'Total Revenue', value: this.formatCurrency(fullMetrics.totalRevenue), rawValue: fullMetrics.totalRevenue },
            { label: 'Active Subscribers', value: this.formatNumber(fullMetrics.activeSubscribers), rawValue: fullMetrics.activeSubscribers },
            { label: 'Average Order Value', value: this.formatCurrency(fullMetrics.averageOrderValue), rawValue: fullMetrics.averageOrderValue },
            { label: 'Churn Rate', value: this.formatPercentage(fullMetrics.churnRate), rawValue: fullMetrics.churnRate }
          ];
        case 'fluxly':
          return [
            { label: 'Gross Volume', value: this.formatCurrency(fullMetrics.grossVolume), rawValue: fullMetrics.grossVolume },
            { label: 'Total Customers', value: this.formatNumber(fullMetrics.totalCustomers), rawValue: fullMetrics.totalCustomers },
            { label: 'Trial Conversion Rate', value: this.formatPercentage(fullMetrics.trialConversionRate), rawValue: fullMetrics.trialConversionRate },
            { label: 'Average Order Value', value: this.formatCurrency(fullMetrics.averageOrderValue), rawValue: fullMetrics.averageOrderValue }
          ];
        case 'brightfund':
          return [
            { label: 'Gross Volume', value: this.formatCurrency(fullMetrics.grossVolume), rawValue: fullMetrics.grossVolume },
            { label: 'Customers', value: this.formatNumber(fullMetrics.customers), rawValue: fullMetrics.customers },
            { label: 'Retention Rate', value: this.formatPercentage(fullMetrics.retentionRate), rawValue: fullMetrics.retentionRate },
            { label: 'Payment Acceptance Rate', value: this.formatPercentage(fullMetrics.paymentAcceptanceRate), rawValue: fullMetrics.paymentAcceptanceRate }
          ];
        case 'procura':
          return [
            { label: 'Gross Volume', value: this.formatCurrency(fullMetrics.grossVolume), rawValue: fullMetrics.grossVolume },
            { label: 'Customers', value: this.formatNumber(fullMetrics.customers), rawValue: fullMetrics.customers },
            { label: 'Invoice Payment Rate', value: this.formatPercentage(fullMetrics.invoicePaymentRate), rawValue: fullMetrics.invoicePaymentRate },
            { label: 'Invoice Collection Time', value: `${fullMetrics.invoiceCollectionTime} days`, rawValue: fullMetrics.invoiceCollectionTime }
          ];
        case 'stratus':
          return [
            { label: 'Gross Revenue', value: this.formatCurrency(fullMetrics.grossRevenue), rawValue: fullMetrics.grossRevenue },
            { label: 'Active Subscribers', value: this.formatNumber(fullMetrics.activeSubscribers), rawValue: fullMetrics.activeSubscribers },
            { label: 'Net Revenue Retention', value: this.formatPercentage(fullMetrics.netRevenueRetention), rawValue: fullMetrics.netRevenueRetention },
            { label: 'Churn Rate', value: this.formatPercentage(fullMetrics.churnRate), rawValue: fullMetrics.churnRate }
          ];
        case 'forksy':
          return [
            { label: 'Net Volume from Sales', value: this.formatCurrency(fullMetrics.netVolumeFromSales), rawValue: fullMetrics.netVolumeFromSales },
            { label: 'Connected Accounts', value: this.formatNumber(fullMetrics.connectedAccounts), rawValue: fullMetrics.connectedAccounts },
            { label: 'Blocked Payments Rate', value: this.formatPercentage(fullMetrics.blockedPaymentsRate), rawValue: fullMetrics.blockedPaymentsRate },
            { label: 'Card Spend Volume', value: this.formatCurrency(fullMetrics.cardSpendVolume), rawValue: fullMetrics.cardSpendVolume }
          ];
        default:
          return [
            { label: 'Total Revenue', value: this.formatCurrency(fullMetrics.totalRevenue), rawValue: fullMetrics.totalRevenue },
            { label: 'Total Customers', value: this.formatNumber(fullMetrics.totalCustomers), rawValue: fullMetrics.totalCustomers },
            { label: 'Total Transactions', value: this.formatNumber(fullMetrics.totalTransactions), rawValue: fullMetrics.totalTransactions },
            { label: 'Average Order Value', value: this.formatCurrency(fullMetrics.averageOrderValue), rawValue: fullMetrics.averageOrderValue }
          ];
      }
    }

    getData(type) {
      return this.currentData[type] || [];
    }

    getCurrentPersona() {
      return this.currentPersona;
    }

    getCurrentStage() {
      return this.currentStage;
    }

    getAvailablePersonas() {
      return this.availablePersonas;
    }

    switchPersona(personaId, stage = null) {
      if (stage) this.currentStage = stage;
      this.currentPersona = personaId;
      
      const cacheKey = `${personaId}_${this.currentStage}`;
      
      if (this.cache.has(cacheKey)) {
        this.currentData = this.cache.get(cacheKey);
      } else {
        this.generateFallbackData(personaId);
      }
      
      // Notify subscribers
      this.subscribers.forEach(callback => {
        callback(this.currentData, personaId, this.currentStage);
      });
    }

    subscribe(callback) {
      this.subscribers.push(callback);
      return () => {
        const index = this.subscribers.indexOf(callback);
        if (index > -1) this.subscribers.splice(index, 1);
      };
    }

    // Formatting utilities
    formatCurrency(amount) {
      const dollars = amount / 100;
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      }).format(dollars);
    }

    formatNumber(num) {
      return new Intl.NumberFormat('en-US').format(num);
    }

    formatPercentage(rate) {
      return new Intl.NumberFormat('en-US', {
        style: 'percent',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      }).format(rate);
    }
  }

  // Persona Selector UI Component
  class PersonaSelectorUI {
    constructor(dataClient, options = {}) {
      this.dataClient = dataClient;
      this.options = {
        target: options.target || 'body',
        position: options.position || 'top-left',
        autoInject: options.autoInject !== false,
        onPersonaChange: options.onPersonaChange || (() => {}),
        ...options
      };
      
      this.currentPersona = this.dataClient.getCurrentPersona();
      this.currentStage = this.dataClient.getCurrentStage();
      
      if (this.options.autoInject) {
        this.inject();
      }
      
      this.setupEventListeners();
    }

    inject() {
      const targetElement = typeof this.options.target === 'string' 
        ? document.querySelector(this.options.target) 
        : this.options.target;
      
      if (!targetElement) {
        console.warn('Target element not found, injecting into body');
        document.body.appendChild(this.createElement());
      } else {
        targetElement.appendChild(this.createElement());
      }
      
      this.setupUIEvents();
    }

    createElement() {
      const container = document.createElement('div');
      container.className = 'persona-selector-container';
      container.innerHTML = this.getHTML();
      return container;
    }

    getHTML() {
      const personas = this.dataClient.getAvailablePersonas();
      const currentPersona = personas[this.currentPersona];
      
      return `
        <div class="persona-selector-button" id="persona-selector-button">
          <img class="persona-logo" id="current-persona-logo" 
               src="https://swanson-stripe.github.io/synthetic-dataset/docs/assets/${this.currentPersona}.png" 
               alt="${currentPersona.name}"
               onerror="this.style.display='none'">
          <div class="persona-selector-text">
            <div class="persona-name" id="current-persona-name">${currentPersona.name}</div>
          </div>
          <svg class="dropdown-arrow" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </div>

        <div class="persona-popover" id="persona-popover">
          <div class="popover-content">
            <div class="popover-logo-section">
              <img class="popover-persona-logo" id="popover-persona-logo" 
                   src="https://swanson-stripe.github.io/synthetic-dataset/docs/assets/${this.currentPersona}.png" 
                   alt="${currentPersona.name}"
                   onerror="this.style.display='none'">
              <div class="popover-title" id="popover-persona-name">${currentPersona.name}</div>
              <div class="popover-description" id="popover-persona-description">${currentPersona.description}</div>
            </div>
            
            <hr class="popover-divider">
            
            <div class="stage-section">
              <div class="stage-label">Business stage</div>
              <div class="stage-options">
                ${['early', 'growth', 'mature'].map(stage => `
                  <div class="stage-option ${stage === this.currentStage ? 'selected' : ''}" data-stage="${stage}">
                    <span class="stage-text">${stage.charAt(0).toUpperCase() + stage.slice(1)}</span>
                    <div class="stage-check">✓</div>
                  </div>
                `).join('')}
              </div>
              
              <button class="change-persona-btn" id="change-persona-btn">Change business</button>
            </div>
          </div>
        </div>

        ${this.getModalHTML()}
      `;
    }

    getModalHTML() {
      const personas = this.dataClient.getAvailablePersonas();
      
      return `
        <div class="persona-modal" id="persona-modal">
          <div class="modal-content">
            <div class="persona-list-panel">
              <div class="modal-header">
                <h3 class="modal-title">Choose a business</h3>
                <p class="modal-description">Select a business model to explore different payment scenarios and data patterns.</p>
              </div>
              
              <div class="personas-list">
                ${Object.values(personas).map(persona => `
                  <div class="persona-option ${persona.id === this.currentPersona ? 'selected' : ''}" data-persona="${persona.id}">
                    <img class="persona-option-logo" 
                         src="https://swanson-stripe.github.io/synthetic-dataset/docs/assets/${persona.id}.png" 
                         alt="${persona.name}"
                         onerror="this.style.display='none'">
                    <div class="persona-option-info">
                      <div class="persona-option-name">${persona.name}</div>
                      <div class="persona-option-type">${persona.business_model.replace(/_/g, ' ')}</div>
                    </div>
                  </div>
                `).join('')}
              </div>
              
              <div class="modal-footer-left">
                <button class="btn" id="modal-done">Done</button>
              </div>
            </div>
            
            <div class="persona-details-panel" id="persona-details-panel">
              <!-- Dynamic content populated by updatePersonaDetails -->
            </div>
          </div>
        </div>
      `;
    }

    setupUIEvents() {
      const selector = document.getElementById('persona-selector-button');
      const popover = document.getElementById('persona-popover');
      const modal = document.getElementById('persona-modal');
      const changeBtn = document.getElementById('change-persona-btn');
      const modalDone = document.getElementById('modal-done');

      // Selector toggle
      selector?.addEventListener('click', (e) => {
        e.stopPropagation();
        this.togglePopover();
      });

      // Stage selection
      const stageOptions = document.querySelectorAll('.stage-option');
      stageOptions.forEach(option => {
        option.addEventListener('click', (e) => {
          const stage = e.currentTarget.getAttribute('data-stage');
          this.selectStage(stage);
          this.closePopover();
        });
      });

      // Change persona button
      changeBtn?.addEventListener('click', () => {
        this.closePopover();
        this.openModal();
      });

      // Modal done button
      modalDone?.addEventListener('click', () => {
        this.applyPersonaSelection();
      });

      // Persona options in modal
      const personaOptions = document.querySelectorAll('.persona-option');
      personaOptions.forEach(option => {
        option.addEventListener('click', (e) => {
          this.selectPersonaInModal(e.currentTarget.getAttribute('data-persona'));
        });
      });

      // Close popover when clicking outside
      document.addEventListener('click', (e) => {
        if (!selector?.contains(e.target) && !popover?.contains(e.target)) {
          this.closePopover();
        }
      });

      // Close modal when clicking backdrop
      modal?.addEventListener('click', (e) => {
        if (e.target === modal) {
          this.closeModal();
        }
      });

      // Initialize persona details
      this.updatePersonaDetails(this.currentPersona);
    }

    setupEventListeners() {
      // Subscribe to data client changes
      this.dataClient.subscribe((data, personaId, stage) => {
        this.currentPersona = personaId;
        this.currentStage = stage;
        this.updateDisplay();
        this.options.onPersonaChange(data, personaId, stage);
      });
    }

    togglePopover() {
      const popover = document.getElementById('persona-popover');
      const selector = document.getElementById('persona-selector-button');
      
      popover?.classList.toggle('show');
      selector?.classList.toggle('open');
    }

    closePopover() {
      const popover = document.getElementById('persona-popover');
      const selector = document.getElementById('persona-selector-button');
      
      popover?.classList.remove('show');
      selector?.classList.remove('open');
    }

    openModal() {
      const modal = document.getElementById('persona-modal');
      modal?.classList.add('show');
      document.body.style.overflow = 'hidden';
    }

    closeModal() {
      const modal = document.getElementById('persona-modal');
      modal?.classList.remove('show');
      document.body.style.overflow = '';
    }

    selectStage(stage) {
      this.currentStage = stage;
      
      // Update UI
      const stageOptions = document.querySelectorAll('.stage-option');
      stageOptions.forEach(option => {
        option.classList.toggle('selected', option.getAttribute('data-stage') === stage);
      });
      
      // Update data
      this.dataClient.switchPersona(this.currentPersona, stage);
    }

    selectPersonaInModal(personaId) {
      // Update modal selection
      const personaOptions = document.querySelectorAll('.persona-option');
      personaOptions.forEach(option => {
        option.classList.toggle('selected', option.getAttribute('data-persona') === personaId);
      });
      
      // Update details panel
      this.updatePersonaDetails(personaId);
    }

    applyPersonaSelection() {
      const selected = document.querySelector('.persona-option.selected');
      if (selected) {
        const personaId = selected.getAttribute('data-persona');
        this.dataClient.switchPersona(personaId, this.currentStage);
      }
      this.closeModal();
    }

    updatePersonaDetails(personaId) {
      const personas = this.dataClient.getAvailablePersonas();
      const persona = personas[personaId];
      const detailsPanel = document.getElementById('persona-details-panel');
      
      if (detailsPanel && persona) {
        detailsPanel.innerHTML = `
          <h3 class="persona-details-title">${persona.name}</h3>
          <p class="persona-details-description">${persona.description}</p>
          
          <div class="products-section">
            <h4 class="products-title">Products used</h4>
            <ul class="products-list">
              ${persona.products.map(product => `<li>${product}</li>`).join('')}
            </ul>
          </div>
        `;
      }
    }

    updateDisplay() {
      const personas = this.dataClient.getAvailablePersonas();
      const currentPersona = personas[this.currentPersona];
      
      if (currentPersona) {
        // Update selector
        const logo = document.getElementById('current-persona-logo');
        const name = document.getElementById('current-persona-name');
        
        if (logo) {
          logo.src = `https://swanson-stripe.github.io/synthetic-dataset/docs/assets/${this.currentPersona}.png`;
          logo.alt = currentPersona.name;
        }
        
        if (name) {
          name.textContent = currentPersona.name;
        }

        // Update popover
        const popoverLogo = document.getElementById('popover-persona-logo');
        const popoverName = document.getElementById('popover-persona-name');
        const popoverDesc = document.getElementById('popover-persona-description');
        
        if (popoverLogo) {
          popoverLogo.src = `https://swanson-stripe.github.io/synthetic-dataset/docs/assets/${this.currentPersona}.png`;
          popoverLogo.alt = currentPersona.name;
        }
        
        if (popoverName) {
          popoverName.textContent = currentPersona.name;
        }
        
        if (popoverDesc) {
          popoverDesc.textContent = currentPersona.description;
        }

        // Update stage selection
        const stageOptions = document.querySelectorAll('.stage-option');
        stageOptions.forEach(option => {
          option.classList.toggle('selected', option.getAttribute('data-stage') === this.currentStage);
        });
      }
    }
  }

  // Main Dashboard Synthetic Data Kit Class
  class DashboardSyntheticData {
    constructor(options = {}) {
      this.options = {
        defaultPersona: 'modaic',
        defaultStage: 'growth',
        autoInject: true,
        target: 'body',
        position: 'top-left',
        onPersonaChange: null,
        ...options
      };
      
      // Auto-inject CSS
      injectCSS();
      
      // Initialize data client
      this.dataClient = new DataClient({
        defaultPersona: this.options.defaultPersona,
        defaultStage: this.options.defaultStage
      });
      
      // Initialize UI if auto-inject is enabled
      if (this.options.autoInject) {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
          document.addEventListener('DOMContentLoaded', () => this.initUI());
        } else {
          this.initUI();
        }
      }
    }

    initUI() {
      this.ui = new PersonaSelectorUI(this.dataClient, {
        target: this.options.target,
        position: this.options.position,
        autoInject: true,
        onPersonaChange: this.options.onPersonaChange
      });
    }

    // Public API methods
    getDataClient() {
      return this.dataClient;
    }

    getMetrics() {
      return this.dataClient.calculateMetrics();
    }

    getData(type) {
      return this.dataClient.getData(type);
    }

    getCurrentPersona() {
      return this.dataClient.getCurrentPersona();
    }

    getCurrentStage() {
      return this.dataClient.getCurrentStage();
    }

    getAvailablePersonas() {
      return this.dataClient.getAvailablePersonas();
    }

    switchPersona(personaId, stage = null) {
      this.dataClient.switchPersona(personaId, stage);
    }

    subscribe(callback) {
      return this.dataClient.subscribe(callback);
    }

    // Manual UI creation for advanced usage
    createSelector(targetElement, options = {}) {
      return new PersonaSelectorUI(this.dataClient, {
        target: targetElement,
        autoInject: true,
        ...options
      });
    }
  }

  // Export for global usage
  if (typeof window !== 'undefined') {
    window.DashboardSyntheticData = DashboardSyntheticData;
    
    // Auto-initialize with default options if data-auto-init is present
    document.addEventListener('DOMContentLoaded', () => {
      const autoInit = document.querySelector('[data-dashboard-synthetic-data-auto]');
      if (autoInit) {
        const options = {};
        
        // Parse options from data attributes
        if (autoInit.hasAttribute('data-persona')) {
          options.defaultPersona = autoInit.getAttribute('data-persona');
        }
        if (autoInit.hasAttribute('data-stage')) {
          options.defaultStage = autoInit.getAttribute('data-stage');
        }
        if (autoInit.hasAttribute('data-target')) {
          options.target = autoInit.getAttribute('data-target');
        }
        
        window.dashboardSyntheticData = new DashboardSyntheticData(options);
      }
    });
  }

  // Export for module systems
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = DashboardSyntheticData;
  }

})();
