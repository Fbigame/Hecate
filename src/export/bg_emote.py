import UnityPy
from PIL import Image

from context import ExportContext
from unity3d import DbfReader, AssetManifestReader
from utils import get_obj, to_safe_filename, export_sprite_animation


def export_bg_emote(context: ExportContext):
    folder = context.input / 'Data/Win'
    dbf = DbfReader(context.input)
    manifest = AssetManifestReader(context.input)
    bg_emote = dbf.get_bg_emote(context.locale)
    # 收集guid对应的文件，同系列的文件往往集中
    bundles = {manifest.base_assets_catalog[guid] for guid in bg_emote.values()}
    # 根据bundle_deps把依赖也加载进来
    for bundle in bundles.copy():
        bundles.update(manifest.bundle_deps[bundle])
    
    # 把文件全部放进环境中
    env = UnityPy.load(*((folder / bundle).as_posix() for bundle in bundles))
    for name, guid in bg_emote.items():
        name = to_safe_filename(name)
        animator_controller = env.container[guid]
        pair = animator_controller.read_typetree()['m_AnimationClips'][0]
        # clip 会定义实际内容
        asset, clip = get_obj(env, animator_controller.assetsfile, pair)
        clip = clip.read_typetree()
        pairs = clip['m_ClipBindingConstant']['pptrCurveMapping']
        
        if is_static_sprite_clip(pairs):
            _, obj = get_obj(env, asset, pairs[0])
            export_static_image(context, name, obj.parse_as_object().image)
        else:
            images = [
                get_obj(env, asset, pair)[1].parse_as_object().image
                for pair in pairs
            ]
            stop_time = clip['m_MuscleClip']['m_StopTime']
            export_dynamic_image(context, name, stop_time, images)


def is_static_sprite_clip(pairs: list[dict]):
    first, *rest = pairs
    for pair in rest:
        for key in ('m_FileID', 'm_PathID'):
            if first[key] != pair[key]:
                return False
    return True


def export_static_image(context: ExportContext, name: str, image: Image.Image):
    path = context.output / 'bg_emote' / f'{name}.png'
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path.as_posix())


def export_dynamic_image(
        context: ExportContext,
        name: str,
        stop_time: float,
        images: list[Image.Image],
):
    output = context.output / 'bg_emote'
    output.mkdir(parents=True, exist_ok=True)
    export_sprite_animation(
        images,
        stop_time,
        output,
        name,
        context.dynamic_image,
    )
