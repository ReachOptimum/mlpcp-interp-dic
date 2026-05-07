import argparse
import csv
import os


def main():
    parser = argparse.ArgumentParser(
        description="Extract one row from a CSV file and write it to a new CSV file."
    )
    parser.add_argument("input_csv", help="Full path to the input CSV file")
    parser.add_argument(
        "row_number",
        nargs="?",
        type=int,
        default=1,
        help="Row number to extract, starting at 1. Defaults to 1.",
    )
    args = parser.parse_args()

    if args.row_number < 1:
        raise ValueError("row_number must be 1 or greater")

    input_path = args.input_csv

    folder = os.path.dirname(input_path)
    filename = os.path.basename(input_path)
    name, ext = os.path.splitext(filename)

    output_path = os.path.join(folder, f"{name}_row_{args.row_number}{ext}")

    with open(input_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)

        selected_row = None
        for current_row_number, row in enumerate(reader, start=1):
            if current_row_number == args.row_number:
                selected_row = row
                break

    if selected_row is None:
        raise ValueError(f"Row {args.row_number} does not exist in {input_path}")

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(selected_row)

    print(f"Wrote row {args.row_number} to: {output_path}")


if __name__ == "__main__":
    main()