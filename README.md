# CSR-Utils

This repository contains a set of scripts to create and manage key pairs (public and private key).  
The created keys can be split in N shares using Shamir's Secret Sharing Scheme.

## Overview

The repository contains the following scripts:  
    - GenerateKeys.py: generates a private and public key pair  
    - GenerateSplitKeys.py: generates a private and public key pair and splits the private key in N shares  
    - SplitKey.py: splits a private key in N shares using Shamir's Secret Sharing Scheme  
    - CombineKey.py: combines shares of a private key returning the original private key  

## Installation

To install the required libraries, run the following command:  
    - pip install -r requirements.txt

## Scripts

### GenerateKeys.py

This script generates a private and a public key. The keys are stored in 2 separate files:  
    - file_name_private.key  
    - file_name_public.csr  
Inputs:  
    file_name: name of the files where the keys will be stored  
    folder_path: path to folder in which files will be saved. Leave empty to use current directory

### GenerateSplitKeys.py

This script generates a private and a public key and splits the private key in N shares. 
The public key is stored in a file named file_name_public.csr.  
The shares of the private key are stored in N files named file_name_private_share_1.key, ..., file_name_private_share_N.key.  
Inputs:  
    - file_name: name of the files where the keys will be stored  
    - folder_path: path to folder in which files will be saved. Leave empty to use current directory  
    - num_shares: number of shares in which the private key will be split  
    - num_shares_for_rebuild: number of shares needed to rebuild the original string. must be <= num_shares.

### SplitKey.py

This script splits a private key in N shares using Shamir's Secret Sharing Scheme. 
The created shares are stored in N files named file_name_private_share_1.key, ..., file_name_private_share_N.key.  
Inputs:  
    - path_to_key: path to folder with key file. Leave empty if file is in current directory  
    - num_shares: number of shares in which the private key will be split  
    - num_shares_for_rebuild: number of shares needed to rebuild the original string. must be <= num_shares.  

### CombineShares.py

This script combines shares of a private key returning the original private key. 
The share files must have name in format: file_name_private_share_n.key  
Inputs:  
    - file_name: name of share files (only the prefix without "_private_share_n.key")  
    - folder_path: path to folder with shares files. Leave empty if files are in current directory

## Examples

python GenerateKeys.py --file_name="my_key"  
python GenerateKeys.py --file_name="my_key" --folder_path="PATH_TO_FOLDER"  
python GenerateSplitKeys.py --file_name="my_key" --num_shares=3 --num_shares_for_rebuild=2  
python SplitKey.py --path_to_key="PATH_TO_KEY_FILE" --num_shares=4 --num_shares_for_rebuild=4  
python CombineShares.py --file_name="my_key" --folder_path="PATH_TO_FOLDER"

```