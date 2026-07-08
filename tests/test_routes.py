import asyncio
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from app.api.routes import ask
from app.models.schemas import AskRequest


class AskRouteTests(unittest.TestCase):
    def test_ask_uses_agent_message_output(self):
        async def run_test():
            fake_agent = SimpleNamespace(
                invoke=lambda *args, **kwargs: {"messages": [SimpleNamespace(content="Ticket created")]}
            )

            with patch("app.api.routes.agent_with_memory", fake_agent), \
                 patch("app.api.routes.llm_fallback", return_value="fallback"):
                response = await ask(AskRequest(question="Create a ticket", session_id="demo"))

            self.assertEqual(response.answer, "Ticket created")
            self.assertEqual(response.status, "success")

        asyncio.run(run_test())


if __name__ == "__main__":
    unittest.main()
