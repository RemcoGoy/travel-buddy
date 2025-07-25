"""Manage the memory of the travel assistant agent."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

from google.adk.agents.callback_context import CallbackContext
from google.adk.sessions.state import State

from travel_assistant.shared import consts

SAMPLE_SCENARIO_PATH = os.getenv(
    "TRAVEL_ASSISTANT_SCENARIO", "travel_assistant/profiles/itinerary_empty_default.json",
)

def _set_initial_states(source: dict[str, Any], target: State | dict[str, Any]) -> None:
    """Set the initial session state given a JSON object of states.

    Args:
        source: A JSON object of states.
        target: The session state object to insert into.

    """
    if consts.SYSTEM_TIME not in target:
        target[consts.SYSTEM_TIME] = str(datetime.now())

    if consts.ITIN_INITIALIZED not in target:
        target[consts.ITIN_INITIALIZED] = True

        target.update(source)

        itinerary = source.get(consts.ITIN_KEY, {})
        if itinerary:
            target[consts.ITIN_START_DATE] = itinerary[consts.START_DATE]
            target[consts.ITIN_END_DATE] = itinerary[consts.END_DATE]
            target[consts.ITIN_DATETIME] = itinerary[consts.START_DATE]

def _load_precreated_itinerary(callback_context: CallbackContext) -> None:
    """Set up the initial state.

    Set this as a callback as before_agent_call of the root_agent.
    This gets called before the system instruction is constructed.

    Args:
        callback_context: The callback context.

    """
    data = {}
    with Path(SAMPLE_SCENARIO_PATH).open("r") as file:
        data = json.load(file)
        print(f"\nLoading Initial State: {data}\n")

    _set_initial_states(data["state"], callback_context.state)
