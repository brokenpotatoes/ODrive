#!/usr/bin/env python3

import argparse
import sys

import yaml


def main() -> None:
    parser = argparse.ArgumentParser(description="Filter ODrive interface YAML for a specific board SKU.")
    parser.add_argument("input", help="Path to the canonical interface YAML OR '-' to read from stdin")
    parser.add_argument("output", help="Path to write the filtered interface YAML")
    parser.add_argument("--strip-axis1", action="store_true", help="Remove axis1 from the top-level interface definition")
    args = parser.parse_args()
    
    # Read from stdin or file
    if args.input == "-" or not sys.stdin.isatty():
        # Read from stdin
        content = sys.stdin.read()
        data = yaml.safe_load(content)
    else:
        # Read from file
        with open(args.input, "r", encoding="utf-8") as infile:
            data = yaml.safe_load(infile)

    if data is None:
        data = {}

    if args.strip_axis1:
        if "interfaces" in data and "ODrive3" in data["interfaces"] and "attributes" in data["interfaces"]["ODrive3"]:
            data["interfaces"]["ODrive3"]["attributes"].pop("axis1", None)

    with open(args.output, "w", encoding="utf-8") as outfile:
        yaml.safe_dump(data, outfile, sort_keys=False)


if __name__ == "__main__":
    main()
