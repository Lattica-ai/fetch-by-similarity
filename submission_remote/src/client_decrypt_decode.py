import pickle
import sys

import submission_utils

local_file_paths, _ = submission_utils.init(sys.argv)

ct_res = local_file_paths.get_ct_download_path("results").read_bytes()

with submission_utils.get_lattica_client(local_file_paths) as client:
    key = client.keys.load(local_file_paths.KEY_DIR)
    raw_result = client.query.decrypt(ct_res, key=key)

pickle.dump(raw_result, open(local_file_paths.PATH_RAW_RESULT, "wb"))
