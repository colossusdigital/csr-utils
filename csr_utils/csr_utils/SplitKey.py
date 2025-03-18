import argparse
import os
import sys
import logging
import json
from typing import List
from utils.encoding_functions import split_and_encode_string

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def split_string_into_shares(
    path_to_key: str,
    file_name: str,
    num_shares: int,
    num_shares_for_rebuild: int,
) -> List[str]:
    """
    Splits a string into different shares using Shamir's secret sharing algorithm.

    Args:
    path_to_key (str): The path to the folder containing the key file.
    file_name (str): The name of the key file.
    num_shares (int): The number of shares to be created.
    num_shares_for_rebuild (int): The number of shares needed to rebuild the original string.

    Returns:
    List[str]: A list of file paths of the saved key shares.

    Raises:
    Exception: If any error occurs during the splitting process or file writing.
    """
    with open(os.path.join(path_to_key, file_name), "r") as file:
        secret_string = file.read()

    share_chunks = split_and_encode_string(
        secret_string, k=num_shares_for_rebuild, n=num_shares, chunk_size=1024
    )
    share_files = []
    for client_n in range(num_shares):
        client_chunks = [j[client_n] for j in share_chunks]
        share_file_path = os.path.join(
            path_to_key,
            file_name.replace(".key", "") + f"_share_{client_n + 1}.key",
        )
        with open(share_file_path, "w") as key_share_file:
            key_share_file.write(json.dumps(client_chunks))
        share_files.append(share_file_path)

    return share_files


def main() -> None:
    """
    Main function to parse arguments and call the string splitting function.
    """
    parser = argparse.ArgumentParser(
        description="Splits a string in different shares using Shamir's secret sharing algorithm"
    )
    parser.add_argument(
        "--path_to_key",
        type=str,
        help="path to folder with key file. Leave empty if file is in current directory",
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

    path_to_key = args.path_to_key or ""
    if path_to_key and not path_to_key.endswith(os.sep):
        path_to_key += os.sep

    key_files = [
        f
        for f in os.listdir(path_to_key)
        if f.endswith(".key") and "share_" not in f
    ]
    if not key_files:
        logging.error(f'File ".key" not found in {path_to_key}')
        file_name = input("Insert file name:")
    elif len(key_files) == 1:
        file_name = key_files[0]
    else:
        logging.info(f'Found different ".key" files: {key_files}')
        file_name = input("Insert file name:")

    if not os.path.exists(os.path.join(path_to_key, file_name)):
        logging.error("Invalid file name. Aborted process.")
        sys.exit(1)

    try:
        share_files = split_string_into_shares(
            path_to_key, file_name, args.num_shares, args.num_shares_for_rebuild
        )
        logging.info(f'Files saved: {", ".join(share_files)}')
    except Exception as e:
        logging.error(f"Error!! {e}")


if __name__ == "__main__":
    main()
