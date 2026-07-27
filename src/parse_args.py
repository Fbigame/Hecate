import argparse
import logging
import platform
import sys
from pathlib import Path
from typing import Callable

from context import ExtractContext
from version import __version__


def wrap_parse_list_arg(
        *allow_args: str,
        name: str,
        cannot_none: bool = False,
) -> Callable[[str], tuple[str, ...]]:
    def wrap(value: str) -> tuple[str, ...]:
        if not value:
            return tuple()
        args = tuple(strip_id for id in value.split(',') if (strip_id := id.strip()))
        # case none
        if 'none' in args:
            if cannot_none:
                raise argparse.ArgumentTypeError(f'Invalid argument: "none" in {name}')
            if len(args) > 1:
                raise argparse.ArgumentTypeError('Cannot use "none" with other arguments')
            return tuple()
        # case all
        if 'all' in args:
            if len(args) > 1:
                raise argparse.ArgumentTypeError('Cannot use "all" with other arguments')
            elif allow_args:
                return allow_args
            else:
                raise argparse.ArgumentTypeError(f'"all" is not supported in {name}')
        
        # validate arguments
        if allow_args:
            valid_args = set(allow_args)
            for arg in args:
                if arg not in valid_args:
                    raise argparse.ArgumentTypeError(f'Invalid argument: "{arg}" in {name}')
        return args
    
    return wrap


def configure_logging(output_path, level: str):
    level = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL,
    }.get(level, logging.WARNING)
    logging.basicConfig(
        filename=output_path / "log.txt",
        level=level,
        filemode='w',
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def get_input() -> Path | None:
    if platform.system() != "Windows":
        return None
    # 仅仅当 windows 环境的时候使用 winreg
    import winreg
    try:
        key_path = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Hearthstone"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
            install_location, _ = winreg.QueryValueEx(key, "InstallLocation")
            return Path(install_location)
    except (OSError, FileNotFoundError):
        return None


def parse_args():
    parser = argparse.ArgumentParser(description="hearthstone-misc-asset-extractor")
    
    # Add help and version handling
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    
    # 输入参数
    parser.add_argument(
        "--input",
        type=Path,
        default=(auto_input := get_input()),
        help="Input folder containing Hearthstone assets" + (
            f"(default: {auto_input})" if auto_input else ""
        ),
        required=auto_input is None,
    )
    
    # 输出参数
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(default := "./output"),
        help=f"Output folder for extracted assets (default: {default})",
    )
    # 导出内容
    parser.add_argument(
        '--export',
        type=wrap_parse_list_arg(*(args := (
            'bg-emote',
        )), name='export', cannot_none=True),
        help=f'Contents to export: all, {", ".join(args)}',
        required=True,
    )
    # 语言参数
    # 这会决定导出文件的名字
    parser.add_argument(
        "--locale",
        choices=(args := (
            'enus', 'zhcn', 'zhtw', 'jajp',
            'eses', 'kokr', 'ptbr', 'ruru',
            'frfr', 'esmx', 'itit', 'dede',
            'plpl', 'thth',
        )),
        default=(default := 'zhcn'),
        help=f"Language locale to extract: {', '.join(args)} (default: {default})",
    )
    # 设置如何保存动态图片
    parser.add_argument(
        "--dynamic-image",
        choices=("gif", "apng", "webp"),
        default=(default := 'gif'),
        help=f"Output format for dynamic image (default: {default})"
    )
    # log_level参数
    parser.add_argument(
        "--log-level",
        type=str,
        choices=('debug', 'info', 'warning', 'error', 'critical'),
        default=(default := 'error'),
        help=f"Set the logging level (default: {default}).\n"
             "Available options: debug, info, warning, error, critical"
    )

    # fallback_unity_version参数
    parser.add_argument(
        "--fallback-unity-version",
        type=str,
        default=(default := "6000.3.11f1"),
        help=f"Set the fallback Unity version for asset parsing (default: {default})"
    )
    
    # 如果没有传任何参数，打印帮助并退出
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(-1)
    args = parser.parse_args()
    
    if not args.input.exists() or not args.input.is_dir():
        parser.error(f"Input folder '{args.input}' does not exist or is not a directory.")
    
    output: Path = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    configure_logging(output, args.log_level)
    
    return ExtractContext(
        input=args.input,
        output=output,
        export=args.export,
        dynamic_image=args.dynamic_image,
        locale=args.locale,
        fallback_unity_version=args.fallback_unity_version,
    )
