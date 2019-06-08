from unittest import mock

import pytest

from status_map import __version__
from status_map.exceptions import RepeatedTransition, StatusNotFound, TransitionNotFound


def test_version():
    assert __version__ == "0.4.0"


def test_validate_transition_invalid_from_status(status_map):
    with pytest.raises(StatusNotFound) as exc:
        status_map.validate_transition("does-not-exists", "processing")

    assert "does-not-exists" in str(exc)
    assert "from_status" in str(exc)


def test_validate_transition_invalid_to_status(status_map):
    with pytest.raises(StatusNotFound) as exc:
        status_map.validate_transition("processing", "does-not-exists")

    assert "does-not-exists" in str(exc)
    assert "to_status" in str(exc)


def test_validate_transition_repeated_transition(status_map):
    with pytest.raises(RepeatedTransition):
        status_map.validate_transition("processing", "pending")

    with pytest.raises(RepeatedTransition):
        status_map.validate_transition("approved", "pending")

    with pytest.raises(RepeatedTransition):
        status_map.validate_transition("processed", "pending")

    with pytest.raises(RepeatedTransition):
        status_map.validate_transition("processed", "processing")

    with pytest.raises(RepeatedTransition):
        status_map.validate_transition("processed", "approved")


def test_validate_transition_transition_not_found(status_map):
    with pytest.raises(TransitionNotFound):
        status_map.validate_transition("pending", "processed")

    with pytest.raises(TransitionNotFound):
        status_map.validate_transition("pending", "approved")

    with pytest.raises(TransitionNotFound):
        status_map.validate_transition("processed", "rejected")

    with pytest.raises(TransitionNotFound):
    status_map.validate_transition("rejected", "processed")
