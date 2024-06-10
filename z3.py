import yaml
from typing import Any

# YAMLファイルの読み込み
def yml_load() -> dict[str, dict[str, str]]:
    with open('messages.yml', 'r') as file:
        messages: dict[str, dict[str, str]] = yaml.safe_load(file)
    return messages

messages = yml_load()
print(messages)

def get_message(language: str, message_key: str, **kwargs: str) -> str:
    template = messages.get(language, {}).get(message_key, '')
    return template.format(**kwargs)

# 例として日本語のメッセージを取得
kard_name = "カード名"
player_name = "プレイヤー名"
message = get_message('jp', 'elimination_message', kard_name=kard_name, player_name=player_name)
print(message)

# 例として英語のメッセージを取得
message = get_message('en', 'elimination_message', kard_name=kard_name, player_name=player_name)
print(message)

# 例として韓国語のメッセージを取得
message = get_message('kr', 'elimination_message', kard_name=kard_name, player_name=player_name)
print(message)
