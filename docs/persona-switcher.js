/**
 * Persona Switcher Component
 * Drop-in component for prototype bases to enable persona switching
 * Version: 1.0.0
 */

class PersonaSwitcher {
  constructor(dataClient, options = {}) {
    this.dataClient = dataClient;
    this.container = options.container;
    this.position = options.position || 'top-right';
    this.theme = options.theme || 'light';
    this.showInfo = options.showInfo !== false;
    this.onSwitch = options.onSwitch || (() => {});
    
    this.element = null;
    this.currentPersona = dataClient.currentPersona;
    
    this.init();
  }

  init() {
    this.createElement();
    this.attachStyles();
    this.bindEvents();
    
    // Subscribe to data client changes
    this.dataClient.subscribe((data, personaId) => {
      this.currentPersona = personaId;
      this.updateUI();
    });
  }

  createElement() {
    const switcher = document.createElement('div');
    switcher.className = `persona-switcher persona-switcher--${this.theme} persona-switcher--${this.position}`;
    switcher.innerHTML = this.getHTML();
    
    this.element = switcher;
    
    if (this.container) {
      this.container.appendChild(switcher);
    } else {
      document.body.appendChild(switcher);
    }
  }

  getHTML() {
    const personas = this.dataClient.getAvailablePersonas() || {};
    
    return `
      <div class="persona-switcher__header">
        <span class="persona-switcher__icon">🎭</span>
        <span class="persona-switcher__label">Business Scenario</span>
        <button class="persona-switcher__toggle" type="button">
          <span class="persona-switcher__current">${this.getPersonaDisplayName()}</span>
          <span class="persona-switcher__arrow">▼</span>
        </button>
      </div>
      
      <div class="persona-switcher__dropdown">
        <div class="persona-switcher__options">
          ${Object.entries(personas).map(([id, persona]) => `
            <button 
              class="persona-switcher__option ${id === this.currentPersona ? 'persona-switcher__option--active' : ''}"
              data-persona="${id}"
              type="button"
            >
              <div class="persona-switcher__option-main">
                <span class="persona-switcher__option-icon">${this.getPersonaIcon(persona.business_model)}</span>
                <div class="persona-switcher__option-content">
                  <div class="persona-switcher__option-name">${persona.name}</div>
                  <div class="persona-switcher__option-desc">${persona.description}</div>
                </div>
              </div>
              ${id === this.currentPersona ? '<span class="persona-switcher__option-check">✓</span>' : ''}
            </button>
          `).join('')}
        </div>
        
        ${this.showInfo ? `
          <div class="persona-switcher__info">
            <div class="persona-switcher__info-title">Current Scenario Details</div>
            <div class="persona-switcher__info-content" id="persona-info-content">
              ${this.getCurrentPersonaInfo()}
            </div>
          </div>
        ` : ''}
      </div>
      
      <div class="persona-switcher__loading">
        <div class="persona-switcher__spinner"></div>
        <span>Loading new scenario...</span>
      </div>
    `;
  }

  getPersonaDisplayName() {
    const personas = this.dataClient.getAvailablePersonas() || {};
    const current = personas[this.currentPersona];
    return current ? current.name : this.currentPersona;
  }

  getPersonaIcon(businessModel) {
    const icons = {
      'ecommerce': '🛍️',
      'marketplace': '🎓',
      'property_management': '🏠',
      'subscription': '💪',
      'creator_economy': '🎨',
      'education_marketplace': '📚',
      'default': '💼'
    };
    return icons[businessModel] || icons.default;
  }

  getCurrentPersonaInfo() {
    const personas = this.dataClient.getAvailablePersonas() || {};
    const current = personas[this.currentPersona];
    
    if (!current) return 'Loading...';
    
    return `
      <div class="persona-info-item">
        <strong>Business Model:</strong> ${current.business_model.replace('_', ' ')}
      </div>
      <div class="persona-info-item">
        <strong>Industry:</strong> ${current.industry?.replace('_', ' ') || 'N/A'}
      </div>
      <div class="persona-info-item">
        <strong>Data Scale:</strong> ${current.data_scale || 'N/A'}
      </div>
      <div class="persona-info-item">
        <strong>Key Features:</strong> ${(current.features || []).slice(0, 3).join(', ')}
      </div>
    `;
  }

