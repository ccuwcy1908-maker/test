import React, { useState, useMemo, useEffect } from 'react';
import { Plus, Trash2, Wallet, ArrowRight, CheckCircle2 } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Tooltip as RechartsTooltip, Cell } from 'recharts';
import { MEMBERS } from '../constants';
import { Expense } from '../types';

const COLORS = ['#0A84FF', '#30D158', '#BF5AF2', '#FF9F0A'];

const ExpenseTracker: React.FC = () => {
  // 從 LocalStorage 讀取初始資料
  const [expenses, setExpenses] = useState<Expense[]>(() => {
    try {
      const saved = localStorage.getItem('seoul_trip_expenses');
      return saved ? JSON.parse(saved) : [];
    } catch (e) {
      return [];
    }
  });
  
  // 當 expenses 改變時，存入 LocalStorage
  useEffect(() => {
    localStorage.setItem('seoul_trip_expenses', JSON.stringify(expenses));
  }, [expenses]);
  
  // Form State
  const [item, setItem] = useState('');
  const [amount, setAmount] = useState<string>('');
  const [payer, setPayer] = useState(MEMBERS[0]);
  const [sharers, setSharers] = useState<string[]>(MEMBERS);

  const handleAdd = (e: React.FormEvent) => {
    e.preventDefault();
    if (!item || !amount) return;
    
    const newExpense: Expense = {
      id: Date.now().toString(),
      item,
      amount: parseFloat(amount),
      payer,
      sharers
    };

    setExpenses([...expenses, newExpense]);
    setItem('');
    setAmount('');
    setSharers(MEMBERS); // Reset to all
  };

  const totalSpent = useMemo(() => expenses.reduce((acc, curr) => acc + curr.amount, 0), [expenses]);
  
  const payerStats = useMemo(() => {
    const stats: Record<string, number> = {};
    MEMBERS.forEach(m => stats[m] = 0);
    expenses.forEach(exp => {
      stats[exp.payer] += exp.amount;
    });
    return Object.entries(stats).map(([name, value]) => ({ name, value }));
  }, [expenses]);

  const toggleSharer = (member: string) => {
    if (sharers.includes(member)) {
      setSharers(sharers.filter(s => s !== member));
    } else {
      setSharers([...sharers, member]);
    }
  };

  // 結算邏輯
  const settlements = useMemo(() => {
    if (expenses.length === 0) return [];

    // 1. 計算每個人的淨餘額 (正 = 別人欠我不夠多 / 負 = 我欠別人錢)
    const balances: Record<string, number> = {};
    MEMBERS.forEach(m => balances[m] = 0);

    expenses.forEach(exp => {
      const paid = exp.amount;
      const splitAmount = paid / exp.sharers.length;

      // 付款人 +全額
      balances[exp.payer] += paid;
      
      // 分擔人 -應付金額
      exp.sharers.forEach(s => {
        balances[s] -= splitAmount;
      });
    });

    // 2. 分類債務人與債權人
    const debtors: {name: string, amount: number}[] = [];
    const creditors: {name: string, amount: number}[] = [];

    Object.entries(balances).forEach(([name, amount]) => {
      // 忽略極小誤差
      if (amount < -1) debtors.push({ name, amount });
      else if (amount > 1) creditors.push({ name, amount });
    });

    // 排序：欠最多錢的排前面，被欠最多錢的也排前面
    debtors.sort((a, b) => a.amount - b.amount);
    creditors.sort((a, b) => b.amount - a.amount);

    // 3. 配對轉帳
    const result: {from: string, to: string, amount: number}[] = [];
    let i = 0;
    let j = 0;

    while (i < debtors.length && j < creditors.length) {
      const debtor = debtors[i];
      const creditor = creditors[j];

      // 找出這筆交易的金額 (取兩者絕對值的最小值)
      const amount = Math.min(Math.abs(debtor.amount), creditor.amount);
      
      // 無條件捨去小數點，避免太複雜
      if (amount >= 1) {
        result.push({ from: debtor.name, to: creditor.name, amount: Math.round(amount) });
      }

      // 更新餘額
      debtor.amount += amount;
      creditor.amount -= amount;

      // 如果某一方結清了，移動指標
      if (Math.abs(debtor.amount) < 1) i++;
      if (creditor.amount < 1) j++;
    }

    return result;
  }, [expenses]);

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Summary Card */}
      <div className="bg-[#1C1C1E] p-6 rounded-xl border border-[#333] flex justify-between items-center">
         <div>
           <p className="text-gray-400 text-sm">總開銷 (TWD)</p>
           <h2 className="text-3xl font-bold text-white">${totalSpent.toLocaleString()}</h2>
         </div>
         <div className="bg-[#0A84FF]/20 p-3 rounded-full">
            <Wallet className="text-[#0A84FF] w-6 h-6" />
         </div>
      </div>
      
      {/* 結算方案 (新增區塊) */}
      {expenses.length > 0 && (
        <div className="bg-[#1C1C1E] p-6 rounded-xl border border-[#333]">
          <h3 className="text-white font-semibold mb-4 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-green-500" /> 結算方案
          </h3>
          
          {settlements.length > 0 ? (
            <div className="space-y-3">
              {settlements.map((tx, idx) => (
                <div key={idx} className="flex items-center justify-between bg-black/40 p-3 rounded-lg border border-[#333]">
                  <div className="flex items-center gap-3">
                    <span className="text-red-400 font-bold">{tx.from}</span>
                    <ArrowRight className="w-4 h-4 text-gray-500" />
                    <span className="text-green-400 font-bold">{tx.to}</span>
                  </div>
                  <div className="font-mono text-white font-bold">
                    ${tx.amount.toLocaleString()}
                  </div>
                </div>
              ))}
              <p className="text-xs text-gray-500 text-center mt-2">
                *此方案為最簡轉帳建議，已四捨五入至整數。
              </p>
            </div>
          ) : (
            <div className="text-center text-gray-500 py-4">
              目前大家收支平衡，不需要轉帳！
            </div>
          )}
        </div>
      )}

      {/* Add New Form */}
      <div className="bg-[#1C1C1E] p-6 rounded-xl border border-[#333]">
        <h3 className="text-white font-semibold mb-4 flex items-center gap-2">
          <Plus className="w-4 h-4" /> 新增消費
        </h3>
        <form onSubmit={handleAdd} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <input 
              type="text" 
              placeholder="項目 (ex. 烤肉)" 
              className="bg-[#2C2C2E] text-white p-3 rounded-lg outline-none focus:ring-2 focus:ring-[#0A84FF]"
              value={item}
              onChange={(e) => setItem(e.target.value)}
            />
            <input 
              type="number" 
              placeholder="金額" 
              className="bg-[#2C2C2E] text-white p-3 rounded-lg outline-none focus:ring-2 focus:ring-[#0A84FF]"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
            />
          </div>
          
          <div>
            <label className="text-xs text-gray-500 mb-2 block uppercase font-bold">付款人 (先墊錢的人)</label>
            <div className="flex gap-2 overflow-x-auto scrollbar-hide">
              {MEMBERS.map(m => (
                <button
                  key={m}
                  type="button"
                  onClick={() => setPayer(m)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-all whitespace-nowrap ${
                    payer === m 
                      ? 'bg-[#0A84FF] text-white' 
                      : 'bg-[#2C2C2E] text-gray-400 hover:bg-[#3A3A3C]'
                  }`}
                >
                  {m}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="text-xs text-gray-500 mb-2 block uppercase font-bold">分擔人 (誰要一起付)</label>
             <div className="flex flex-wrap gap-2">
              {MEMBERS.map(m => (
                <button
                  key={m}
                  type="button"
                  onClick={() => toggleSharer(m)}
                  className={`px-3 py-1 rounded-full text-xs font-medium transition-all border ${
                    sharers.includes(m) 
                      ? 'bg-[#30D158]/20 border-[#30D158] text-[#30D158]' 
                      : 'bg-transparent border-[#333] text-gray-500'
                  }`}
                >
                  {m}
                </button>
              ))}
            </div>
          </div>

          <button 
            type="submit" 
            className="w-full bg-[#0A84FF] hover:bg-[#0071e3] text-white py-3 rounded-lg font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={!item || !amount || sharers.length === 0}
          >
            新增款項
          </button>
        </form>
      </div>

      {/* Chart */}
      {expenses.length > 0 && (
        <div className="bg-[#1C1C1E] p-6 rounded-xl border border-[#333]">
          <h3 className="text-white font-semibold mb-4">誰先墊了多少？(總墊款)</h3>
          <div className="h-48 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={payerStats}>
                <XAxis dataKey="name" stroke="#888" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis hide />
                <RechartsTooltip 
                  cursor={{fill: 'transparent'}}
                  contentStyle={{ backgroundColor: '#000', borderRadius: '8px', border: '1px solid #333' }}
                />
                <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                   {payerStats.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* List */}
      {expenses.length > 0 && (
        <div className="space-y-3">
          <h3 className="text-white font-semibold">消費明細</h3>
          {expenses.slice().reverse().map(exp => (
            <div key={exp.id} className="bg-[#1C1C1E] p-4 rounded-xl flex justify-between items-center border border-transparent hover:border-[#333]">
              <div>
                <p className="font-medium text-white">{exp.item}</p>
                <p className="text-xs text-gray-500">
                  <span className="text-[#0A84FF]">{exp.payer}</span> 先付 (分擔: {exp.sharers.length} 人)
                </p>
              </div>
              <div className="flex items-center gap-4">
                <span className="font-mono text-white">${exp.amount}</span>
                <button 
                  onClick={() => setExpenses(expenses.filter(e => e.id !== exp.id))}
                  className="text-gray-600 hover:text-red-500 transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ExpenseTracker;