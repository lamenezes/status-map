from collections.abc import Mapping
from functools import total_ordering

from .exceptions import RepeatedTransition, StatusNotFound, TransitionNotFound

__version__ = "0.2.0"


@total_ordering
class Status:
    def __init__(self, name, next=None):
        self.name = name
        self.previous = []
        self.next = []

        if next:
            self._add_next(next)

    def __repr__(self):
        return f"Status(name={self.name!r})"

    def __eq__(self, other):
        if isinstance(other, str):
            return other == self.name

        if isinstance(other, Status):
            return other.name == self.name

        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, str):
            return self.name < other

        if isinstance(other, Status):
            return self.name < other.name

        return NotImplemented

    def _add_many(self, attr, status):
        method = getattr(self, f"_add_{attr}")

        for status in status:
            method(status)

    def _add_next(self, other_status):
        if isinstance(other_status, str):
            other_status = Status(other_status)

        if isinstance(other_status, (list, set, tuple)):
            return self._add_many("next", other_status)

        self.next.append(other_status)

    def _add_previous(self, previous):
        if isinstance(previous, (list, set, tuple)):
            return self._add_many("previous", previous)

        self.previous.append(previous)
        self.previous.extend(previous.previous)


class StatusMap(Mapping):
    def __init__(self, transitions):
        self._transitions = dict(transitions)
        assert self._transitions, "must pass a non-empty dict"

        self._statuses = {}
        self._parent = None

        name, next_status = list(transitions.items())[0]
        parent = Status(name, next_status)
        self._add_status(parent)

    def __getitem__(self, key):
        if isinstance(key, Status):
            key = key.name
        return self._statuses[key]

    def __len__(self):
        return len(self._statuses)

    def __iter__(self):
        return iter(self._statuses)

    def _add_status(self, status, previous=None):
        if self._parent is None:
            self._parent = status

        self._statuses[status.name] = status

        for current in status.next:
            current._add_previous(status)
            current._add_next(self._transitions[current.name])

            if current.name not in self._statuses:
                self._add_status(current, status)

    def validate_transition(self, from_status, to_status):
        if from_status not in self._statuses:
            raise StatusNotFound(f"from status {from_status} not found")

        if to_status not in self._statuses:
            raise StatusNotFound(f"to status {to_status} not found")

        from_status = self._statuses[from_status]
        to_status = self._statuses[to_status]

        if to_status in from_status.next:
            return

        if to_status in from_status.previous:
            msg = f"transition from {from_status} to {to_status} should have happened in the past"
            raise RepeatedTransition(msg)

        raise TransitionNotFound(f"transition from {from_status} to {to_status} not found")
