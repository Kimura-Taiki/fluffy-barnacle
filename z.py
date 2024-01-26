class Huda:
    pass

def custom_repr(obj):
    obj_type = type(obj).__name__
    obj_address = hex(id(obj))
    return f"<{obj_type} object at {obj_address}>"

# インスタンスの作成
huda_instance = Huda()

# カスタムな表示を得る
custom_representation = custom_repr(huda_instance)

# 表示
print(custom_representation)
print(huda_instance)