import hvac
import os

def get_api_key():
    client = hvac.Client(
        url=os.getenv("VAULT_ADDR", "http://127.0.0.1:8200"),
        token=os.getenv("VAULT_TOKEN", "root")
    )
    secret = client.secrets.kv.v2.read_secret_version(path="api")
    return secret["data"]["data"]["KEY"]
