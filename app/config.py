import hvac
import os

VAULT_ADDR = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")
VAULT_TOKEN = os.getenv("VAULT_TOKEN", "myroot")

# Initialize Vault client
client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)

if not client.is_authenticated():
    raise Exception("Vault authentication failed")

# Read secret from Vault
secret_path = "secret/myapp/config"
secret = client.secrets.kv.read_secret_version(path=secret_path)
db_password = secret["data"]["data"]["DB_PASSWORD"]
api_key = secret["data"]["data"]["API_KEY"]
