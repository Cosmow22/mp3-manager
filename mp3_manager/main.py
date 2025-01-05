from argparse import ArgumentParser
from .mp3_manager import scan, edit, run_equalize


def cli():
    parser = ArgumentParser(
        prog="mp3",
        description="A CLI to manage mp3."
        )
    parser.add_argument(
        "-p", "--path",
        help="The path to mp3.",
        default=".",
        )
    parser.add_argument(
        "-csv",
        "--csv", 
        help="The path to csv file.",
        default="musics.csv",
        )
    parser.add_argument(
        "-dBFS",
        help="The desired sound level wanted. (default: -14)",
        default=-14,
        type=float,
        )
    subparsers = parser.add_subparsers()
    
    scan_parser = subparsers.add_parser("scan", help="Scan the folder and create a csv file.")
    scan_parser.set_defaults(func=scan)
    
    edit_parser = subparsers.add_parser("edit", help="Parse csv file and edit musics metadata.")
    edit_parser.set_defaults(func=edit)
    
    equalize_parser = subparsers.add_parser("equalize", help="Equalize the volume of all musics.")
    equalize_parser.set_defaults(func=run_equalize)
    
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    cli()