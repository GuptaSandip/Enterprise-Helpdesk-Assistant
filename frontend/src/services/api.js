// src/services/api.js
// All API calls to the FastAPI backend

const BASE_URL = import.meta.env.VITE_API_URL || ''

export async function askAgent({ question, session_id }) {
  const res = await fetch(`${BASE_URL}/ask`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, session_id }),
  })
  if (!res.ok) throw new Error(`API error: ${res.status}`)
  return res.json()
}

export async function fetchTickets() {
  const res = await fetch(`${BASE_URL}/tickets`)
  if (!res.ok) throw new Error(`API error: ${res.status}`)
  return res.json()
}

export async function fetchHealth() {
  const res = await fetch(`${BASE_URL}/health`)
  if (!res.ok) throw new Error(`API error: ${res.status}`)
  return res.json()
}

export async function clearSession(session_id) {
  const res = await fetch(`${BASE_URL}/session/${session_id}`, {
    method: 'DELETE',
  })
  if (!res.ok) throw new Error(`API error: ${res.status}`)
  return res.json()
}