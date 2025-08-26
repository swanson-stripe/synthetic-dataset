import { useState, useEffect, useCallback } from 'react';
import { DataSource, MetricsResponse, LoadingState } from '../types/metrics';
import { useDataLoader } from './useDataLoader';

export interface UseMetricsOptions {
  refreshInterval?: number;
  transform?: (data: any) => MetricsResponse;
  onError?: (error: string) => void;
  onLoad?: (data: MetricsResponse) => void;
}

export const useMetrics = (
  dataSource: DataSource,
  options: UseMetricsOptions = {}
): LoadingState & {
  metricCards: any[];
  timeSeriesCharts: any[];
  categoricalCharts: any[];
  dataTables: any[];
} => {
  const { refreshInterval, transform, onError, onLoad } = options;
  
  const { data, loading, error, refresh } = useDataLoader(
    dataSource,
    refreshInterval,
    transform
  );

  const [metricCards, setMetricCards] = useState<any[]>([]);
  const [timeSeriesCharts, setTimeSeriesCharts] = useState<any[]>([]);
  const [categoricalCharts, setCategoricalCharts] = useState<any[]>([]);
  const [dataTables, setDataTables] = useState<any[]>([]);

  // Process data when it changes
  useEffect(() => {
    if (data) {
      // Extract different data types
      setMetricCards(data.cards || []);
      
      // Separate charts by type
      const charts = data.charts || [];
      setTimeSeriesCharts(charts.filter(chart => chart.type === 'line'));
      setCategoricalCharts(charts.filter(chart => 
        ['bar', 'doughnut', 'pie'].includes(chart.type)
      ));
      
      setDataTables(data.tables || []);

      // Call onLoad callback
      if (onLoad) {
        onLoad(data);
      }
    }
  }, [data, onLoad]);

  // Handle errors
  useEffect(() => {
    if (error && onError) {
      onError(error);
    }
  }, [error, onError]);

  return {
    data,
    loading,
    error,
    refresh,
    metricCards,
    timeSeriesCharts,
    categoricalCharts,
    dataTables,
  };
};
