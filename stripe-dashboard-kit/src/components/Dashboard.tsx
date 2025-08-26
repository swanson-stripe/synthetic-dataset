import React from 'react';
import clsx from 'clsx';
import { DataSource } from '../types/metrics';
import { useMetrics } from '../hooks/useMetrics';
import { MetricCard } from './MetricCard';
import { LineChart } from './LineChart';
import { BarChart } from './BarChart';
import { DataTable } from './DataTable';

export interface DashboardProps {
  dataSource: DataSource;
  layout?: 'stripe' | 'custom';
  theme?: 'light' | 'dark';
  refreshInterval?: number;
  onError?: (error: string) => void;
  className?: string;
  title?: string;
}

export const Dashboard: React.FC<DashboardProps> = ({
  dataSource,
  layout = 'stripe',
  theme = 'light',
  refreshInterval,
  onError,
  className,
  title = 'Payment Analytics Dashboard',
}) => {
  const {
    data,
    loading,
    error,
    refresh,
    metricCards,
    timeSeriesCharts,
    categoricalCharts,
    dataTables,
  } = useMetrics(dataSource, {
    refreshInterval,
    onError,
  });

  // Convert chart data to component props
  const convertChartData = (chart: any) => {
    const data = chart.labels.map((label: string, index: number) => {
      const point: any = { name: label };
      chart.datasets.forEach((dataset: any) => {
        point[dataset.label] = dataset.data[index];
      });
      return point;
    });

    return { data, chart };
  };

  const renderErrorState = () => (
    <div className="dashboard__error">
      <div className="error-message">
        <h3>Failed to load dashboard data</h3>
        <p>{error}</p>
        <button className="error-message__retry" onClick={refresh}>
          Try Again
        </button>
      </div>
    </div>
  );

  const renderLoadingState = () => (
    <div className={clsx('dashboard', `dashboard--${layout}`, `dashboard--${theme}`, className)}>
      <div className="dashboard__header">
        <div className="skeleton skeleton--text skeleton--large"></div>
      </div>

      {/* Loading metric cards */}
      <div className="dashboard__metric-cards">
        {Array.from({ length: 4 }).map((_, index) => (
          <MetricCard
            key={index}
            title=""
            value={0}
            format="number"
            loading={true}
          />
        ))}
      </div>

      {/* Loading charts */}
      <div className="dashboard__charts">
        <div className="dashboard__chart-row">
          <LineChart
            data={[]}
            lines={[]}
            xAxisKey="name"
            loading={true}
          />
          <BarChart
            data={[]}
            dataKey="value"
            loading={true}
          />
        </div>
      </div>

      {/* Loading table */}
      <div className="dashboard__tables">
        <DataTable
          columns={[]}
          data={[]}
          loading={true}
        />
      </div>
    </div>
  );

  if (error) {
    return renderErrorState();
  }

  if (loading) {
    return renderLoadingState();
  }

  return (
    <div className={clsx('dashboard', `dashboard--${layout}`, `dashboard--${theme}`, className)}>
      <div className="dashboard__header">
        <h1 className="dashboard__title">{title}</h1>
        <div className="dashboard__actions">
          <button className="dashboard__refresh" onClick={refresh}>
            Refresh
          </button>
        </div>
      </div>

      {/* Metric Cards */}
      {metricCards.length > 0 && (
        <div className="dashboard__metric-cards">
          {metricCards.map((card, index) => (
            <MetricCard
              key={card.id || index}
              title={card.title}
              value={card.value}
              format={card.format}
              change={card.change}
              sparkline={card.sparkline}
              description={card.description}
            />
          ))}
        </div>
      )}

      {/* Charts Section */}
      {(timeSeriesCharts.length > 0 || categoricalCharts.length > 0) && (
        <div className="dashboard__charts">
          {/* Time Series Charts */}
          {timeSeriesCharts.length > 0 && (
            <div className="dashboard__chart-row">
              {timeSeriesCharts.map((chart, index) => {
                const { data: chartData } = convertChartData(chart);
                const lines = chart.datasets.map((dataset: any) => ({
                  dataKey: dataset.label,
                  stroke: dataset.borderColor,
                  name: dataset.label,
                }));

                return (
                  <LineChart
                    key={index}
                    data={chartData}
                    lines={lines}
                    xAxisKey="name"
                    xAxisFormat="date"
                    yAxisFormat={chart.options?.scales?.y?.ticks?.callback === 'currency' ? 'currency' : 'number'}
                    title={chart.title}
                    height={350}
                  />
                );
              })}
            </div>
          )}

          {/* Categorical Charts */}
          {categoricalCharts.length > 0 && (
            <div className="dashboard__chart-row">
              {categoricalCharts.map((chart, index) => {
                const { data: chartData } = convertChartData(chart);

                return (
                  <BarChart
                    key={index}
                    data={chartData}
                    dataKey={chart.datasets[0]?.label || 'value'}
                    type={chart.type as 'bar' | 'pie' | 'doughnut'}
                    colors={chart.datasets[0]?.backgroundColor || undefined}
                    title={chart.title}
                    height={350}
                  />
                );
              })}
            </div>
          )}
        </div>
      )}

      {/* Data Tables */}
      {dataTables.length > 0 && (
        <div className="dashboard__tables">
          {dataTables.map((table, index) => (
            <DataTable
              key={index}
              title={table.title}
              columns={table.columns}
              data={table.data}
              pageSize={table.pagination?.page_size || 10}
              showPagination={table.pagination?.total_pages > 1}
            />
          ))}
        </div>
      )}

      {/* Empty State */}
      {!loading && metricCards.length === 0 && timeSeriesCharts.length === 0 && 
       categoricalCharts.length === 0 && dataTables.length === 0 && (
        <div className="dashboard__empty">
          <div className="empty-state">
            <h3>No data available</h3>
            <p>There's no data to display at the moment.</p>
            <button className="empty-state__retry" onClick={refresh}>
              Refresh Data
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
