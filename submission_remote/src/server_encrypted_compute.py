"""
server_encrypted_compute.py - Run homomorphic computation on Lattica server
"""
import json
import sys
import submission_utils

local_file_paths, _ = submission_utils.init(sys.argv)
# Load encrypted query from step 8
ct = local_file_paths.get_ct_upload_path("query").read_bytes()

# Run homomorphic computation
with submission_utils.get_lattica_client(local_file_paths) as client:
    ct_res = client.query.execute(ct)
    server_report_for_harness = submission_utils.server_timing_report(client)

# Save encrypted result
local_file_paths.get_ct_download_path("results").write_bytes(ct_res)

# Save server timing report
with open(local_file_paths.SERVER_TIMES_PATH, "w") as f:
    json.dump(server_report_for_harness, f)
