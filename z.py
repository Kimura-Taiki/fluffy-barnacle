class Mikoto():
    def __init__(self, is_own: bool) -> None:
        self.is_own = is_own
        self.yamahuda: Tehuda = Tehuda.made_by_files(
            surfaces=[HONOKA(i) for i in range(1, 2)],
            delivery=self, is_own=True
        )
        self.tehuda: Tehuda = Tehuda.made_by_files(
            surfaces=[UTURO(i) for i in range(1, CARDS+1)],
            delivery=self, is_own=True
        )
        self.husesute: Tehuda = Tehuda.made_by_files(
            surfaces=[HONOKA(i) for i in range(2, 4)],
            delivery=self, is_own=True
        )
        self.kirihuda: Tehuda = Tehuda.made_by_files(
            surfaces=[HONOKA(i) for i in range(4, 7)],
            delivery=self, is_own=True
        )
#                 20                  40                  60                 79
        self.gottena: Gottena = Gottena(
            data=[
                Gottenon(taba=self.yamahuda, text="山札", x=WX-140, y=WY-210),
                Gottenon(taba=self.tehuda, text="手札", x=WX-140, y=WY-150),
                Gottenon(taba=self.husesute, text="伏せ札・捨て札", x=WX-140,
                         y=WY-90),
                Gottenon(taba=self.kirihuda, text="切り札", x=WX-140, y=WY-30)
            ],
            call=partial(self._gottena_hover_select, mikoto=self)
        )
        self.view_taba: Taba = self.tehuda
