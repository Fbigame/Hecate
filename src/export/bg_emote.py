import logging

from PIL import Image

from context import ExportContext
from unity3d import DbfReader, ManifestReader, AssetReader
from utils import to_safe_filename, export_sprite_animation


def export_bg_emote(context: ExportContext):
    folder = context.input / 'Data/Win'
    dbf = DbfReader(context.input)
    manifest = ManifestReader(context.input)
    bg_emote = dbf.get_bg_emote(context.locale)
    # 收集guid对应的文件，同系列的文件往往集中
    bundles = {manifest.base_assets_catalog[guid] for guid in bg_emote.values()}
    # 根据bundle_deps把依赖也加载进来
    for bundle in bundles.copy():
        bundles.update(manifest.bundle_deps[bundle])
    
    # 把文件全部放进环境中
    for name, guid in bg_emote.items():
        try:
            name = to_safe_filename(name)
            reader = AssetReader(context.input, manifest.base_assets_catalog[guid])
            # 只提供了一个壳，不负责实际内容
            animator_controller = reader.container[guid].read_typetree()
            # clip 会定义实际内容
            clip = reader.get_pair(animator_controller['m_AnimationClips'][0]).read_typetree()
            # sprite 列表，连续播放sprite达到动画效果
            pairs = clip['m_ClipBindingConstant']['pptrCurveMapping']
            
            if is_static_sprite_clip(pairs):
                image = reader.get_pair(pairs[0]).parse_as_object().image
                export_static_image(context, name, image)
            else:
                images = [
                    reader.get_pair(pair).parse_as_object().image
                    for pair in pairs
                ]
                # 动图通过停止时间推测每一帧的时间
                stop_time = clip['m_MuscleClip']['m_StopTime']
                export_dynamic_image(context, name, stop_time, images)
        except Exception as e:
            logging.warning(f'{name} 解析失败： {e}')


def is_static_sprite_clip(pairs: list[dict]):
    # 有时候会用两张相同精灵图表示静态图片，所以要比较是否所有pair都是相同
    first, *rest = pairs
    for pair in rest:
        for key in ('m_FileID', 'm_PathID'):
            if first[key] != pair[key]:
                return False
    return True


def export_static_image(context: ExportContext, name: str, image: Image.Image):
    path = context.output / 'bg-emote' / f'{name}.png'
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path.as_posix())


def export_dynamic_image(
        context: ExportContext,
        name: str,
        stop_time: float,
        images: list[Image.Image],
):
    output = context.output / 'bg-emote'
    output.mkdir(parents=True, exist_ok=True)
    export_sprite_animation(
        images,
        stop_time,
        output,
        name,
        context.dynamic_image,
    )
