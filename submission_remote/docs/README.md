# Remote Submission Example

This directory contains a remote submission example for the benchmarking suite.

As part of the benchmarking process, all remote backends are expected to make their homomorphic encryption parameters explicit and reviewable, since these parameters directly affect security, performance, and comparability across submissions. Ideally, such parameters should be reported automatically by the backend.

This document provides a static description of the homomorphic encryption parameters used by this example backend, along with a minimal execution trace to illustrate end-to-end operation.

Additional details that can be provided include things like workload structure, level consumption, scale management, parameterization at higher security levels and performance characteristics. You can see an example of such details (for the Lattica submission) at [README_Lattica_submission.md](https://github.com/Lattica-ai/fetch-by-similarity/blob/public_submission/submission_remote/docs/README_Lattica_submission.md).

---

## FHE parameters

The example backend runs in the TOY setting and uses the following homomorphic encryption parameters:

```python
homomorphic_params = {
    "q_bits": 1059,       # 693 compute levels + 366 GHS
    "n": 2 ** 10,         # polynomial degree
    "err_std": 1,         # standard deviation of the encryption noise
    "sk_hw": 0,          # ternary secret key with equal probability of -1, 0, and 1
}
```

These parameters are chosen for simplicity and reproducibility and are not intended to represent a security-hardened or final challenge submission.



---

## Example execution

```
python3 harness/run_submission.py 0 --num_runs 3 --remote

[harness] Running submission for toy dataset
          returning matching payloads
15:08:04 [harness] 1: Dataset generation completed (elapsed: 0.1027s)
15:08:09 [harness] 1.1: Communication: Get cryptographic context completed (elapsed: 4.17s)
15:08:10 [harness] 2: Dataset preprocessing completed (elapsed: 1.1292s)
15:08:11 [harness] 3: Key Generation completed (elapsed: 1.2626s)
         [harness] Public and evaluation keys size: 17.5M
15:08:31 [harness] 3.1: Communication: Upload evaluation key completed (elapsed: 19.5481s)
15:08:32 [harness] 4: Dataset encoding and encryption completed (elapsed: 1.6035s)
         [harness] Encrypted database size: 45.2M
15:08:49 [harness] 4.1: Communication: Upload encrypted database completed (elapsed: 16.7999s)
15:08:49 [harness] 5: Encrypted dataset preprocessing completed (elapsed: 0.0003s)

         [harness] Run 1 of 3
15:08:49 [harness] 6: Query generation completed (elapsed: 0.1393s)
15:08:49 [harness] 7: Query preprocessing completed (elapsed: 0.0002s)
15:08:50 [harness] 8: Query encryption completed (elapsed: 1.1922s)
         [harness] Encrypted query size: 192.1K
15:08:53 [harness] 9: Encrypted computation completed (elapsed: 2.7726s)
15:08:55 [harness] 10: Result decryption and postprocessing completed (elapsed: 2.3468s)
         [harness] PASS (All 0 payload vectors match)
         [submission] Encrypted computation: 0.162s
         [submission] Backend overhead: 0.071s
         [submission] Upload time: 0.289s
         [submission] Download time: 1.072s
[total latency] 51.0673s

         [harness] Run 2 of 3
15:08:56 [harness] 6: Query generation completed (elapsed: 0.2886s)
15:08:56 [harness] 7: Query preprocessing completed (elapsed: 0.0002s)
15:08:57 [harness] 8: Query encryption completed (elapsed: 1.1838s)
         [harness] Encrypted query size: 192.1K
15:09:00 [harness] 9: Encrypted computation completed (elapsed: 3.1522s)
15:09:02 [harness] 10: Result decryption and postprocessing completed (elapsed: 2.3912s)
         [harness] PASS (All 0 payload vectors match)
         [submission] Encrypted computation: 0.159s
         [submission] Backend overhead: 0.073s
         [submission] Upload time: 0.522s
         [submission] Download time: 1.123s
[total latency] 51.6322s

         [harness] Run 3 of 3
15:09:03 [harness] 6: Query generation completed (elapsed: 0.3526s)
15:09:03 [harness] 7: Query preprocessing completed (elapsed: 0.0002s)
15:09:04 [harness] 8: Query encryption completed (elapsed: 1.2347s)
         [harness] Encrypted query size: 192.1K
15:09:07 [harness] 9: Encrypted computation completed (elapsed: 3.2832s)
15:09:10 [harness] 10: Result decryption and postprocessing completed (elapsed: 2.3481s)
         [harness] PASS (All 19 payload vectors match)
         [submission] Encrypted computation: 0.158s
         [submission] Backend overhead: 0.077s
         [submission] Upload time: 0.588s
         [submission] Download time: 1.259s
[total latency] 51.835s

All steps completed for the toy dataset!
```

- Public + evaluation keys size: 17.5 MB
- Encrypted DB size: 45.2 MB
- Encrypted query size: 192 KB
- Total inference time: ~2 s
- Compute inference time: ~160 ms
---
