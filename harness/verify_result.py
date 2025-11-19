#!/usr/bin/env python3
"""
verify_result.py - correctness oracle for cosine similarity
"""
# Copyright (c) 2025, Amazon Web Services
# All rights reserved.
#
# This software is licensed under the terms of the Apache v2 License.
# See the LICENSE.md file for details.
import argparse
import sys
import numpy as np

# The payloads are vectors of 7 int16 numbers
PAYLOAD_DIM = 7

GREEN = '\033[92m'
BOLD = '\033[1m'
RESET = '\033[0m'


def main():
    """
    Usage:  python3 verify_result.py  <expected_file>  <result_file> [--count_only]
    Returns exit-code 0 if equal or if there are more than 32 expected results, 1 otherwise.
    Prints a message so the caller can log it.
    """
    # Parse arguments using argparse
    parser = argparse.ArgumentParser(description='Copmare expeocted vs obtained results.')
    parser.add_argument('expected_file', type=str,
                        help='File containing the expected results')
    parser.add_argument('result_file', type=str,
                        help='File containing the obtained results')
    parser.add_argument('--count_only', action='store_true',
                        help='Only # of matches, not payloads')

    args = parser.parse_args()

    if args.count_only: # not payloads
        # Read the expected and result binary files, containing just a counter
        expected_data = np.fromfile(args.expected_file, dtype=np.int_)
        result_data = np.fromfile(args.result_file, dtype=np.int_)

        if np.array_equal(expected_data, result_data):
            print(f"         [harness] PASS (result={expected_data})")
            sys.exit(0)
        else:
            print(f"         [harness] FAIL (expected {expected_data}",
                  f"but found {result_data})")
            sys.exit(1)

    # Read the expected and result binary files containing payload vectors
    expected_data = np.fromfile(args.expected_file, dtype=np.int16)
    result_data = np.fromfile(args.result_file, dtype=np.int16)

    # Reshape into payload vectors
    expected_payloads = expected_data.reshape(-1, PAYLOAD_DIM)
    result_payloads = result_data.reshape(-1, PAYLOAD_DIM)

    num_expected = len(expected_payloads)
    num_results = len(result_payloads)

    # Otherwise, compare the payloads
    if num_expected != num_results:
        print(f"         [harness] FAIL (Expected {num_expected} payloads, got {num_results})")
        sys.exit(1)

    # Compare each payload vector
    if not np.array_equal(expected_payloads, result_payloads):
        print(f"         [harness] FAIL (Payload mismatch)")
        print(f"  Expected: {expected_payloads[0]}")
        print(f"  Got:      {result_payloads[0]}")
        sys.exit(1)

    if num_expected == 0:
        print(f"         [harness] {BOLD}{GREEN}UNKNOWN{RESET} {BOLD}caller ID{RESET}")
        sys.exit(0)
    caller_id = ''.join(chr(x) for x in result_payloads[0] if x != 0)
    print(f"         [harness] {BOLD}Retrieved caller ID: {GREEN}{caller_id}{RESET}")
    sys.exit(0)


if __name__ == "__main__":
    main()
