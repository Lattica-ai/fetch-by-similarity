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

GREEN = '\033[92m'
MAGENTA = '\033[35m'
BOLD = '\033[1m'
RESET = '\033[0m'


def generate_random_query(dim: int) -> np.array:
    print(
        f"         [harness] {BOLD}Simulating {GREEN}UNKNOWN{RESET} {BOLD}caller ID.{RESET}")
    rng = np.random.default_rng()
    qry = rng.standard_normal(dim, dtype=np.float32)
    qry /= np.linalg.norm(qry)  # normalize to unit length
    return qry


def get_query_from_contacts(idx, contacts, dataset_dir, dim) -> np.array:
    print(
        f"         [harness] {BOLD}Selected phone number for query: {MAGENTA}{contacts[idx]['phone_number']} {GREEN}{contacts[idx]['contact_name']}{RESET}")

    db_file = dataset_dir / "db.bin"
    db = np.fromfile(db_file, dtype=np.float32).reshape(-1, dim)
    return db[idx]


def main():
    """
    Generate a random query vector and write to disk
    """
    # Parse arguments using argparse
    parser = argparse.ArgumentParser(description='Generate query for FHE benchmark.')
    parser.add_argument('size', type=int, choices=range(TOY, LARGE+1),
                        help='Dataset size (0-toy/1-small/2-medium/3-large)')
    parser.add_argument('--seed', type=int, help='Random seed for reproducibility')
    parser.add_argument('--phone_number', type=str,
                        help='Phone number to search for')
    
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

    # if a phone number is provided, use it;
    # otherwise, with 50% probability choose a random phone number from the predefined contacts
    if random.randint(0, 1) == 0 or args.phone_number is not None:
        with open(f"contacts_db_{n_records}.csv", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            contacts = list(reader)
        if args.phone_number:
            # Find the index of the contact with the specified phone number
            idx = None
            for i, contact in enumerate(contacts):
                if contact['phone_number'] == args.phone_number:
                    idx = i
                    break
            if idx is None:
                qry = generate_random_query(dim)
            else:
                qry = get_query_from_contacts(idx, contacts, dataset_dir, dim)
        else:
            idx = random.randint(0, n_records - 1)
            qry = get_query_from_contacts(idx, contacts, dataset_dir, dim)
    else:  # With 50% probability, generate a random query vector (unknown caller)
        qry = generate_random_query(dim)

    # store the query to file
    query_file = dataset_dir / "query.bin"
    qry.tofile(query_file)


if __name__ == "__main__":
    main()
