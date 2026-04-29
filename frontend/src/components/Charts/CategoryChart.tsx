import React from 'react';
import { PieChart, Pie, Cell, Legend, Tooltip, ResponsiveContainer } from 'recharts';
import type { CategoryMetric } from '../../services/api';

interface CategoryChartProps {
  data: CategoryMetric[];
  loading: boolean;
}

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899', '#14B8A6', '#F97316'];

const CategoryChart: React.FC<CategoryChartProps> = ({ data, loading }) => {
  if (loading) {
    return <div className="text-center text-gray-500 py-8">Loading chart...</div>;
  }

  if (data.length === 0) {
    return <div className="text-center text-gray-500 py-8">No data available</div>;
  }

  return (
    <div className="w-full h-80 bg-white rounded-lg shadow-sm p-6">
      <h3 className="text-lg font-semibold mb-4 text-gray-800">Spending by Category</h3>
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            dataKey="total"
            nameKey="category"
            cx="50%"
            cy="50%"
            outerRadius={120}
            label={({ payload }: any) => `${payload.category}: $${payload.total.toFixed(2)}`}
          >
            {data.map((_, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip formatter={(value: any) => `$${value.toFixed(2)}`} />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default CategoryChart;
