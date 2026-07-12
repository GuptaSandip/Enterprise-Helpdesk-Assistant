// src/components/Header.jsx
import { Building2, Activity, Wifi } from 'lucide-react'

export default function Header({ health, stats }) {
  return (
    <header className="flex items-center justify-between px-6 py-3 border-b border-slate-800 bg-surface-950/80 backdrop-blur-sm">

      {/* Left — Logo + Title */}
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-lg bg-brand-600 flex items-center justify-center">
          <Building2 size={16} className="text-white" />
        </div>
        <div>
          <h1 className="text-sm font-semibold text-white leading-none">Enterprise Helpdesk Assistant</h1>
          <p className="text-xs text-slate-500 mt-0.5">AI-powered · MongoDB · LangSmith</p>
        </div>
      </div>

      {/* Center — Tech badges */}
      <div className="hidden md:flex items-center gap-2">
        {['Groq LLaMA 3.3', 'LangChain', 'MongoDB Atlas', 'LangSmith'].map(b => (
          <span key={b} className="px-2.5 py-1 rounded-full bg-slate-800 border border-slate-700 text-xs text-slate-400 font-medium">
            {b}
          </span>
        ))}
      </div>

      {/* Right — Stats + Status */}
      <div className="flex items-center gap-4">
        <div className="hidden sm:flex items-center gap-4 text-xs text-slate-400">
          <span>
            <span className="text-white font-semibold">{stats.total}</span> total
          </span>
          <span>
            <span className="text-amber-400 font-semibold">{stats.open}</span> open
          </span>
          <span>
            <span className="text-red-400 font-semibold">{stats.high}</span> high
          </span>
        </div>

        <div className="flex items-center gap-1.5">
          {health ? (
            <><Wifi size={12} className="text-emerald-400" />
            <span className="text-xs text-emerald-400 font-medium">Live</span></>
          ) : (
            <><Activity size={12} className="text-red-400" />
            <span className="text-xs text-red-400 font-medium">Offline</span></>
          )}
        </div>
      </div>

    </header>
  )
}