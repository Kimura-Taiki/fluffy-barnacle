from typing import Type, TypeVar, Any

T = TypeVar('T')

def ensure_instance(__object: Any, __type: type[T]) -> T:
    if not isinstance(__object, __type):
        raise ValueError(f"{__object} is not an instance of {__type.__name__}")
    return __object

# 使用例
class ExampleClass:
    pass

example_instance = ExampleClass()
vvv = 55

# 正常な場合
print(ensure_instance(example_instance, ExampleClass))

# # エラーが発生する場合
ggg = ensure_instance(vvv, ExampleClass)
print(ensure_instance(vvv, ExampleClass))
# try:
#     invalid_instance = "Invalid"
#     result = ensure_instance(invalid_instance, ExampleClass)
# except ValueError as e:
#     print(f"Error: {e}")
