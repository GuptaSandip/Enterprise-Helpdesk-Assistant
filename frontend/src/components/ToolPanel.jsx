// src/components/ToolPanel.jsx
import { Terminal, Zap } from 'lucide-react'

function ToolLine({ line }) {
  if (line.type === 'call') return (
    <div className="mb-3">
      <div className="flex items-center gap-2 mb-1">
        <span className="text-slate-500 font-mono text-xs">→</span>
        <span className="text-sky-400 font-mono text-xs font-medium">tool_call</span>
      </div>
      <div className="ml-4">
        <span className="font-mono text-xs">
          <span className="text-purple-400">fn</span>
          <span className="text-white">{'('}</span>
          <span className="text-emerald-300 font-semibold">{line.tool}</span>
          <span className="text-white">{')'}</span>
        </span>
        {line.input && (
          <div className="mt-1 ml-2 text-xs font-mono text-slate-400">
            <span className="text-slate-600">input: </span>
            <span className="text-amber-300">{line.input}</span>
          </div>
        )}
      </div>
    </div>
  )

  if (line.type === 'result') return (
    <div className="mb-3 ml-4">
      <div className="flex items-center gap-2 mb-1">
        <span className="text-emerald-400 text-xs">✓</span>
        <span className="text-emerald-400 font-mono text-xs font-medium">result</span>
      </div>
      <div className="ml-2 text-xs font-mono text-slate-400 bg-slate-800/60 rounded px-2 py-1 border-l-2 border-emerald-500/40">
        {line.output}
      </div>
    </div>
  )

  if (line.type === 'error') return (
    <div className="mb-3 ml-4">
      <span className="text-red-400 font-mono text-xs">✗ error: {line.message}</span>
    </div>
  )

  if (line.type === 'fallback') return (
    <div className="mb-2">
      <span className="text-amber-400 font-mono text-xs">⚠ fallback: direct LLM response</span>
    </div>
  )

  return null
}

export default function ToolPanel({ logs }) {
  return (
    <aside className="w-72 flex flex-col border-l border-slate-800 bg-surface-950/80">

      {/* Header */}
      <div className="flex items-center gap-2 px-4 py-3 border-b border-slate-800">
        <Terminal size={14} className="text-sky-400" />
        <span className="text-sm font-semibold text-white">Agent Activity</span>
        <div className="ml-auto flex items-center gap-1">
          <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          <span className="text-xs text-emerald-400">Live</span>
        </div>
      </div>

      {/* Legend */}
      <div className="flex items-center gap-3 px-4 py-2 border-b border-slate-800 bg-slate-900/50">
        <span className="text-xs text-sky-400 font-mono">tool_call</span>
        <span className="text-xs text-slate-600">·</span>
        <span className="text-xs text-emerald-400 font-mono">result</span>
        <span className="text-xs text-slate-600">·</span>
        <span className="text-xs text-red-400 font-mono">error</span>
      </div>

      {/* Log area */}
      <div className="flex-1 overflow-y-auto p-4 font-mono">
        {logs.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full gap-3 text-slate-600">
            <Zap size={22} />
            <span className="text-xs text-center">
              Waiting for input...<br />
              <span className="text-slate-700">Tool calls will appear here</span>
            </span>
          </div>
        ) : (
          <div>
            {logs.map((entry, i) => (
              <div key={i} className="border-b border-slate-800/60 pb-3 mb-3 last:border-0">
                <div className="text-xs text-slate-600 font-mono mb-2">
                  [{new Date(entry.timestamp).toLocaleTimeString()}] query #{i + 1}
                </div>
                {entry.lines.map((line, j) => <ToolLine key={j} line={line} />)}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="px-4 py-2.5 border-t border-slate-800 bg-slate-900/50">
        <div className="flex items-center gap-1.5">
          <div className="w-1.5 h-1.5 rounded-full bg-sky-400" />
          <span className="text-xs text-slate-500 font-mono">LangSmith tracing enabled</span>
        </div>
      </div>

    </aside>
  )
}