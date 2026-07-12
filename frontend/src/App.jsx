// src/App.jsx
import { useState, useEffect, useCallback } from 'react'
import Header from './components/Header.jsx'
import TicketSidebar from './components/TicketSidebar.jsx'
import ChatPanel from './components/ChatPanel.jsx'
import ToolPanel from './components/ToolPanel.jsx'
import { askAgent, fetchTickets, fetchHealth, clearSession } from './services/api.js'

function generateId() {
  return Math.random().toString(36).substring(2) + Date.now().toString(36)
}

function parseToolLogs(tools_used, status) {
  if (status === 'fallback') return [{ type: 'fallback' }]

  if (!tools_used || tools_used.length === 0) {
    return [{ type: 'call', tool: 'llm_reasoning', input: 'direct answer' }]
  }

  const lines = []
  tools_used.forEach(t => {
    lines.push({ type: 'call',   tool: t.tool,   input:  t.input  })
    if (t.error)  lines.push({ type: 'error',  message: t.error  })
    if (t.output) lines.push({ type: 'result', output:  t.output })
  })
  return lines
}

export default function App() {
  const [sessionId]             = useState(() => generateId())
  const [tickets, setTickets]   = useState([])
  const [ticketsLoading, setTL] = useState(false)
  const [health, setHealth]     = useState(false)
  const [toolLogs, setToolLogs] = useState([])

  const stats = {
    total: tickets.length,
    open:  tickets.filter(t => t.status === 'open').length,
    high:  tickets.filter(t => t.priority === 'high' && t.status === 'open').length,
  }

  const loadTickets = useCallback(async () => {
    setTL(true)
    try {
      const data = await fetchTickets()
      setTickets(data.tickets || [])
    } catch(e) { console.error(e) }
    finally { setTL(false) }
  }, [])

  const checkHealth = useCallback(async () => {
    try { await fetchHealth(); setHealth(true) }
    catch { setHealth(false) }
  }, [])

  useEffect(() => {
    checkHealth()
    loadTickets()
    const interval = setInterval(loadTickets, 10000)
    return () => clearInterval(interval)
  }, [loadTickets, checkHealth])

  async function handleMessage(question) {
    const data = await askAgent({ question, session_id: sessionId })
    const lines = parseToolLogs(data.tools_used, data.status)
    setToolLogs(prev => [...prev, { timestamp: Date.now(), lines }])
    const ticketActions = ['create_ticket', 'list_open_tickets', 'get_ticket_status', 'generate_report']
    if (lines.some(l => ticketActions.includes(l.tool))) setTimeout(loadTickets, 1500)
    return data
  }

  async function handleClear() {
    setToolLogs([])
    try { await clearSession(sessionId) } catch(e) { console.error(e) }
  }

  return (
    <div className="h-screen flex flex-col bg-surface-900 overflow-hidden">
      <Header health={health} stats={stats} />
      <div className="flex flex-1 overflow-hidden">
        <TicketSidebar tickets={tickets} loading={ticketsLoading} onRefresh={loadTickets} />
        <ChatPanel sessionId={sessionId} onMessage={handleMessage} onClear={handleClear} />
        <ToolPanel logs={toolLogs} />
      </div>
    </div>
  )
}