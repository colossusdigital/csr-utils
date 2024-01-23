# CSR-Utils

This repository contains a set of scripts to create and manage key pairs (public and private key).  
The created keys can be split into N shares using Shamir's Secret Sharing Scheme.

## Overview

The repository contains the following scripts:  
- `GenerateKeys.py`: generates a private and public key pair  
- `GenerateSplitKeys.py`: generates a private and public key pair and splits the private key into N shares  
- `SplitKey.py`: splits a private key into N shares using Shamir's Secret Sharing Scheme  
- `CombineShares.py`: combines shares of a private key returning the original private key  

### Prerequisites for csr-utils

- **Python**: Version 3.8
- **Poetry**: Dependency management tool for [Python](https://python-poetry.org/docs/).

### Installing `csr_utils`

Before building the program, ensure you have the following prerequisites:

1. Navigate to the project directory:
   ```bash
   cd csr-utils
   ```

2. **Setup Environment**:

   Create a virtual environment and activate it:
   ```bash
   python3.8 -m venv venv
   source venv/bin/activate
   ```

3. Install the necessary dependencies using Poetry:
   ```bash
   poetry install
   ```

## Scripts

### GenerateKeys.py

This script generates a private and a public key. The keys are stored in two separate files:  
1. `file_name_private.key`  
2. `file_name_public.csr`  

Inputs:  
- `file_name`: name of the files where the keys will be stored  
- `folder_path`: path to folder in which files will be saved. Leave empty to use the current directory

### GenerateSplitKeys.py

This script generates a private and a public key and splits the private key into N shares. 
The public key is stored in a file named `file_name_public.csr`. 
The shares of the private key are stored in N files named `file_name_private_share_1.key`, ..., `file_name_private_share_N.key`.  

Inputs:  
- `file_name`: name of the files where the keys will be stored  
- `folder_path`: path to folder in which files will be saved. Leave empty to use the current directory  
- `num_shares`: number of shares into which the private key will be split  
- `num_shares_for_rebuild`: number of shares needed to rebuild the original string. Must be ≤ `num_shares`.

### SplitKey.py

This script splits a private key into N shares using Shamir's Secret Sharing Scheme. 
The created shares are stored in N files named `file_name_private_share_1.key`, ..., `file_name_private_share_N.key`.  

Inputs:  
- `path_to_key`: path to folder with key file. Leave empty if file is in the current directory  
- `num_shares`: number of shares into which the private key will be split  
- `num_shares_for_rebuild`: number of shares needed to rebuild the original string. Must be ≤ `num_shares`.  

### CombineShares.py

This script combines shares of a private key returning the original private key. 
The share files must have names in the format: `file_name_private_share_n.key`  

Inputs:  
- `file_name`: name of share files (only the prefix without "_private_share_n.key")  
- `folder_path`: path to folder with share files. Leave empty if files are in the current directory

## Examples

```bash
poetry run python csr-utils/GenerateKeys.py --file_name="my_key"
poetry run python csr-utils/GenerateKeys.py --file_name="my_key" --folder_path="PATH_TO_FOLDER"
poetry run python csr-utils/GenerateSplitKeys.py --file_name="my_key" --num_shares=3 --num_shares_for_rebuild=2
poetry run python csr-utils/SplitKey.py --path_to_key="PATH_TO_KEY_FILE" --num_shares=4 --num_shares_for_rebuild=4
poetry run python csr-utils/CombineShares.py --file_name="my_key" --folder_path="PATH_TO_FOLDER"
```
