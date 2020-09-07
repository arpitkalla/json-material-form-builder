import os
import json
import argparse

from parser import parse_json


def main():
    argparser = argparse.ArgumentParser(description="JSON to Form Builder")
    argparser.add_argument("--json", type=str, default="basic_form.json")
    args = argparser.parse_args()

    # Read JSON file
    with open(args.json, "r") as f:
        data = json.load(f)

    # Parse out to HTML string
    out_str = parse_json(data)

    # Write to a file
    out_filepath = os.path.splitext(args.json)[0] + ".js"
    with open(out_filepath, "w") as f:
        f.write(out_str)


if __name__ == "__main__":
    main()