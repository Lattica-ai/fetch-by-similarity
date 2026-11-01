import base64
import json
import os
import pickle
import secrets
import time
from pathlib import Path

import torch
from lattica_query import QueryClient, QueryToken
from lattica_query.logging import QUERY_THEME
from lattica_query.transport.backend import BackendAPI
from lattica_query.transport.settings import ClientInfo
from harness.params import InstanceParams as HarnessInstanceParams, instance_name, PAYLOAD_DIM, SMALL

# The public model the remote backend runs, for the SMALL instance
MODEL_ID = "similarityFetchSmall"

# Runs reuse one token, so each run replaces its key and db instead of adding new ones.
# A new token is fetched a day before it expires.
TOKEN_PATH = Path(__file__).resolve().parent.parent / ".access_token"
TOKEN_MIN_VALIDITY = 24 * 3600   # seconds

# constants used in pre and post processing
PAYLOAD_PRECISION = 16
PAYLOAD_MAX = 512
INTERNAL_N = 2**15   # slots per ciphertext (N = 2^16)
N_COLS = 1024 


def init(argv, mute_logs=True):
    instance_params = InstanceParams(argv)

    if mute_logs:
        devnull_fd = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull_fd, 1)
        os.dup2(devnull_fd, 2)
        os.close(devnull_fd)

    file_paths = LocalFilePaths(instance_params)
    return file_paths, instance_params

class InstanceParams(HarnessInstanceParams):
    def __init__(self, argv):
        self.size = int(argv[1])
        if self.size != SMALL:
            raise ValueError(f"The remote backend serves only SIZE={SMALL} (small).")
        super().__init__(self.size)
        self.count_only = len(argv) > 2 and argv[2] == "--count_only"
        self.name = instance_name(self.size, self.count_only)
        self.payload_dim = PAYLOAD_DIM

class LocalFilePaths:
    def __init__(self, instance_params):
        DATA_DIR = instance_params.datadir()
        IO_DIR   = instance_params.iodir()

        self.DB_PATH      = DATA_DIR / "db.bin"
        self.PAYLOAD_PATH = DATA_DIR / "payloads.bin"
        self.QUERY_PATH   = DATA_DIR / "query.bin"


        self.PROCESSED_DB_PATH      = IO_DIR / "db.pkl"
        self.PROCESSED_PAYLOAD_PATH = IO_DIR / "payloads.pkl"
        self.PROCESSED_QUERY_PATH   = IO_DIR / "query.pkl"
        self.PATH_INITIALIZATION    = IO_DIR / "initialization.pkl"  # the model's context and client model
        self.PATH_ACCESS_TOKEN      = IO_DIR / "access_token.pkl"
        self.KEY_DIR                = IO_DIR / "keys"   # the key: context, client model, secret and evaluation keys
        self.CT_UPLOAD_DIR          = IO_DIR / "ciphertexts_upload"
        self.CT_DOWNLOAD_DIR        = IO_DIR / "ciphertexts_download"
        self.PATH_RAW_RESULT        = IO_DIR / "raw_result.pkl"
        self.PREDICTIONS_PATH       = IO_DIR / "results.bin"
        self.SERVER_TIMES_PATH      = IO_DIR / "server_reported_steps.json"

        self.CT_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        self.CT_DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    def get_ct_upload_path(self, name):
        return self.CT_UPLOAD_DIR / f"{name}.bin"

    def get_ct_download_path(self, name):
        return self.CT_DOWNLOAD_DIR / f"{name}.bin"


# The layout the model takes its inputs in

def pack_complex(x):
    """Pairs feature j with feature j + D/2 as the real and imaginary parts of one value: [..., D] -> [..., D/2]."""
    half = x.shape[-1] // 2
    return torch.complex(x[..., :half], x[..., half:])

def pad_to_blocks(x):
    """[db_size, d] -> [num_blocks, INTERNAL_N, d], zero-padding the last block."""
    padding = -x.shape[0] % INTERNAL_N
    return torch.nn.functional.pad(x, (0, 0, 0, padding)).view(-1, INTERNAL_N, x.shape[-1])

def db_layout(db):
    """The db [db_size, D]: complex-packed, record i's features rotated by i (out[i, d] = x[i, (i + d) % D/2]),
    padded to blocks of INTERNAL_N records, features first: [num_blocks, D/2, INTERNAL_N]. The backend multiplies
    feature d by the query rotated by d."""
    x = pack_complex(db)
    k = x.shape[-1]
    idx = (torch.arange(x.shape[0]).unsqueeze(1) + torch.arange(k)) % k
    return pad_to_blocks(torch.gather(x, 1, idx)).transpose(1, 2).contiguous()

def query_layout(query):
    """The query [D]: complex-packed, conjugated and halved (the score is z + conj(z) for the inner product z),
    repeated over the INTERNAL_N slots."""
    packed = (pack_complex(query).conj() / 2).resolve_conj()
    return packed.repeat(INTERNAL_N // packed.shape[-1])


# The token and the client

def _token_expiry(token):
    """The token's expiry time (the JWT's exp claim), in seconds since the epoch."""
    payload = token.split(".")[1]
    return json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))["exp"]

def get_demo_token(model_id):
    """A query token for a public model: the one at TOKEN_PATH, unless it expires within TOKEN_MIN_VALIDITY."""
    if TOKEN_PATH.exists():
        token = TOKEN_PATH.read_text()
        if _token_expiry(token) - time.time() > TOKEN_MIN_VALIDITY:
            return token

    with BackendAPI(client_info=ClientInfo.from_package("lattica_query"), theme=QUERY_THEME) as backend:
        response = backend.call("api/token/generate_token_demo", {
            "modelId": model_id,
            "tokenName": f"fetch-by-similarity-{secrets.token_hex(4)}",
        })
    TOKEN_PATH.write_text(response["token"])
    return response["token"]

def get_lattica_client(local_file_paths):
    access_token = pickle.load(open(local_file_paths.PATH_ACCESS_TOKEN, "rb"))
    return QueryClient(QueryToken(access_token))

def server_timing_report(client):
    """The server's timing of the client's last query, in seconds, in the harness's steps."""
    components = client.query.last_server_timing
    report = {
        "Encrypted computation": components.get("worker", 0),
        "Backend overhead": components.get("instance", 0) + components.get("logic", 0),
        "Upload time": components.get("upload", 0),
        "Download time": components.get("download", 0),
    }
    return {k: round(v, 3) for k, v in report.items()}
