import argparse
import sys

from add_contributors import load_allcontrib, root_dir


def main(argv=sys.argv):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=("Check if a github username is listed in the BIDS contributors."),
    )
    parser.add_argument(
        "username",
        type=str,
        help="username to check",
    )

    args = parser.parse_args(argv[1:])

    allcontrib_file = root_dir() / ".all-contributorsrc"
    allcontrib = load_allcontrib(allcontrib_file)

    if any(args.username == x["login"] for x in allcontrib["contributors"]):
        print(f"{args.username} found")
        sys.exit(0)

    raise ValueError(f"{args.username} not found")


if __name__ == "__main__":
    main()
