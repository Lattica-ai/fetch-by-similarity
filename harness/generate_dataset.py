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
from params import InstanceParams, TOY, LARGE, PAYLOAD_DIM, instance_name
import string
import json

def generate_random_phones(n):
    chars = string.digits
    results = []
    for _ in range(n):
        rnd_digits = random.choices(chars, k=8)
        phone = '05' + rnd_digits[0] + '-' + ''.join(rnd_digits[1:])
        results.append(phone)
    return results

def generate_db_points(n_records: int, n_centers: int, dim: int) -> tuple:
    """
    Generate database points, half as random points and the other half by
    selecting random centers and adding noise.
    
    Args:
        n_records: Number of database records to generate
        n_centers: Number of centers to use
        dim: Dimension of the space
        
    Returns:
        Tuple containing:
        - Array of shape (n_records, dim) containing the database points
        - Array of shape (n_centers, dim) containing the centers
    """
    assert n_records >= n_centers, "Number of records must be at least number of centers"
    rng = np.random.default_rng()

    # Generate centers on the unit sphere
    centers = rng.standard_normal(size=(n_centers, dim), dtype=np.float32)
    centers /= np.linalg.norm(centers, axis=1, keepdims=True)  # normalize to unit length

    # Database points are same as center and padded to some constant vector
    db = np.ones((n_records, dim), dtype=np.float32)
    db /= np.linalg.norm(db, axis=1, keepdims=True)  # normalize to unit length
    db[:n_centers] = centers  # ensure all centers are included

    return db, centers

def generate_payloads(n_records: int, n_centers: int) -> np.ndarray:
    """
    Returns:
        Array of shape (n_records, PAYLOAD_DIM=7) with the payload vectors
    """
    ascii_names = [
 [70, 101, 108, 105, 120, 0, 0],  # Felix
 [65,110,110,97,0,0,0],      # Anna
 [76,105,97,109,0,0,0],      # Liam
 [78,111,97,104,0,0,0],      # Noah
 [69,109,109,97,0,0,0],      # Emma
 [90,111,101,0,0,0,0],       # Zoe
 [77,105,97,0,0,0,0],        # Mia
 [69,108,108,97,0,0,0],      # Ella
 [82,121,97,110,0,0,0],      # Ryan
 [73,118,97,110,0,0,0],      # Ivan
 [65,108,101,120,0,0,0],     # Alex
 [77,97,121,97,0,0,0],       # Maya
 [83,97,114,97,0,0,0],       # Sara
 [76,105,108,121,0,0,0],     # Lily
 [77,97,114,107,0,0,0],      # Mark
 [74,111,104,110,0,0,0],     # John
 [80,97,117,108,0,0,0],      # Paul
 [69,114,105,99,0,0,0],      # Eric
 [65,100,97,109,0,0,0],      # Adam
 [76,101,111,110,0,0,0],     # Leon
 [69,100,101,110,0,0,0],     # Eden
 [68,97,110,97,0,0,0],       # Dana
 [84,97,108,105,0,0,0],      # Tali
 [65,109,105,114,0,0,0],     # Amir
 [78,105,110,97,0,0,0],      # Nina
 [69,108,115,97,0,0,0],      # Elsa
 [65,108,109,97,0,0,0],      # Alma
 [79,109,101,114,0,0,0],     # Omer
 [89,97,114,97,0,0,0],       # Yara
 [73,114,105,115,0,0,0],     # Iris
 [76,117,99,97,0,0,0],       # Luca
 [68,97,118,105,100,0,0],    # David
 [74,111,110,97,104,0,0],    # Jonah
 [79,115,99,97,114,0,0],     # Oscar
 [83,105,109,111,110,0,0],   # Simon
 [68,97,110,105,101,108,0],  # Daniel
 [82,117,98,101,110,0,0],    # Ruben
 [65,97,114,111,110,0,0],    # Aaron
 [69,116,104,97,110,0,0],    # Ethan
 [67,104,108,111,101,0,0],   # Chloe
 [68,97,112,104,110,101,0],  # Daphne
 [78,97,111,109,105,0,0],    # Naomi
 [72,101,108,101,110,0,0],   # Helen
 [74,97,109,105,101,0,0],    # Jamie
 [75,97,114,101,110,0,0],    # Karen
 [65,108,105,99,101,0,0],    # Alice
 [66,114,117,99,101,0,0],    # Bruce
 [83,116,101,118,101,0,0],   # Steve
 [75,101,118,105,110,0,0],   # Kevin
 [74,97,115,111,110,0,0]     # Jason
]
    assert n_centers <= len(ascii_names), "Not enough predefined names for the centers"

    payloads = np.zeros((n_records, PAYLOAD_DIM), dtype=np.int16)

    names_array = np.array(ascii_names[:n_centers], dtype=np.int16)

    payloads[:n_centers, :] = names_array

    return payloads

def paylaod_to_name(payload: list[int]) -> str:
    return ''.join(chr(x) for x in payload if x != 0)


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

    n_centers = 20

    # Get dataset directory from params and ensure it exists
    dataset_dir = params.datadir()
    dataset_dir.mkdir(parents=True, exist_ok=True)

    # Generate database points and centers, and then payloads
    db, centers = generate_db_points(
        n_records, n_centers, params.get_record_dim())
    payloads = generate_payloads(n_records, n_centers)

    phones = generate_random_phones(n_centers)
    names = [paylaod_to_name(payloads[i].tolist()) for i in range(n_centers)]
    contacts = list(zip(phones, names))

    # Write data to files
    with open(dataset_dir / "contacts.json", "w") as f:
        json.dump(contacts, f, indent=4)  # indent for readability
    db.tofile(dataset_dir / "db.bin")
    centers.tofile(dataset_dir / "centers.bin")
    payloads.tofile(dataset_dir / "payloads.bin")


if __name__ == "__main__":
    main()
