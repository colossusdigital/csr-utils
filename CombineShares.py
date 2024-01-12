import argparse
from encoding_functions import combine_secret_shares
import os
import ast

parser = argparse.ArgumentParser(description="Recombines Shamir's shares and generates the private key. The \
                                    share files must have name in format: file_name_private_share_1.key")
parser.add_argument("--folder_path", type=str,
                    help="path to folder with shares files", required=False)
parser.add_argument("--file_name", type=str, help=" name of key files.", required=True)
args = parser.parse_args()

try:
    if not args.folder_path:
        path = ''
    else:
        if args.folder_path[-1] != '/':
            args.folder_path = args.folder_path + '/'
        path = args.folder_path

    shares = []
    for name in os.listdir(args.folder_path):
        print(name)
        if args.file_name + '_private_share' in name:
            share_n = name.split('_')[-1].split('.')[0]
            with open(path + name, 'r') as f:
                my_list = ast.literal_eval(f.read())
                shares.append(my_list)
    res = combine_secret_shares(shares)
except Exception as e:
    res = 'Error!!' + str(e)
print(res)




'''
if len(shares) < 2:
    res = {"status": "False",
           "message": "Not enough shares."}
else:
    try:
        original_string = combine_secret_shares(shares)
        res = {"status": "True", "result": original_string}
    except Exception as e:
        res = {"status": "False",
               "message": str(e)}
print(json.dumps(res))
'''