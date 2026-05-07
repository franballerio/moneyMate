import React from 'react';

interface MetricCardProps {
  title: string;
  value: string;
  icon?: React.ReactNode;
  trend?: string;
}

const MetricCard: React.FC<MetricCardProps> = ({ title, value, icon, trend }) => {
  return (
    <div className="bg-canvas border border-hairline rounded-[18px] p-[24px] flex flex-col justify-between transition-shadow duration-300 hover:shadow-[0_2px_12px_rgba(0,0,0,0.04)]">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-caption-strong text-ink-muted-80 mb-1.5">{title}</p>
          <p className="text-display-lg text-ink tracking-tight">{value}</p>
        </div>
        {icon && (
          <div className="w-9 h-9 rounded-full bg-surface-pearl flex items-center justify-center text-ink-muted-48 shrink-0">
            {icon}
          </div>
        )}
      </div>
      {trend && (
        <p className="text-caption text-ink-muted-48 mt-4 pt-4 border-t border-divider-soft">
          {trend}
        </p>
      )}
    </div>
  );
};

export default MetricCard;
