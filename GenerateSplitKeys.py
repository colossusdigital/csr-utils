import argparse
from encoding_functions import generate_rsa_key_and_public_key, split_and_encode_string
import os
import sys

parser = argparse.ArgumentParser(description="Generates a public key (file_name_public.csr) and a split private\
                    key applying Shamir's sharing algorithm (file_name_private_share_n.key).")
parser.add_argument("--file_name", type=str,  help="name of key files.",
                    required=False)
parser.add_argument("--folder_path", type=str,
                    help="path to folder in which files will be saved", required=False)
parser.add_argument("--num_shares", type=int,
                    help="number of shares to be created", required=False, default=4)
parser.add_argument("--num_shares_for_rebuild", type=int,
                    help="number of shares needed to rebuild the original \
                    string. must be <= num_shares.", required=False, default=2)
args = parser.parse_args()

if not args.file_name:
    args.file_name = input('Insert name for files:')
    if len(args.file_name) == 0:
        print('Invalid file name. Length must be >1.')
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

    share_chunks = split_and_encode_string(private_key, k=args.num_shares_for_rebuild, n=args.num_shares,
                                           chunk_size=1024)
    for client_n in range(args.num_shares):
        client_chunks = [j[client_n] for j in share_chunks]
        file_path = args.folder_path + args.file_name + '_private_share_' + str(client_n + 1) + '.key'
        with open(file_path, 'w') as key_share_file:
            key_share_file.write(str(client_chunks))
    res = 'Files saved.'
except Exception as e:
    res = 'Error!!' + str(e)
print(res)
