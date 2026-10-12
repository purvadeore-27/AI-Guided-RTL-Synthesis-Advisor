import argparse
import csv
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from extract_features import extract_features

CSV_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "DATA",
    "raw",
    "synthesis_results.csv"
)

FIELDNAMES = [
    "design_name",
    "device",
    "date_recorded",
    "input_count",
    "output_count",
    "signal_count",
    "process_count",
    "and_count",
    "or_count",
    "xor_count",
    "not_count",
    "add_count",
    "sub_count",
    "mul_count",
    "if_count",
    "case_count",
    "loop_count",
    "when_count",
    "clocked_process",
    "reset_present",
    "register_count",
    "loc",
    "worst_delay_ns",
    "timing_constrained",
    "path_detail",
    "slice_luts",
    "slice_registers",
    "occupied_slices",
    "muxcys",
    "bonded_iobs",
    "notes",
]


def main():
    parser = argparse.ArgumentParser(
        description="Record RTL features and verified ISE synthesis results."
    )

    parser.add_argument("--vhdl", required=True)
    parser.add_argument("--design-name", required=True)
    parser.add_argument("--device", required=True)

    parser.add_argument(
        "--worst-delay-ns",
        required=True,
        type=float
    )

    parser.add_argument(
        "--timing-constrained",
        required=True,
        choices=["yes", "no"]
    )

    parser.add_argument(
        "--path-detail",
        default=""
    )

    parser.add_argument(
        "--slice-luts",
        required=True,
        type=int
    )

    parser.add_argument(
        "--slice-registers",
        required=True,
        type=int
    )

    parser.add_argument(
        "--occupied-slices",
        required=True,
        type=int
    )

    parser.add_argument(
        "--muxcys",
        required=True,
        type=int
    )

    parser.add_argument(
        "--bonded-iobs",
        required=True,
        type=int
    )

    parser.add_argument(
        "--notes",
        default=""
    )

    args = parser.parse_args()

    # Extract the actual RTL features from the VHDL file.
    features = extract_features(args.vhdl)

    row = {
        "design_name": args.design_name,
        "device": args.device,
        "date_recorded": datetime.date.today().isoformat(),
        **features,
        "worst_delay_ns": args.worst_delay_ns,
        "timing_constrained": args.timing_constrained,
        "path_detail": args.path_detail,
        "slice_luts": args.slice_luts,
        "slice_registers": args.slice_registers,
        "occupied_slices": args.occupied_slices,
        "muxcys": args.muxcys,
        "bonded_iobs": args.bonded_iobs,
        "notes": args.notes,
    }

    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)

    file_exists = os.path.isfile(CSV_PATH)

    with open(CSV_PATH, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=FIELDNAMES
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)

    print()
    print(f"Recorded '{args.design_name}'")
    print(f"CSV: {os.path.abspath(CSV_PATH)}")


if __name__ == "__main__":
    main()