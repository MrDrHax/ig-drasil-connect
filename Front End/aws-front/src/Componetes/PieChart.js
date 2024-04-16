import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

const PieChart = ({ data }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    if (chartRef && chartRef.current) {
      const ctx = chartRef.current.getContext('2d');
      new Chart(ctx, {
        type: 'pie',
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false
        }
      });
    }
  }, [data]);

  return (
    <div className="metrics-chart">
      <canvas ref={chartRef}></canvas>
    </div>
  );
};

export default PieChart;