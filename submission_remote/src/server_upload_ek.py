import sys
import submission_utils

local_file_paths, _ = submission_utils.init(sys.argv)

# Upload the evaluation key generated in client_key_generation and have the worker preprocess it
with submission_utils.get_lattica_client(local_file_paths) as client:
    client.keys.ensure(local_file_paths.KEY_DIR)
