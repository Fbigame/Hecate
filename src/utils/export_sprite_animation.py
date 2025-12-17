import os
from pathlib import Path
from typing import Sequence

from PIL import Image


def export_sprite_animation(
        frames: Sequence[Image.Image],
        stop_time: float,
        output_folder: os.PathLike[str] | str,
        name: str,
        file_type: str,
        loop: int = 0,
):
    """导出 Sprite 动画（GIF / APNG / WebP）

    规则：
    - GIF：白底（不透明）
    - APNG / WebP：透明底

    Args:
        frames: PIL.Image 列表（顺序即动画顺序）
        stop_time: AnimationClip.m_StopTime（秒）
        output_folder: 输出目录
        name: 文件名（不含后缀）
        file_type: gif / apng / webp
        loop: 循环次数，0 表示无限
    """
    frames = list(frames)
    if not frames:
        raise ValueError("frames is empty")
    
    fmt = file_type.lower()
    if fmt not in {"gif", "apng", "webp"}:
        raise ValueError(f"Unsupported file_type: {file_type}")
    
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)
    
    # ======================
    # 1. 统一 RGBA
    # ======================
    rgba_frames = [img.convert("RGBA") for img in frames]
    
    # ======================
    # 2. 统一尺寸
    # ======================
    max_w = max(img.width for img in rgba_frames)
    max_h = max(img.height for img in rgba_frames)
    
    normalized = []
    for img in rgba_frames:
        canvas = Image.new("RGBA", (max_w, max_h), (0, 0, 0, 0))
        x = (max_w - img.width) // 2
        y = (max_h - img.height) // 2
        canvas.paste(img, (x, y), img)
        normalized.append(canvas)
    
    frames = normalized
    
    # ======================
    # 3. 时间计算
    # ======================
    frame_count = len(frames)
    per_frame_ms = int(stop_time / frame_count * 1000)
    durations = [0] + [per_frame_ms] * (frame_count - 1)
    
    output_path = output_folder / f"{name}.{fmt}"
    
    # ======================
    # GIF（白底）
    # ======================
    if fmt == "gif":
        white_bg = (255, 255, 255, 255)
        
        gif_frames = []
        for img in frames:
            bg = Image.new("RGBA", img.size, white_bg)
            bg.paste(img, (0, 0), img)
            pal = bg.convert("RGB").quantize(
                colors=256,
                method=Image.Quantize.MEDIANCUT,
                dither=Image.Dither.FLOYDSTEINBERG,
            )
            gif_frames.append(pal)
        
        gif_frames[0].save(
            output_path,
            save_all=True,
            append_images=gif_frames[1:],
            duration=durations,
            loop=loop,
            disposal=2,
            optimize=False,
        )
    
    # ======================
    # APNG（透明）
    # ======================
    elif fmt == "apng":
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=durations,
            loop=loop,
            format="PNG",
            disposal=2,
            optimize=False,
        )
    
    # ======================
    # WebP（透明）
    # ======================
    elif fmt == "webp":
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=durations,
            loop=loop,
            format="WEBP",
            lossless=True,
            method=6,
            exact=True,
        )
    
    return output_path
