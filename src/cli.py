import argparse

from context import ExportContext
from export import (
    export_bg_emote,
    export_bg_board,
    export_bg_finisher,
    export_card_back,
    export_set_watermark,
    export_set_filter_icon,
    export_league_rank,
)
from parse_args import parse_args


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
            case 'bg-board':
                export_bg_board(context)
            case 'bg-finisher':
                export_bg_finisher(context)
            case 'card-back':
                export_card_back(context)
            case 'set-watermark':
                export_set_watermark(context)
            case 'set-filter-icon':
                export_set_filter_icon(context)
            case 'league-rank':
                export_league_rank(context)
            case _:
                raise argparse.ArgumentTypeError(f'not found {export} parament in export')
