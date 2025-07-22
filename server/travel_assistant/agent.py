"""Setup root travel assistant agent with necessary tools and memory management."""
from google.adk.agents import Agent

from travel_assistant import prompt
from travel_assistant.tools.memory import _load_precreated_itinerary

root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="A Travel Assistant using the services of multiple sub-agents",
    instruction=prompt.ROOT_AGENT_INSTR,
    sub_agents=[
        # inspiration_agent,
        # planning_agent,
        # booking_agent,
        # pre_trip_agent,
        # in_trip_agent,
        # post_trip_agent,
    ],
    before_agent_callback=_load_precreated_itinerary,
)
