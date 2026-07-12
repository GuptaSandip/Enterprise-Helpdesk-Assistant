// src/components/ChatPanel.jsx
import { useState, useRef, useEffect } from 'react'
import { Send, Bot, User, Loader2, Trash2 } from 'lucide-react'

const EXAMPLES = [
  'Create a high priority ticket — WiFi is down on floor 2',
  'Get details for employee E003',
  'Show me all open tickets',
  'Generate a full ticket summary report',
  'my laptop screen is broken fix it',
]

function Message({ msg }) {
  const isUser = msg.role === 'user'
  return (
    <div className={`flex gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      {/* Avatar */}
      <div className={`w-7 h-7 rounded-full flex-shrink-0 flex items-center justify-center text-xs font-bold ${
        isUser ? 'bg-brand-600 text-white' : 'bg-slate-700 text-brand-400'
      }`}>
        {isUser ? <User size={13} /> : <Bot size={13} />}
      </div>

      {/* Bubble */}
      <div className={`max-w-[78%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed whitespace-pre-wrap ${
        isUser
          ? 'bg-brand-600 text-white rounded-tr-sm'
          : 'bg-slate-800 text-slate-100 rounded-tl-sm border border-slate-700'
      }`}>
        {msg.content}
        {msg.status === 'fallback' && (
          <span className="ml-2 text-xs opacity-60">[fallback]</span>
        )}
      </div>
    </div>
  )
}

export default function ChatPanel({ sessionId, onMessage, onClear }) {
  const [messages, setMessages]   = useState([])
  const [input, setInput]         = useState('')
  const [loading, setLoading]     = useState(false)
  const bottomRef                 = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  async function send(text) {
    const question = text || input.trim()
    if (!question || loading) return

    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: question }])
    setLoading(true)

    try {
      const data = await onMessage(question)
      setMessages(prev => [...prev, {
        role:    'assistant',
        content: data.answer,
        status:  data.status,
      }])
    } catch (err) {
      setMessages(prev => [...prev, {
        role:    'assistant',
        content: '⚠️ Service temporarily unavailable. Please try again.',
        status:  'error',
      }])
    } finally {
      setLoading(false)
    }
  }

  function handleClear() {
    setMessages([])
    onClear()
  }

  return (
    <div className="flex-1 flex flex-col min-w-0">

      {/* Chat header */}
      <div className="flex items-center justify-between px-5 py-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <Bot size={15} className="text-brand-400" />
          <span className="text-sm font-semibold text-white">AI Assistant</span>
          {loading && <Loader2 size={12} className="text-brand-400 animate-spin" />}
        </div>
        <button onClick={handleClear} className="flex items-center gap-1.5 text-xs text-slate-500 hover:text-slate-300 transition-colors px-2 py-1 rounded hover:bg-slate-800">
          <Trash2 size={11} />
          Clear chat
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-5 py-4 space-y-4">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full gap-6 text-center">
            <div>
              <div className="w-14 h-14 rounded-2xl bg-brand-600/20 border border-brand-600/30 flex items-center justify-center mx-auto mb-3">
                <Bot size={26} className="text-brand-400" />
              </div>
              <p className="text-sm font-medium text-white">Enterprise Helpdesk Assistant</p>
              <p className="text-xs text-slate-500 mt-1">Create tickets · Look up employees · Generate reports</p>
            </div>

            {/* Example prompts */}
            <div className="w-full max-w-sm space-y-2">
              <p className="text-xs text-slate-600 font-medium uppercase tracking-wider">Try an example</p>
              {EXAMPLES.map((ex, i) => (
                <button key={i} onClick={() => send(ex)}
                  className="w-full text-left px-3 py-2 rounded-lg bg-slate-800/60 border border-slate-700 hover:border-brand-600/50 hover:bg-slate-800 text-xs text-slate-400 hover:text-slate-200 transition-all">
                  {ex}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg, i) => <Message key={i} msg={msg} />)}

        {loading && (
          <div className="flex gap-3">
            <div className="w-7 h-7 rounded-full flex-shrink-0 flex items-center justify-center bg-slate-700">
              <Bot size={13} className="text-brand-400" />
            </div>
            <div className="bg-slate-800 rounded-2xl rounded-tl-sm border border-slate-700 px-4 py-3 flex items-center gap-2">
              <span className="w-1.5 h-1.5 bg-brand-400 rounded-full animate-bounce" style={{animationDelay:'0ms'}} />
              <span className="w-1.5 h-1.5 bg-brand-400 rounded-full animate-bounce" style={{animationDelay:'150ms'}} />
              <span className="w-1.5 h-1.5 bg-brand-400 rounded-full animate-bounce" style={{animationDelay:'300ms'}} />
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input box */}
      <div className="px-5 pb-5 pt-3 border-t border-slate-800">
        <div className="flex gap-2 items-end">
          <textarea
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send() }}}
            placeholder="Ask anything — create tickets, look up employees, generate reports..."
            rows={2}
            className="flex-1 bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 resize-none focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500/30 transition-colors"
          />
          <button onClick={() => send()}
            disabled={!input.trim() || loading}
            className="h-11 px-5 rounded-xl bg-brand-600 hover:bg-brand-700 disabled:opacity-40 disabled:cursor-not-allowed text-white font-semibold text-sm flex items-center gap-2 transition-colors flex-shrink-0">
            {loading ? <Loader2 size={15} className="animate-spin" /> : <Send size={15} />}
            Send
          </button>
        </div>
        <p className="text-xs text-slate-600 mt-2 text-center">Press Enter to send · Shift+Enter for new line</p>
      </div>

    </div>
  )
}