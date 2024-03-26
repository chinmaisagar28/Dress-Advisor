import secrets

# Generate a secure random string of 24 bytes (48 characters when hex-encoded)
secret_key = secrets.token_hex(24)

print(secret_key)
