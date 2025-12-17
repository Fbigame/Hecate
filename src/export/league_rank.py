from context import ExportContext
from unity3d import DbfReader, ManifestReader, AssetReader
from utils import to_safe_filename


def export_league_rank(context: ExportContext):
    dbf = DbfReader(context.input)
    manifest = ManifestReader(context.input)
    save_dir = context.output / 'league-rank'
    save_dir.mkdir(parents=True, exist_ok=True)
    for name, guid in dbf.get_league_rank(context.locale).items():
        name = to_safe_filename(name)
        reader = AssetReader(context.input, manifest.base_assets_catalog[guid])
        image = reader.container[guid].deref_parse_as_object().image
        image.save(save_dir / f'{name}.png')
