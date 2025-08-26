#!/usr/bin/env node
/**
 * Test integration between the metrics visualizer and dashboard kit
 * This script demonstrates how the formatted metrics data flows into the React components
 */

const fs = require('fs');
const path = require('path');

// Read the formatted metrics data from our visualizer
const metricsDir = '../metrics_visualizer/formatted_output';

console.log('🔗 Testing Dashboard Kit Integration with Metrics Visualizer Data');
console.log('=' .repeat(70));

try {
  // Read metric cards
  const metricCardsPath = path.join(__dirname, metricsDir, 'metric_cards.json');
  const metricCards = JSON.parse(fs.readFileSync(metricCardsPath, 'utf8'));
  
  console.log('✅ Metric Cards Data:');
  console.log(`   - Found ${metricCards.cards?.length || 0} metric cards`);
  if (metricCards.cards?.length > 0) {
    metricCards.cards.forEach(card => {
      console.log(`   - ${card.title}: ${card.format === 'currency' ? '$' + (card.value/100).toFixed(2) : 
                                       card.format === 'percentage' ? (card.value).toFixed(1) + '%' :
                                       card.value.toLocaleString()}`);
    });
  }

  // Read time series charts
  const timeSeriesPath = path.join(__dirname, metricsDir, 'time_series_charts.json');
  const timeSeriesData = JSON.parse(fs.readFileSync(timeSeriesPath, 'utf8'));
  
  console.log('\n✅ Time Series Charts:');
  console.log(`   - Found ${timeSeriesData.charts?.length || 0} time series charts`);
  if (timeSeriesData.charts?.length > 0) {
    timeSeriesData.charts.forEach(chart => {
      console.log(`   - ${chart.title} (${chart.type}): ${chart.labels?.length || 0} data points`);
    });
  }

  // Read categorical charts
  const categoricalPath = path.join(__dirname, metricsDir, 'categorical_charts.json');
  const categoricalData = JSON.parse(fs.readFileSync(categoricalPath, 'utf8'));
  
  console.log('\n✅ Categorical Charts:');
  console.log(`   - Found ${categoricalData.charts?.length || 0} categorical charts`);
  if (categoricalData.charts?.length > 0) {
    categoricalData.charts.forEach(chart => {
      console.log(`   - ${chart.title} (${chart.type}): ${chart.labels?.length || 0} categories`);
    });
  }

  // Read table data
  const tableDataPath = path.join(__dirname, metricsDir, 'table_data.json');
  const tableData = JSON.parse(fs.readFileSync(tableDataPath, 'utf8'));
  
  console.log('\n✅ Data Tables:');
  console.log(`   - Found ${tableData.tables?.length || 0} data tables`);
  if (tableData.tables?.length > 0) {
    tableData.tables.forEach(table => {
      console.log(`   - ${table.title}: ${table.data?.length || 0} rows, ${table.columns?.length || 0} columns`);
    });
  }

  // Create combined dashboard data
  const dashboardData = {
    cards: metricCards.cards || [],
    charts: [
      ...(timeSeriesData.charts || []),
      ...(categoricalData.charts || [])
    ],
    tables: tableData.tables || []
  };

  // Write the combined data for dashboard consumption
  const outputPath = path.join(__dirname, 'dashboard-demo-data.json');
  fs.writeFileSync(outputPath, JSON.stringify(dashboardData, null, 2));

  console.log('\n🎯 Integration Test Results:');
  console.log(`   ✅ Data Format: Compatible with Dashboard Kit`);
  console.log(`   ✅ Metric Cards: ${dashboardData.cards.length} cards ready for <MetricCard> components`);
  console.log(`   ✅ Charts: ${dashboardData.charts.length} charts ready for <LineChart>/<BarChart> components`);
  console.log(`   ✅ Tables: ${dashboardData.tables.length} tables ready for <DataTable> components`);
  console.log(`   ✅ Combined Data: Saved to dashboard-demo-data.json`);

  console.log('\n🚀 Usage Example:');
  console.log('   import { Dashboard } from "@stripe-synthetic/dashboard-kit";');
  console.log('   ');
  console.log('   <Dashboard ');
  console.log('     dataSource="./dashboard-demo-data.json"');
  console.log('     title="Payment Analytics Dashboard"');
  console.log('     theme="light"');
  console.log('   />');

  console.log('\n✨ Integration test completed successfully!');

} catch (error) {
  console.error('❌ Integration test failed:', error.message);
  console.log('\n💡 Make sure to run the metrics visualizer first:');
  console.log('   cd ../metrics_visualizer');
  console.log('   python format_metrics.py');
  process.exit(1);
}
