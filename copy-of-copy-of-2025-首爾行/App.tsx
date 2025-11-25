import React, { useState, useEffect } from 'react';
import { Calendar, CreditCard, Map, Umbrella, Plane } from 'lucide-react';
import { ITINERARY } from './constants';
import ItineraryTab from './components/ItineraryTab';
import ExpenseTracker from './components/ExpenseTracker';
import BackupPlans from './components/BackupPlans';

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('Day 1');
  const [daysLeft, setDaysLeft] = useState<number>(0);

  useEffect(() => {
    const tripStart = new Date('2025-12-05');
    const today = new Date();
    const diffTime = tripStart.getTime() - today.getTime();
    setDaysLeft(Math.ceil(diffTime / (1000 * 60 * 60 * 24)));
  }, []);

  const tabs = [
    { id: 'Day 1', label: '第一天', icon: Plane },
    { id: 'Day 2', label: '第二天', icon: Map },
    { id: 'Day 3', label: '第三天', icon: Calendar },
    { id: 'money', label: '分帳', icon: CreditCard },
    { id: 'backup', label: '備案', icon: Umbrella },
  ];

  return (
    <div className="min-h-screen bg-black pb-24">
      {/* Header */}
      <header className="px-6 pt-12 pb-6 sticky top-0 bg-black/80 backdrop-blur-md z-10 border-b border-[#333]">
        <div className="max-w-2xl mx-auto">
            <h1 className="text-3xl font-bold tracking-tight text-white mb-2">
            2025 <span className="text-[#0A84FF]">首爾行</span> 🇰🇷
            </h1>
            {daysLeft > 0 ? (
                <p className="text-[#0A84FF] font-medium text-sm flex items-center gap-2">
                    🚀 距離出發還有 {daysLeft} 天
                </p>
            ) : (
                <p className="text-green-500 font-medium text-sm">旅程進行中！</p>
            )}
        </div>
      </header>

      {/* Main Content */}
      <main className="px-6 pt-6 max-w-2xl mx-auto">
        {activeTab === 'Day 1' && <ItineraryTab plan={ITINERARY['Day 1']} />}
        {activeTab === 'Day 2' && <ItineraryTab plan={ITINERARY['Day 2']} />}
        {activeTab === 'Day 3' && <ItineraryTab plan={ITINERARY['Day 3']} />}
        {activeTab === 'money' && <ExpenseTracker />}
        {activeTab === 'backup' && <BackupPlans />}
      </main>

      {/* Bottom Navigation */}
      <nav className="fixed bottom-0 left-0 right-0 bg-[#1C1C1E]/90 backdrop-blur-lg border-t border-[#333] py-2 px-6 pb-safe z-20">
        <div className="max-w-2xl mx-auto flex justify-between items-center">
            {tabs.map((tab) => {
                const Icon = tab.icon;
                const isActive = activeTab === tab.id;
                return (
                    <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`flex flex-col items-center gap-1 w-full py-1 transition-colors ${
                            isActive ? 'text-[#0A84FF]' : 'text-gray-500 hover:text-gray-300'
                        }`}
                    >
                        <Icon className={`w-6 h-6 ${isActive ? 'fill-current' : ''} stroke-2`} />
                        <span className="text-[10px] font-medium">{tab.label}</span>
                    </button>
                );
            })}
        </div>
      </nav>
      
      {/* Safe area spacer for bottom nav */}
      <div className="h-safe-bottom" />
    </div>
  );
};

export default App;