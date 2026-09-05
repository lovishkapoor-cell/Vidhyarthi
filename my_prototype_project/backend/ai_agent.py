import json
from .schemas import NavigateToPage, FetchUpcomingDeadlines, RegisterForEventTool
from pathlib import Path

PROMPT_PATH = Path(__file__).parent / "prompts" / "system_role.md"

def load_system_prompt() -> str:
    if PROMPT_PATH.exists():
        return PROMPT_PATH.read_text(encoding="utf-8")
    return "You are HubBot, a helpful assistant."

# This is a mocked AI Agent for prototype purposes.
# In a real app, this would use a library like litellm, openai, or an MCP client
# and pass the Pydantic schemas as json_schema tools.
class HubBotAgent:
    def __init__(self):
        self.system_prompt = load_system_prompt()
        self.tools = [
            NavigateToPage.model_json_schema(),
            FetchUpcomingDeadlines.model_json_schema(),
            RegisterForEventTool.model_json_schema()
        ]

    def process_message(self, user_message: str) -> dict:
        """
        Mock processing of a user message.
        """
        message_lower = user_message.lower()
        
        # Mocking tool calling logic based on keywords
        if "zen" in message_lower or "stress" in message_lower:
            return {
                "text": "Sounds like you need a break, friend. Sending you to the Zen Zone.",
                "tool_call": {
                    "name": "navigate_to_page",
                    "arguments": {"page_name": "Zen Zone"}
                }
            }
        elif "register" in message_lower or "hackathon" in message_lower:
            # Assuming a mocked event ID for demonstration
            return {
                "text": "Alright, let's get you signed up.",
                "tool_call": {
                    "name": "register_for_event",
                    "arguments": {"event_id": "mock-event-id-123"}
                }
            }
        elif "dashboard" in message_lower:
             return {
                "text": "Taking you home.",
                "tool_call": {
                    "name": "navigate_to_page",
                    "arguments": {"page_name": "Dashboard"}
                }
            }
        elif "deadline" in message_lower or "calendar" in message_lower:
            return {
                "text": "Let me check your calendar.",
                "tool_call": {
                    "name": "fetch_upcoming_deadlines",
                    "arguments": {"student_id": "current-student-id"}
                }
            }
        
        return {
            "text": "I'm HubBot. I can help you register for events, check deadlines, or chill out in the Zen Zone. What do you need?",
            "tool_call": None
        }

agent = HubBotAgent()
