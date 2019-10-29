import pytest

from status_map import StatusMap, __version__
from status_map.exceptions import (
    AmbiguousTransitionError,
    FutureTransitionError,
    PastTransitionError,
    StatusNotFoundError,
    TransitionNotFoundError,
)


def test_version():
    assert __version__ == "0.5.1"


def test_status_map_magic_methods(transitions_map):
    assert str(transitions_map) == "('pending', 'processing', 'approved', 'rejected', 'processed')"

    assert (
        repr(transitions_map)
        == "StatusMap(statuses=('pending', 'processing', 'approved', 'rejected', 'processed'))"
    )
    assert len(transitions_map) == 5

    assert transitions_map["pending"]
    with pytest.raises(KeyError):
        transitions_map["does_not_exist"]

    assert "pending" in iter(transitions_map)


def test_status_map_properties(transitions_map):
    assert transitions_map.statuses == ("pending", "processing", "approved", "rejected", "processed")


def test_status_map_cached_get_ancestors(transitions_map, repeated_statuses):
    for status in repeated_statuses:
        transitions_map.get_ancestors(transitions_map._graph, status)

    cache_info = transitions_map.get_ancestors.cache_info()
    assert cache_info.hits == 8
    assert cache_info.misses == 5
    assert cache_info.maxsize == 512
    assert cache_info.currsize == 5


def test_status_map_cached_get_descendants(transitions_map, repeated_statuses):
    for status in repeated_statuses:
        transitions_map.get_descendants(transitions_map._graph, status)

    cache_info = transitions_map.get_descendants.cache_info()
    assert cache_info.hits == 8
    assert cache_info.misses == 5
    assert cache_info.maxsize == 512
    assert cache_info.currsize == 5


def test_simple_transition_invalid_from_status(transitions_map):
    with pytest.raises(StatusNotFoundError) as exc:
        transitions_map.validate_transition("does-not-exists", "pending")

    assert "does-not-exists" in str(exc)
    assert "from_status" in str(exc)


def test_simple_transition_invalid_to_status(transitions_map):
    with pytest.raises(StatusNotFoundError) as exc:
        transitions_map.validate_transition("pending", "does-not-exists")

    assert "does-not-exists" in str(exc)
    assert "to_status" in str(exc)


@pytest.mark.parametrize("from_status,to_status", [("approved", "rejected"), ("processed", "rejected")])
def test_simple_validate_transition_not_found(from_status, to_status, transitions_map):
    with pytest.raises(TransitionNotFoundError):
        transitions_map.validate_transition(from_status, to_status)


@pytest.mark.parametrize(
    "from_status,to_status",
    [
        ("approved", "pending"),
        ("approved", "processing"),
        ("processed", "pending"),
        ("processed", "processing"),
        ("processed", "approved"),
    ],
)
def test_simple_validate_transition_repeated_transition(from_status, to_status, transitions_map):
    with pytest.raises(PastTransitionError):
        transitions_map.validate_transition(from_status, to_status)


@pytest.mark.parametrize(
    "from_status,to_status",
    [
        ("approved", "pending"),
        ("approved", "processing"),
        ("processed", "pending"),
        ("processed", "processing"),
        ("processed", "approved"),
        ("approved", "rejected"),
        ("processed", "rejected"),
    ],
)
def test_simple_validate_transition_repeated_transition_cyclic(from_status, to_status, cycle_transitions_map):
    with pytest.raises(PastTransitionError):
        cycle_transitions_map.validate_transition(from_status, to_status)


@pytest.mark.parametrize(
    "from_status,to_status",
    [
        ("pending", "processed"),
        ("pending", "approved"),
        ("pending", "processed"),
        ("processing", "processed"),
    ],
)
def test_simple_validate_future_transition(from_status, to_status, transitions_map):
    with pytest.raises(FutureTransitionError):
        transitions_map.validate_transition(from_status, to_status)


