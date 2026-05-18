import { useState, useEffect, useCallback, useRef, useMemo } from 'react';
import { Search, Users, Briefcase, TrendingUp, Activity, Phone, Mail, Calendar, Plus, X, ChevronDown, ChevronUp, Clock, Building2, User, Flag, DollarSign } from 'lucide-react';

const BASE = window.__BACKEND_URL__ || '';

async function apiFetch(path, opts = {}) {
  for (let i = 0; i < 5; i++) {
    try {
      const r = await fetch(BASE + path, opts);
      if (r.ok) return r.json();
    } catch (_) {}
    await new Promise(r => setTimeout(r, 1500));
  }
  return null;
}

function useInjectStyles() {
  useEffect(() => {
    const style = document.createElement('style');
    style.textContent = `
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
      :root { --accent: #00A86B; --accent2: #1A3A5C; }
      .glass { background: rgba(255,255,255,0.04); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; }
      .gradient-text { background: linear-gradient(135deg, #00A86B, #1A3A5C, #00A86B); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
      .shimmer { background: linear-gradient(90deg, rgba(255,255,255,0.04) 25%, rgba(255,255,255,0.08) 50%, rgba(255,255,255,0.04) 75%); background-size: 200% 100%; animation: shimmer 1.5s infinite; }
      @keyframes shimmer { 0% { background-position: -200% 0 } 100% { background-position: 200% 0 } }
      @keyframes fadeIn { from { opacity:0; transform:translateY(8px) } to { opacity:1; transform:translateY(0) } }
      .fade-in { animation: fadeIn 0.3s ease forwards; }
    `;
    document.head.appendChild(style);
  }, []);
}

function Sidebar({ activeView, setActiveView }) {
  const navItems = [
    { id: 'contacts', label: 'Contacts', icon: Users },
    { id: 'deals', label: 'Deals', icon: DollarSign },
    { id: 'pipeline', label: 'Pipeline', icon: TrendingUp },
    { id: 'activities', label: 'Activities', icon: Activity },
    { id: 'reports', label: 'Reports', icon: Briefcase },
  ];

  return (
    <aside className="w-64 flex-shrink-0 flex flex-col border-r border-white/5 bg-white/[0.02] h-full">
      <div className="p-6 border-b border-white/5">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#00A86B] to-[#1A3A5C] flex items-center justify-center">
            <TrendingUp className="w-4 h-4 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold gradient-text">NovaStrategy</h1>
            <p className="text-xs text-slate-500">AI Market Intelligence</p>
          </div>
        </div>
      </div>
      <nav className="flex-1 p-4 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <button
              key={item.id}
              onClick={() => setActiveView(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-lg transition-all duration-200 ${
                activeView === item.id
                  ? 'bg-white/10 border border-white/10 text-white'
                  : 'text-slate-400 hover:bg-white/5 hover:text-slate-300'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span className="text-sm font-medium">{item.label}</span>
            </button>
          );
        })}
      </nav>
      <div className="p-4 border-t border-white/5">
        <div className="glass p-4">
          <p className="text-xs text-slate-500 mb-1">Active Engagements</p>
          <p className="text-lg font-bold text-white">24</p>
          <div className="flex items-center gap-1 mt-1">
            <span className="text-xs text-[#00A86B]">+3 this week</span>
          </div>
        </div>
      </div>
    </aside>
  );
}

function TopBar({ title, onAddContact, onAddDeal }) {
  return (
    <header className="h-14 flex items-center justify-between px-6 border-b border-white/5 flex-shrink-0">
      <div className="flex items-center gap-4">
        <h2 className="text-lg font-semibold text-white">{title}</h2>
      </div>
      <div className="flex items-center gap-3">
        {onAddContact && (
          <button onClick={onAddContact} className="glass px-4 py-2 text-sm text-white hover:bg-white/10 transition-all duration-200 flex items-center gap-2">
            <Plus className="w-4 h-4" /> Add Contact
          </button>
        )}
        {onAddDeal && (
          <button onClick={onAddDeal} className="glass px-4 py-2 text-sm text-white hover:bg-white/10 transition-all duration-200 flex items-center gap-2">
            <Plus className="w-4 h-4" /> New Deal
          </button>
        )}
      </div>
    </header>
  );
}

