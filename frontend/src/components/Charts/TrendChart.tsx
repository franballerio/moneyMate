import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import type { TrendData } from '../../services/api';

interface TrendChartProps {
  data: TrendData[];
  loading: boolean;
}

const TrendChart: React.FC<TrendChartProps> = ({ data, loading }) => {
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
        <p className="text-caption text-ink-muted-48">No spending data yet</p>
      </div>
    );
  }

  return (
    <div className="w-full h-[400px] bg-canvas border border-hairline rounded-[18px] p-[24px] flex flex-col">
      <h3 className="text-body-strong text-ink mb-6">Spending Trends</h3>
      <div className="flex-1 min-h-0">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--color-divider-soft)" />
            <XAxis
              dataKey="date"
              axisLine={false}
              tickLine={false}
              tick={{ fill: 'var(--color-ink-muted-48)', fontSize: 12, fontFamily: 'var(--font-text)' }}
              dy={10}
            />
            <YAxis
              axisLine={false}
              tickLine={false}
              tick={{ fill: 'var(--color-ink-muted-48)', fontSize: 12, fontFamily: 'var(--font-text)' }}
              tickFormatter={(value) => `$${value}`}
            />
            <Tooltip
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
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              formatter={(value: any) => [`$${Number(value || 0).toFixed(2)}`, 'Spending']}
              labelStyle={{ color: 'var(--color-ink-muted-48)', marginBottom: '4px', fontSize: '12px', fontWeight: 400 }}
            />
            <Line
              type="monotone"
              dataKey="total"
              stroke="var(--color-primary)"
              strokeWidth={3}
              dot={false}
              activeDot={{ r: 6, fill: 'var(--color-primary)', stroke: '#fff', strokeWidth: 2 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default TrendChart;
