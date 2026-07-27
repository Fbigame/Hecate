import argparse
import warnings

import UnityPy.config
from UnityPy.exceptions import UnityVersionFallbackWarning

from context import ExportContext
from export.bg_emote import export_bg_emote
from parse_args import parse_args

UnityPy.config.FALLBACK_UNITY_VERSION = "6000.3.11f1"
warnings.filterwarnings("ignore", category=UnityVersionFallbackWarning)


def main():
    args = parse_args()
    context = ExportContext(
        input=args.input,
        output=args.output,
        locale=args.locale,
        dynamic_image=args.dynamic_image,
    
    )
    for export in args.export:
        match export:
            case 'bg-emote':
                export_bg_emote(context)
            case _:
                raise argparse.ArgumentTypeError(f'not found {export} parament in export')
