from argparse import ArgumentParser
from mp3_manager import scan, edit


def cli():
    parser = ArgumentParser(
        prog="mp3",
        description="A CLI to manage mp3."
        )
    parser.add_argument(
        "path",
        help="The path to mp3."
        )
    subparsers = parser.add_subparsers()
    
    scan_parser = subparsers.add_parser("scan", help="Scan the folder and create a csv file.")
    scan_parser.set_defaults(func=scan)
    
    edit_parser = subparsers.add_parser("edit", help="Parse csv file and edit songs metadata.")
    edit_parser.add_argument(
        "-csv",
        "--csv", 
        help="The path to csv file.",
        )
    edit_parser.set_defaults(func=edit)
    
    args = parser.parse_args()
    print(args)
    args.func(args)


if __name__ == "__main__":
    cli()