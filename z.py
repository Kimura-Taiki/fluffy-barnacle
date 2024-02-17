class Graecia:
    class_name = ""
    def __init__(self, name: str) -> None:
        self.name = self.class_name+" "+name

def make_class(name: str) -> type[Graecia]:
    class Concrete(Graecia):
        class_name = name
    return Concrete

Alpha = make_class(name="Alpha")
a1 = Alpha(name="Aburakatabura")
print(a1.name)