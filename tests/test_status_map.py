from unittest import mock
import pytest

from status_map import __version__, Status, StatusMap
from status_map.exceptions import RepeatedTransition, StatusNotFound, TransitionNotFound
from .utils import assert_list


@pytest.fixture
def transitions():
    return {
        "pending": ["processing"],
        "processing": ["approved", "rejected"],
        "approved": ["processed"],
        "rejected": ["pending"],
        "processed": [],
    }


@pytest.fixture
def status_map(transitions):
    return StatusMap(transitions)


def test_version():
    assert __version__ == "0.1.0"


def test_status():
    status = Status("stat")

    assert status.name == "stat"
    assert status.next == []


def test_status_magic_methods():
    status = Status("stat")

    assert status.name in repr(status)
    assert status == Status("stat")
    assert status == "stat"
    assert status != 1


@mock.patch("status_map.Status._add_next")
def test_status_calls_add_next(mock_add_next):
    Status("stat", "next")

    mock_add_next.assert_called_once_with("next")


def test_status_add_next_str():
    status = Status("stat")

    status._add_next("other")

    assert status.next == ["other"]
    for next_status in status.next:
        assert isinstance(next_status, Status)


def test_status_add_next_set():
    status = Status("stat")

    status._add_next(["other", "+1", "foo"])

    assert_list(status.next, ["other", "+1", "foo"])
    for next_status in status.next:
        assert isinstance(next_status, Status)


def test_status_add_previous_str():
    status = Status("stat")

    status._add_previous(Status("other"))

    assert status.previous == ["other"]
    for previous_status in status.previous:
        assert isinstance(previous_status, Status)


def test_status_add_previous_list():
    status = Status("stat")

    status._add_previous([Status("other"), Status("+1"), Status("foo")])

    assert_list(status.previous, ["other", "+1", "foo"])
    for previous_status in status.previous:
        assert isinstance(previous_status, Status)


def test_status_map(status_map, transitions):
    assert status_map._transitions == transitions
    assert status_map._transitions is not transitions
    assert status_map._statuses
    assert status_map._parent


def test_status_map_magic_methods(status_map):
    pending = status_map["pending"]
    assert pending.name == "pending"
    assert status_map[pending] == pending
    assert len(status_map) == 5
    assert iter(status_map)
    with pytest.raises(KeyError):
        status_map["does-not-exist"]

    # inherited
    assert_list(status_map.keys(), ["pending", "processing", "approved", "rejected", "processed"])
    assert "pending" in status_map
    assert "does-not-exist" not in status_map
    assert status_map.values()
    assert status_map.items()
    assert status_map.get("pending")
    assert status_map.get("does-not-exist", None) is None


def test_status_map_build_statuses(status_map):
    assert_list(status_map["pending"].next, ["processing"])
    assert_list(status_map["pending"].previous, [])
    assert_list(status_map["processing"].next, ["approved", "rejected"])
    assert_list(status_map["processing"].previous, ["pending"])
    assert_list(status_map["approved"].next, ["processed"])
    assert_list(status_map["approved"].previous, ["processing", "pending"])
    assert_list(status_map["rejected"].next, ["pending"])
    assert_list(status_map["rejected"].previous, ["processing", "pending"])
    assert_list(status_map["processed"].next, [])
    assert_list(status_map["processed"].previous, ["processing", "pending", "approved"])


def test_validate_transition_accepeted_transitions(status_map):
    assert status_map.validate_transition("pending", "processing") is None

    assert status_map.validate_transition("processing", "approved") is None
    assert status_map.validate_transition("processing", "rejected") is None

    assert status_map.validate_transition("approved", "processed") is None

    assert status_map.validate_transition("rejected", "pending") is None


def test_validate_transition_invalid_from_status(status_map):
    with pytest.raises(StatusNotFound) as exc:
        status_map.validate_transition("does-not-exist", "processing")

    assert "does-not-exist" in str(exc)
    assert "from status" in str(exc)


def test_validate_transition_invalid_to_status(status_map):
    with pytest.raises(StatusNotFound) as exc:
        status_map.validate_transition("processing", "does-not-exist")

    assert "does-not-exist" in str(exc)
    assert "to status" in str(exc)


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


@pytest.mark.repeat(10)
def test_validate_status_should_work_in_correct_values_order():
    status_map = StatusMap({
        "": ("created", "sent"),
        "created": ("sent", "sent_error"),
        "sent": ("published", "rejected"),
        "sent_error": ("created",),
        "rejected": ("sent",),
        "published": ("rejected",),
    })

    assert_list(status_map[""].previous, [])
    assert_list(status_map[""].next, ["created", "sent"])

    assert_list(status_map["created"].previous, [""])
    assert_list(status_map["created"].next, ["sent", "sent_error"])

    assert_list(status_map["sent"].previous, ["", "created"])
    assert_list(status_map["sent"].next, ["published", "rejected"])

    assert_list(status_map["sent_error"].previous, ["", "created"])
    assert_list(status_map["sent_error"].next, ["created"])

    assert_list(status_map["rejected"].previous, ["", "created", "sent", "published"])
    assert_list(status_map["rejected"].next, ["sent"])

    assert_list(status_map["published"].previous, ["", "created", "sent"])
    assert_list(status_map["published"].next, ["rejected"])
