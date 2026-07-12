// src/components/TicketSidebar.jsx
import { Ticket, RefreshCw, AlertCircle, Clock, CheckCircle } from 'lucide-react'

const PRIORITY_CONFIG = {
  high:   { color: 'text-red-400',    bg: 'bg-red-400/10',    border: 'border-red-400/20',    dot: 'bg-red-400'    },
  medium: { color: 'text-amber-400',  bg: 'bg-amber-400/10',  border: 'border-amber-400/20',  dot: 'bg-amber-400'  },
  low:    { color: 'text-emerald-400',bg: 'bg-emerald-400/10',border: 'border-emerald-400/20',dot: 'bg-emerald-400'},
}

function PriorityBadge({ priority }) {
  const cfg = PRIORITY_CONFIG[priority] || PRIORITY_CONFIG.medium
  return (
    <span className={`inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-xs font-medium ${cfg.bg} ${cfg.color} border ${cfg.border}`}>
      <span className={`w-1 h-1 rounded-full ${cfg.dot}`} />
      {priority}
    </span>
  )
}

export default function TicketSidebar({ tickets, loading, onRefresh }) {
  const open   = tickets.filter(t => t.status === 'open')
  const high   = open.filter(t => t.priority === 'high')
  const medium = open.filter(t => t.priority === 'medium')
  const low    = open.filter(t => t.priority === 'low')

  return (
    <aside className="w-64 flex flex-col border-r border-slate-800 bg-surface-950/60">

      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <Ticket size={14} className="text-brand-400" />
          <span className="text-sm font-semibold text-white">Tickets</span>
        </div>
        <button onClick={onRefresh} className="p-1 rounded hover:bg-slate-800 transition-colors" title="Refresh">
          <RefreshCw size={12} className={`text-slate-400 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      {/* Stats row */}
      <div className="grid grid-cols-3 gap-px m-3 rounded-lg overflow-hidden border border-slate-800">
        {[
          { label: 'High',   value: high.length,   color: 'text-red-400'     },
          { label: 'Medium', value: medium.length,  color: 'text-amber-400'   },
          { label: 'Low',    value: low.length,     color: 'text-emerald-400' },
        ].map(s => (
          <div key={s.label} className="bg-slate-800/60 px-2 py-2 text-center">
            <div className={`text-lg font-bold ${s.color}`}>{s.value}</div>
            <div className="text-xs text-slate-500">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Ticket list */}
      <div className="flex-1 overflow-y-auto px-3 pb-3 space-y-2">
        {loading && (
          <div className="text-xs text-slate-500 text-center py-4">Loading tickets...</div>
        )}

        {!loading && open.length === 0 && (
          <div className="flex flex-col items-center gap-2 py-8 text-slate-600">
            <CheckCircle size={24} />
            <span className="text-xs">No open tickets</span>
          </div>
        )}

        {!loading && open.map(ticket => (
          <div key={ticket.ticket_id} className="p-2.5 rounded-lg bg-slate-800/40 border border-slate-700/50 hover:border-slate-600 transition-colors">
            <div className="flex items-start justify-between gap-1 mb-1.5">
              <span className="text-xs font-mono text-brand-400 font-medium">{ticket.ticket_id}</span>
              <PriorityBadge priority={ticket.priority} />
            </div>
            <p className="text-xs text-slate-300 leading-snug line-clamp-2">{ticket.title}</p>
            <div className="flex items-center gap-1 mt-1.5 text-slate-500">
              <Clock size={10} />
              <span className="text-xs">{new Date(ticket.created_at).toLocaleDateString()}</span>
            </div>
          </div>
        ))}
      </div>

    </aside>
  )
}