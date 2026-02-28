from pydoku.domain.models.updates.update import Update


class EarlyStopException(Exception):
    """Raised when the algorithm should stop early, for example when a solution is found."""

    def __init__(self, updates: list[Update]) -> None:
        self.updates = updates
