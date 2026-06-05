import json
import os
from abc import ABC, abstractmethod
from collections import UserDict
from pathlib import Path
from typing import Any

from .tile import AbcTile


class AbcTilePack(ABC, UserDict[str, AbcTile]):
    rules_file_name = 'ruleset.json'

    def __init__(self, folder: Path):
        super().__init__()
        self.name = folder.name
        self._load(folder)

    @abstractmethod
    def load_tile(self, tile_name: str, content: list[Any]) -> AbcTile:
        pass

    def _load(self, folder: Path):
        path  = folder / AbcTilePack.rules_file_name
        assert path.exists(), f'Rules file doesn`t exist: {path}'

        with open(path, 'r', encoding='utf-8') as f:
            ruleset = json.load(f)
            for tile_name, content in ruleset.items():
                self.data[tile_name] = self.load_tile(tile_name, content)
        print(f'TilePack successfully loaded! ({path})')

    def keys(self) -> set[str]:
        return set(self.data.keys())

    @property
    def size(self) -> int:
        return len(self.data)
