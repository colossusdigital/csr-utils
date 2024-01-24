import argparse
import os
import sys
import logging
from typing import List
from utils.encoding_functions import (
    generate_rsa_key_and_public_key,
    split_and_encode_string,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def generate_and_split_keys(
    file_name: str,
    folder_path: str,
    num_shares: int,
    num_shares_for_rebuild: int,
) -> List[str]:
    """
    Generates RSA public key and splits the private key into shares using Shamir's sharing algorithm.

    Args:
    file_name (str): The base name for the key files.
    folder_path (str): The directory where the key files will be saved.
    num_shares (int): The number of shares to be created.
    num_shares_for_rebuild (int): The number of shares needed to rebuild the original string.

    Returns:
    List[str]: A list of file paths of the saved key shares.

    Raises:
    Exception: If any error occurs during key generation or file writing.
    """
    private_key, public_key = generate_rsa_key_and_public_key()
    public_key_path = os.path.join(folder_path, f"{file_name}_public.csr")
    with open(public_key_path, "w") as f:
        f.write(public_key)

    share_chunks = split_and_encode_string(
        private_key, k=num_shares_for_rebuild, n=num_shares, chunk_size=1024
    )
    share_files = []
    for client_n in range(num_shares):
        client_chunks = [j[client_n] for j in share_chunks]
        share_file_path = os.path.join(
            folder_path, f"{file_name}_private_share_{client_n + 1}.key"
        )
        with open(share_file_path, "w") as key_share_file:
            key_share_file.write(str(client_chunks))
        share_files.append(share_file_path)

    return share_files


def main() -> None:
    """
    Main function to parse arguments and call the key generation and splitting function.
    """
    parser = argparse.ArgumentParser(
        description="Generates a public key (file_name_public.csr) and a split private key applying Shamir's \
        sharing algorithm (file_name_private_share_n.key)."
    )
    parser.add_argument(
        "--file_name", type=str, help="name of key files.", required=False, default="my_key"
    )
    parser.add_argument(
        "--folder_path",
        type=str,
        help="path to folder in which files will be saved. Leave empty to use current directory",
        required=False,
    )
    parser.add_argument(
        "--num_shares",
        type=int,
        help="number of shares to be created",
        required=False,
        default=4,
    )
    parser.add_argument(
        "--num_shares_for_rebuild",
        type=int,
        help="number of shares needed to rebuild the original string. Must be <= num_shares.",
        required=False,
        default=2,
    )
    args = parser.parse_args()

    if not args.file_name:
        logging.error("Invalid file name. Length must be > 0.")
        sys.exit(1)

    folder_path = args.folder_path or ""
    if folder_path and not folder_path.endswith("/"):
        folder_path += "/"

    if os.path.exists(os.path.join(folder_path, args.file_name + "_public.csr")):
        resp = input("file_name already exists. Overwrite file? [y/n]")
        if resp.lower() != "y":
            logging.info("Aborted process.")
            sys.exit(1)

    try:
        share_files = generate_and_split_keys(
            args.file_name, folder_path, args.num_shares, args.num_shares_for_rebuild
        )
        logging.info(f'Files saved: {", ".join(share_files)}')
    except Exception as e:
        logging.error(f"Error!! {e}")


if __name__ == "__main__":
    main()
