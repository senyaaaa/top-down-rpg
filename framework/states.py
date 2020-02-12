import collections
import enum
from typing import Deque


class Transition:
    class Type(enum.Enum):
        Pass = 1
        Quit = 2
        Pop = 3
        Push = 4
        Switch = 5

    def __init__(self, t, state):
        self.tType = t
        self.state = state


class Trans:
    Pass = Transition(Transition.Type.Pass, None)
    Quit = Transition(Transition.Type.Quit, None)
    Pop = Transition(Transition.Type.Pop, None)
    Push = lambda s: Transition(Transition.Type.Push, s)
    Switch = lambda s: Transition(Transition.Type.Switch, s)


class State:
    def on_start(self):
        pass

    def on_stop(self):
        pass

    def handle_event(self, event) -> Transition:
        return Trans.Pass

    def update(self) -> Transition:
        return Trans.Pass


class StateMachine:
    def __init__(self, s):
        self.states: Deque[State] = collections.deque()
        self.states.append(s)
        self.running: bool = False

    def start(self):
        assert not self.running and len(self.states)

        last = self.states[-1]
        last.on_start()

        self.running = 1

    def finish(self):
        if not self.running: return

        while len(self.states):
            last = self.states.pop()
            last.on_stop()

        self.running = False

    def handle_event(self, event):
        if not self.running: return

        last = self.states[-1]
        trans = last.handle_event(event)

        self.transition(trans)

    def update(self):
        if not self.running: return

        last = self.states[-1]
        trans = last.update()
        self.transition(trans)

    def transition(self, trans):
        if not self.running: return

        if trans.tType == Transition.Type.Pass:
            pass
        elif trans.tType == Transition.Type.Quit:
            self.finish()
        elif trans.tType == Transition.Type.Pop:
            last = self.states.pop()
            last.on_stop()

            if len(self.states) == 0:
                self.running = 0
        elif trans.tType == Transition.Type.Push:

            self.states.append(trans.state)
            trans.state.on_start()
        elif trans.tType == Transition.Type.Switch:
            last = self.states.pop()
            last.on_stop()

            self.states.append(trans.state)
            trans.state.on_start()
