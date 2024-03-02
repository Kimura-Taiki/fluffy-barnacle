#                 20                  40                  60                 79
def use_card(cards: list[Card]=[], name: str="", text: str="", mode: int=
OBAL_KIHONDOUSA, code: int=POP_OK) -> Callable[[Youso], None]:
    ...

def func(youso: Youso) -> None:
    # カードの選択肢が１枚しかなく且つそれが使用不能な場合は、ポップアップと共に弾き返す。
    if len(cards) == 1 and not cards[0].can_play(delivery=youso.delivery, hoyuusya=youso.hoyuusya, popup=True):
        return
    # カードを固有の効果で使う際に固有の条件を満たせない場合は、ポップアップと共に弾き返す。
    if isinstance(youso, Huda) and not youso.can_standard(popup=True, is_zenryoku=mode==OBAL_USE_CARD):
        return
    # ポップアップしたいテキストが存在する場合は、ポップアップする。
    if text:
        popup_message.add(text=text)
    # 条件を満たしている場合、レイヤーを作成してモデレーターに投げる。
    moderator.append(over_layer=_others_basic_action_layer(
        delivery=youso.delivery, hoyuusya=youso.hoyuusya, name=name, huda=youso if
        isinstance(youso, Huda) else None,cards=cards, mode=mode, code=code))

def _others_basic_action_layer(
        delivery: Delivery, hoyuusya: int, name: str="", huda: Any | None=None, cards:
        list[Card]=[], mode: int=OBAL_KIHONDOUSA, code: int=POP_OK) -> MonoChoiceLayer:
    # レイヤーの雛形を作る。
    mcl = MonoChoiceLayer(
        name=name if name else "<OthersBasicActionLayer>", delivery=delivery, hoyuusya=hoyuusya, huda=huda,
        mode=mode, moderate=_moderate, code=code)
    # ファクトリーを準備する。
    factory = TabaFactory(inject_kwargs={"mouseup": _mouseup}, is_ol=True)
    # OBAL_定数に応じて、mc_layer.taba属性を修正する。
    if mode == OBAL_KIHONDOUSA or mode == OBAL_SYUUTYUU:
        mcl.taba = factory.maid_by_cards(cards=cards, delivery=delivery, hoyuusya=hoyuusya)
    elif mode == OBAL_USE_CARD:
        mcl.taba = factory.maid_by_hudas(hudas=[enforce(huda, Huda)], hoyuusya=hoyuusya)
    # カード以外をクリックした際にメイン側へ戻れる様にmc_layer.other_hover属性を修正する。
    mcl.other_hover = make_undo_youso(text="OthersBasicAction")
    return mcl

def _moderate(mcl: MonoChoiceLayer, stat: PopStat) -> None:
    # 標準行動済みにする。
    mcl.delivery.m_params(mcl.hoyuusya).played_standard = True
    # カードを用いた基本動作の場合は、捨て札へカードを送る。
    if mcl.mode == OBAL_KIHONDOUSA:
        mcl.delivery.send_huda_to_ryouiki(huda=mcl.source_huda, is_mine=True, taba_code=TC_HUSEHUDA)
    # カードの効果を解決する場合は、様々な処理を適用する。
    elif mcl.mode == OBAL_USE_CARD:
        # カードをHudaクラスに確定する。
        source_huda = enforce(mcl.source_huda, Huda)
        # 使ったのが全力カードの場合は、
        if source_huda.card.zenryoku:
            mcl.delivery.m_params(mcl.hoyuusya).played_zenryoku = True
        # 使ったのが切り札の場合は、カードを使用済みにする。
        if source_huda.card.kirihuda:
            source_huda.usage = USAGE_USED
        # 使ったのが手札の場合は、捨て札へカードを送る。
        else:
            mcl.delivery.send_huda_to_ryouiki(huda=mcl.source_huda, is_mine=True, taba_code=TC_SUTEHUDA)
    # 集中を用いた基本動作の場合は、
    elif mcl.mode == OBAL_SYUUTYUU:
        mcl.delivery.send_ouka_to_ryouiki(
            hoyuusya=mcl.hoyuusya, from_mine=True, from_code=UC_SYUUTYUU,
            to_mine=False, to_code=UC_ZYOGAI)
    moderator.pop()
