import os

secret_key = os.urandom(24)

secret_key = secret_key.hex()
print(secret_key)