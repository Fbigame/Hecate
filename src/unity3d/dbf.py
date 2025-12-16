import os
from functools import cached_property, lru_cache
from pathlib import Path

import UnityPy

from constants import LANGUAGE_CODES


class DbfReader:
    _instances = {}
    
    def __new__(cls, folder: os.PathLike[str] | str):
        folder = Path(folder).resolve() / 'Data/Win'
        if folder not in cls._instances:
            instance = super().__new__(cls)
            instance._instances[folder] = instance
        return cls._instances[folder]
    
    def __init__(self, folder: os.PathLike[str] | str):
        self._unity3d_folder = Path(folder) / 'Data/Win'
    
    @cached_property
    def _container(self):
        return UnityPy.load((self._unity3d_folder / 'dbf.unity3d').as_posix()).container
    
    @lru_cache
    def _get_locale_index(self, locale: str) -> int:
        for i, lang in enumerate(LANGUAGE_CODES):
            if lang.lower() == locale:
                return i
    
    def get_locale_text(self, source, locale: str) -> str:
        return source['m_locValues'][self._get_locale_index(locale)]
    
    def get_bg_emote(self, locale: str):
        data = self._container['Assets/Game/DBF-Asset/BATTLEGROUNDS_EMOTE.asset'].read_typetree()['Records']
        return {
            self.get_locale_text(u['m_collectionShortName'], locale): guid
            for u in data if (guid := u['m_animationPath'].split(':')[-1])
        }