function KPICard({ icon: Icon, label, value, delta, positive }) {
  return (
    <div className="glass p-5 fade-in">
      <div className="flex items-center justify-between mb-3">
        <div className="p-2 rounded-lg bg-white/5">
          <Icon className="w-5 h-5 text-[#00A86B]" />
        </div>
        {delta !== undefined && (
          <span className={`text-xs font-medium flex items-center gap-1 ${positive ? 'text-[#00A86B]' : 'text-red-400'}`}>
            {positive ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
            {Math.abs(delta)}%
          </span>
        )}
      </div>
      <p className="text-2xl font-bold text-white mb-1">{value}</p>
      <p className="text-xs text-slate-500">{label}</p>
    </div>
  );
}

function LineChart() {
  const data = [30, 45, 38, 52, 48, 60, 55, 70, 65, 80, 75, 90];
  const max = Math.max(...data);
  const width = 400;
  const height = 200;
  const padding = { top: 20, right: 20, bottom: 30, left: 40 };
  const chartWidth = width - padding.left - padding.right;
  const chartHeight = height - padding.top - padding.bottom;
  const xStep = chartWidth / (data.length - 1);

  const points = data.map((d, i) => ({
    x: padding.left + i * xStep,
    y: padding.top + chartHeight - (d / max) * chartHeight
  }));

  const pathD = points.map((p, i) => (i === 0 ? `M${p.x},${p.y}` : `L${p.x},${p.y}`)).join(' ');
  const areaD = pathD + ` L${points[points.length - 1].x},${padding.top + chartHeight} L${points[0].x},${padding.top + chartHeight} Z`;

  return (
    <svg width={width} height={height} className="w-full h-auto">
      <defs>
        <linearGradient id="lineGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#00A86B" stopOpacity="0.3" />
          <stop offset="100%" stopColor="#00A86B" stopOpacity="0" />
        </linearGradient>
      </defs>
      <path d={areaD} fill="url(#lineGrad)" />
      <path d={pathD} fill="none" stroke="#00A86B" strokeWidth="2" className="animate-[draw_1s_ease-out_forwards]" />
      <style>{`@keyframes draw { from { stroke-dasharray: 1000; stroke-dashoffset: 1000; } to { stroke-dashoffset: 0; } }`}</style>
    </svg>
  );
}

function BarChart({ data = [40, 65, 35, 80, 55, 70] }) {
  const max = Math.max(...data);
  const barWidth = 40;
  const spacing = 20;
  const height = 200;
  const totalWidth = data.length * (barWidth + spacing);

  return (
    <svg width={totalWidth} height={height} className="w-full h-auto">
      <defs>
        <linearGradient id="barGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#00A86B" />
          <stop offset="100%" stopColor="#1A3A5C" />
        </linearGradient>
      </defs>
      {data.map((d, i) => (
        <g key={i}>
          <rect
            x={i * (barWidth + spacing)}
            y={height - (d / max) * height}
            width={barWidth}
            height={(d / max) * height}
            fill="url(#barGrad)"
            rx="4"
            className="animate-[grow_0.5s_ease-out_forwards]"
            style={{ animationDelay: `${i * 0.1}s` }}
          />
          <text x={i * (barWidth + spacing) + barWidth / 2} y={height - 5} textAnchor="middle" fill="#64748b" fontSize="10">
            {d}
          </text>
        </g>
      ))}
      <style>{`@keyframes grow { from { transform: scaleY(0); transform-origin: bottom; } to { transform: scaleY(1); } }`}</style>
    </svg>
  );
}

function DataTable({ columns, data, onRowClick }) {
  const [sortField, setSortField] = useState(null);
  const [sortDir, setSortDir] = useState('asc');
  const [search, setSearch] = useState('');

  const handleSort = useCallback((field) => {
    setSortDir((prev) => (sortField === field && prev === 'asc' ? 'desc' : 'asc'));
    setSortField(field);
  }, [sortField]);

  const filteredData = useMemo(() => {
    let result = (data || []).filter((row) =>
      Object.values(row).some((val) => String(val).toLowerCase().includes(search.toLowerCase()))
    );
    if (sortField) {
      result.sort((a, b) => {
        const aVal = a[sortField];
        const bVal = b[sortField];
        if (typeof aVal === 'string') {
          return sortDir === 'asc' ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
        }
        return sortDir === 'asc' ? aVal - bVal : bVal - aVal;
      });
    }
    return result;
  }, [data, search, sortField, sortDir]);

  return (
    <div className="glass p-5">
      <div className="relative mb-4">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
        <input
          type="text"
          placeholder="Search..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full bg-white/5 border border-white/10 rounded-lg pl-10 pr-4 py-2 text-sm text-white placeholder:text-slate-500 focus:outline-none focus:border-[#00A86B] transition-colors"
        />
      </div>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-white/5">
              {columns.map((col) => (
                <th
                  key={col.key}
                  onClick={() => handleSort(col.key)}
                  className="text-left py-3 px-4 text-xs font-medium text-slate-500 cursor-pointer hover:text-white transition-colors"
                >
                  <div className="flex items-center gap-1">
                    {col.label}
                    {sortField === col.key && (
                      sortDir === 'asc' ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />
                    )}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filteredData.map((row, i) => (
              <tr
                key={row.id || i}
                onClick={() => onRowClick && onRowClick(row)}
                className="border-b border-white/5 hover:bg-white/5 transition-colors cursor-pointer"
              >
                {columns.map((col) => (
                  <td key={col.key} className="py-3 px-4 text-sm text-slate-300">
                    {row[col.key]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function Modal({ isOpen, onClose, title, children }) {
  if (!isOpen) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm" onClick={onClose}>
      <div className="glass p-6 max-w-lg w-full mx-4 fade-in" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-white">{title}</h3>
          <button onClick={onClose} className="text-slate-500 hover:text-white transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>
        {children}
      </div>
    </div>
  );
}

function OpportunityKanban() {
  const [deals, setDeals] = useState([
    { id: 1, name: 'TechCorp AI Strategy', value: 450000, stage: 'lead', contact: 'Sarah Chen' },
    { id: 2, name: 'FinData Migration', value: 320000, stage: 'lead', contact: 'Mike Johnson' },
    { id: 3, name: 'HealthPlus Analytics', value: 280000, stage: 'qualified', contact: 'Emily Davis' },
    { id: 4, name: 'RetailMax Omnichannel', value: 520000, stage: 'qualified', contact: 'James Wilson' },
    { id: 5, name: 'GreenEnergy Advisory', value: 410000, stage: 'proposal', contact: 'Lisa Brown' },
    { id: 6, name: 'CloudSync Integration', value: 380000, stage: 'proposal', contact: 'David Lee' },
    { id: 7, name: 'AutoInnovate Strategy', value: 610000, stage: 'won', contact: 'Anna Kim' },
    { id: 8, name: 'BioGen Research', value: 290000, stage: 'won', contact: 'Tom Harris' },
  ]);

  const columns = [
    { id: 'lead', label: 'Lead', color: '#64748b' },
    { id: 'qualified', label: 'Qualified', color: '#3b82f6' },
    { id: 'proposal', label: 'Proposal', color: '#f59e0b' },
    { id: 'won', label: 'Won', color: '#00A86B' },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 h-full">
      {columns.map((col) => {
        const columnDeals = deals.filter((d) => d.stage === col.id);
        return (
          <div key={col.id} className="glass p-4 min-h-[400px]">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full" style={{ backgroundColor: col.color }} />
                <h3 className="text-sm font-medium text-white">{col.label}</h3>
              </div>
              <span className="text-xs text-slate-500">{columnDeals.length}</span>
            </div>
            <div className="space-y-3">
              {columnDeals.map((deal) => (
                <div key={deal.id} className="glass p-3 hover:bg-white/10 transition-all duration-200 cursor-pointer">
                  <h4 className="text-sm font-medium text-white mb-2">{deal.name}</h4>
                  <div className="flex items-center gap-2 mb-2">
                    <DollarSign className="w-3 h-3 text-[#00A86B]" />
                    <span className="text-xs text-slate-400">${deal.value.toLocaleString()}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <User className="w-3 h-3 text-slate-500" />
                    <span className="text-xs text-slate-500">{deal.contact}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}

function ActivityFeed() {
  const activities = [
    { id: 1, type: 'call', title: 'Discovery Call - TechCorp', time: '2 hours ago', description: 'Discussed AI strategy requirements' },
    { id: 2, type: 'email', title: 'Proposal sent to FinData', time: '4 hours ago', description: 'Sent detailed market entry proposal' },
    { id: 3, type: 'meeting', title: 'Strategy Workshop - HealthPlus', time: '1 day ago', description: '3-hour workshop on analytics framework' },
    { id: 4, type: 'call', title: 'Follow-up with RetailMax', time: '2 days ago', description: 'Discussed omnichannel implementation' },
    { id: 5, type: 'email', title: 'Resource allocation plan', time: '3 days ago', description: 'Sent team structure for GreenEnergy' },
  ];

  const getIcon = (type) => {
    switch (type) {
      case 'call': return <Phone className="w-4 h-4 text-[#00A86B]" />;
      case 'email': return <Mail className="w-4 h-4 text-blue-400" />;
      case 'meeting': return <Calendar className="w-4 h-4 text-yellow-400" />;
      default: return <Clock className="w-4 h-4 text-slate-400" />;
    }
  };

  return (
    <div className="space-y-4">
      {activities.map((activity) => (
        <div key={activity.id} className="glass p-4 fade-in flex items-start gap-4">
          <div className="p-2 rounded-lg bg-white/5">{getIcon(activity.type)}</div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between mb-1">
              <h4 className="text-sm font-medium text-white">{activity.title}</h4>
              <span className="text-xs text-slate-500">{activity.time}</span>
            </div>
            <p className="text-xs text-slate-400">{activity.description}</p>
          </div>
        </div>
      ))}
    </div>
  );
}

export default function App() {
  useInjectStyles();
  const [activeView, setActiveView] = useState('contacts');
  const [contactsModalOpen, setContactsModalOpen] = useState(false);
  const [dealsModalOpen, setDealsModalOpen] = useState(false);
  const [toast, setToast] = useState(null);

  const showToast = useCallback((message, type = 'success') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3000);
  }, []);

  const contactsColumns = [
    { key: 'name', label: 'Name' },
    { key: 'company', label: 'Company' },
    { key: 'status', label: 'Status' },
    { key: 'lastContact', label: 'Last Contact' },
  ];

  const contactsData = [
    { id: 1, name: 'Sarah Chen', company: 'TechCorp Industries', status: 'Active', lastContact: '2 days ago' },
    { id: 2, name: 'Mike Johnson', company: 'FinData Solutions', status: 'New', lastContact: 'Today' },
    { id: 3, name: 'Emily Davis', company: 'HealthPlus Corp', status: 'Active', lastContact: '1 week ago' },
    { id: 4, name: 'James Wilson', company: 'RetailMax Group', status: 'Inactive', lastContact: '1 month ago' },
    { id: 5, name: 'Lisa Brown', company: 'GreenEnergy Ltd', status: 'Active', lastContact: '3 days ago' },
    { id: 6, name: 'David Lee', company: 'CloudSync Tech', status: 'New', lastContact: 'Yesterday' },
  ];

  const [newContact, setNewContact] = useState({ name: '', company: '', email: '', phone: '' });
  const [newDeal, setNewDeal] = useState({ name: '', value: '', company: '', stage: 'lead' });

  const handleAddContact = useCallback((e) => {
    e.preventDefault();
    if (!newContact.name || !newContact.company || !newContact.email) {
      showToast('Please fill in all required fields', 'error');
      return;
    }
    showToast('Contact added successfully!');
    setContactsModalOpen(false);
    setNewContact({ name: '', company: '', email: '', phone: '' });
  }, [newContact, showToast]);

  const handleAddDeal = useCallback((e) => {
    e.preventDefault();
    if (!newDeal.name || !newDeal.value || !newDeal.company) {
      showToast('Please fill in all required fields', 'error');
      return;
    }
    showToast('Deal created successfully!');
    setDealsModalOpen(false);
    setNewDeal({ name: '', value: '', company: '', stage: 'lead' });
  }, [newDeal, showToast]);

  const renderView = () => {
    switch (activeView) {
      case 'contacts':
        return (
          <>
            <TopBar title="Contacts" onAddContact={() => setContactsModalOpen(true)} />
            <main className="flex-1 overflow-y-auto p-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 mb-6">
                <KPICard icon={Users} label="Total Contacts" value="6,245" delta={12} positive />
                <KPICard icon={Building2} label="Active Clients" value="234" delta={8} positive />
                <KPICard icon={Phone} label="Calls This Week" value="89" delta={5} positive />
                <KPICard icon={Mail} label="Emails Sent" value="1,342" delta={3} positive={false} />
              </div>
              <DataTable columns={contactsColumns} data={contactsData} onRowClick={(row) => showToast(`Viewing ${row.name}`)} />
            </main>
          </>
        );
      case 'deals':
        return (
          <>
            <TopBar title="Deals" onAddDeal={() => setDealsModalOpen(true)} />
            <main className="flex-1 overflow-y-auto p-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 mb-6">
                <KPICard icon={DollarSign} label="Total Pipeline Value" value="$3.26M" delta={15} positive />
                <KPICard icon={TrendingUp} label="Active Deals" value="28" delta={10} positive />
                <KPICard icon={Flag} label="Won This Quarter" value="$1.2M" delta={25} positive />
                <KPICard icon={Clock} label="Avg. Deal Cycle" value="45 days" delta={8} positive />
              </div>
              <div className="glass p-5 mb-6">
                <h3 className="text-sm font-medium text-white mb-4">Revenue Forecast</h3>
                <BarChart />
              </div>
              <div className="glass p-5">
                <h3 className="text-sm font-medium text-white mb-4">Deal Performance</h3>
                <LineChart />
              </div>
            </main>
          </>
        );
      case 'pipeline':
        return (
          <>
            <TopBar title="Pipeline" />
            <main className="flex-1 overflow-y-auto p-6">
              <OpportunityKanban />
            </main>
          </>
        );
      case 'activities':
        return (
          <>
            <TopBar title="Activities" />
            <main className="flex-1 overflow-y-auto p-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 mb-6">
                <KPICard icon={Phone} label="Calls" value="45" delta={8} positive />
                <KPICard icon={Mail} label="Emails" value="127" delta={3} positive={false} />
                <KPICard icon={Calendar} label="Meetings" value="12" delta={20} positive />
                <KPICard icon={Clock} label="Tasks Completed" value="89" delta={5} positive />
              </div>
              <ActivityFeed />
            </main>
          </>
        );
      case 'reports':
        return (
          <>
            <TopBar title="Reports" />
            <main className="flex-1 overflow-y-auto p-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 mb-6">
                <KPICard icon={Briefcase} label="Total Revenue" value="$4.8M" delta={22} positive />
                <KPICard icon={TrendingUp} label="Growth Rate" value="18.5%" delta={3} positive />
                <KPICard icon={Users} label="Client Retention" value="94%" delta={2} positive />
                <KPICard icon={DollarSign} label="Avg. Deal Size" value="$165K" delta={7} positive />
              </div>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="glass p-5">
                  <h3 className="text-sm font-medium text-white mb-4">Quarterly Revenue</h3>
                  <BarChart data={[250, 400, 350, 520, 480, 600]} />
                </div>
                <div className="glass p-5">
                  <h3 className="text-sm font-medium text-white mb-4">Client Acquisition</h3>
                  <LineChart />
                </div>
              </div>
            </main>
          </>
        );
      default:
        return null;
    }
  };

  return (
    <div className="flex h-screen overflow-hidden bg-[#06080f] text-slate-100">
      <Sidebar activeView={activeView} setActiveView={setActiveView} />
      <div className="flex-1 flex flex-col overflow-hidden">
        {renderView()}
      </div>

      <Modal isOpen={contactsModalOpen} onClose={() => setContactsModalOpen(false)} title="Add New Contact">
        <form onSubmit={handleAddContact} className="space-y-4">
          <div>
            <label className="block text-xs text-slate-500 mb-1">Name *</label>
            <input
              type="text"
              value={newContact.name}
              onChange={(e) => setNewContact({ ...newContact, name: e.target.value })}
              className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:border-[#00A86B]"
            />
          </div>
          <div>
            <label className="block text-xs text-slate-500 mb-1">Company *</label>
            <input
              type="text"
              value={newContact.company}
              onChange={(e) => setNewContact({ ...newContact, company: e.target.value })}
              className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:border-[#00A86B]"
            />
          </div>
          <div>
            <label className="block text-xs text-slate-500 mb-1">Email *</label>
            <input
              type="email"
              value={newContact.email}
              onChange={(e) => setNewContact({ ...newContact, email: e.target.value })}
              className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:border-[#00A86B]"
            />
          </div>
          <div>
            <label className="block text-xs text-slate-500 mb-1">Phone</label>
            <input
              type="tel"
              value={newContact.phone}
              onChange={(e) => setNewContact({ ...newContact, phone: e.target.value })}
              className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:border-[#00A86B]"
            />
          </div>
          <button type="submit" className="w-full py-2 bg-[#00A86B] rounded-lg text-sm font-medium text-white hover:bg-[#00A86B]/90 transition-colors">
            Add Contact
          </button>
        </form>
      </Modal>

      <Modal isOpen={dealsModalOpen} onClose={() => setDealsModalOpen(false)} title="Create New Deal">
        <form onSubmit={handleAddDeal} className="space-y-4">
          <div>
            <label className="block text-xs text-slate-500 mb-1">Deal Name *</label>
            <input
              type="text"
              value={newDeal.name}
              onChange={(e) => setNewDeal({ ...newDeal, name: e.target.value })}
              className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:border-[#00A86B]"
            />
          </div>
          <div>
            <label className="block text-xs text-slate-500 mb-1">Value *</label>
            <input
              type="number"
              value={newDeal.value}
              onChange={(e) => setNewDeal({ ...newDeal, value: e.target.value })}
              className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:border-[#00A86B]"
            />
          </div>
          <div>
            <label className="block text-xs text-slate-500 mb-1">Company *</label>
            <input
              type="text"
              value={newDeal.company}
              onChange={(e) => setNewDeal({ ...newDeal, company: e.target.value })}
              className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:border-[#00A86B]"
            />
          </div>
          <div>
            <label className="block text-xs text-slate-500 mb-1">Stage</label>
            <select
              value={newDeal.stage}
              onChange={(e) => setNewDeal({ ...newDeal, stage: e.target.value })}
              className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:border-[#00A86B]"
            >
              <option value="lead">Lead</option>
              <option value="qualified">Qualified</option>
              <option value="proposal">Proposal</option>
            </select>
          </div>
          <button type="submit" className="w-full py-2 bg-[#00A86B] rounded-lg text-sm font-medium text-white hover:bg-[#00A86B]/90 transition-colors">
            Create Deal
          </button>
        </form>
      </Modal>

      {toast && (
        <div className="fixed bottom-6 right-6 z-50 glass px-6 py-3 fade-in">
          <p className={`text-sm ${toast.type === 'error' ? 'text-red-400' : 'text-[#00A86B]'}`}>{toast.message}</p>
        </div>
      )}
    </div>
  );
}