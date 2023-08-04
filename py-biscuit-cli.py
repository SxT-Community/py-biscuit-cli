
import argparse
import sys
import logging
from biscuit_auth import Authorizer, Biscuit, BiscuitBuilder, BlockBuilder, KeyPair, PrivateKey, PublicKey, Rule

logging.basicConfig(level=logging.INFO)

def main():
    # get command line arguments
    args = parse_arguments(sys.argv[1:])
    logging.info(f"Arguments: {args}")
    # Check if use supplied a biscuit private key argument 
    if 'biscuit_private_key' in args and args['biscuit_private_key'] is not None:
        logging.info(f"Biscuit private key provided : {args['biscuit_private_key']}")
    else:
        logging.info("'bpk' argument has not been set so we will generate a keypair for you now")
        new_biscuit_keypair = generate_biscuit_keypair()
    
    if 'datalog_file' in args and args['datalog_file'] is not None:
        logging.info(f"Datalog file provided : {args['datalog_file']}")
        biscuit_payload = load_file_into_string(args['datalog_file'])
    else:
        logging.info("'d' argument has not been set so we will just create a random biscuit")
        biscuit_payload = False
        # new_biscuit_datalog_file = generate_biscuit_datalog_file()
    
    # Check if use supplied a resource id argument
    if 'resource_id' in args and args['resource_id'] is not None:
        logging.info(f"Resource ID provided : {args['resource_id']}")
        resource_id = args['resource_id']
    else:
        logging.info("'resource_id' argument has not been set so we will rely on what is in the datalog file provided!")
        resource_id = False

    generate_biscuit(args['biscuit_private_key'], resource_id, biscuit_payload)

# need to add a check that says if we dont get a resource id or datalog file, we need to prompt user to enter at least one 
def parse_arguments(args):
    # create parser
    parser = argparse.ArgumentParser(description="Space and Time Biscuit Python CLI Help Menu 🚀")

    # add arguments
    parser.add_argument("-bpk", "--biscuit-private-key", help="Private key you want to create your biscuit with", required=False)
    parser.add_argument("-rid", "--resource-id", help="Resource ID you want to assoicate your biscuit with", required=False)
    parser.add_argument("-d", "--datalog-file", help="datalog file to read", required=False)

    # parse arguments
    parsed_args = parser.parse_args(args)

    # return as a dictionary
    return vars(parsed_args)

# need to add parsing checks to ensure sxt:capability is in the datalog file 
def load_file_into_string(filename):
    try:
        with open(filename, 'r') as file:
            data = file.read().lower() # sxt only accepts lowercase biscuits
        return data
    except FileNotFoundError:
        logging.error(f"File {filename} not found.")
        return None
    except Exception as e:
        logging.error(f"An error occurred while reading the file: {str(e)}")
        return None

def generate_biscuit_keypair():
    keypair = KeyPair()
    private_key_str = keypair.private_key.to_hex()
    public_key_str = keypair.public_key.to_hex()
    logging.info(f"Biscuit private Key: {private_key_str}")
    logging.info(f"Biscuit public Key: {public_key_str}")
    return keypair

def generate_biscuit(private_key_str, resource_id, biscuit_payload):

    # for when user supplies a private key string 
    parse_private_key = PrivateKey.from_hex(private_key_str)

    logging.info(f"resource_id: {resource_id}, biscuit_payload: {biscuit_payload}")
    
    if resource_id and biscuit_payload: # if we have a resource Id and datalog file 
        builder = BiscuitBuilder(f"""
            {biscuit_payload}
        """,
        {
            'resource_id': resource_id
        }
        )

    if resource_id and biscuit_payload == False: # if we have a resource Id but no datalog file then create a full access biscuit
   
        builder = BiscuitBuilder(f"""
            sxt:capability("ddl_create", {resource_id});
            sxt:capability("ddl_drop", {resource_id});
            sxt:capability("dml_insert", {resource_id});
            sxt:capability("dml_update", {resource_id});
            sxt:capability("dml_merge", {resource_id});
            sxt:capability("dml_delete", {resource_id});
            sxt:capability("dql_select", {resource_id});
        """,
        {
            'resource_id': resource_id
        }
        )
    
    if not resource_id and biscuit_payload: # if we have a datalog file but no resource Id then create a biscuit with the datalog file only
        builder = BiscuitBuilder(f"""
            {biscuit_payload}
        """, {})


    token = builder.build(parse_private_key)
    token_string = token.to_base64()
    
    # logging.info(f"Biscuit private Key: {private_key_str}")
    # logging.info(f"Biscuit public Key: {public_key_str}")
    # logging.info(f"Resource ID: {resource_id}")    
    logging.info(f"Biscuit: {token_string}")
    
    """
    biscuit = {
        "private_key": private_key_str,
        "public_key": public_key_str,
        "resource_id": resource_id,
        "token": token_string
    }
    return biscuit
    """

if __name__ == "__main__":
    main()
