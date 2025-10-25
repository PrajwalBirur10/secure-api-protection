import hvac
import os

client = hvac.Client(url=os.environ['VAULT_ADDR'], token=os.environ['VAULT_TOKEN'])
read_response = client.secrets.kv.v2.read_secret_version(path='api')
api_key = read_response['data']['data']['KEY']

print("API Key from Vault:", api_key)
