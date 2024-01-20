class Youso():
    ...

class Huda(Youso):
    def is_cursor_on(self) -> bool:
        ...
    ...

class Gottenon(Youso):
    def is_cursor_on(self) -> bool:
        ...
    ...

class Gottena(list[Gottenon]):
    def get_hover_gotten(self) -> Gottenon | None:
        return next((gottenon for gottenon in self[::-1] if gottenon.is_cursor_on()), None)
    ...

    def get_hover_huda(self) -> Huda | None:
        return next((huda for huda in self[::-1] if huda.is_cursor_on()), None)
    ...

...
def get_hover() -> Youso | None:
    if youso := own_mikoto.gottena.get_hover_gotten():
        return youso
    elif youso := own_mikoto.gottena.selected.core_view.get_hover_huda():
        return youso
    else:
        return enemy_tehuda.get_hover_huda()
...

上記のPythonコードを走らせると
py.py:27: error: Incompatible types in assignment (expression has type "Huda | None", variable has type "Gottenon | None")  [assignment]
というエラーが返ります。
一方、

    elif youso_2gou := own_mikoto.gottena.selected.core_view.get_hover_huda():
        return youso_2gou

と書き換えるとエラーが無くなります。

1️⃣ yousoがGottenonでもHudaでもYousoに変わりはないのに何故エラーになるのか。
2️⃣ youso_2gouと書き換えると何故エラーが消えるのか。

解説をお願いします。