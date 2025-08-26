import React, { useState, useMemo } from 'react';
import clsx from 'clsx';
import { ColumnConfig, DataPoint } from '../types/metrics';
import { formatValue, formatDateTime, truncate } from '../utils/formatters';

export interface DataTableProps {
  columns: ColumnConfig[];
  data: DataPoint[];
  pageSize?: number;
  showPagination?: boolean;
  onRowClick?: (row: DataPoint, index: number) => void;
  title?: string;
  loading?: boolean;
  className?: string;
}

type SortDirection = 'asc' | 'desc' | null;

export const DataTable: React.FC<DataTableProps> = ({
  columns,
  data,
  pageSize = 10,
  showPagination = true,
  onRowClick,
  title,
  loading = false,
  className,
}) => {
  const [currentPage, setCurrentPage] = useState(1);
  const [sortColumn, setSortColumn] = useState<string | null>(null);
  const [sortDirection, setSortDirection] = useState<SortDirection>(null);

  // Sort data
  const sortedData = useMemo(() => {
    if (!sortColumn || !sortDirection) return data;

    return [...data].sort((a, b) => {
      const aValue = a[sortColumn];
      const bValue = b[sortColumn];

      // Handle different data types
      if (typeof aValue === 'number' && typeof bValue === 'number') {
        return sortDirection === 'asc' ? aValue - bValue : bValue - aValue;
      }

      // Convert to strings for comparison
      const aStr = String(aValue).toLowerCase();
      const bStr = String(bValue).toLowerCase();

      if (aStr < bStr) return sortDirection === 'asc' ? -1 : 1;
      if (aStr > bStr) return sortDirection === 'asc' ? 1 : -1;
      return 0;
    });
  }, [data, sortColumn, sortDirection]);

  // Paginate data
  const paginatedData = useMemo(() => {
    if (!showPagination) return sortedData;

    const startIndex = (currentPage - 1) * pageSize;
    const endIndex = startIndex + pageSize;
    return sortedData.slice(startIndex, endIndex);
  }, [sortedData, currentPage, pageSize, showPagination]);

  const totalPages = Math.ceil(data.length / pageSize);

  // Handle sorting
  const handleSort = (column: ColumnConfig) => {
    if (!column.sortable) return;

    if (sortColumn === column.key) {
      // Toggle direction or clear sort
      if (sortDirection === 'asc') {
        setSortDirection('desc');
      } else if (sortDirection === 'desc') {
        setSortColumn(null);
        setSortDirection(null);
      } else {
        setSortDirection('asc');
      }
    } else {
      setSortColumn(column.key);
      setSortDirection('asc');
    }
  };

  // Format cell value
  const formatCellValue = (value: any, format: string) => {
    if (value === null || value === undefined) return '--';

    switch (format) {
      case 'currency':
        return formatValue(Number(value), 'currency');
      case 'percentage':
        return formatValue(Number(value), 'percentage');
      case 'number':
        return formatValue(Number(value), 'number');
      case 'datetime':
        return formatDateTime(value);
      case 'status':
        return (
          <span className={clsx('status-badge', `status-badge--${String(value).toLowerCase()}`)}>
            {String(value)}
          </span>
        );
      default:
        return truncate(String(value), 50);
    }
  };

  // Render loading skeleton
  if (loading) {
    return (
      <div className={clsx('data-table', 'data-table--loading', className)}>
        {title && (
          <div className="data-table__header">
            <div className="skeleton skeleton--text skeleton--medium"></div>
          </div>
        )}
        <div className="data-table__content">
          <table className="data-table__table">
            <thead>
              <tr>
                {Array.from({ length: 5 }).map((_, index) => (
                  <th key={index}>
                    <div className="skeleton skeleton--text skeleton--small"></div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {Array.from({ length: pageSize }).map((_, rowIndex) => (
                <tr key={rowIndex}>
                  {Array.from({ length: 5 }).map((_, colIndex) => (
                    <td key={colIndex}>
                      <div className="skeleton skeleton--text skeleton--small"></div>
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  }

  return (
    <div className={clsx('data-table', className)}>
      {title && (
        <div className="data-table__header">
          <h3 className="data-table__title">{title}</h3>
        </div>
      )}

      <div className="data-table__content">
        <table className="data-table__table">
          <thead>
            <tr>
              {columns.map((column) => (
                <th
                  key={column.key}
                  className={clsx(
                    'data-table__header-cell',
                    column.sortable && 'data-table__header-cell--sortable',
                    sortColumn === column.key && 'data-table__header-cell--sorted'
                  )}
                  style={{ width: column.width }}
                  onClick={() => handleSort(column)}
                >
                  <div className="data-table__header-content">
                    <span>{column.title}</span>
                    {column.sortable && (
                      <span className="data-table__sort-icon">
                        {sortColumn === column.key ? (
                          sortDirection === 'asc' ? '↑' : '↓'
                        ) : (
                          '↕'
                        )}
                      </span>
                    )}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {paginatedData.map((row, index) => (
              <tr
                key={index}
                className={clsx(
                  'data-table__row',
                  onRowClick && 'data-table__row--clickable'
                )}
                onClick={() => onRowClick?.(row, index)}
              >
                {columns.map((column) => (
                  <td key={column.key} className="data-table__cell">
                    {formatCellValue(row[column.key], column.format)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>

        {data.length === 0 && (
          <div className="data-table__empty">
            <p>No data available</p>
          </div>
        )}
      </div>

      {showPagination && totalPages > 1 && (
        <div className="data-table__pagination">
          <div className="pagination">
            <button
              className="pagination__button"
              disabled={currentPage === 1}
              onClick={() => setCurrentPage(currentPage - 1)}
            >
              Previous
            </button>

            <div className="pagination__info">
              <span>
                Page {currentPage} of {totalPages} ({data.length} total)
              </span>
            </div>

            <button
              className="pagination__button"
              disabled={currentPage === totalPages}
              onClick={() => setCurrentPage(currentPage + 1)}
            >
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
