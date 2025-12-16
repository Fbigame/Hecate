import UnityPy
from UnityPy.files import SerializedFile, ObjectReader


def get_obj(
        env: UnityPy.Environment, base: SerializedFile, file_path_pair: dict[str, int]
) -> tuple[SerializedFile, ObjectReader]:
    file_id, path_id = file_path_pair['m_FileID'], file_path_pair['m_PathID']
    if file_id == 0:
        return base, base.objects[path_id]
    
    dependencies = base.objects[1].read_typetree()['m_Dependencies']
    for name in dependencies:
        asset = env.get_cab(name)
        if path_id in asset.objects:
            return asset, asset.objects[path_id]
