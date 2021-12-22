import subprocess
from threading import Timer, Lock
from pathlib import Path
from typing import Dict, Tuple, Optional

INFINITE_TIMEOUT = None

class State(ABC):
    def __init__(self, name, max_seconds_in_state=INFINITE_TIMEOUT):
        self._name = name
        self._max_seconds_in_state = max_seconds_in_state

    @property
    def name(self):
        return self._name

    def on_enter(self) -> None:
        pass

    def on_exit(self) -> None:
        pass

    def on_abort(self) -> None:
        pass

    def on_event(self) -> State:
        pass

    @property
    def max_seconds_in_state(self) -> Optional[float]:
        return self._max_seconds_in_state


class Event:
    def __init__(self, name, data)
        self._name = name
        self._data = data


    @property
    def name(self):
        return self._name


    @property
    def data(self):
        return self._data

class FSMError(RuntimeError):
    pass

class FSMInitError(RuntimeError):
    pass

class FSMStateTransitionError(RuntimeError):
    pass

class FSM:
    def __init__(
            states: Tuple[State],
            events: Tuple[Event],
            transitions: Tuple[Tuple[State, Event, State]],
            initial_state: State,
            timeout_state: State
    ):
        self._states = states
        self._events = events
        self._transitions = transitions
        self._transitions_from_state: Dict[State, Dict[Event, State]] = {}
        self._timeout_state = timeout_state
        self._critical_region = Lock()
        self._timeout_timer = None

        for from_state, event, to_state in transitions:
            if from_state not in self._transitions_from_state:
                self._transitions_from_state[from_state] = {}
            if event in self._transitions_from_state[from_state]:
                raise FSMInitError(
                    f"One state ('{from_state}') cannot transition to multiple states "
                    f"(['{self._transitions_from_state[from_state][event]}', '{to_state}', ...]) "
                    f"due to one event ('{event}')"
                )
            self._transitions_from_state[from_state][event] = to_state

        with self._critical_region:
            self._enter_new_state_unlocked(initial_state)


    def _enter_new_state_unlocked(self, new_state: state):
        self._current_state = next_state
        self._current_state.on_enter()
        self._timeout_timer = Timer(
            self._current_state.max_seconds_in_state, self._timeout_handler, args=(new_state, )
        )
        self._timeout_timer.start()


    def _timeout_handler(self, state_timeout_applies_to):
        with self._critical_region:
            # The timer could have expired whilst on_event() was running, just before the timer
            # was cancelled whilst event was being handled. Thus it must check that it still
            # applies to the current state.
            # NOTE: This makes the assumption states cannot re-enter
            if state_timeout_applies_to is self._current_state:
                self._current_state.on_abort()
                self._current_state = self._timeout_state


    def get_current_state(self) -> State:
        with self._critical_region:
            return self._current_state


    def on_event(self, event: Event) -> None:
        with self._critical_region:
            if event not in self._transitions_from_state[self._current_state]:
                raise FSMStateTransitionError(
                    f"Event '{event}' not handled by state '{self._current_state}'"
                )

            next_state = self._current_state.on_event()
            if next_state is not self._current_state:
                if next_state not in self._transitions_from_state[self._current_state][event]:
                    raise FSMStateTransitionError(
                        f"Next state '{next_state}' not allowed from state '{self._current_state}'"
                    )
                self._timeout_timer.cancel()
                self._current_state.on_exit()
                self._enter_new_state_unlocked(next_state)

    def render(self, svg_path: Path):
        file_lines = ["digraph FSM {"]
        for from_state, event_to_states = self._transitions_from_state.items():
            for event, to_state in event_to_states.items():
                file_lines.append(
                    f'   {from_state.name} -> {to_state.name}  [label="{event.name"];'
                )
        file_lines.append("}")
        "\n".join(file_lines)

        subprocess.run()



class MyFSM:
    _FSM_Event_GatewayStartedWan = lambda data: Event("GatewayStartedWanEvent", data)
    _FSM_Event_GatewayEneteredNewState = lambda data: Event("GatewayEneteredNewStateEvent", data)
    _FSM_Event_GatewayObtainedIpAddress = lambda data: Event("GatewayObtainedIpAddress", data)
    _FSM_Event_GatewayRebooting = lambda data: Event("GatewayRebooting", data)
    _FSM_Event_GatewayAppliedUpdate = lambda data: Event("GatewayAppliedUpdate", data)
    _FSM_Event_GatewayStartedApp = lambda data: Event("GatewayStartedApp", data)
    _FSM_Event_GatewaySetClockUsingUcontrol = lambda data: Event("GatewaySetClockUsingUcontrol", data)

    class _FSM_State_1(State):
        pass

    class _FSM_State_2(State):
        pass

    _FSM_Transition_XXX = (X,X,X)
