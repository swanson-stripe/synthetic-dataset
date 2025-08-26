import { useState, useEffect, useCallback } from 'react';
import { DataSource, MetricsResponse, LoadingState } from '../types/metrics';

export const useDataLoader = (
  dataSource: DataSource,
  refreshInterval?: number,
  transform?: (data: any) => MetricsResponse
): LoadingState => {
  const [data, setData] = useState<MetricsResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      let result: MetricsResponse;

      if (typeof dataSource === 'string') {
        // Fetch from URL
        const response = await fetch(dataSource);
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        result = await response.json();
      } else {
        // Call function
        result = await dataSource();
      }

      // Apply transform if provided
      if (transform) {
        result = transform(result);
      }

      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load data');
    } finally {
      setLoading(false);
    }
  }, [dataSource, transform]);

  const refresh = useCallback(() => {
    fetchData();
  }, [fetchData]);

  // Initial load
  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Auto-refresh interval
  useEffect(() => {
    if (refreshInterval && refreshInterval > 0) {
      const interval = setInterval(fetchData, refreshInterval);
      return () => clearInterval(interval);
    }
  }, [fetchData, refreshInterval]);

  return { data, loading, error, refresh };
};
