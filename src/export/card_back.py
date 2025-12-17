from context import ExportContext
from unity3d import DbfReader, ManifestReader, AssetReader
from utils import to_safe_filename


def export_card_back(context: ExportContext):
    dbf = DbfReader(context.input)
    manifest = ManifestReader(context.input)
    save_dir = context.output / 'card-back'
    save_dir.mkdir(parents=True, exist_ok=True)
    for name, guid in dbf.get_card_back(context.locale).items():
        name = to_safe_filename(name)
        bundle = manifest.base_assets_catalog[guid]
        reader = AssetReader(context.input, bundle)
        game_object = reader.container[guid].read_typetree()
        pair = game_object['m_Component'][1]['component']
        card_back_def = reader.get_pair(pair)
        pair = card_back_def.read_typetree()['m_CardBackTexture']
        image = reader.get_pair(pair).parse_as_object().image
        image.save((save_dir / f'{name}.png'))
