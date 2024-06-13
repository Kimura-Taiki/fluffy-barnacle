from enum import Enum, auto

class KardID(Enum):
    BANPEI = auto()
    HEISI = auto()
    DOUKE = auto()
    KISI = auto()
    SOURYO = auto()
    MAZYUTUSI = auto()
    SYOUGUN = auto()
    DAIZIN = auto()
    HIME = auto()
    # 他の識別子も追加できます

    @property
    def to_yaml_key(self) -> str:
        # Enum名を小文字にして返す
        return self.name.lower()
