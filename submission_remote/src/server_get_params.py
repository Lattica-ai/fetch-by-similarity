import sys
import pickle

import submission_utils
from lattica_query.auth import get_demo_token

local_file_paths, instance_params = submission_utils.init(sys.argv)

if instance_params.size == 0:
    # Get access_token for public model
    access_token = get_demo_token("similarityFetchToy")
    pickle.dump(access_token, open(local_file_paths.PATH_ACCESS_TOKEN, "wb"))
elif instance_params.size == 1:
    # Non-public model, use pre-shared access token. Note that if multiple users run at the same time they may interfere.
    access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlIwRTR5Ujd2RnFNSW9ESTBrdGVlayJ9.eyJ0b2tlbklkIjoiMzVhNzBmM2MtZjg3My00YWI5LWI5N2QtNWI5NGM0MmVjYjgzIiwiaXNzIjoiaHR0cHM6Ly9sYXR0aWNhLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJtUWFORWR6R1pVd1o1TDVRSjlrNTFVOG91TjRHOTJicEBjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly9teWFwaS9hcGkiLCJpYXQiOjE3Nzk3MTY3MTcsImV4cCI6MTc4MjMwODcxNywic2NvcGUiOiJ1c2VyIGRlZmF1bHQiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJhenAiOiJtUWFORWR6R1pVd1o1TDVRSjlrNTFVOG91TjRHOTJicCIsInBlcm1pc3Npb25zIjpbInVzZXIiLCJkZWZhdWx0Il19.my68dMtKMvqVrQ4vjqAZeBnRvc8CaTBYjbiDh7hpYWLKQ4ALnKq83_A7mOE2lHHXJRuQ8mcTQ7VxesWhmdNONrEi947TCtSeHPpqYJWJpg6fFOPtvUnCruJjuCO2lBJX6Wl7KKPgUnQWZauAWPM6GNhORj96ftfO9MJ6VAqTp-KQLa2XeOq3dchButtmAHRiOsUIlHKXZTxRR5IH4ExGDJ6gX2pM-00wQtP1N5EEbEkLmh0vPiOg2SRIdYFizew505aUJNQHp2R8lbq-HDUDw1EHV_HvQHx8HIOJKpb2WkPgveLdG2moYUCjtBq2kSFO5cnuCy-gRcOBmgrDpFz6Og"
    pickle.dump(access_token, open(local_file_paths.PATH_ACCESS_TOKEN, "wb"))
else:
    raise ValueError("Submission is publicly available only for SIZE=0 or SIZE=1, for other sizes please contact hello@lattica.ai.")


# Get encryption params and model metadata from BE
client = submission_utils.get_lattica_client(local_file_paths)
context, hom_seq = client.get_init_data()

# Save data to local file system
pickle.dump(context, open(local_file_paths.PATH_CONTEXT, "wb"))
pickle.dump(hom_seq, open(local_file_paths.PATH_HOM_SEQ, "wb"))
