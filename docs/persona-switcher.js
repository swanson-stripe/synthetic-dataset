/**
 * Persona Switcher Component
 * Adds dynamic persona switching to prototypes
 * Version: 1.0.0
 */

class PersonaSwitcher {
  constructor(dataClient, options = {}) {
    this.dataClient = dataClient;
    this.options = {
      position: 'top-right',
      showLabels: true,
      style: 'dropdown',
      onSwitch: null,
      ...options
    };
    
    this.isOpen = false;
    this.currentPersona = this.dataClient.currentPersona;
    
    this.render();
    this.bindEvents();
  }

  render() {
    // Create switcher container
    this.container = document.createElement('div');
    this.container.className = 'persona-switcher';
    this.container.innerHTML = this.getHTML();
    
    // Apply styles
    this.addStyles();
    
    // Position it
    this.position();
    
    // Add to page
    document.body.appendChild(this.container);
    
    // Update current selection
    this.updateCurrentSelection();
  }

  getHTML() {
    const personas = this.dataClient.getAvailablePersonas() || {};
    const currentPersona = personas[this.currentPersona] || { name: 'Loading...', business_model: 'unknown' };
    
    return `
      <div class="persona-switcher-trigger" id="persona-trigger">
        <span class="persona-icon">${this.getPersonaIcon(currentPersona.business_model)}</span>
        <span class="persona-name">${currentPersona.name}</span>
        <span class="persona-arrow">▼</span>
      </div>
      <div class="persona-switcher-dropdown" id="persona-dropdown">
        <div class="persona-switcher-header">Switch Business Model</div>
        ${Object.entries(personas).map(([id, persona]) => `
          <div class="persona-option ${id === this.currentPersona ? 'active' : ''}" 
               data-persona="${id}">
            <span class="persona-icon">${this.getPersonaIcon(persona.business_model)}</span>
            <div class="persona-info">
              <div class="persona-name">${persona.name}</div>
              <div class="persona-description">${persona.description || persona.business_model}</div>
            </div>
          </div>
        `).join('')}
      </div>
    `;
  }

  addStyles() {
    if (document.getElementById('persona-switcher-styles')) return;
    
    const style = document.createElement('style');
    style.id = 'persona-switcher-styles';
    style.textContent = `
      .persona-switcher {
        position: fixed;
        z-index: 10000;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      }
      
      .persona-switcher-trigger {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 8px 12px;
        display: flex;
        align-items: center;
        gap: 8px;
        cursor: pointer;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        transition: all 0.2s;
        min-width: 200px;
      }
      
      .persona-switcher-trigger:hover {
        border-color: #635bff;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
      }
      
      .persona-icon {
        font-size: 16px;
        flex-shrink: 0;
      }
      
      .persona-name {
        flex: 1;
        font-weight: 500;
        color: #1e293b;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      
      .persona-arrow {
        color: #64748b;
        font-size: 12px;
        transition: transform 0.2s;
      }
      
      .persona-switcher.open .persona-arrow {
        transform: rotate(180deg);
      }
      
      .persona-switcher-dropdown {
        position: absolute;
        top: calc(100% + 4px);
        left: 0;
        right: 0;
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
        max-height: 300px;
        overflow-y: auto;
        opacity: 0;
        visibility: hidden;
        transform: translateY(-8px);
        transition: all 0.2s;
      }
      
      .persona-switcher.open .persona-switcher-dropdown {
        opacity: 1;
        visibility: visible;
        transform: translateY(0);
      }
      
      .persona-switcher-header {
        padding: 12px 16px;
        font-size: 12px;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border-bottom: 1px solid #f1f5f9;
      }
      
      .persona-option {
        padding: 12px 16px;
        display: flex;
        align-items: center;
        gap: 12px;
        cursor: pointer;
        transition: background-color 0.2s;
        border-bottom: 1px solid #f8fafc;
      }
      
      .persona-option:last-child {
        border-bottom: none;
      }
      
      .persona-option:hover {
        background: #f8fafc;
      }
      
      .persona-option.active {
        background: #eef2ff;
        border-color: #e0e7ff;
      }
      
      .persona-info {
        flex: 1;
      }
      
      .persona-option .persona-name {
        font-size: 14px;
        font-weight: 500;
        color: #1e293b;
        margin-bottom: 2px;
      }
      
      .persona-description {
        font-size: 12px;
        color: #64748b;
        line-height: 1.3;
      }
      
      /* Position variants */
      .persona-switcher.position-top-right {
        top: 20px;
        right: 20px;
      }
      
      .persona-switcher.position-top-left {
        top: 20px;
        left: 20px;
      }
      
      .persona-switcher.position-bottom-right {
        bottom: 20px;
        right: 20px;
      }
      
      .persona-switcher.position-bottom-left {
        bottom: 20px;
        left: 20px;
      }
    `;
    
    document.head.appendChild(style);
  }