@pytest.mark.parametrize(
    "from_status,to_status",
    [
        ("pending", "processed"),
        ("pending", "approved"),
        ("pending", "processed"),
        ("processing", "processed"),
        ("rejected", "approved"),
        ("rejected", "processed"),
    ],
)
def test_simple_validate_future_cyclic_transition(from_status, to_status, cycle_transitions_map):
    with pytest.raises(FutureTransitionError):
        cycle_transitions_map.validate_transition(from_status, to_status)


@pytest.mark.parametrize("from_status,to_status", (("rejected", "processing"), ("processing", "pending")))
def test_ambiguous_transitions(from_status, to_status, cycle_transitions_map):
    with pytest.raises(AmbiguousTransitionError):
        cycle_transitions_map.validate_transition(from_status, to_status)


@pytest.mark.parametrize(
    "from_status,to_status",
    [
        ("pending", "pending"),
        ("processing", "processing"),
        ("approved", "approved"),
        ("rejected", "rejected"),
        ("processed", "processed"),
    ],
)
def test_simple_validate_same_transition(from_status, to_status, transitions_map):
    assert transitions_map.validate_transition(from_status, to_status) is None


@pytest.mark.parametrize(
    "from_status,to_status",
    [
        ("pending", "pending"),
        ("processing", "processing"),
        ("approved", "approved"),
        ("rejected", "rejected"),
        ("processed", "processed"),
    ],
)
def test_simple_validate_same_cyclic_transition(from_status, to_status, cycle_transitions_map):
    assert cycle_transitions_map.validate_transition(from_status, to_status) is None


@pytest.mark.parametrize(
    "from_status,to_status",
    [
        ("pending", "processing"),
        ("processing", "approved"),
        ("processing", "rejected"),
        ("approved", "processed"),
    ],
)
def test_simple_validate_next_transition(from_status, to_status, transitions_map):
    assert transitions_map.validate_transition(from_status, to_status) is None


@pytest.mark.parametrize(
    "from_status,to_status",
    [
        ("pending", "processing"),
        ("processing", "approved"),
        ("processing", "rejected"),
        ("approved", "processed"),
        # is next status because transitions are cyclic
        ("rejected", "pending"),
    ],
)
def test_simple_validate_next_cyclic_transition(from_status, to_status, cycle_transitions_map):
    assert cycle_transitions_map.validate_transition(from_status, to_status) is None


def test_custom_status_map_case():
    status_map = {
        "": {"created"},
        "created": {"sent", "sent_error"},
        "sent": {"published"},
        "published": {"rejected"},
        "rejected": {"sent"},
        "sent_error": {"created"},
    }

    sm = StatusMap(status_map)
    assert sm.validate_transition("sent", "published") is None
    with pytest.raises(AmbiguousTransitionError):
        sm.validate_transition("published", "sent")


@pytest.mark.parametrize(
    "from_status,to_status",
    [
        ("pending", "pending"),
        ("shipped", "shipped"),
        ("lost", "lost"),
        ("stolen", "stolen"),
        ("seized_for_inspection", "seized_for_inspection"),
        ("awaiting_pickup_by_receiver", "awaiting_pickup_by_receiver"),
        ("delivered", "delivered"),
        ("returning_to_sender", "returning_to_sender"),
        ("returned_to_sender", "returned_to_sender"),
    ],
)
def test_validate_transition_same_status(from_status, to_status, complex_transitions_map):
    assert complex_transitions_map.validate_transition(from_status, to_status) is None


