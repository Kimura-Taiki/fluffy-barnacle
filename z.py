def logical_or_lists(li_1: list[bool], li_2: list[bool]) -> list[bool]:
    return [a or b for a, b in zip(li_1, li_2)]

# テスト
li_1 = [True, True, True, False, False, False, False, False, False, False]
li_2 = [False, False, False, False, True, True, True, False, False, False]
li_wa = logical_or_lists(li_1, li_2)
print(li_wa)  # Output: [True, True, True, False, True, True, True, False, False, False]
