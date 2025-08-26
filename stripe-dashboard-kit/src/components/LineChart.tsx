import React from 'react';
import {
  LineChart as RechartsLineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import clsx from 'clsx';
import { formatValue, formatDateTime } from '../utils/formatters';

export interface LineProps {
  dataKey: string;
  stroke?: string;
  strokeWidth?: number;
  name?: string;
  type?: 'monotone' | 'linear' | 'step';
}

export interface LineChartProps {
  data: any[];
  lines: LineProps[];
  xAxisKey: string;
  xAxisFormat?: 'date' | 'number' | 'string';
  yAxisFormat?: 'currency' | 'percentage' | 'number';
  height?: number;
  showGrid?: boolean;
  showLegend?: boolean;
  title?: string;
  loading?: boolean;
  className?: string;
}

export const LineChart: React.FC<LineChartProps> = ({
  data,
  lines,
  xAxisKey,
  xAxisFormat = 'string',
  yAxisFormat = 'number',
  height = 300,
  showGrid = true,
  showLegend = true,
  title,
  loading = false,
  className,
}) => {
  // Format X-axis values
  const formatXAxis = (value: any) => {
    switch (xAxisFormat) {
      case 'date':
        return formatDateTime(value);
      case 'number':
        return formatValue(value, 'number');
      default:
        return value;
    }
  };

  // Format Y-axis values
  const formatYAxis = (value: number) => {
    return formatValue(value, yAxisFormat);
  };

  // Custom tooltip formatter
  const tooltipFormatter = (value: number, name: string) => {
    return [formatValue(value, yAxisFormat), name];
  };

  const tooltipLabelFormatter = (label: any) => {
    return formatXAxis(label);
  };

  if (loading) {
    return (
      <div className={clsx('chart-container', 'chart-container--loading', className)}>
        {title && (
          <div className="chart-container__header">
            <div className="skeleton skeleton--text skeleton--medium"></div>
          </div>
        )}
        <div className="chart-container__content" style={{ height }}>
          <div className="skeleton skeleton--chart"></div>
        </div>
      </div>
    );
  }

  return (
    <div className={clsx('chart-container', className)}>
      {title && (
        <div className="chart-container__header">
          <h3 className="chart-container__title">{title}</h3>
        </div>
      )}
      
      <div className="chart-container__content" style={{ height }}>
        <ResponsiveContainer width="100%" height="100%">
          <RechartsLineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            {showGrid && <CartesianGrid strokeDasharray="3 3" />}
            
            <XAxis
              dataKey={xAxisKey}
              tickFormatter={formatXAxis}
              tick={{ fontSize: 12 }}
            />
            
            <YAxis
              tickFormatter={formatYAxis}
              tick={{ fontSize: 12 }}
            />
            
            <Tooltip
              formatter={tooltipFormatter}
              labelFormatter={tooltipLabelFormatter}
              contentStyle={{
                backgroundColor: 'white',
                border: '1px solid #e5e7eb',
                borderRadius: '6px',
                fontSize: '12px',
              }}
            />
            
            {showLegend && <Legend />}
            
            {lines.map((line, index) => (
              <Line
                key={line.dataKey}
                type={line.type || 'monotone'}
                dataKey={line.dataKey}
                stroke={line.stroke || `hsl(${index * 137.5}, 70%, 50%)`}
                strokeWidth={line.strokeWidth || 2}
                name={line.name || line.dataKey}
                dot={{ r: 3 }}
                activeDot={{ r: 5 }}
              />
            ))}
          </RechartsLineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
