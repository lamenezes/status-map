from unittest import mock

import pytest

from status_map import __version__
from status_map.exceptions import FutureTransition, RepeatedTransition, StatusNotFound, TransitionNotFound


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
    ('pending', 'pending'),
    ('shipped', 'shipped'),
    ('lost', 'lost'),
    ('stolen', 'stolen'),
    ('seized_for_inspection', 'seized_for_inspection'),
    ('awaiting_pickup_by_receiver', 'awaiting_pickup_by_receiver'),
    ('delivered', 'delivered'),
    ('returning_to_sender', 'returning_to_sender'),
    ('returned_to_sender', 'returned_to_sender'),
])
def test_validate_transition_same_status(from_status, to_status, status_map_object):
    assert status_map_object.validate_transition(from_status, to_status) is None


@pytest.mark.parametrize('from_status,to_status', [
    ('pending', 'shipped'),
    ('shipped', 'lost'),
    ('shipped', 'stolen'),
    ('shipped', 'seized_for_inspection'),
    ('shipped', 'awaiting_pickup_by_receiver'),
    ('shipped', 'delivered'),
    ('shipped', 'returning_to_sender'),
    ('shipped', 'returned_to_sender'),
    ('lost', 'stolen'),
    ('lost', 'seized_for_inspection'),
    ('lost', 'awaiting_pickup_by_receiver'),
    ('lost', 'delivered'),
    ('lost', 'returning_to_sender'),
    ('lost', 'returned_to_sender'),
    ('stolen', 'lost'),
    ('stolen', 'seized_for_inspection'),
    ('stolen', 'awaiting_pickup_by_receiver'),
    ('stolen', 'delivered'),
    ('stolen', 'returning_to_sender'),
    ('stolen', 'returned_to_sender'),
    ('seized_for_inspection', 'lost'),
    ('seized_for_inspection', 'stolen'),
    ('seized_for_inspection', 'awaiting_pickup_by_receiver'),
    ('seized_for_inspection', 'delivered'),
    ('seized_for_inspection', 'returning_to_sender'),
    ('seized_for_inspection', 'returned_to_sender'),
    ('awaiting_pickup_by_receiver', 'lost'),
    ('awaiting_pickup_by_receiver', 'stolen'),
    ('awaiting_pickup_by_receiver', 'seized_for_inspection'),
    ('awaiting_pickup_by_receiver', 'delivered'),
    ('awaiting_pickup_by_receiver', 'returning_to_sender'),
    ('awaiting_pickup_by_receiver', 'returned_to_sender'),
    ('returning_to_sender', 'lost'),
    ('returning_to_sender', 'stolen'),
    ('returning_to_sender', 'seized_for_inspection'),
    ('returning_to_sender', 'delivered'),
    ('returning_to_sender', 'returned_to_sender'),
])
def test_validate_transition_next_status(from_status, to_status, status_map_object):
    assert status_map_object.validate_transition(from_status, to_status) is None


@pytest.mark.parametrize('from_status,to_status', [
    ('delivered', 'returned_to_sender'),
    ('returned_to_sender', 'delivered'),
])
def test_validate_transitions_transition_not_found(from_status, to_status, status_map_object):
    with pytest.raises(TransitionNotFound):
        status_map_object.validate_transition(from_status, to_status)


@pytest.mark.parametrize('from_status,to_status', [
    ('shipped', 'pending'),
    ('lost', 'pending'),
    ('lost', 'shipped'),
    ('stolen', 'pending'),
    ('stolen', 'shipped'),
    ('seized_for_inspection', 'pending'),
    ('seized_for_inspection', 'shipped'),
    ('awaiting_pickup_by_receiver', 'pending'),
    ('awaiting_pickup_by_receiver', 'shipped'),
    ('delivered', 'pending'),
    ('delivered', 'shipped'),
    ('delivered', 'lost'),
    ('delivered', 'stolen'),
    ('delivered', 'seized_for_inspection'),
    ('delivered', 'awaiting_pickup_by_receiver'),
    ('delivered', 'returning_to_sender'),
    ('returning_to_sender', 'pending'),
    ('returning_to_sender', 'shipped'),
    ('returned_to_sender', 'pending'),
    ('returned_to_sender', 'shipped'),
    ('returned_to_sender', 'lost'),
    ('returned_to_sender', 'stolen'),
    ('returned_to_sender', 'seized_for_inspection'),
    ('returned_to_sender', 'awaiting_pickup_by_receiver'),
    ('returned_to_sender', 'returning_to_sender'),
])
def test_validate_transitions_repeated_transition(from_status, to_status, status_map_object):
    with pytest.raises(RepeatedTransition):
        status_map_object.validate_transition(from_status, to_status)


@pytest.mark.parametrize('from_status,to_status', [
    ('pending', 'lost'),
    ('pending', 'stolen'),
    ('pending', 'seized_for_inspection'),
    ('pending', 'awaiting_pickup_by_receiver'),
    ('pending', 'delivered'),
    ('pending', 'returning_to_sender'),
    ('pending', 'returned_to_sender'),
    ('returning_to_sender', 'awaiting_pickup_by_receiver'),
])
def test_validate_transitions_future_transition(from_status, to_status, status_map_object):
    with pytest.raises(FutureTransition):
        status_map_object.validate_transition(from_status, to_status)
