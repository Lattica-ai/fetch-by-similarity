# Lattica – Fetch-by-Similarity Phone-Number Demo 

This repository contains Lattica’s implementation of the **fetch-by-similarity** workload, customized to demonstrate **encrypted phone-number search**.

It is based on the original FHE benchmarking harness from [HomomorphicEncryption.org]

## Dependencies

The harness requires python and some corresponding packages specified in `requirements.txt`. 
```console
python3 -m venv virtualenv
source ./virtualenv/bin/activate
pip3 install -r requirements.txt
```

## Running the fetch-by-similarity workload

Configure your Lattica access token `TOKEN` in the file `submission/src/lib/constants.py`.

An example run is provided below.

```console
$ python3 harness/run_submission.py -h
usage: ./run_pip [-h] [--phone_number] [--num_runs NUM_RUNS] [--seed SEED]

Run the fetch-by-similarity FHE benchmark.

options:
  -h, --help           show this help message and exit
  --phone_number       Phone number to search for from contacts_db_1000.csv
  --num_runs NUM_RUNS  Number of times to run steps 4-9 (default: 1)
  --seed SEED          Random seed for dataset and query generation

$ ./run_pip --seed 12345 --num_runs 1 --phone_number 058-5827732
[harness] Running submission for toy dataset
          returning matching payloads
11:38:08 [harness] 1: Dataset generation completed (elapsed: 0.1036s)
11:38:08 [server] Database shape: (1000, 128) (128 vector dims
11:38:08 [server] Extended payloads shape: (1000, 8) (8 payload values per record)
11:38:08 [harness] 2: Dataset preprocessing completed (elapsed: 0.0815s)
Retrieving user init data from worker...
get_user_init_data timing: network;dur=1987, logic;dur=247, instance;dur=208, worker;dur=0
Creating client FHE keys...
AbstractEncryptionScheme::_sample_randomness
AbstractEncryptionScheme::_sample_randomness
Registering FHE evaluation key...
Uploading evaluation key file 'io/toy/keys/evk.lpk' (15.9 MB) to server...
Uploading file (15.9 MB)...
pk io/toy/keys/evk.lpk uploaded status is Success.
Calling to preprocess io/toy/keys/evk.lpk
preprocess_pk: COMPLETED
preprocess_pk timing: network;dur=760, logic;dur=415, instance;dur=406, worker;dur=286
Evaluation key preprocessing on worker is complete.
11:38:15 [server] Keys generated and saved to io/toy/keys/
11:38:16 [harness] 3: Key Generation completed (elapsed: 8.0746s)
11:38:17 [server] Loaded database with shape: torch.Size([1000, 128])
11:38:17 [server] Loaded payloads with shape: torch.Size([1000, 8])
Encrypting using custom state: db
AbstractEncryptionScheme::_sample_randomness
11:38:18 [server] Encrypted db size: 58958512 bytes
11:38:18 [server] 4.11: Database encryption completed (elapsed 0.628s)
Encrypting using custom state: payloads
AbstractEncryptionScheme::_sample_randomness
11:38:18 [server] Encrypted payloads size: 837204 bytes
11:38:18 [server] 4.12: Payloads encryption completed (elapsed 0.043s)
11:38:18 [server] db.bin & payloads.bin archive created successfully.
11:38:18 [server] Uploading encrypted database & payloads from io/toy/encrypted/encrypted_data.zip...
11:38:24 [server] 4.2: Database & payloads upload completed (elapsed 6.466s)
11:38:24 [harness] 4: Dataset encoding and encryption completed (elapsed: 8.4208s)
         [harness] Public and evaluation keys size: 17.0M
         [harness] Encrypted database size: 57.0M
11:38:25 [server] Loading database into worker...
load_custom_encrypted_data: COMPLETED
load_custom_encrypted_data timing: network;dur=1427, logic;dur=1017, instance;dur=1006, worker;dur=822
11:38:27 [server] Database loaded into worker successfully!
11:38:27 [harness] 5: Encrypted dataset preprocessing completed (elapsed: 2.5964s)
         [harness] Selected phone number for query: 058-5827732 Jody D
11:38:27 [harness] 6: Query generation completed (elapsed: 0.1432s)
11:38:27 [harness] 7: Query preprocessing completed (elapsed: 0.0498s)
11:38:28 [server] Loaded query with shape: torch.Size([128])
11:38:28 [server] 8.1: Expand and reshape completed (elapsed 0.000s)
11:38:28 [server] Encrypting query...
AbstractEncryptionScheme::_sample_randomness
11:38:28 [server] 8.2: Encrypt query completed (elapsed 0.030s)
11:38:28 [server] Encrypted query saved to io/toy/encrypted/query.bin
11:38:28 [harness] 8: Query encryption completed (elapsed: 1.1501s)
         [harness] Encrypted query size: 256.1K
11:38:29 [server] Loading encrypted query from io/toy/encrypted/query.bin
11:38:29 [server] Initializing LatticaWorkerAPI...
11:38:29 [server] Running homomorphic computation on Lattica server...
ct size: 0.3MB
apply_hom_pipeline timing: network;dur=1258, logic;dur=429, instance;dur=406, worker;dur=324
11:38:30 [server] 9.1: Homomorphic computation completed (elapsed 1.260s)
11:38:30 [server] Encrypted results saved to io/toy/encrypted/results.bin
11:38:31 [harness] 9: Encrypted computation completed (elapsed: 2.3588s)
11:38:32 [server] Loading encrypted results from io/toy/encrypted/results.bin
11:38:32 [server] Decrypting results...
11:38:32 [server] 10.1: Decrypt results completed (elapsed 0.057s)
11:38:32 [server] Converting decrypted result to tensor...
11:38:32 [server] Result shape: torch.Size([512]) and dtype: torch.float64
11:38:32 [server] Final result array shape: (512,) and dtype: float64
11:38:32 [server] Raw results saved to io/toy/raw-result.bin
11:38:33 [server] Loaded raw_results: shape: torch.Size([512]), dtype: torch.float64
11:38:33 [server] results shape: torch.Size([1, 8])
11:38:33 [server] 10.2: Postprocessing completed (elapsed 0.001s)
11:38:33 [harness] 10: Result decryption and postprocessing completed (elapsed: 2.5542s)
         [harness] Retrieved caller ID: Jody D
[total latency] 25.5329s

All steps completed for the toy dataset!
```

