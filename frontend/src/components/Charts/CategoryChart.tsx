import React from 'react';
import { PieChart, Pie, Cell, Legend, Tooltip, ResponsiveContainer } from 'recharts';
import type { CategoryMetric } from '../../services/api';

interface CategoryChartProps {
  data: CategoryMetric[];
  loading: boolean;
}

const COLORS = [
  '#0066cc',
  '#34c759',
  '#ff9500',
  '#ff3b30',
  '#af52de',
  '#ff2d55',
  '#5ac8fa',
  '#5856d6',
];

const CategoryChart: React.FC<CategoryChartProps> = ({ data, loading }) => {
  if (loading) {
    return (
      <div className="w-full h-[400px] bg-canvas border border-hairline rounded-[18px] p-[24px] flex items-center justify-center">
        <p className="text-caption text-ink-muted-48">Loading chart...</p>
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="w-full h-[400px] bg-canvas border border-hairline rounded-[18px] p-[24px] flex items-center justify-center">
        <p className="text-caption text-ink-muted-48">No category data yet</p>
      </div>
    );
  }

  return (
    <div className="w-full h-[400px] bg-canvas border border-hairline rounded-[18px] p-[24px] flex flex-col">
      <h3 className="text-body-strong text-ink mb-6">Spending by Category</h3>
      <div className="flex-1 min-h-0 relative">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              dataKey="total"
              nameKey="category"
              cx="50%"
              cy="50%"
              innerRadius={80}
              outerRadius={110}
              paddingAngle={2}
              stroke="none"
              cornerRadius={6}
            >
              {data.map((_, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              formatter={(value: any) => [`$${Number(value || 0).toFixed(2)}`, 'Spent']}
              contentStyle={{
                backgroundColor: 'rgba(255, 255, 255, 0.85)',
                backdropFilter: 'blur(20px)',
                border: '1px solid var(--color-hairline)',
                borderRadius: '12px',
                boxShadow: '0 4px 24px rgba(0,0,0,0.08)',
                color: 'var(--color-ink)',
                fontSize: '14px',
                fontWeight: 600,
                fontFamily: 'var(--font-text)',
              }}
              itemStyle={{ color: 'var(--color-ink)' }}
              labelStyle={{ display: 'none' }}
            />
            <Legend
              iconType="circle"
              iconSize={8}
              wrapperStyle={{ fontSize: '12px', color: 'var(--color-ink-muted-48)', fontFamily: 'var(--font-text)' }}
              layout="horizontal"
              verticalAlign="bottom"
              align="center"
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default CategoryChart;
