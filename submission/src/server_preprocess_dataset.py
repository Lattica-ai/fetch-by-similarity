#!/usr/bin/env python3
"""
server_preprocess_dataset.py - Load database to server
"""
from submission.src.lib.constants import TOKEN
from lattica_query.worker_api import LatticaWorkerAPI
from submission.src.lib.server_logger import server_print


def main():
    worker_api = LatticaWorkerAPI(TOKEN)

    server_print("Loading database into worker...")
    worker_api.http_client.send_multipart_request("load_custom_encrypted_data")
    
    server_print("Database loaded into worker successfully!")


if __name__ == "__main__":
    main()
