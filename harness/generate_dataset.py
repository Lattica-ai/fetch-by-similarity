#!/usr/bin/env python3
"""
generate_dataset.py - Generate random centers, database points, and payloads
for the fetch-by-similarity benchmark.
"""
# Copyright (c) 2025, Amazon Web Services
# All rights reserved.
#
# This software is licensed under the terms of the Apache v2 License.
# See the LICENSE.md file for details.
import random
import argparse
import numpy as np
from params import InstanceParams, TOY, LARGE, PAYLOAD_DIM
import csv


def generate_db_points(n_records: int, dim: int) -> np.array:
    """
    Generate database points, half as random points and the other half by
    selecting random centers and adding noise.
    
    Args:
        n_records: Number of database records to generate
        dim: Dimension of the space
        
    Returns:
        Array of shape (n_records, dim) containing the database points
    """
    rng = np.random.default_rng()

    # Generate centers on the unit sphere
    centers = rng.standard_normal(size=(n_records, dim), dtype=np.float32)
    centers /= np.linalg.norm(centers, axis=1, keepdims=True)  # normalize to unit length

    return centers


def main():
    """
    Generate random centers, database points, and payloads for the fetch-by-similarity benchmark.
    """
    # Parse arguments using argparse
    parser = argparse.ArgumentParser(description='Generate dataset for FHE benchmark.')
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
    n_records = params.get_db_size()

    # Get dataset directory from params and ensure it exists
    dataset_dir = params.datadir()
    dataset_dir.mkdir(parents=True, exist_ok=True)

    # Generate database points and centers, and then payloads
    db = generate_db_points(n_records, params.get_record_dim())

    # read contacts from csv
    with open(f"contacts_db_{n_records}.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        contacts = list(reader)

    payloads = []
    for line in contacts:
        name = line['contact_name']
        # if name shorter than PAYLOAD_DIM, pad with zeros
        if len(name) < PAYLOAD_DIM:
            name = name.ljust(PAYLOAD_DIM, '\0')
        payloads.append([ord(ch) for ch in name])
    payloads = np.array(payloads, dtype=np.int16)

    db.tofile(dataset_dir / "db.bin")
    payloads.tofile(dataset_dir / "payloads.bin")


if __name__ == "__main__":
    main()