  position() {
    this.container.classList.add(`position-${this.options.position}`);
  }

  bindEvents() {
    const trigger = this.container.querySelector('#persona-trigger');
    const dropdown = this.container.querySelector('#persona-dropdown');
    
    // Toggle dropdown
    trigger.addEventListener('click', (e) => {
      e.stopPropagation();
      this.toggle();
    });
    
    // Handle persona selection
    dropdown.addEventListener('click', (e) => {
      const option = e.target.closest('.persona-option');
      if (option) {
        const personaId = option.dataset.persona;
        this.switchPersona(personaId);
      }
    });
    
    // Close when clicking outside
    document.addEventListener('click', () => {
      this.close();
    });
    
    // Prevent dropdown clicks from closing
    dropdown.addEventListener('click', (e) => {
      e.stopPropagation();
    });
  }

  toggle() {
    if (this.isOpen) {
      this.close();
    } else {
      this.open();
    }
  }

  open() {
    this.isOpen = true;
    this.container.classList.add('open');
  }

  close() {
    this.isOpen = false;
    this.container.classList.remove('open');
  }

  async switchPersona(personaId) {
    if (personaId === this.currentPersona) {
      this.close();
      return;
    }

    // Show loading state
    const trigger = this.container.querySelector('#persona-trigger');
    const originalHTML = trigger.innerHTML;
    trigger.innerHTML = `
      <span class="persona-icon">⏳</span>
      <span class="persona-name">Switching...</span>
      <span class="persona-arrow">▼</span>
    `;

    try {
      // Switch persona in data client
      await this.dataClient.switchPersona(personaId);
      
      this.currentPersona = personaId;
      this.updateCurrentSelection();
      
      // Notify callback
      if (this.options.onSwitch) {
        const personas = this.dataClient.getAvailablePersonas();
        this.options.onSwitch(personaId, personas[personaId]);
      }
      
    } catch (error) {
      console.error('Failed to switch persona:', error);
      trigger.innerHTML = originalHTML;
    }
    
    this.close();
  }

  updateCurrentSelection() {
    const personas = this.dataClient.getAvailablePersonas() || {};
    const currentPersona = personas[this.currentPersona] || { 
      name: this.currentPersona, 
      business_model: 'unknown' 
    };
    
    // Update trigger
    const trigger = this.container.querySelector('#persona-trigger');
    trigger.innerHTML = `
      <span class="persona-icon">${this.getPersonaIcon(currentPersona.business_model)}</span>
      <span class="persona-name">${currentPersona.name}</span>
      <span class="persona-arrow">▼</span>
    `;
    
    // Update active state in dropdown
    this.container.querySelectorAll('.persona-option').forEach(option => {
      option.classList.toggle('active', option.dataset.persona === this.currentPersona);
    });
  }

  getPersonaIcon(businessModel) {
    const icons = {
      'ecommerce': '🛍️',
      'marketplace': '🌐',
      'education_marketplace': '🎓',
      'property_management': '🏠',
      'subscription': '💪',
      'creator_economy': '🎨',
      'nonprofit': '❤️',
      'b2b_wholesale': '🏥',
      'saas': '☁️',
      'food_delivery': '🍕',
      'rideshare': '🚗',
      'unknown': '💼'
    };
    
    return icons[businessModel] || icons.unknown;
  }

  // Public API
  refresh() {
    this.container.innerHTML = this.getHTML();
    this.bindEvents();
    this.updateCurrentSelection();
  }

  destroy() {
    if (this.container && this.container.parentNode) {
      this.container.parentNode.removeChild(this.container);
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