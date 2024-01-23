from functools import cached_property

def sanbai(i):
    return i*3

class MyClass:
    def __init__(self):
        self.power = 10
        self._expensive_data = None

    @cached_property
    def expensive_data(self):
        # この部分は初回のみ実行され、結果はキャッシュされる
        print("Calculating expensive data...")
        result = 1
        for _ in range(self.power):
          result = sanbai(result)
        return result

# インスタンスを作成
obj = MyClass()

# 初回アクセス時に計算が行われ、その結果がキャッシュされる
data1 = obj.expensive_data
print(data1)

# 2回目以降はキャッシュから取得されるため、再び計算は行われない
data2 = obj.expensive_data
print(data2)

obj.power = 5
data3 = obj.expensive_data
print(data3)