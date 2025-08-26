import React from 'react';
import { LineChart, Line, ResponsiveContainer } from 'recharts';
import clsx from 'clsx';
import { formatValue, formatChange } from '../utils/formatters';

export interface MetricCardProps {
  title: string;
  value: number;
  format: 'currency' | 'percentage' | 'number';
  change?: number;
  changeLabel?: string;
  sparkline?: number[];
  loading?: boolean;
  description?: string;
  className?: string;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  format,
  change,
  changeLabel,
  sparkline = [],
  loading = false,
  description,
  className,
}) => {
  const changeData = change !== undefined ? formatChange(change) : null;
  
  // Convert sparkline data to format expected by recharts
  const sparklineData = sparkline.map((value, index) => ({
    index,
    value,
  }));

  if (loading) {
    return (
      <div className={clsx('metric-card', 'metric-card--loading', className)}>
        <div className="metric-card__header">
          <div className="skeleton skeleton--text skeleton--small"></div>
        </div>
        <div className="metric-card__value">
          <div className="skeleton skeleton--text skeleton--large"></div>
        </div>
        <div className="metric-card__change">
          <div className="skeleton skeleton--text skeleton--small"></div>
        </div>
        <div className="metric-card__sparkline">
          <div className="skeleton skeleton--chart"></div>
        </div>
      </div>
    );
  }

  return (
    <div className={clsx('metric-card', className)}>
      <div className="metric-card__header">
        <h3 className="metric-card__title">{title}</h3>
      </div>
      
      <div className="metric-card__value">
        <span className="metric-card__number">
          {formatValue(value, format)}
        </span>
      </div>

      {changeData && (
        <div className="metric-card__change">
          <span 
            className={clsx(
              'metric-card__change-value',
              `metric-card__change-value--${changeData.className}`
            )}
          >
            <span className="metric-card__change-icon">
              {changeData.trend === 'up' ? '↗' : changeData.trend === 'down' ? '↘' : '→'}
            </span>
            {changeData.formatted}
          </span>
          {changeLabel && (
            <span className="metric-card__change-label">{changeLabel}</span>
          )}
        </div>
      )}

      {sparklineData.length > 0 && (
        <div className="metric-card__sparkline">
          <ResponsiveContainer width="100%" height={40}>
            <LineChart data={sparklineData}>
              <Line
                type="monotone"
                dataKey="value"
                stroke="currentColor"
                strokeWidth={2}
                dot={false}
                activeDot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {description && (
        <div className="metric-card__description">
          {description}
        </div>
      )}
    </div>
  );
};