  bindEvents() {
    const toggle = this.element.querySelector('.persona-switcher__toggle');
    const dropdown = this.element.querySelector('.persona-switcher__dropdown');
    const options = this.element.querySelectorAll('.persona-switcher__option');
    
    // Toggle dropdown
    toggle.addEventListener('click', (e) => {
      e.stopPropagation();
      this.toggleDropdown();
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
      if (!this.element.contains(e.target)) {
        this.closeDropdown();
      }
    });
    
    // Handle persona selection
    options.forEach(option => {
      option.addEventListener('click', async (e) => {
        e.stopPropagation();
        const personaId = option.dataset.persona;
        await this.switchToPersona(personaId);
      });
    });
  }

  toggleDropdown() {
    const dropdown = this.element.querySelector('.persona-switcher__dropdown');
    const isOpen = dropdown.classList.contains('persona-switcher__dropdown--open');
    
    if (isOpen) {
      this.closeDropdown();
    } else {
      this.openDropdown();
    }
  }

  openDropdown() {
    const dropdown = this.element.querySelector('.persona-switcher__dropdown');
    dropdown.classList.add('persona-switcher__dropdown--open');
    this.element.classList.add('persona-switcher--open');
  }

  closeDropdown() {
    const dropdown = this.element.querySelector('.persona-switcher__dropdown');
    dropdown.classList.remove('persona-switcher__dropdown--open');
    this.element.classList.remove('persona-switcher--open');
  }

  async switchToPersona(personaId) {
    if (personaId === this.currentPersona) {
      this.closeDropdown();
      return;
    }

    try {
      // Show loading state
      this.showLoading();
      
      // Switch persona in data client
      await this.dataClient.switchPersona(personaId);
      
      // Update UI
      this.currentPersona = personaId;
      this.updateUI();
      
      // Call callback
      this.onSwitch(personaId, this.dataClient.getCurrentPersona());
      
      // Hide loading and close dropdown
      this.hideLoading();
      this.closeDropdown();
      
    } catch (error) {
      console.error('Failed to switch persona:', error);
      this.hideLoading();
      this.showError('Failed to switch scenario. Please try again.');
    }
  }

  showLoading() {
    this.element.classList.add('persona-switcher--loading');
  }

  hideLoading() {
    this.element.classList.remove('persona-switcher--loading');
  }

  showError(message) {
    // You could implement a toast notification here
    alert(message);
  }

  updateUI() {
    // Update current persona display
    const currentSpan = this.element.querySelector('.persona-switcher__current');
    if (currentSpan) {
      currentSpan.textContent = this.getPersonaDisplayName();
    }
    
    // Update active option
    const options = this.element.querySelectorAll('.persona-switcher__option');
    options.forEach(option => {
      const isActive = option.dataset.persona === this.currentPersona;
      option.classList.toggle('persona-switcher__option--active', isActive);
      
      const check = option.querySelector('.persona-switcher__option-check');
      if (check) {
        check.style.display = isActive ? 'block' : 'none';
      } else if (isActive) {
        option.innerHTML += '<span class="persona-switcher__option-check">✓</span>';
      }
    });
    
    // Update info panel if visible
    if (this.showInfo) {
      const infoContent = this.element.querySelector('#persona-info-content');
      if (infoContent) {
        infoContent.innerHTML = this.getCurrentPersonaInfo();
      }
    }
  }

  attachStyles() {
    if (document.querySelector('#persona-switcher-styles')) return;
    
    const styles = document.createElement('style');
    styles.id = 'persona-switcher-styles';
    styles.textContent = this.getCSS();
    document.head.appendChild(styles);
  }

