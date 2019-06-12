class StatusNotFoundError(Exception):
    pass


class InvalidTransitionError(Exception):
    pass


class TransitionNotFoundError(InvalidTransitionError):
    pass


class PastTransitionError(InvalidTransitionError):
    pass


class FutureTransitionError(InvalidTransitionError):
    pass


class AmbiguousTransitionError(InvalidTransitionError):
    pass
