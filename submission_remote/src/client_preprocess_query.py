"""
client_preprocess_query.py - Lay out query.bin as the model takes it
"""
import pickle
import sys
import numpy as np
import torch

import submission_utils

local_file_paths, _ = submission_utils.init(sys.argv)

# Read the query vector (float32) and lay it out over the slots
query = torch.from_numpy(np.fromfile(local_file_paths.QUERY_PATH, dtype=np.float32))
query = submission_utils.query_layout(query)

# Save
pickle.dump(query, open(local_file_paths.PROCESSED_QUERY_PATH, "wb"))
