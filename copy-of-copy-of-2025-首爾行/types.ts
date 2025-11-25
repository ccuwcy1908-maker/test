export interface ItineraryItem {
  time: string;
  title: string;
  desc: string;
  transport: string;
  lat: number;
  lon: number;
  loc: string;
}

export interface DayPlan {
  date: string;
  items: ItineraryItem[];
}

export interface ItineraryData {
  [key: string]: DayPlan;
}

export interface Expense {
  id: string;
  item: string;
  amount: number;
  payer: string;
  sharers: string[];
}

export interface WeatherPoint {
  time: string;
  temp: number;
}

export interface BackupPlan {
  name: string;
  desc: string;
}