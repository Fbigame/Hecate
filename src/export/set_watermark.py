from context import ExportContext
from unity3d import DbfReader, ManifestReader, AssetReader
from utils import to_safe_filename


def export_set_watermark(context: ExportContext):
    folder = context.input
    dbf = DbfReader(folder)
    manifest = ManifestReader(folder)
    save_dir = context.output / 'set-watermark'
    save_dir.mkdir(parents=True, exist_ok=True)
    expansions = set()
    for unit in dbf.card_set:
        guid = unit['m_cardWatermarkTexture'].split(':')[-1]
        set_id = unit['m_ID']
        if not guid:
            continue
        expansions.add(guid)
        name = f'{set_id}'
        if set_id in dbf.set_name:
            name = f'{set_id}-{to_safe_filename(dbf.set_name[set_id][context.locale])}'
        
        reader = AssetReader(folder, manifest.base_assets_catalog[guid])
        image = reader.container[guid].deref_parse_as_object().image
        image.save(save_dir / f'{name}.png')
    for set_id, guid in dbf.mini_set_watermark.items():
        if guid in expansions:
            continue
        
        name = f'{set_id}-mini'
        if set_id in dbf.set_name:
            name = f'{set_id}-mini-{to_safe_filename(dbf.set_name[set_id][context.locale])}'
        
        reader = AssetReader(folder, manifest.base_assets_catalog[guid])
        image = reader.container[guid].deref_parse_as_object().image
        image.save(save_dir / f'{name}.png')
