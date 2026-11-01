"""
client_encode_encrypt_db.py - Encrypt the database
"""
import pickle
import sys

import submission_utils

local_file_paths, _ = submission_utils.init(sys.argv)

# Load the db and payloads from step 2
db =      pickle.load(open(local_file_paths.PROCESSED_DB_PATH,      "rb"))
payload = pickle.load(open(local_file_paths.PROCESSED_PAYLOAD_PATH, "rb"))

# Encrypt the db and the payloads, the model's custom inputs, into one archive
with submission_utils.get_lattica_client(local_file_paths) as client:
    key = client.keys.load(local_file_paths.KEY_DIR)
    client.encrypted_data.encrypt(
        {"db": db, "payloads": payload},
        local_file_paths.get_ct_upload_path("db_and_payloads_zip"),
        key=key,
    )
