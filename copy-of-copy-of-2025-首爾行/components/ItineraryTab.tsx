import React, { useMemo } from 'react';
import { DayPlan } from '../types';
import WeatherWidget from './WeatherWidget';
import { getMockWeather } from '../services/weatherService';
import { MapPin, Navigation, Train } from 'lucide-react';

interface ItineraryTabProps {
  plan: DayPlan;
}

const ItineraryTab: React.FC<ItineraryTabProps> = ({ plan }) => {
  const weatherData = useMemo(() => getMockWeather(plan.date), [plan.date]);

  const getMapLink = (lat: number, lon: number, name: string) => {
    return `https://maps.apple.com/?q=${encodeURIComponent(name)}&ll=${lat},${lon}`;
  };

  return (
    <div className="animate-fade-in">
      <WeatherWidget data={weatherData} dateStr={plan.date} />
      
      <div className="space-y-4">
        {plan.items.map((item, idx) => (
          <div key={idx} className="bg-[#1C1C1E] rounded-xl p-5 border border-transparent hover:border-[#333] transition-colors relative group">
            <div className="flex justify-between items-start mb-2">
              <h3 className="font-bold text-lg text-white">{item.title}</h3>
              <span className="text-[#0A84FF] font-mono font-medium text-sm bg-[#0A84FF]/10 px-2 py-1 rounded">
                {item.time}
              </span>
            </div>
            
            <p className="text-gray-400 text-sm mb-4 leading-relaxed">
              {item.desc}
            </p>

            <div className="flex items-center justify-between mt-4 pt-4 border-t border-[#333]">
              <div className="flex items-center gap-2 text-xs text-gray-500">
                <Train className="w-4 h-4" />
                <span>{item.transport}</span>
              </div>
              
              <a 
                href={getMapLink(item.lat, item.lon, item.loc)}
                target="_blank"
                rel="noreferrer"
                className="flex items-center gap-2 bg-[#0A84FF] hover:bg-[#0071e3] text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
              >
                <Navigation className="w-4 h-4" />
                導航
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ItineraryTab;