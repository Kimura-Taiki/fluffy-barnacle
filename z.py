a = {1, 2}
b = {3, 4, 5}
c = {2, 3}
if a & b: print("AB")
if b & c: print("BC")
if c & a: print("CA")

def func(et: set[int]) -> None:
    for i in et:
        print(i)

func(b)