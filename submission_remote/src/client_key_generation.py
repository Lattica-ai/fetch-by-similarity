"""
client_key_generation.py - Generate and save FHE keys
"""
import pickle
import shutil
import sys

import submission_utils

local_file_paths, _ = submission_utils.init(sys.argv)

# Load the model's context and client model from step 1
init_data = pickle.load(open(local_file_paths.PATH_INITIALIZATION, "rb"))

# Generate the keys locally, in the client's key folder; server_upload_ek uploads the evaluation key
with submission_utils.get_lattica_client(local_file_paths) as client:
    client.keys.generate(initialization=init_data, register=False)
    shutil.copy(client.keys.evaluation_key_path(), local_file_paths.KEY_DIR)
