import logging

from context import ExportContext
from unity3d import DbfReader, ManifestReader, AssetReader
from utils import to_safe_filename


def export_bg_finisher(context: ExportContext):
    dbf = DbfReader(context.input)
    manifest = ManifestReader(context.input)
    save_dir = context.output / 'bg-finisher'
    save_dir.mkdir(parents=True, exist_ok=True)
    for name, guid in dbf.get_bg_board_finisher(context.locale).items():
        try:
            name = to_safe_filename(name)
            bundle = manifest.base_assets_catalog[guid]
            reader = AssetReader(context.input, bundle)
            
            reader.container[guid].deref_parse_as_object().image.save((save_dir / f'{name}.png'))
        except Exception as e:
            logging.warning(f'{name} 解析失败： {e}')