@pytest.mark.parametrize(
    "from_status,to_status",
    [
        ("pending", "shipped"),
        ("shipped", "lost"),
        ("shipped", "stolen"),
        ("shipped", "seized_for_inspection"),
        ("shipped", "awaiting_pickup_by_receiver"),
        ("shipped", "delivered"),
        ("shipped", "returning_to_sender"),
        ("shipped", "returned_to_sender"),
        ("lost", "stolen"),
        ("lost", "seized_for_inspection"),
        ("lost", "awaiting_pickup_by_receiver"),
        ("lost", "delivered"),
        ("lost", "returning_to_sender"),
        ("lost", "returned_to_sender"),
        ("stolen", "lost"),
        ("stolen", "seized_for_inspection"),
        ("stolen", "awaiting_pickup_by_receiver"),
        ("stolen", "delivered"),
        ("stolen", "returning_to_sender"),
        ("stolen", "returned_to_sender"),
        ("seized_for_inspection", "lost"),
        ("seized_for_inspection", "stolen"),
        ("seized_for_inspection", "awaiting_pickup_by_receiver"),
        ("seized_for_inspection", "delivered"),
        ("seized_for_inspection", "returning_to_sender"),
        ("seized_for_inspection", "returned_to_sender"),
        ("awaiting_pickup_by_receiver", "lost"),
        ("awaiting_pickup_by_receiver", "stolen"),
        ("awaiting_pickup_by_receiver", "seized_for_inspection"),
        ("awaiting_pickup_by_receiver", "delivered"),
        ("awaiting_pickup_by_receiver", "returning_to_sender"),
        ("awaiting_pickup_by_receiver", "returned_to_sender"),
        ("returning_to_sender", "lost"),
        ("returning_to_sender", "stolen"),
        ("returning_to_sender", "seized_for_inspection"),
        ("returning_to_sender", "delivered"),
        ("returning_to_sender", "returned_to_sender"),
    ],
)
def test_validate_transition_next_status(from_status, to_status, complex_transitions_map):
    assert complex_transitions_map.validate_transition(from_status, to_status) is None


@pytest.mark.parametrize(
    "from_status,to_status", [("delivered", "returned_to_sender"), ("returned_to_sender", "delivered")]
)
def test_validate_transitions_transition_not_found(from_status, to_status, complex_transitions_map):
    with pytest.raises(TransitionNotFoundError):
        complex_transitions_map.validate_transition(from_status, to_status)


@pytest.mark.parametrize(
    "from_status,to_status",
    [
        ("shipped", "pending"),
        ("lost", "pending"),
        ("lost", "shipped"),
        ("stolen", "pending"),
        ("stolen", "shipped"),
        ("seized_for_inspection", "pending"),
        ("seized_for_inspection", "shipped"),
        ("awaiting_pickup_by_receiver", "pending"),
        ("awaiting_pickup_by_receiver", "shipped"),
        ("delivered", "pending"),
        ("delivered", "shipped"),
        ("delivered", "lost"),
        ("delivered", "stolen"),
        ("delivered", "seized_for_inspection"),
        ("delivered", "awaiting_pickup_by_receiver"),
        ("delivered", "returning_to_sender"),
        ("returning_to_sender", "pending"),
        ("returning_to_sender", "shipped"),
        ("returned_to_sender", "pending"),
        ("returned_to_sender", "shipped"),
        ("returned_to_sender", "lost"),
        ("returned_to_sender", "stolen"),
        ("returned_to_sender", "seized_for_inspection"),
        ("returned_to_sender", "awaiting_pickup_by_receiver"),
        ("returned_to_sender", "returning_to_sender"),
    ],
)
def test_validate_transitions_repeated_transition(from_status, to_status, complex_transitions_map):
    with pytest.raises(PastTransitionError):
        complex_transitions_map.validate_transition(from_status, to_status)


@pytest.mark.parametrize(
    "from_status,to_status",
    [
        ("pending", "lost"),
        ("pending", "stolen"),
        ("pending", "seized_for_inspection"),
        ("pending", "awaiting_pickup_by_receiver"),
        ("pending", "delivered"),
        ("pending", "returning_to_sender"),
        ("pending", "returned_to_sender"),
    ],
)
def test_validate_transitions_future_transition(from_status, to_status, complex_transitions_map):
    with pytest.raises(FutureTransitionError):
        complex_transitions_map.validate_transition(from_status, to_status)


def test_complex_transitions_ambiguous_transition(complex_transitions_map):
    with pytest.raises(AmbiguousTransitionError):
        complex_transitions_map.validate_transition("returning_to_sender", "awaiting_pickup_by_receiver")
