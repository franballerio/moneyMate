import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import type { TrendData } from '../../services/api';

interface TrendChartProps {
  data: TrendData[];
  loading: boolean;
}

const TrendChart: React.FC<TrendChartProps> = ({ data, loading }) => {
  if (loading) {
    return <div className="text-center text-gray-500 py-8">Loading chart...</div>;
  }

  if (data.length === 0) {
    return <div className="text-center text-gray-500 py-8">No data available</div>;
  }

  return (
    <div className="w-full h-80 bg-white rounded-lg shadow-sm p-6">
      <h3 className="text-lg font-semibold mb-4 text-gray-800">Spending Trends</h3>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis dataKey="date" stroke="#6b7280" />
          <YAxis stroke="#6b7280" />
          <Tooltip
            contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
            formatter={(value: any) => `$${value.toFixed(2)}`}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="total"
            stroke="#3B82F6"
            strokeWidth={2}
            dot={{ fill: '#3B82F6', r: 5 }}
            activeDot={{ r: 7 }}
            name="Daily Spending"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TrendChart;
