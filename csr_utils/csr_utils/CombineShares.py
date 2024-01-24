import argparse
import os
import ast
import logging
from typing import Optional
from utils.encoding_functions import combine_secret_shares

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def combine_shares(file_name: str, folder_path: Optional[str] = None) -> None:
    """
    Combines Shamir's shares to regenerate the private key.

    Args:
    file_name (str): The prefix of the share files.
    folder_path (Optional[str]): The directory containing the share files.
                                 Defaults to the current directory if None.

    Raises:
    Exception: If any error occurs during file reading or writing.
    """
    path = folder_path if folder_path else ""
    if folder_path and not folder_path.endswith("/"):
        path += "/"

    shares = []
    for name in os.listdir(path):
        if file_name + "_private_share" in name:
            with open(os.path.join(path, name), "r") as file:
                share_content = ast.literal_eval(file.read())
                shares.append(share_content)

    combined_key = combine_secret_shares(shares)

    with open(os.path.join(path, file_name + "_combined_private.key"), "w") as file:
        file.write(combined_key)

    logging.info(f"Files saved: {file_name}_combined_private.key")


def main() -> None:
    """
    Main function to parse arguments and call the combine shares function.
    """
    parser = argparse.ArgumentParser(
        description="Recombines Shamir's shares and generates the private key. The"
        " share files must have name in format: file_name_private_share_n.key"
    )

    parser.add_argument(
        "--file_name", type=str, help="name of key files.", required=True
    )

    parser.add_argument(
        "--folder_path",
        type=str,
        help="path to folder with shares files. Leave empty if files are in current directory",
        required=False,
    )

    args = parser.parse_args()

    try:
        combine_shares(args.file_name, args.folder_path)
    except Exception as e:
        logging.error(f"Error!! {e}")


if __name__ == "__main__":
    main()
