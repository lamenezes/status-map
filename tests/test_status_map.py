from unittest import mock

import pytest

from status_map import __version__
from status_map.exceptions import RepeatedTransition, StatusNotFound, TransitionNotFound


def test_version():
    assert __version__ == "0.4.0"


def test_validate_transition_invalid_from_status(status_map_object):
    with pytest.raises(StatusNotFound) as exc:
        status_map_object.validate_transition("does-not-exists", "pending")

    assert "does-not-exists" in str(exc)
    assert "from_status" in str(exc)


def test_validate_transition_invalid_to_status(status_map_object):
    with pytest.raises(StatusNotFound) as exc:
        status_map_object.validate_transition("pending", "does-not-exists")

    assert "does-not-exists" in str(exc)
    assert "to_status" in str(exc)


@pytest.mark.parametrize('from_status,to_status', [
    ('delivered', 'pending'),
    ('delivered', 'shipped'),
    ('delivered', 'lost'),
    ('delivered', 'stolen'),
    ('delivered', 'returning_to_sender'), # its a bug, shouldnt return 0
    ('delivered', 'returned_to_sender'),
    ('delivered', 'seized_for_inspection'),
    ('delivered', 'awaiting_pickup_by_receiver'),
])
def test_validate_transition_repeated_transition(from_status, to_status, status_map_object):
    with pytest.raises(RepeatedTransition):
        status_map_object.validate_transition(from_status, to_status)


@pytest.mark.parametrize('from_status,to_status', [
    ('pending' ,'delivered'),
    ('returning_to_sender', 'awaiting_pickup_by_receiver')
])
def test_validate_transition_transition_not_found(from_status, to_status, status_map_object):
    with pytest.raises(TransitionNotFound):
        status_map_object.validate_transition(from_status, to_status)
