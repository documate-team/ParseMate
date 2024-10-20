from argparse import ArgumentParser
from utils import check_file_exists, check_file_extension
from parser.fastapi import FastAPIParser

def main() -> None:
    parser = ArgumentParser()

    parser.add_argument(
        "-w", "--framework", required=True, help="Framework being used", type=str, choices=["fastapi", "express"]
    )
    parser.add_argument(
        "-f", "--file",  required=True, help="Path to the source file", type=str,
    )

    args = parser.parse_args()

    file_exists = check_file_exists(args.file)

    if not file_exists:
        print(f'ERROR: File [{args.file}] does not exist')
        exit(1)

    is_valid_file, suffix = check_file_extension(args.framework, args.file)
    if not is_valid_file:
        print(f'ERROR: Invalid file type [{suffix}] for framework [{args.framework}]')
        exit(1)

    if args.framework == "fastapi":
        code_parser = FastAPIParser()
        tree = code_parser.parse(args.file)
        print(code_parser.extract(tree))



if __name__ == '__main__':
    main()
