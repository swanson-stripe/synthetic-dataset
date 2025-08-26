import React from 'react';
import {
  BarChart as RechartsBarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import clsx from 'clsx';
import { formatValue } from '../utils/formatters';

export interface BarChartProps {
  data: any[];
  dataKey: string;
  xAxisKey?: string;
  type?: 'bar' | 'pie' | 'doughnut';
  yAxisFormat?: 'currency' | 'percentage' | 'number';
  height?: number;
  showGrid?: boolean;
  showLegend?: boolean;
  title?: string;
  colors?: string[];
  loading?: boolean;
  className?: string;
}

const DEFAULT_COLORS = [
  '#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', 
  '#06B6D4', '#84CC16', '#F97316', '#EC4899', '#6366F1'
];

export const BarChart: React.FC<BarChartProps> = ({
  data,
  dataKey,
  xAxisKey = 'name',
  type = 'bar',
  yAxisFormat = 'number',
  height = 300,
  showGrid = true,
  showLegend = true,
  title,
  colors = DEFAULT_COLORS,
  loading = false,
  className,
}) => {
  // Format Y-axis values
  const formatYAxis = (value: number) => {
    return formatValue(value, yAxisFormat);
  };

  // Custom tooltip formatter
  const tooltipFormatter = (value: number, name: string) => {
    return [formatValue(value, yAxisFormat), name];
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

  const renderBarChart = () => (
    <ResponsiveContainer width="100%" height="100%">
      <RechartsBarChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
        {showGrid && <CartesianGrid strokeDasharray="3 3" />}
        
        <XAxis
          dataKey={xAxisKey}
          tick={{ fontSize: 12 }}
        />
        
        <YAxis
          tickFormatter={formatYAxis}
          tick={{ fontSize: 12 }}
        />
        
        <Tooltip
          formatter={tooltipFormatter}
          contentStyle={{
            backgroundColor: 'white',
            border: '1px solid #e5e7eb',
            borderRadius: '6px',
            fontSize: '12px',
          }}
        />
        
        {showLegend && <Legend />}
        
        <Bar
          dataKey={dataKey}
          fill={colors[0]}
          radius={[2, 2, 0, 0]}
        />
      </RechartsBarChart>
    </ResponsiveContainer>
  );

  const renderPieChart = () => {
    const pieData = data.map((item, index) => ({
      ...item,
      fill: colors[index % colors.length],
    }));

    return (
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={pieData}
            cx="50%"
            cy="50%"
            innerRadius={type === 'doughnut' ? height * 0.15 : 0}
            outerRadius={height * 0.3}
            paddingAngle={2}
            dataKey={dataKey}
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
          >
            {pieData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.fill} />
            ))}
          </Pie>
          
          <Tooltip
            formatter={tooltipFormatter}
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '6px',
              fontSize: '12px',
            }}
          />
          
          {showLegend && <Legend />}
        </PieChart>
      </ResponsiveContainer>
    );
  };

  return (
    <div className={clsx('chart-container', className)}>
      {title && (
        <div className="chart-container__header">
          <h3 className="chart-container__title">{title}</h3>
        </div>
      )}
      
      <div className="chart-container__content" style={{ height }}>
        {type === 'bar' ? renderBarChart() : renderPieChart()}
      </div>
    </div>
  );
};
