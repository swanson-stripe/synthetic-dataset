/**
 * Dashboard Synthetic Data - React Component Kit
 * Drop-in React components with pre-built styling and UX
 * Version: 1.0.0
 */

(function() {
  'use strict';

  // React component source code as strings
  const ReactComponents = {
    
    // Hook for managing dashboard data
    useDashboardData: `
import { useState, useEffect } from 'react'

interface DataKit {
  getMetrics: () => any[]
  getData: (type: string) => any[]
  switchPersona: (persona: string, stage?: string) => void
  getCurrentPersona: () => string
  getCurrentStage: () => string
  getAvailablePersonas: () => any
  subscribe: (callback: Function) => Function
}

interface UseDashboardDataOptions {
  defaultPersona?: string
  defaultStage?: string
  onPersonaChange?: (data: any, persona: string, stage: string) => void
}

export function useDashboardData(options: UseDashboardDataOptions = {}) {
  const [kit, setKit] = useState<DataKit | null>(null)
  const [metrics, setMetrics] = useState<any[]>([])
  const [payments, setPayments] = useState<any[]>([])
  const [customers, setCustomers] = useState<any[]>([])
  const [currentPersona, setCurrentPersona] = useState<string>('')
  const [currentStage, setCurrentStage] = useState<string>('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let mounted = true
    
    const loadDataKit = async () => {
      try {
        // Check if script already loaded
        if (!(window as any).DashboardSyntheticData) {
          const script = document.createElement('script')
          script.src = 'https://swanson-stripe.github.io/synthetic-dataset/docs/dashboard-synthetic-data.js'
          
          await new Promise((resolve, reject) => {
            script.onload = resolve
            script.onerror = reject
            document.head.appendChild(script)
          })
        }

        if (!mounted) return

        const newKit = new (window as any).DashboardSyntheticData({
          autoInject: false, // React handles UI
          defaultPersona: options.defaultPersona || 'modaic',
          defaultStage: options.defaultStage || 'growth',
          onPersonaChange: (data: any, persona: string, stage: string) => {
            if (mounted) {
              updateData(newKit)
              options.onPersonaChange?.(data, persona, stage)
            }
          }
        })
        
        if (mounted) {
          setKit(newKit)
          updateData(newKit)
          setLoading(false)
        }
      } catch (err) {
        if (mounted) {
          setError('Failed to load dashboard data')
          setLoading(false)
        }
      }
    }

    loadDataKit()
    
    return () => {
      mounted = false
    }
  }, [])

  const updateData = (dataKit: DataKit) => {
    setMetrics(dataKit.getMetrics())
    setPayments(dataKit.getData('payments'))
    setCustomers(dataKit.getData('customers'))
    setCurrentPersona(dataKit.getCurrentPersona())
    setCurrentStage(dataKit.getCurrentStage())
  }

  const switchPersona = (persona: string, stage?: string) => {
    if (kit) {
      kit.switchPersona(persona, stage)
    }
  }

  return {
    kit,
    metrics,
    payments,
    customers,
    currentPersona,
    currentStage,
    loading,
    error,
    switchPersona,
    availablePersonas: kit?.getAvailablePersonas() || {},
    getData: (type: string) => kit?.getData(type) || []
  }
}`,

    // Persona Selector Component
    PersonaSelector: `
import { useState, useRef, useEffect } from 'react'

interface PersonaSelectorProps {
  currentPersona: string
  currentStage: string
  availablePersonas: any
  onPersonaChange: (persona: string) => void
  onStageChange: (stage: string) => void
  className?: string
}

export function PersonaSelector({ 
  currentPersona, 
  currentStage,
  availablePersonas, 
  onPersonaChange, 
  onStageChange,
  className = '' 
}: PersonaSelectorProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [showModal, setShowModal] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)
  
  const currentPersonaData = availablePersonas[currentPersona]
  const stages = ['early', 'growth', 'mature']
  
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }
    
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])
  
  if (!currentPersonaData) return null

  const getPersonaLogo = (personaId: string) => 
    \`https://swanson-stripe.github.io/synthetic-dataset/docs/assets/\${personaId}.png\`

  return (
    <>
      <div className={\`relative \${className}\`} ref={dropdownRef}>
        {/* Main Selector Button */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="flex items-center gap-3 bg-white border border-gray-200 rounded-xl px-4 py-3 hover:bg-gray-50 transition-all duration-200 shadow-sm min-w-[240px]"
        >
          <img 
            src={getPersonaLogo(currentPersona)}
            alt={currentPersonaData.name}
            className="w-8 h-8 rounded-lg object-cover"
            onError={(e) => {
              const target = e.target as HTMLImageElement
              target.style.display = 'none'
            }}
          />
          <div className="flex-1 text-left">
            <div className="font-medium text-gray-900">{currentPersonaData.name}</div>
          </div>
          <svg 
            className={\`w-3 h-3 text-gray-400 transition-transform duration-200 \${isOpen ? 'rotate-180' : ''}\`}
            fill="currentColor" 
            viewBox="0 0 20 20"
          >
            <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </button>

        {/* Dropdown Popover */}
        {isOpen && (
          <div className="absolute top-full left-0 right-0 mt-2 bg-white border border-gray-200 rounded-2xl shadow-xl z-50 overflow-hidden">
            {/* Current Persona Info */}
            <div className="p-6 text-center border-b border-gray-100">
              <img 
                src={getPersonaLogo(currentPersona)}
                alt={currentPersonaData.name}
                className="w-12 h-12 rounded-lg object-cover mx-auto mb-3"
                onError={(e) => {
                  const target = e.target as HTMLImageElement
                  target.style.display = 'none'
                }}
              />
              <h3 className="font-semibold text-lg text-gray-900 mb-2">{currentPersonaData.name}</h3>
              <p className="text-sm text-gray-500 mb-4">{currentPersonaData.description}</p>
              
              {/* Stage Selection */}
              <div className="space-y-2">
                <p className="text-sm font-medium text-gray-600">Business stage</p>
                <div className="space-y-1">
                  {stages.map((stage) => (
                    <button
                      key={stage}
                      onClick={() => {
                        onStageChange(stage)
                        setIsOpen(false)
                      }}
                      className={\`w-full flex items-center justify-between px-2 py-2 rounded-lg transition-colors \${
                        stage === currentStage 
                          ? 'bg-gray-100' 
                          : 'hover:bg-gray-50'
                      }\`}
                    >
                      <span className="text-sm capitalize">{stage}</span>
                      {stage === currentStage && (
                        <div className="w-5 h-5 bg-gray-600 rounded-full flex items-center justify-center">
                          <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                          </svg>
                        </div>
                      )}
                    </button>
                  ))}
                </div>
                
                <button
                  onClick={() => {
                    setShowModal(true)
                    setIsOpen(false)
                  }}
                  className="text-sm text-gray-700 hover:text-gray-900 underline mt-4"
                >
                  Change business
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Modal for Persona Selection */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl max-w-4xl w-full max-h-[80vh] overflow-hidden flex">
            {/* Left Panel - Persona List */}
            <div className="w-1/2 p-6 border-r border-gray-200 flex flex-col">
              <div className="mb-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-2">Choose a business</h2>
                <p className="text-gray-600">Select a business model to explore different payment scenarios.</p>
              </div>
              
              <div className="flex-1 overflow-y-auto space-y-2">
                {Object.values(availablePersonas).map((persona: any) => (
                  <button
                    key={persona.id}
                    onClick={() => onPersonaChange(persona.id)}
                    className={\`w-full flex items-center gap-3 p-3 rounded-lg border-2 transition-all \${
                      persona.id === currentPersona
                        ? 'border-purple-500 bg-purple-50'
                        : 'border-transparent hover:bg-gray-50'
                    }\`}
                  >
                    <img 
                      src={getPersonaLogo(persona.id)}
                      alt={persona.name}
                      className="w-10 h-10 rounded-lg object-cover"
                      onError={(e) => {
                        const target = e.target as HTMLImageElement
                        target.style.display = 'none'
                      }}
                    />
                    <div className="text-left">
                      <div className="font-medium text-gray-900">{persona.name}</div>
                      <div className="text-sm text-gray-500">{persona.business_model?.replace(/_/g, ' ')}</div>
                    </div>
                  </button>
                ))}
              </div>
              
              <button
                onClick={() => setShowModal(false)}
                className="w-full mt-6 px-4 py-3 bg-white border border-gray-300 rounded-lg font-medium text-gray-700 hover:bg-gray-50 transition-colors"
              >
                Done
              </button>
            </div>

            {/* Right Panel - Persona Details */}
            <div className="w-1/2 p-6 overflow-y-auto">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">{currentPersonaData.name}</h3>
              <p className="text-gray-600 mb-6 leading-relaxed">{currentPersonaData.description}</p>
              
              <div>
                <h4 className="font-medium text-gray-900 mb-3">Products used</h4>
                <ul className="space-y-2">
                  {currentPersonaData.products?.map((product: string, index: number) => (
                    <li key={index} className="text-gray-600 flex items-center gap-2">
                      <div className="w-1.5 h-1.5 bg-gray-400 rounded-full"></div>
                      {product}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  )
}`,

    // Metric Cards Component
    MetricCards: `
interface Metric {
  label: string
  value: string
  rawValue: number
}

interface MetricCardsProps {
  metrics: Metric[]
  className?: string
}

export function MetricCards({ metrics, className = '' }: MetricCardsProps) {
  if (!metrics.length) {
    return (
      <div className={\`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 \${className}\`}>
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="bg-white p-6 rounded-xl border border-gray-200 animate-pulse">
            <div className="h-4 bg-gray-200 rounded mb-3"></div>
            <div className="h-8 bg-gray-200 rounded"></div>
          </div>
        ))}
      </div>
    )
  }

  return (
    <div className={\`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 \${className}\`}>
      {metrics.map((metric, index) => (
        <div key={metric.label} className="bg-white p-6 rounded-xl border border-gray-200 hover:shadow-lg transition-shadow duration-200">
          <div className="text-sm font-medium text-gray-500 mb-2">{metric.label}</div>
          <div className="text-2xl font-bold text-gray-900">{metric.value}</div>
        </div>
      ))}
    </div>
  )
}`,

    // Payments Table Component
    PaymentsTable: `
interface Payment {
  id: string
  amount: number
  status: string
  created: number
  customer: string
}

interface PaymentsTableProps {
  payments: Payment[]
  className?: string
}

export function PaymentsTable({ payments, className = '' }: PaymentsTableProps) {
  const formatCurrency = (cents: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(cents / 100)
  }

  const formatDate = (timestamp: number) => {
    return new Date(timestamp * 1000).toLocaleDateString()
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'succeeded': return 'bg-green-100 text-green-800'
      case 'pending': return 'bg-yellow-100 text-yellow-800'
      case 'failed': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  if (!payments.length) {
    return (
      <div className={\`bg-white rounded-xl border border-gray-200 \${className}\`}>
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-medium text-gray-900">Recent Payments</h2>
        </div>
        <div className="p-6">
          <div className="animate-pulse space-y-4">
            {[1, 2, 3, 4, 5].map((i) => (
              <div key={i} className="flex space-x-4">
                <div className="h-4 bg-gray-200 rounded flex-1"></div>
                <div className="h-4 bg-gray-200 rounded w-20"></div>
                <div className="h-4 bg-gray-200 rounded w-16"></div>
                <div className="h-4 bg-gray-200 rounded w-24"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className={\`bg-white rounded-xl border border-gray-200 overflow-hidden \${className}\`}>
      <div className="px-6 py-4 border-b border-gray-200">
        <h2 className="text-lg font-medium text-gray-900">Recent Payments</h2>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {payments.slice(0, 10).map((payment) => (
              <tr key={payment.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-900">{payment.id}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {formatCurrency(payment.amount)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={\`inline-flex px-2 py-1 text-xs font-semibold rounded-full \${getStatusColor(payment.status)}\`}>
                    {payment.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {formatDate(payment.created)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}`,

    // Complete Dashboard Component
    DashboardKit: `
import { useDashboardData } from './useDashboardData'
import { PersonaSelector } from './PersonaSelector'
import { MetricCards } from './MetricCards'
import { PaymentsTable } from './PaymentsTable'

interface DashboardKitProps {
  defaultPersona?: string
  defaultStage?: string
  onPersonaChange?: (data: any, persona: string, stage: string) => void
  className?: string
}

export function DashboardKit({ 
  defaultPersona, 
  defaultStage, 
  onPersonaChange, 
  className = '' 
}: DashboardKitProps) {
  const { 
    metrics, 
    payments, 
    currentPersona, 
    currentStage,
    loading, 
    error, 
    switchPersona,
    availablePersonas,
    kit
  } = useDashboardData({ defaultPersona, defaultStage, onPersonaChange })

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <div className="text-red-800 font-medium">Error loading dashboard data</div>
        <div className="text-red-600 text-sm mt-1">{error}</div>
      </div>
    )
  }

  if (loading) {
    return (
      <div className={\`space-y-6 \${className}\`}>
        <div className="flex justify-between items-center">
          <div className="h-8 bg-gray-200 rounded w-48 animate-pulse"></div>
          <div className="h-12 bg-gray-200 rounded w-60 animate-pulse"></div>
        </div>
        <MetricCards metrics={[]} />
        <PaymentsTable payments={[]} />
      </div>
    )
  }

  const handleStageChange = (stage: string) => {
    if (kit) {
      kit.switchPersona(currentPersona, stage)
    }
  }

  return (
    <div className={\`space-y-6 \${className}\`}>
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Business Dashboard</h1>
        <PersonaSelector
          currentPersona={currentPersona}
          currentStage={currentStage}
          availablePersonas={availablePersonas}
          onPersonaChange={switchPersona}
          onStageChange={handleStageChange}
        />
      </div>

      {/* Metrics */}
      <MetricCards metrics={metrics} />

      {/* Payments Table */}
      <PaymentsTable payments={payments} />
    </div>
  )
}`
  };

  // Instructions for usage
  const UsageInstructions = {
    quickStart: \`
// Quick start - Complete dashboard in one component
import DashboardKit from './path/to/components'

export default function Dashboard() {
  return (
    <DashboardKit 
      defaultPersona="modaic"
      onPersonaChange={(data, persona, stage) => {
        console.log('Switched to:', persona, stage)
      }}
    />
  )
}
\`,

    customUsage: \`
// Custom usage - Individual components
import { useDashboardData, PersonaSelector, MetricCards, PaymentsTable } from './path/to/components'

export default function Dashboard() {
  const { 
    metrics, 
    payments, 
    currentPersona, 
    currentStage,
    switchPersona,
    availablePersonas 
  } = useDashboardData()

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">My Dashboard</h1>
        <PersonaSelector 
          currentPersona={currentPersona}
          currentStage={currentStage}
          availablePersonas={availablePersonas}
          onPersonaChange={switchPersona}
          onStageChange={(stage) => switchPersona(currentPersona, stage)}
        />
      </div>
      <MetricCards metrics={metrics} />
      <PaymentsTable payments={payments} />
    </div>
  )
}
\`
  };

  // Export all components and instructions
  if (typeof window !== 'undefined') {
    window.DashboardSyntheticDataReact = {
      components: ReactComponents,
      usage: UsageInstructions
    };
  }

  // Export for module systems
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
      components: ReactComponents,
      usage: UsageInstructions
    };
  }

})();
