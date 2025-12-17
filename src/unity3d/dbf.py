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
    
    def _get_locale_text(self, source, locale: str) -> str:
        return source['m_locValues'][self._get_locale_index(locale)]
    
    def get_bg_emote(self, locale: str):
        data = self._container['Assets/Game/DBF-Asset/BATTLEGROUNDS_EMOTE.asset'].read_typetree()['Records']
        return {
            self._get_locale_text(u['m_collectionShortName'], locale): guid
            for u in data if (guid := u['m_animationPath'].split(':')[-1])
        }
    
    def get_bg_board_skin(self, locale: str):
        data = self._container['Assets/Game/DBF-Asset/BATTLEGROUNDS_BOARD_SKIN.asset'].read_typetree()['Records']
        return {
            self._get_locale_text(u['m_collectionName'], locale): guid
            for u in data if (guid := u['m_detailsTexture'].split(':')[-1])
        }
    
    def get_bg_board_finisher(self, locale: str):
        data = self._container['Assets/Game/DBF-Asset/BATTLEGROUNDS_FINISHER.asset'].read_typetree()['Records']
        return {
            self._get_locale_text(u['m_collectionName'], locale): guid
            for u in data if (guid := u['m_detailsTexture'].split(':')[-1])
        }
    
    def get_card_back(self, locale: str):
        data = self._container['Assets/Game/DBF-Asset/CARD_BACK.asset'].read_typetree()['Records']
        return {
            self._get_locale_text(u['m_name'], locale): guid
            for u in data if (guid := u['m_prefabName'].split(':')[-1])
        }
    
    @cached_property
    def card_set(self):
        data = self._container['Assets/Game/DBF-Asset/CARD_SET.asset'].read_typetree()['Records']
        return data
    
    @cached_property
    def set_name(self):
        data = self._container['Assets/Game/DBF-Asset/BOOSTER.asset'].read_typetree()['Records']
        return {
            set_id: {
                lang.lower(): value
                for lang, value in zip(LANGUAGE_CODES, unit['m_name']['m_locValues'])
            }
            for unit in data
            if (
                    (set_id := unit['m_cardSetId'])
                    and unit['m_premium'] != 1
                    and all(text != '' for text in unit['m_name']['m_locValues'])
            )
        }
    
    @cached_property
    def card(self):
        data = self._container['Assets/Game/DBF-Asset/CARD.asset'].read_typetree()['Records']
        return data
    
    @cached_property
    def event_map(self):
        data = self._container['Assets/Game/DBF-Asset/EventMap.asset'].read_typetree()
        return {v: k for k, v in zip(data["m_Keys"], data["m_Values"])}
    
    @cached_property
    def card_set_timing(self):
        data = self._container['Assets/Game/DBF-Asset/CARD_SET_TIMING.asset'].read_typetree()['Records']
        return {
            unit['m_cardId']: unit['m_cardSetId']
            for unit in data
            if unit['m_eventTimingEvent'] == 203 or self.event_map[unit["m_eventTimingEvent"]].startswith('post')
        }
    
    @cached_property
    def mini_set_watermark(self):
        return {
            self.card_set_timing[card['m_ID']]: mark
            for card in self.card
            if (mark := card["m_watermarkTextureOverride"].split(':')[-1])
        }
    
    def get_league_rank(self, locale: str):
        data = self._container['Assets/Game/DBF-Asset/LEAGUE_RANK.asset'].read_typetree()['Records']
        return {
            f"{self._get_locale_text(unit['m_medalText'], locale)}_"
            f"{self._get_locale_text(unit['m_rankName'], locale)}": guid
            for unit in data
            if (guid := unit['m_medalTexture'].split(':')[-1])
        }
    
    def test(self, locale: str):
        data = self._container['Assets/Game/DBF-Asset/CARD_BACK.asset'].read_typetree()['Records']
        return {
            self._get_locale_text(u['m_name'], locale): guid
            for u in data if (guid := u['m_prefabName'].split(':')[-1])
        }
