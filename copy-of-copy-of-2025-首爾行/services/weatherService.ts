import { WeatherPoint } from '../types';

// Since the trip is in Dec 2025, real API calls will likely fail or return nothing relevant.
// We simulate the data structure to match the visual requirements.
export const getMockWeather = (dateStr: string): WeatherPoint[] => {
  const baseTemps: Record<string, number> = {
    '2025-12-05': 2,
    '2025-12-06': -1,
    '2025-12-07': 0
  };

  const startTemp = baseTemps[dateStr] || 0;
  const data: WeatherPoint[] = [];

  // Generate hourly data from 8 AM to 11 PM
  for (let hour = 8; hour <= 23; hour++) {
    // Simulate a temperature curve (rising until 2 PM then falling)
    let adjust = 0;
    if (hour < 14) adjust = (hour - 8) * 0.8;
    else adjust = (14 - 8) * 0.8 - (hour - 14) * 0.9;

    data.push({
      time: `${hour}:00`,
      temp: parseFloat((startTemp + adjust).toFixed(1))
    });
  }

  return data;
};