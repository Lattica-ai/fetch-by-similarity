"""
client_encode_encrypt_query.py - Encrypt query for homomorphic computation
"""
import pickle
import sys

import submission_utils

local_file_paths, _ = submission_utils.init(sys.argv)

# Load the query from step 7
query = pickle.load(open(local_file_paths.PROCESSED_QUERY_PATH, "rb"))

# Encrypt the query
with submission_utils.get_lattica_client(local_file_paths) as client:
    key = client.keys.load(local_file_paths.KEY_DIR)
    ct = client.query.encrypt(query, key=key)
local_file_paths.get_ct_upload_path("query").write_bytes(ct)
