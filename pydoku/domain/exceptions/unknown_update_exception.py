from pydoku.domain.models.updates.update import Update


class UnknownUpdateException(Exception):
    def __init__(self, update: Update) -> None:
        self.update = update
