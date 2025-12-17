from context import ExportContext
from unity3d import DbfReader, ManifestReader, AssetReader


def export_set_filter_icon(context: ExportContext):
    folder = context.input
    dbf = DbfReader(folder)
    manifest = ManifestReader(folder)
    save_dir = context.output / 'set-filter-icon'
    save_dir.mkdir(parents=True, exist_ok=True)
    icons = {
        guid
        for unit in dbf.card_set
        if (guid := unit['m_filterIconTexture'].split(':')[-1])
    }
    for guid in icons:
        reader = AssetReader(folder, manifest.base_assets_catalog[guid])
        image = reader.container[guid].deref_parse_as_object().image
        image.save(save_dir / f'{guid}.png')
