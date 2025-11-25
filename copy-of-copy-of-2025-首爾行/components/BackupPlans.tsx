import React from 'react';
import { BACKUP_PLANS } from '../constants';
import { Umbrella } from 'lucide-react';

const BackupPlans: React.FC = () => {
  return (
    <div className="space-y-4 animate-fade-in">
      <div className="bg-[#1C1C1E] p-6 rounded-xl border border-[#333] mb-6">
        <div className="flex items-center gap-3 mb-2">
            <div className="bg-yellow-500/10 p-2 rounded-full">
                <Umbrella className="text-yellow-500 w-5 h-5" />
            </div>
            <h3 className="text-white font-bold">備案 & 雨天計畫</h3>
        </div>
        <p className="text-gray-400 text-sm">
            如果天氣不好或行程提早結束，可以參考這些地點。
        </p>
      </div>

      {BACKUP_PLANS.map((plan, idx) => (
        <div key={idx} className="bg-[#1C1C1E] p-5 rounded-xl border-l-4 border-yellow-500">
          <h4 className="font-bold text-white mb-1">{plan.name}</h4>
          <p className="text-gray-400 text-sm">{plan.desc}</p>
        </div>
      ))}
    </div>
  );
};

export default BackupPlans;