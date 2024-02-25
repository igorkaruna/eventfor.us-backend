from typing import List, Tuple


class BaseConstant:
    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        return [
            (getattr(cls, attr), attr.replace("_", " ").capitalize())
            for attr in dir(cls)
            if not callable(getattr(cls, attr)) and not attr.startswith("__")
        ]
