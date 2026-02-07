from dataclasses import dataclass, asdict


@dataclass()
class User:
    name: str
    fullname: str
    nickname: str

    def to_dict(self) -> dict:
        return asdict(self)
