import argparse
import os
import sys
from encoding_functions import split_and_encode_string

parser = argparse.ArgumentParser(description="Splits a string in different shares using shamir\
                                             secret sharing algorithm")
parser.add_argument("--path_to_key", type=str,  help="path to folder with key file. Leave empty \
                                            if file is in current directory", required=False)
parser.add_argument("--num_shares", type=int,
                    help="number of shares to be created", required=False, default=4)
parser.add_argument("--num_shares_for_rebuild", type=int,
                    help="number of shares needed to rebuild the original \
                    string. must be <= num_shares.", required=False, default=2)
args = parser.parse_args()
names = []
for i in os.listdir(args.path_to_key):
   if '.key' in i:
       names.append(i)
if len(names) == 0:
    print('File ".key" not found.\n', os.listdir(args.path_to_key))
    file_name = input('Insert file name:')
elif len(names) == 1:
    file_name = names[0]
else:
    print('Found different ".key" files.\n', names)
    file_name = input('Insert file name:')

if file_name not in os.listdir(args.path_to_key):
    print('Invalid file name. Aborted process.')
    sys.exit(1)

if len(args.path_to_key) > 0:
    if args.path_to_key[-1] != '/':
        args.path_to_key += '/'

try:
    secret_string = open(args.path_to_key+file_name, "r").read()
    share_chunks = split_and_encode_string(secret_string, k=args.num_shares_for_rebuild,
                                           n=args.num_shares, chunk_size=1024)
    for client_n in range(args.num_shares):
        client_chunks = [j[client_n] for j in share_chunks]
        file_path = args.path_to_key + file_name + '_share_' + str(client_n + 1) + '.key'
        with open(file_path, 'w') as key_share_file:
            key_share_file.write(str(client_chunks))
    res = 'Files saved.'
except Exception as e:
    res = 'Error!!' + str(e)
print(res)
