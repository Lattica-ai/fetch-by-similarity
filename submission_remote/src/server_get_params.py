import sys
import pickle

import submission_utils

local_file_paths, _ = submission_utils.init(sys.argv)

# Get access_token for public model
access_token = submission_utils.get_demo_token(submission_utils.MODEL_ID)
pickle.dump(access_token, open(local_file_paths.PATH_ACCESS_TOKEN, "wb"))

# Get the model's cryptographic context and client model from the backend
with submission_utils.get_lattica_client(local_file_paths) as client:
    init_data = client.keys.fetch_initialization()

# Save data to local file system
pickle.dump(init_data, open(local_file_paths.PATH_INITIALIZATION, "wb"))
