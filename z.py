from functools import reduce

# 例として適当な _Donor クラスを仮定します
class _Donor:
    def __init__(self, name: str) -> None:
        self.name = name

    def pour(self, amount: int) -> int:
        # 何らかの処理（ここではamountを単純に加算して返す）
        return amount + 10

# サンプルデータ
dust_doner = _Donor("Dust Doner")
aura_doner = _Donor("Aura Doner")

# 処理対象の _Donor インスタンスリスト
donors_list = [dust_doner, aura_doner]

# amount の初期値
amount = 100

# functools.reduce を使用して pour メソッドをまとめて呼び出す
amount = reduce(lambda acc, donor: donor.pour(acc), donors_list, amount)

print(amount)
