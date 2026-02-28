from typing import Callable


def deprecated(override_class: type) -> Callable[[type], type]:
    def decorator(class_: type) -> type:
        print(
            f"The strategy '{class_.__name__}' is depreciated and is fully included in '{override_class.__name__}'")
        return class_

    return decorator
