# Remote Submission Example

This directory contains a remote submission example for the benchmarking suite.

As part of the benchmarking process, all remote backends are expected to make their homomorphic encryption parameters explicit and reviewable, since these parameters directly affect security, performance, and comparability across submissions. Ideally, such parameters should be reported automatically by the backend.

This document provides a static description of the homomorphic encryption parameters used by this example backend, along with a minimal execution trace to illustrate end-to-end operation.

Additional details that can be provided include things like workload structure, level consumption, scale management, parameterization at higher security levels and performance characteristics. You can see an example of such details (for the Lattica submission) at [README_Lattica_submission.md](https://github.com/Lattica-ai/fetch-by-similarity/blob/public_submission/submission_remote/docs/README_Lattica_submission.md).

---

## FHE parameters

The example backend runs the SMALL instance (size 1: 50,000 records of dimension 128), with the following homomorphic encryption parameters:

```python
homomorphic_params = {
    "q_bits": 786,        # 481 compute (14 levels in 8 rows of ~60 bits) + 305 GHS (5 special primes of 61 bits)
    "n": 2 ** 16,         # polynomial degree
    "err_std": 3.19,      # standard deviation of the encryption noise
    "sk_hw": 192,         # secret key Hamming weight
}
```

These parameters target at least 128-bit security.



---

## Example execution

The remote backend serves only the small instance:

```
python3 harness/run_submission.py 1 --num_runs 3 --remote
```

The harness gets a token for the public model and its cryptographic context, generates the keys locally and uploads the evaluation key and the encrypted database once. Each query is then encrypted locally, run on the backend and decrypted locally.
