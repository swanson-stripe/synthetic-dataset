import { format, parseISO } from 'date-fns';

/**
 * Format a number as currency (assumes cents input, outputs dollars)
 */
export const formatCurrency = (value: number, currency = 'USD'): string => {
  const dollars = value / 100;
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(dollars);
};

/**
 * Format a number as percentage with 1 decimal place
 */
export const formatPercentage = (value: number): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'percent',
    minimumFractionDigits: 1,
    maximumFractionDigits: 1,
  }).format(value / 100);
};

/**
 * Format a number with thousand separators
 */
export const formatNumber = (value: number): string => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
};

/**
 * Format Unix timestamp to readable date
 */
export const formatDateTime = (timestamp: number | string | Date): string => {
  try {
    let date: Date;
    
    if (typeof timestamp === 'number') {
      // Unix timestamp (assume seconds, convert to milliseconds if needed)
      date = timestamp > 1e10 ? new Date(timestamp) : new Date(timestamp * 1000);
    } else if (typeof timestamp === 'string') {
      // ISO string or date string
      date = parseISO(timestamp);
    } else {
      date = timestamp;
    }
    
    return format(date, 'MMM dd, yyyy');
  } catch (error) {
    return 'Invalid Date';
  }
};

/**
 * Format Unix timestamp to short time format
 */
export const formatTime = (timestamp: number | string | Date): string => {
  try {
    let date: Date;
    
    if (typeof timestamp === 'number') {
      date = timestamp > 1e10 ? new Date(timestamp) : new Date(timestamp * 1000);
    } else if (typeof timestamp === 'string') {
      date = parseISO(timestamp);
    } else {
      date = timestamp;
    }
    
    return format(date, 'HH:mm');
  } catch (error) {
    return '--:--';
  }
};

/**
 * Format a value based on its format type
 */
export const formatValue = (value: number, formatType: string): string => {
  switch (formatType) {
    case 'currency':
      return formatCurrency(value);
    case 'percentage':
      return formatPercentage(value);
    case 'number':
      return formatNumber(value);
    default:
      return value.toString();
  }
};

/**
 * Format change percentage with sign and color class
 */
export const formatChange = (change: number): { 
  formatted: string; 
  className: string; 
  trend: 'up' | 'down' | 'neutral' 
} => {
  const formatted = `${change >= 0 ? '+' : ''}${change.toFixed(1)}%`;
  const trend = change > 0 ? 'up' : change < 0 ? 'down' : 'neutral';
  const className = trend === 'up' ? 'positive' : trend === 'down' ? 'negative' : 'neutral';
  
  return { formatted, className, trend };
};

/**
 * Truncate text with ellipsis
 */
export const truncate = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength - 3) + '...';
};

/**
 * Format large numbers with K, M, B suffixes
 */
export const formatCompactNumber = (value: number): string => {
  const absValue = Math.abs(value);
  
  if (absValue >= 1e9) {
    return (value / 1e9).toFixed(1) + 'B';
  } else if (absValue >= 1e6) {
    return (value / 1e6).toFixed(1) + 'M';
  } else if (absValue >= 1e3) {
    return (value / 1e3).toFixed(1) + 'K';
  }
  
  return value.toString();
};
