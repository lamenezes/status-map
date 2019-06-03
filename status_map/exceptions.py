class StatusNotFound(Exception):
    pass


class InvalidTransition(Exception):
    pass


class TransitionNotFound(InvalidTransition):
    pass


class RepeatedTransition(InvalidTransition):
    pass