After finishing the run, deactivate the virtual environment.
```console
deactivate
```

## Directory structure

```bash
[root] /
├─ README.md          # This file
├─ LICENSE.md         # Software license (Apache v2)
├─ pyproject.toml     # Python project configuration
├─ requirements.txt   # Python dependencies for the harness + query client
├─ run_pip, run_uv    # Helper scripts for Python environment setup (optional)
├─ harness/           # Python scripts to drive the workload
│   ├─ run_submission.py   # Main entry point
│   ├─ cleartext_impl.py   # Cleartext reference implementation
│   ├─ verify_result.py    # Result checking utilities
│   └─ [...]
├─ datasets/          # Created/populated by the harness (plaintext/encrypted datasets)
├─ io/                # Used for client ↔ server intermediate files (if any)
├─ measurements/      # Logs with timing / performance numbers
├─ scripts/           # Helper scripts for build and setup
└─ submission/        # Lattica’s workload implementation
    ├─ src/           # Client/server code, including synthetic dataset for demo logic
    ├─ README.md      # Implementation-level documentation
    └─ [...]
```

## Description of stages

This harness is configured as a **single end-to-end demo**, not as a set of independent stages to run separately.  
The typical usage flow is:

`clone → configure license/token → install requirements → run_submission.py`


The workflow executes the complete encrypted search pipeline:

1. Build and setup
Performed automatically on the first run (compilation, internal initialization, etc.).

2. Create a set of private and evaluation keys

3. Create a vectorized database
The demo uses a synthetic dataset of 1,000 (phone, name) pairs defined in `contacts_db_1000.csv`.
Each entry is converted into an embedding vector of features suitable for similarity search.

4. Encrypt the vectorized DB and upload it
The client side encrypts the vectorized database and uploads the ciphertexts, together with evaluation keys, to Lattica’s server.

5. Select a phone number to search for:
If `--phone_number` is provided, that number is used; otherwise, a random number from the dataset is chosen with probability 50%, or a random non-existing number with probability 50%.

6. Create and encrypt the query embedding
A query embedding is built for the chosen number and encrypted locally.

7. Run similarity search fully on ciphertexts
The encrypted query is sent to the FHE engine, which runs the entire similarity search in the encrypted domain.

8. Receive and decrypt the result
The server returns only encrypted results. The client decrypts the response and decodes the match.

9. Print match and timing
The harness prints the matched phone number and owner name, along with timing and measurement information for the main stages.

> **Note:** Because each stage depends on files, keys, and IDs produced in earlier steps of the same run, running only parts of the flow is **not supported** without modifying the code. This keeps the demo simple to operate (one command runs everything) while still representative of a real FHE pipeline.


