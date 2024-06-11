import yaml
from typing import TypedDict, Any

# 型ヒントの定義
BoardDict = dict[str, str]
KardDict = dict[str, str]

class LangDict(TypedDict):
    board: BoardDict
    kard: KardDict

def load_yaml(file_name: str) -> LangDict:
    """YAMLファイルを読み込んで辞書として返す"""
    with open(file_name, "r") as file:
        data: LangDict = yaml.safe_load(file)
    return data

class Locales:
    def __init__(self, file_name: str = "mono.yml", base_path: str = "ll/locales") -> None:
        self._messages: LangDict = self._load_messages(file_name, base_path)

    def _load_messages(self, file_name: str, base_path: str) -> LangDict:
        """指定されたファイルからメッセージを読み込む"""
        file_path = f"{base_path}/{file_name}"
        return load_yaml(file_path)

    def get_message(self, folder: str, key: str, **kwargs: str) -> str:
        """指定されたキーに対応するメッセージを取得し、フォーマットして返す"""
        folder_dict: Any = self._messages.get(folder)
        if folder_dict is None:
            raise ValueError(f"Folder '{folder}' not found in messages.")
        
        template: str | None = folder_dict.get(key)
        if template is None:
            raise KeyError(f"Key '{key}' not found in folder '{folder}'.")
        
        return template.format(**kwargs)

# # 使用例
# locales = Locales()
# print(locales.get_message(folder="board", key="win_by_strengths", player_name="Hoge"))
