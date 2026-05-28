import { useState, useMemo } from 'react';
import { Filter, SortAsc, SortDesc, Download } from 'lucide-react';

// Helper to download CSV
function downloadCSV(csv, filename) {
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.setAttribute('href', url);
  link.setAttribute('download', filename);
  link.style.visibility = 'hidden';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

export default function ContactsView({ contacts }) {
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');
  const [sortField, setSortField] = useState('name');
  const [sortDir, setSortDir] = useState('asc');

  // Compute active filter count
  const activeFilters = useMemo(() => {
    let count = 0;
    if (search.trim()) count++;
    if (statusFilter) count++;
    if (dateFrom) count++;
    if (dateTo) count++;
    return count;
  }, [search, statusFilter, dateFrom, dateTo]);

  // Filtered contacts
  const filtered = useMemo(() => {
    return contacts.filter(c => {
      const matchesSearch =
        c.name.toLowerCase().includes(search.toLowerCase()) ||
        (c.email && c.email.toLowerCase().includes(search.toLowerCase())) ||
        (c.company && c.company.toLowerCase().includes(search.toLowerCase()));
      const matchesStatus = statusFilter ? c.status === statusFilter : true;
      const matchesDateFrom = dateFrom ? new Date(c.lastContact) >= new Date(dateFrom) : true;
      const matchesDateTo = dateTo ? new Date(c.lastContact) <= new Date(dateTo) : true;
      return matchesSearch && matchesStatus && matchesDateFrom && matchesDateTo;
    });
  }, [contacts, search, statusFilter, dateFrom, dateTo]);

  // Sorted contacts
  const sorted = useMemo(() => {
    const sortedArr = [...filtered];
    sortedArr.sort((a, b) => {
      let valA = a[sortField];
      let valB = b[sortField];
      // For dates, compare as Date objects
      if (sortField === 'lastContact') {
        valA = new Date(valA);
        valB = new Date(valB);
      }
      if (typeof valA === 'string') valA = valA.toLowerCase();
      if (typeof valB === 'string') valB = valB.toLowerCase();
      if (valA < valB) return sortDir === 'asc' ? -1 : 1;
      if (valA > valB) return sortDir === 'asc' ? 1 : -1;
      return 0;
    });
    return sortedArr;
  }, [filtered, sortField, sortDir]);

  const toggleSort = field => {
    if (sortField === field) {
      setSortDir(prev => (prev === 'asc' ? 'desc' : 'asc'));
    } else {
      setSortField(field);
      setSortDir('asc');
    }
  };

  const exportCSV = () => {
    const headers = ['Name', 'Company', 'Email', 'Phone', 'Status', 'Last Contact'];
    const rows = sorted.map(c => [c.name, c.company, c.email, c.phone, c.status, c.lastContact]);
    const csvContent = [headers, ...rows].map(e => e.map(v => `"${String(v).replace(/"/g, '""')}"`).join(','))
      .join('\n');
    const dateStamp = new Date().toISOString().slice(0, 10);
    downloadCSV(csvContent, `novamind-contacts-${dateStamp}.csv`);
  };

  return (
    <div className="space-y-4">
      {/* Toolbar */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Filter size={18} className="text-slate-400" />
          <input
            type="text"
            placeholder="Search name, email, company"
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="px-3 py-1.5 bg-white/5 border border-white/10 rounded text-sm text-slate-300 placeholder-slate-500 focus:outline-none focus:border-[#00BFA5]/50"
          />
          <select
            value={statusFilter}
            onChange={e => setStatusFilter(e.target.value)}
            className="px-2 py-1 bg-white/5 border border-white/10 rounded text-sm text-slate-300 focus:outline-none"
          >
            <option value="">All Statuses</option>
            <option value="Active">Active</option>
            <option value="Lead">Lead</option>
            <option value="Inactive">Inactive</option>
          </select>
          <input
            type="date"
            value={dateFrom}
            onChange={e => setDateFrom(e.target.value)}
            className="px-2 py-1 bg-white/5 border border-white/10 rounded text-sm text-slate-300 focus:outline-none"
            title="From date"
          />
          <input
            type="date"
            value={dateTo}
            onChange={e => setDateTo(e.target.value)}
            className="px-2 py-1 bg-white/5 border border-white/10 rounded text-sm text-slate-300 focus:outline-none"
            title="To date"
          />
          {activeFilters > 0 && (
            <span className="ml-2 px-2 py-0.5 bg-[#00BFA5]/20 text-[#00BFA5] rounded text-xs">{activeFilters} active</span>
          )}
        </div>
        <button
          onClick={exportCSV}
          className="flex items-center gap-1 px-3 py-1.5 bg-gradient-to-r from-[#00BFA5] to-[#1A3A5C] text-white rounded text-sm hover:from-[#00BFA5]/90 hover:to-[#1A3A5C]/90"
        >
          <Download size={16} /> Export
        </button>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white/5 rounded">
          <thead className="text-slate-400">
            <tr>
              {['name', 'company', 'email', 'phone', 'status', 'lastContact'].map(col => (
                <th
                  key={col}
                  onClick={() => toggleSort(col)}
                  className="px-4 py-2 cursor-pointer hover:text-white"
                >
                  <div className="flex items-center gap-1">
                    {col.charAt(0).toUpperCase() + col.slice(1)}
                    {sortField === col && (
                      sortDir === 'asc' ? <SortAsc size={14} /> : <SortDesc size={14} />
                    )}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sorted.map(c => (
              <tr key={c.id} className="border-b border-white/10 hover:bg-white/10">
                <td className="px-4 py-2 text-slate-300">{c.name}</td>
                <td className="px-4 py-2 text-slate-300">{c.company}</td>
                <td className="px-4 py-2 text-slate-300">{c.email}</td>
                <td className="px-4 py-2 text-slate-300">{c.phone}</td>
                <td className="px-4 py-2 text-slate-300">{c.status}</td>
                <td className="px-4 py-2 text-slate-300">{c.lastContact}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {sorted.length === 0 && (
          <p className="p-4 text-center text-slate-400">No contacts match the current filters.</p>
        )}
      </div>
    </div>
  );
}