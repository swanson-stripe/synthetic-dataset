export interface MetricData {
  id: string;
  title: string;
  value: number;
  format: 'currency' | 'percentage' | 'number';
  change?: number;
  trend?: 'up' | 'down' | 'neutral';
  sparkline?: number[];
  description?: string;
}

export interface DataPoint {
  [key: string]: string | number | Date;
}

export interface ChartDataset {
  label: string;
  data: number[];
  borderColor?: string;
  backgroundColor?: string;
  tension?: number;
  fill?: boolean;
}

export interface ChartData {
  type: 'line' | 'bar' | 'doughnut' | 'pie';
  title: string;
  labels: string[];
  datasets: ChartDataset[];
  options?: {
    scales?: {
      x?: { beginAtZero?: boolean };
      y?: { 
        beginAtZero?: boolean; 
        min?: number;
        max?: number;
        ticks?: { callback?: string };
      };
    };
    plugins?: {
      legend?: { position?: string };
    };
  };
}

export interface ColumnConfig {
  key: string;
  title: string;
  sortable: boolean;
  format: 'text' | 'currency' | 'percentage' | 'number' | 'datetime' | 'status';
  width?: string;
}

export interface TableData {
  title: string;
  columns: ColumnConfig[];
  data: DataPoint[];
  pagination: {
    page_size: number;
    total_records: number;
    total_pages: number;
  };
}

export interface DashboardConfig {
  layout: {
    metric_cards: {
      order: number;
      columns: number;
      height: string;
    };
    time_series_charts: {
      order: number;
      columns: number;
      height: string;
    };
    categorical_charts: {
      order: number;
      columns: number;
      height: string;
    };
    data_tables: {
      order: number;
      columns: number;
      height: string;
    };
  };
  theme: {
    primary_color: string;
    success_color: string;
    error_color: string;
    warning_color: string;
    font_family?: string;
  };
  features: {
    real_time_updates: boolean;
    export_enabled: boolean;
    filters_enabled: boolean;
    responsive_design: boolean;
  };
  generated_at: string;
  data_summary: {
    charts_count: number;
    metric_cards_count: number;
    tables_count: number;
  };
}

export interface MetricsResponse {
  cards?: MetricData[];
  charts?: ChartData[];
  tables?: TableData[];
  comparison?: {
    current_period: {
      volume: number;
      transactions: number;
      success_rate: number;
      avg_amount: number;
    };
    previous_period: {
      volume: number;
      transactions: number;
      success_rate: number;
      avg_amount: number;
    };
  };
  date_range?: {
    start: string;
    end: string;
    total_days: number;
  };
}

export type DataSource = string | (() => Promise<MetricsResponse>);

export interface LoadingState {
  data: MetricsResponse | null;
  loading: boolean;
  error: string | null;
  refresh: () => void;
}
