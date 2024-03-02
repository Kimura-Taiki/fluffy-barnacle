
from typing import NamedTuple
POP_OPEN = 0
POP_SOME_OTHER_VALUE = -999

class PopStat(NamedTuple):
    code: int
    var1: int
    var2: int
    var3: int
    text: str
    per: float

def update_code(stat: PopStat, new_code: int) -> PopStat:
    return stat._replace(code=new_code)

# 使用例
original_stat = PopStat(POP_OPEN, 1, 2, 3, "example", 0.5)
updated_stat = update_code(original_stat, new_code=POP_SOME_OTHER_VALUE)

print(updated_stat)  # 新しい code 値を持つ PopStat インスタンス
