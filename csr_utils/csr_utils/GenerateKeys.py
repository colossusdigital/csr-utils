import argparse
import os
import sys
import logging
from typing import Tuple
from utils.encoding_functions import generate_rsa_key_and_public_key

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def generate_keys(file_name: str, folder_path: str) -> Tuple[str, str]:
    """
    Generates RSA public and private keys.

    Args:
    file_name (str): The base name for the key files.
    folder_path (str): The directory where the key files will be saved.

    Returns:
    Tuple[str, str]: A tuple containing the private key and public key.

    Raises:
    Exception: If any error occurs during key generation.
    """
    private_key, public_key = generate_rsa_key_and_public_key()
    public_key_path = os.path.join(folder_path, f"{file_name}_public.csr")
    private_key_path = os.path.join(folder_path, f"{file_name}_private.key")

    with open(public_key_path, "w") as f:
        f.write(public_key)
    with open(private_key_path, "w") as f:
        f.write(private_key)

    return private_key_path, public_key_path


def main() -> None:
    """
    Main function to parse arguments and call the key generation function.
    """
    parser = argparse.ArgumentParser(
        description="Generates 2 files containing public and private keys, \
                     file_name_public.csr and file_name_private.key"
    )
    parser.add_argument(
        "--file_name", type=str, help="name of key files.", required=False
    )
    parser.add_argument(
        "--folder_path",
        type=str,
        help="path to folder in which files will be saved. Leave empty to use current directory",
        required=False,
    )
    args = parser.parse_args()

    file_name = args.file_name or input("Insert name for files:").strip()
    if not file_name:
        logging.error("Invalid key file name. Length must be > 0.")
        sys.exit(1)

    folder_path = args.folder_path or ""
    if folder_path and not folder_path.endswith("/"):
        folder_path += "/"

    if os.path.exists(os.path.join(folder_path, file_name + "_public.csr")):
        resp = input("file_name already exists. Overwrite file? [y/n]")
        if resp.lower() != "y":
            logging.info("Aborted process.")
            sys.exit(1)

    try:
        private_key_path, public_key_path = generate_keys(
            file_name, folder_path
        )
        logging.info(f"Files saved: {public_key_path}, {private_key_path}")
    except Exception as e:
        logging.error(f"Error!! {e}")


if __name__ == "__main__":
    main()