  getCSS() {
    return `
      .persona-switcher {
        position: fixed;
        z-index: 9999;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 14px;
        line-height: 1.4;
        color: #374151;
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        min-width: 280px;
        max-width: 400px;
      }
      
      .persona-switcher--top-right {
        top: 20px;
        right: 20px;
      }
      
      .persona-switcher--top-left {
        top: 20px;
        left: 20px;
      }
      
      .persona-switcher--bottom-right {
        bottom: 20px;
        right: 20px;
      }
      
      .persona-switcher--bottom-left {
        bottom: 20px;
        left: 20px;
      }
      
      .persona-switcher--dark {
        color: #f3f4f6;
        background: #1f2937;
        border-color: #374151;
      }
      
      .persona-switcher__header {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 12px 16px;
        border-bottom: 1px solid #e5e7eb;
      }
      
      .persona-switcher--dark .persona-switcher__header {
        border-bottom-color: #374151;
      }
      
      .persona-switcher__icon {
        font-size: 16px;
      }
      
      .persona-switcher__label {
        font-weight: 500;
        flex-shrink: 0;
      }
      
      .persona-switcher__toggle {
        background: none;
        border: none;
        padding: 0;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 8px;
        color: inherit;
        flex: 1;
        min-width: 0;
      }
      
      .persona-switcher__current {
        font-weight: 500;
        color: #6366f1;
        flex: 1;
        text-align: left;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      
      .persona-switcher__arrow {
        font-size: 12px;
        transition: transform 0.2s;
        flex-shrink: 0;
      }
      
      .persona-switcher--open .persona-switcher__arrow {
        transform: rotate(180deg);
      }
      
      .persona-switcher__dropdown {
        display: none;
        max-height: 400px;
        overflow-y: auto;
      }
      
      .persona-switcher__dropdown--open {
        display: block;
      }
      
      .persona-switcher__options {
        padding: 8px 0;
      }
      
      .persona-switcher__option {
        width: 100%;
        background: none;
        border: none;
        padding: 12px 16px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: background-color 0.2s;
        text-align: left;
      }
      
      .persona-switcher__option:hover {
        background: #f9fafb;
      }
      
      .persona-switcher--dark .persona-switcher__option:hover {
        background: #374151;
      }
      
      .persona-switcher__option--active {
        background: #eef2ff;
      }
      
      .persona-switcher--dark .persona-switcher__option--active {
        background: #312e81;
      }
      
      .persona-switcher__option-main {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        flex: 1;
        min-width: 0;
      }
      
      .persona-switcher__option-icon {
        font-size: 18px;
        flex-shrink: 0;
      }
      
      .persona-switcher__option-content {
        flex: 1;
        min-width: 0;
      }
      
      .persona-switcher__option-name {
        font-weight: 500;
        margin-bottom: 2px;
      }
      
      .persona-switcher__option-desc {
        font-size: 12px;
        color: #6b7280;
        line-height: 1.3;
      }
      
      .persona-switcher--dark .persona-switcher__option-desc {
        color: #9ca3af;
      }
      
      .persona-switcher__option-check {
        color: #059669;
        font-weight: bold;
        flex-shrink: 0;
      }
      
      .persona-switcher__info {
        border-top: 1px solid #e5e7eb;
        padding: 12px 16px;
        background: #f9fafb;
      }
      
      .persona-switcher--dark .persona-switcher__info {
        border-top-color: #374151;
        background: #374151;
      }
      
      .persona-switcher__info-title {
        font-weight: 500;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
        color: #6b7280;
      }
      
      .persona-switcher--dark .persona-switcher__info-title {
        color: #9ca3af;
      }
      
      .persona-info-item {
        margin-bottom: 6px;
        font-size: 12px;
        line-height: 1.4;
      }
      
      .persona-info-item:last-child {
        margin-bottom: 0;
      }
      
      .persona-switcher__loading {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255, 255, 255, 0.95);
        display: none;
        align-items: center;
        justify-content: center;
        gap: 12px;
        border-radius: 8px;
      }
      
      .persona-switcher--dark .persona-switcher__loading {
        background: rgba(31, 41, 55, 0.95);
      }
      
      .persona-switcher--loading .persona-switcher__loading {
        display: flex;
      }
      
      .persona-switcher__spinner {
        width: 16px;
        height: 16px;
        border: 2px solid #e5e7eb;
        border-top: 2px solid #6366f1;
        border-radius: 50%;
        animation: persona-spinner 1s linear infinite;
      }
      
      @keyframes persona-spinner {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
      
      @media (max-width: 640px) {
        .persona-switcher {
          position: fixed;
          top: auto !important;
          bottom: 20px !important;
          left: 20px !important;
          right: 20px !important;
          min-width: 0;
          max-width: none;
        }
      }
    `;
  }

  // Destroy the switcher
  destroy() {
    if (this.element) {
      this.element.remove();
    }
  }
}

// Export for both CommonJS and ES6 modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = PersonaSwitcher;
}
if (typeof window !== 'undefined') {
  window.PersonaSwitcher = PersonaSwitcher;
}
