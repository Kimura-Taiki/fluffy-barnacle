import yaml
from typing import TypedDict

BoardDict = dict[str, str]
KardDict = dict[str, str]
class LangDict(TypedDict):
    board: BoardDict
    kard: KardDict

# YAMLファイルの読み込み
def _yml_load() -> LangDict:
    with open('ll/locales/mono.yml', 'r') as file:
        messages: LangDict = yaml.safe_load(file)
    return messages

messages = _yml_load()
print(messages, messages["board"])

# def get_message(language: str, message_key: str, **kwargs: str) -> str:
#     template = messages.get(language, {}).get(message_key, '')
#     return template.format(**kwargs)

# # 例として日本語のメッセージを取得
# kard_name = "カード名"
# player_name = "プレイヤー名"
# message = get_message('jp', 'elimination_message', kard_name=kard_name, player_name=player_name)
# print(message)

# # 例として英語のメッセージを取得
# message = get_message('en', 'elimination_message', kard_name=kard_name, player_name=player_name)
# print(message)

# # 例として韓国語のメッセージを取得
# message = get_message('kr', 'elimination_message', kard_name=kard_name, player_name=player_name)
# print(message)
