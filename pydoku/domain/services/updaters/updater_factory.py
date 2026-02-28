from pydoku.domain.exceptions.unknown_update_exception import UnknownUpdateException
from pydoku.domain.models.sudoku import Sudoku
from pydoku.domain.models.updates.level_1.hidden_candidates_update import (
    HiddenCandidatesUpdate,
)
from pydoku.domain.models.updates.level_1.naked_candidates_update import (
    NakedCandidatesUpdate,
)
from pydoku.domain.models.updates.unicity_update import UnicityUpdate
from pydoku.domain.models.updates.update import Update
from pydoku.domain.services.updaters.level_1.hidden_candidates_updater import (
    HiddenCandidatesUpdater,
)
from pydoku.domain.services.updaters.level_1.naked_candidates_updater import (
    NakedCandidatesUpdater,
)
from pydoku.domain.services.updaters.unicity_updater import UnicityUpdater


def apply_update(step: int, sudoku: Sudoku, update: Update) -> None:
    if isinstance(update, UnicityUpdate):
        UnicityUpdater.apply_update(step, sudoku, update)
    elif isinstance(update, HiddenCandidatesUpdate):
        HiddenCandidatesUpdater.apply_update(step, sudoku, update)
    elif isinstance(update, NakedCandidatesUpdate):
        NakedCandidatesUpdater.apply_update(step, sudoku, update)
    else:
        raise UnknownUpdateException(update)
