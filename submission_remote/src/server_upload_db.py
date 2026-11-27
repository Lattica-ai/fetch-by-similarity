"""
server_upload_db.py - Upload database to server
"""
import sys
import submission_utils

local_file_paths, _ = submission_utils.init(sys.argv)
archive_path = local_file_paths.get_ct_upload_path("db_and_payloads_zip")
with submission_utils.get_lattica_client(local_file_paths) as client:
    client.encrypted_data.upload(archive_path)
