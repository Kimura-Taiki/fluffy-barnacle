from typing import Callable

def pass_func(i1: int, i2: int, key1: str, key2: str) -> None:
    print(f"{key1}を{i1}回、{key2}を{i2}回行います。")

# def pass_func(*args, **kwargs) -> None:
#     # 適切な処理を行う
#     print(args, kwargs)

func: Callable[..., None] = pass_func

# 関数呼び出し
func(1, 2, key1='value1', key2='value2')

# # mypy --strict z.pyのエラーコード
# z.py:3: error: Function is missing a type annotation for one or more arguments  [no-untyped-def]
# Found 1 error in 1 file (checked 1 source file)
