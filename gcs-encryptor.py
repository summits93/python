import subprocess
from google.cloud import storage
import sys

def encrypt_with_pgp(source_file, encrypted_file, recipient_key_path):
    # Use GPG to encrypt the file
    subprocess.run(["gpg", "--encrypt", "--recipient-file", recipient_key_path, "--output", encrypted_file, source_file])

def upload_encrypted_object(bucket_name, source_file, destination_blob_name, recipient_key_path):
    # Encrypt the file using PGP
    encrypted_file = f"{source_file}.gpg"
    encrypt_with_pgp(source_file, encrypted_file, recipient_key_path)

    # Create a Storage client
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.bucket(bucket_name)

    # Create a Blob object
    blob = bucket.blob(destination_blob_name)

    # Upload the encrypted file
    blob.upload_from_filename(encrypted_file)

    print(f"Encrypted file {source_file} uploaded to {bucket_name}/{destination_blob_name}.")

# Example usage
if len(sys.argv) != 5:
    print("Usage: python script.py <bucket_name> <source_file> <destination_blob_name> <recipient_key_path>")
    sys.exit(1)

bucket_name = sys.argv[1]
source_file = sys.argv[2]
destination_blob = sys.argv[3]
recipient_key_path = sys.argv[4]

upload_encrypted_object(bucket_name, source_file, destination_blob, recipient_key_path)