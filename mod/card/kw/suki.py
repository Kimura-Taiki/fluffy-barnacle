_atk_n_9 = Card(megami=MG_UTURO, img=pygame.image.load("cards/na_01_yurina_o_n_6.png"), name="陰の罠：破棄時攻撃", cond=auto_di, type=CT_KOUGEKI,
                aura_damage_func=int_di(3), life_damage_func=int_di(2), maai_list_func=dima_di(2, 3))

_cond_n_9: BoolDIIC = lambda delivery, call_h, cf_h, card: delivery.b_params.damage_attr != DMG_RESHUFFLE

def _kouka_n_9(delivery: Delivery, hoyuusya: int) -> None:
    if not (huda := next((huda for huda in enforce(delivery.taba_target(
    hoyuusya=hoyuusya, is_mine=True, taba_code=TC_SUTEHUDA), Taba) if
    huda.card.name == "圧気"), None)):
        popup_message.add(f"付与札「圧気」が見つかりませんでした")
        return
    if huda.usage != USAGE_DEPLOYED:
        return
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_huda=huda, to_code=UC_DUST, kazu=99)
    huda.usage = USAGE_USED
    popup_message.add("隙を突かれたので「圧気」を破棄します")

_effect_n_9 = TempKoudou(name="圧気：隙", cond=auto_di, kouka=_kouka_n_9)

_cfs_n_9 = Trigger(name="圧気", cond=_cond_n_9, trigger=TG_1_OR_MORE_DAMAGE, effect=_effect_n_9)

n_6 = Card(megami=MG_YURINA, img=pygame.image.load("cards/na_01_yurina_o_n_6.png"), name="圧気", cond=auto_di, type=CT_HUYO,
           osame=int_di(2), suki=auto_di, hakizi=_atk_n_9, cfs=[_cfs_n_9])
