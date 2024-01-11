import argparse
from encoding_functions import split_and_encode_string
import json
import os
import sys

parser = argparse.ArgumentParser(description="splits a string in different shares using shamir\
                                             secret sharing scheme")
parser.add_argument("--secret_string", type=str,  help="string to split",
                    required=True)
parser.add_argument("--num_shares", type=int,
                    help="number of shares to be created", required=True)
parser.add_argument("--num_shares_for_rebuild", type=int,
                    help="number of shares needed to rebuild the original \
                    string. (must be < num_shares)", required=True)
args = parser.parse_args()

