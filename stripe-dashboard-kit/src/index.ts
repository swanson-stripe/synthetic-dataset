// Main exports for the dashboard kit
export { Dashboard } from './components/Dashboard';
export { MetricCard } from './components/MetricCard';
export { LineChart } from './components/LineChart';
export { BarChart } from './components/BarChart';
export { DataTable } from './components/DataTable';

// Hooks
export { useMetrics } from './hooks/useMetrics';
export { useDataLoader } from './hooks/useDataLoader';

// Utilities
export {
  formatCurrency,
  formatPercentage,
  formatNumber,
  formatDateTime,
  formatTime,
  formatValue,
  formatChange,
  truncate,
  formatCompactNumber,
} from './utils/formatters';

// Types
export type {
  MetricData,
  DataPoint,
  ChartData,
  ChartDataset,
  ColumnConfig,
  TableData,
  DashboardConfig,
  MetricsResponse,
  DataSource,
  LoadingState,
} from './types/metrics';

export type { MetricCardProps } from './components/MetricCard';
export type { LineChartProps, LineProps } from './components/LineChart';
export type { BarChartProps } from './components/BarChart';
export type { DataTableProps } from './components/DataTable';
export type { DashboardProps } from './components/Dashboard';

// CSS import for convenience
import './styles/components.css';
