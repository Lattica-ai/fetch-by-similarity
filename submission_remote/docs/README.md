# Lattica Fetch-by-Similarity Submission

This document describes Lattica's submission to the Fetch-by-Similarity FHE benchmarking workload.

In this doc we provide a description of the workload structure, cryptographic parameterization, level and scale management, and performance characteristics of the submission. Unless stated otherwise, the data reported here corresponds to an end-to-end execution of the harness.

---

## Database Configuration

* **Mode:** SMALL
* **Database size:** 50,000 records
* **Record dimension:** 128
* **Payload dimension:** 7

The submission evaluates encrypted similarity queries against a fixed encrypted database and returns matching payloads.

---

## Execution environment

**Client**

* A rented machine outside AWS
* Intel Core Ultra 7 270K Plus: 11.5 of its 24 CPU threads, 128GB RAM

**Server**

* AWS EC2 g7e.2xlarge
* NVIDIA GB202 (96 GB)
* 8 vCPUs, 64 GB RAM

The client reaches the server over the public internet, so the communication steps and the end-to-end times below include that network.

---

## Cryptographic parameters and security

The submission uses the following parameters:

* **Ring dimension:** 2**15 = 32768
* **Total modulus size:** ~725 bits (420 compute levels + 305 GHS)
* **Secret key distribution:** sparse ternary, Hamming weight 1024

With this secret key distribution, the ring dimension supports a modulus of up to ~836 bits at the 128-bit security target. The ~725-bit modulus used here is below that bound: its lowest attack estimate is approximately 148 bits.

---

## Pipeline levels breakdown

### 2D moduli chain

We are using a technique that we call a *2D modulus chain*, which allows us to decouple optimizations related to plaintext scaling via mod-switching, and optimizations related to the machine register size.

Each ROW of the our 2D chain is a single int64 number, which is the product of one or more “good” primes. Conceptually, each element in the 2D chain can be consumed as a level (in the context of mod-switching), so the overall number of levels is the sum of number of COLs in each ROW. However, the size and computational overhead grows with the number of ROWS rather than with the number of levels.

### Query rotations in groups
The db holds each record's 64 complex-packed features in 4 groups of 16. The backend takes 16 rotations of the query (the unrotated one included), multiplies each group by them and sums, then rotates the 4 group sums into place. The rotations consume no level.

### Moduli chain structure
```python
full_q_list_precision=(
                    (60, 30),  # inner product, chebyshev threshold
                    (60, 30),  # chebyshev threshold
                    (60, 30),  # chebyshev threshold, running sum
                    (60, 30),  # running_sum * selectors, indicator
                    (60, 30),  # indicator
                    (60, 30),  # indicator, one_hots * payloads
                    (60,),     # payloads * packing mask
                ),
query_baby_steps        = 16               # query rotations per db group
stage_sizes_running_sum = [4, 4]           # prod should be 16
ghs_keyswtich_scale     = 5*(61,)          # scale-up by additional 305 bits

input_pt_scale    = 2**30
```

### Scale management and level consumption
The pipeline carefully controls scale growth and modulus switching to maintain precision throughout the computation. Key properties include:

* The running sum's two stages share one 30-bit prime, with their masks encoded at a scale of 2**15.
* The last multiplication, payloads by the packing mask, is not followed by a modulus switch: the two scales share the last prime.


## Performance characteristics

* Evaluation key: 156 MB
* Encrypted database: 473 MB
* Encrypted query: 1.8 MB
* Encrypted result: 1.0 MB
* Total inference time: 1.8 - 1.9 s (**includes network time**, of which 0.4 s on the backend)
* Compute inference time: 7.4 ms (**compute time only**)


### Homomorphic computation time breakdown

* Query rotations: 0.7 ms
* Inner product: 1.7 ms
* Cheb threshold: 1.8 ms
* Running_sum: 0.7 ms
* Mul selectors X running_sum: 0.2 ms
* Indicator masks: 1.3 ms
* Extract and pack payloads: 1.0 ms

## Comparative reference

Relative to the reference OpenFHE implementation provided with the benchmark suite, as measured in the suite's repository (`measurements/small`):

| **Stage** | **Lattica**                    | **OpenFHE** |
| --- |--------------------------------|-------------|
| **Key Generation** | 1.6 s                          | 3.9 s       |
| **DB encryption** | 4.0 s                          | 32.8 s      |
| **Encrypted computation** | 0.0074 s (1.8 - 1.9 s end-to-end) | 76.2 s      |
| **Public & evaluation keys** | 0.16 G                         | 2.4 G       |
| **Encrypted database** | 0.47 G                         | 5.6G        |
| **Encrypted query** | 1.8 M                          | 24M         |


* Encrypted computation is approximately **10,000x faster**.
* Ciphertext sizes (query, keys, database) are **13x, 15x, 12x smaller**, respectively.

All comparisons are performed at comparable security levels.

