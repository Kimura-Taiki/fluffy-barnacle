li = list(range(10))
# fe = list(li)
for i in (fe := list(li)):
    li.remove(i)
    print(i, li, fe)
