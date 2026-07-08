"""
app/agent/agent.py
───────────────────
LangChain tool-calling agent wired up with:
  - Groq LLM (LLaMA 3.3 70B) for fast inference
  - 5 business action tools
  - Per-session conversation memory
  - Fallback to direct LLM on agent failure
"""
import os
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

from app.config import settings
from app.tools.business_tools import ALL_TOOLS
from app.memory.session import get_session_history


# ── System prompt ──────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are an intelligent enterprise AI assistant for an internal helpdesk system.

You help employees with:
- Creating and tracking IT, HR, and Operations support tickets
- Looking up employee information and status
- Generating management-level ticket summary reports
- Answering general business queries

Behaviour guidelines:
- Be professional, concise, and action-oriented in all responses
- AMBIGUOUS request  → state your assumption clearly, then proceed with the most reasonable action
- INVALID request    → explain why it cannot be fulfilled and suggest what the user can do instead
- MISSING info       → ask for only the minimum information needed to complete the action
- Always confirm ticket creation with the full Ticket ID
- Never fabricate ticket IDs or employee records — only surface what the tools return
- Use the conversation history to maintain context across follow-up messages
"""


# ── LLM ───────────────────────────────────────────────────────────────────────

llm = ChatGroq(
    model=settings.GROQ_MODEL,
    temperature=settings.TEMPERATURE,
    api_key=settings.GROQ_API_KEY or os.getenv("GROQ_API_KEY"),
)


# ── Prompt template ────────────────────────────────────────────────────────────

prompt = ChatPromptTemplate.from_messages([
    ("system",      SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human",       "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])


# ── Agent + executor ───────────────────────────────────────────────────────────

_agent = AgentExecutor(
    agent=create_tool_calling_agent(llm, ALL_TOOLS, prompt),
    tools=ALL_TOOLS,
    verbose=True,
    handle_parsing_errors=True,
)


# ── Agent with conversation memory ────────────────────────────────────────────

agent_with_memory = RunnableWithMessageHistory(
    _agent,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)


# ── Fallback: direct LLM call ─────────────────────────────────────────────────

def llm_fallback(question: str) -> str:
    """
    Direct LLM call used when the agent pipeline fails.
    Provides a degraded but still useful response to the user.
    """
    response = llm.invoke(
        f"You are a helpful enterprise assistant. "
        f"Answer this question briefly and professionally: {question}"
    )
    return response.content