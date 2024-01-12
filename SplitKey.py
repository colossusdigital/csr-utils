import argparse
from encoding_functions import split_and_encode_string

parser = argparse.ArgumentParser(description="splits a string in different shares using shamir\
                                             secret sharing algorithm")
parser.add_argument("--path_to_key", type=str,  help="path_to_key_file/file_name.key", required=True)
parser.add_argument("--num_shares", type=int,
                    help="number of shares to be created", required=False, default=4)
parser.add_argument("--num_shares_for_rebuild", type=int,
                    help="number of shares needed to rebuild the original \
                    string. must be <= num_shares.", required=False, default=2)
parser.add_argument("--folder_path", type=str,
                    help="path to folder in which files will be saved", required=False, default='')
args = parser.parse_args()

try:
    secret_string = open(args.path_to_key, "r").read()
    share_chunks = split_and_encode_string(secret_string, k=args.num_shares_for_rebuild,
                                           n=args.num_shares, chunk_size=1024)
    for client_n in range(args.num_shares):
        client_chunks = [j[client_n] for j in share_chunks]
        with open(args.folder_path + 'secret_share_'+str(client_n+1)+'.key', 'w') as key_share_file:
            key_share_file.write(str(client_chunks))
    res = 'Files saved.'
except Exception as e:
    res = 'Error!!' + str(e)
print(res)


