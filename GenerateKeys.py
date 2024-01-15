import argparse
from encoding_functions import generate_rsa_key_and_public_key
import os
import sys

parser = argparse.ArgumentParser(description="Generates 2 files containing public and private keys, \
            file_name_public.csr and file_name_private.key")
parser.add_argument("--file_name", type=str,  help="name of key files.",
                    required=False)
parser.add_argument("--folder_path", type=str,
                    help="path to folder in which files will be saved", required=False)
args = parser.parse_args()

if not args.file_name:
    args.file_name = input('Insert name for files:')
    if len(args.file_name) == 0:
        print('Invalid key file name. Length must be >1.')
        sys.exit(1)

if args.file_name+'_public.csr' in os.listdir(args.folder_path):
    resp = input('file_name already exists. Overwrite file? [y/n]')
    if resp != 'y':
        print('Aborted process.')
        sys.exit(1)

if not args.folder_path:
    args.folder_path = ''
else:
    if args.folder_path[-1] != '/':
        args.folder_path += '/'

try:
    private_key, public_key = generate_rsa_key_and_public_key()
    with open(args.folder_path + args.file_name + '_public.csr', 'w') as f:
        f.write(public_key)
    with open(args.folder_path + args.file_name + '_private.key', 'w') as f:
        f.write(private_key)
    res = 'Files saved.'
except Exception as e:
    res = 'Error!!' + str(e)
print(res)