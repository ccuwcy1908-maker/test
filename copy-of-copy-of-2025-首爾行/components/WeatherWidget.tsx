import React from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { WeatherPoint } from '../types';
import { CloudSun } from 'lucide-react';

interface WeatherWidgetProps {
  data: WeatherPoint[];
  dateStr: string;
}

const WeatherWidget: React.FC<WeatherWidgetProps> = ({ data, dateStr }) => {
  const displayDate = dateStr.slice(5); // Remove Year

  return (
    <div className="w-full h-48 mb-6 bg-gradient-to-b from-[#1C1C1E] to-black rounded-xl p-4 border border-[#333]">
      <div className="flex items-center gap-2 mb-2">
        <CloudSun className="text-blue-500 w-5 h-5" />
        <h3 className="text-white font-semibold text-sm">{displayDate} 氣溫走勢</h3>
      </div>
      <div className="h-32 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="colorTemp" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#0A84FF" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#0A84FF" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <XAxis 
              dataKey="time" 
              tick={{ fill: '#888', fontSize: 10 }} 
              axisLine={false}
              tickLine={false}
              interval={2}
            />
            <YAxis hide domain={['dataMin - 2', 'dataMax + 2']} />
            <Tooltip 
              contentStyle={{ backgroundColor: '#1C1C1E', borderRadius: '8px', border: 'none', color: '#fff' }}
              itemStyle={{ color: '#0A84FF' }}
              formatter={(value: number) => [`${value}°C`, '氣溫']}
            />
            <Area 
              type="monotone" 
              dataKey="temp" 
              stroke="#0A84FF" 
              strokeWidth={3}
              fillOpacity={1} 
              fill="url(#colorTemp)" 
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default WeatherWidget;