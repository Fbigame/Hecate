import logging
import os
from functools import cached_property
from pathlib import Path
from typing import Optional

import UnityPy
from UnityPy.files import ObjectReader, SerializedFile

from .manifest import ManifestReader


class AssetBundleNotFoundError(LookupError):
    """指定的 AssetBundle 在当前 UnityPy env 中未找到。"""
    pass


class AssetReader:
    _instances = {}
    
    def __new__(cls, folder: os.PathLike[str] | str, bundle: os.PathLike[str] | str):
        resolved_path = (Path(folder) / 'Data/Win' / bundle).resolve()
        if resolved_path not in cls._instances:
            instance = super().__new__(cls)
            instance._instances[resolved_path] = instance
        return cls._instances[resolved_path]
    
    def __init__(self, folder: os.PathLike[str] | str, bundle: os.PathLike[str] | str):
        self.folder: Path = Path(folder)
        self.bundle: str = str(bundle)
    
    @cached_property
    def env(self) -> UnityPy.Environment:
        folder = self.folder / 'Data/Win'
        
        manifest = ManifestReader(self.folder)
        dependencies = manifest.bundle_deps[self.bundle]
        logging.debug(f"{self.bundle}'s dependencies: {', '.join(dependencies)}")
        return UnityPy.load(
            (folder / self.bundle).as_posix(),
            *((folder / bundle).as_posix() for bundle in dependencies)
        )
    
    @cached_property
    def container(self):
        return self.env.container
    
    @cached_property
    def assets(self) -> list[SerializedFile]:
        return self.env.assets
    
    @cached_property
    def path_id(self) -> dict[int, list[ObjectReader]]:
        result = {}
        for obj in self.env.objects:
            result.setdefault(obj.path_id, []).append(obj)
        return result
    
    def get_pair(self, pair: dict, typename: Optional[str] = None) -> ObjectReader:
        path_id = pair['m_PathID']
        if path_id not in self.path_id:
            raise LookupError(
                f'Object (PathID={path_id}) '
                f'not found in any loaded asset'
            )
        objects = self.path_id[path_id]
        if len(objects) == 1:
            return self.path_id[path_id][0]
        if typename:
            objects = [obj for obj in objects if obj.type.name == typename]
            if len(objects) == 0:
                raise LookupError(
                    f'Object (PathID={path_id}) '
                    f'not found in any loaded asset'
                )
            if len(objects) == 1:
                return objects[0]
        
        raise LookupError(
            f'Object (PathID={path_id}) '
            f'not found in any loaded asset'
        )
