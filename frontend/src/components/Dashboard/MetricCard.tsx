import React from 'react';

interface MetricCardProps {
  title: string;
  value: string;
  icon: string;
  color: 'blue' | 'green' | 'orange' | 'red';
  trend?: string;
}

const MetricCard: React.FC<MetricCardProps> = ({ title, value, icon, color, trend }) => {
  const colorClasses = {
    blue: 'bg-blue-50 text-blue-600 border-blue-200',
    green: 'bg-green-50 text-green-600 border-green-200',
    orange: 'bg-orange-50 text-orange-600 border-orange-200',
    red: 'bg-red-50 text-red-600 border-red-200',
  };

  return (
    <div className={`${colorClasses[color]} border rounded-lg p-6 shadow-sm hover:shadow-md transition`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-3xl font-bold mt-2">{value}</p>
          {trend && <p className="text-xs text-gray-500 mt-2">{trend}</p>}
        </div>
        <span className="text-4xl">{icon}</span>
      </div>
    </div>
  );
};

export default MetricCard;
