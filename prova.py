import argparse

def generate_documentation(parser):
    doc = parser.description + "\n\n"
    for action in parser._actions:
        option_string = ', '.join(action.option_strings)
        help_string = action.help
        doc += f"{option_string}\n\t{help_string}\n\n"
    return doc

parser = argparse.ArgumentParser(description="Generates a public key (file_name_public.csr) and a split private\
                    key applying Shamir's sharing algorithm (file_name_private_share_n.key).")
parser.add_argument("--file_name", type=str,  help="name of key files.",
                    required=False)
parser.add_argument("--folder_path", type=str,
                    help="path to folder in which files will be saved. Leave empty \
                                            to use current directory", required=False)
parser.add_argument("--num_shares", type=int,
                    help="number of shares to be created", required=False, default=4)
parser.add_argument("--num_shares_for_rebuild", type=int,
                    help="number of shares needed to rebuild the original \
                    string. must be <= num_shares.", required=False, default=2)

documentation = generate_documentation(parser)
print(documentation)