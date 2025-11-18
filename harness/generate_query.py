#!/usr/bin/env python3
"""
generate_query.py - Generate a random query for fetch-by-similarity.
"""
# Copyright (c) 2025, Amazon Web Services
# All rights reserved.
#
# This software is licensed under the terms of the Apache v2 License.
# See the LICENSE.md file for details.
import random
import argparse
import numpy as np
from params import InstanceParams, TOY, LARGE
import csv


def main():
    """
    Generate a random query vector and write to disk
    """
    # Parse arguments using argparse
    parser = argparse.ArgumentParser(description='Generate query for FHE benchmark.')
    parser.add_argument('size', type=int, choices=range(TOY, LARGE+1),
                        help='Dataset size (0-toy/1-small/2-medium/3-large)')
    parser.add_argument('--seed', type=int, help='Random seed for reproducibility')
    
    args = parser.parse_args()
    size = args.size
    
    # Set random seed if provided
    if args.seed is not None:
        random.seed(args.seed)
        np.random.seed(args.seed)

    # Use params.py to get instance parameters
    params = InstanceParams(size)
    dim = params.get_record_dim()
    n_records = params.get_db_size()

    # Get dataset directory from params
    dataset_dir = params.datadir()

    # Choose random phone number from the predefined numbers
    with open(f"contacts_db_{n_records}.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        contacts = list(reader)
    idx = random.randint(0, n_records - 1)
    print(f"         [harness] Selected phone number for query: {contacts[idx]['phone_number']} ({contacts[idx]['contact_name']})")

    db_file = dataset_dir / "db.bin"
    db = np.fromfile(db_file, dtype=np.float32).reshape(-1, dim)
    qry = db[idx]

    # store the query to file
    query_file = dataset_dir / "query.bin"
    qry.tofile(query_file)


if __name__ == "__main__":
    main()
