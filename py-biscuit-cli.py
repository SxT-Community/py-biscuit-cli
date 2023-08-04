
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
    
    """
    # Check if use supplied a resource id argument
    if 'rid' in args and args['rid'] is not None:
        logging.info(f"Resource ID provided : {args['rid']}")
    else:
        logging.info("'rid' argument has not been set so we will generate a resource id for you now")
        new_biscuit_resource_id = generate_biscuit_resource_id()
    """

    generate_biscuit(args['biscuit_private_key'], args['resource_id'])

def parse_arguments(args):
    # create parser
    parser = argparse.ArgumentParser(description="Space and Time Biscuit Python CLI Help Menu 🚀")

    # add arguments
    parser.add_argument("-bpk", "--biscuit-private-key", help="Private key you want to create your biscuit with", required=False)
    parser.add_argument("-rid", "--resource-id", help="Resource ID you want to assoicate your biscuit with", required=True)

    # parse arguments
    parsed_args = parser.parse_args(args)

    # return as a dictionary
    return vars(parsed_args)

def generate_biscuit_keypair():
    keypair = KeyPair()
    private_key_str = keypair.private_key.to_hex()
    public_key_str = keypair.public_key.to_hex()
    logging.info(f"Biscuit private Key: {private_key_str}")
    logging.info(f"Biscuit public Key: {public_key_str}")
    return keypair

def generate_biscuit(private_key_str, resourceId):

    # for when user supplies a private key string 
    parse_private_key = PrivateKey.from_hex(private_key_str)
    """keypair = KeyPair()
    private_key_str = keypair.private_key.to_hex()
    public_key_str = keypair.public_key.to_hex()
    generate_random_word = lambda: ''.join(random.choices(string.ascii_lowercase, k=random.randint(4, 11)))
    random_word = generate_random_word()
    resourceId = f"{conf['schema']}.{random_word}"
    """

    """
    sxt:capability("ddl_create", {resourceId});
    sxt:capability("ddl_drop", {resourceId});
    sxt:capability("dml_insert", {resourceId});
    sxt:capability("dml_update", {resourceId});
    sxt:capability("dml_merge", {resourceId});
    sxt:capability("dml_delete", {resourceId});
    sxt:capability("dql_select", {resourceId});
    """
    # sxt:capability('ddl_create','SE_PLAYGROUND.ETH_BLACKLIST');

    builder = BiscuitBuilder("""
        sxt:capability("ddl_create", "se_playground.eth_blacklist"); 
        sxt:capability("dql_select", {resourceId});
    """,
    {
        'resourceId': resourceId
    }
    )

    token = builder.build(parse_private_key)
    token_string = token.to_base64()
    
    logging.info(f"Biscuit private Key: {private_key_str}")
    # logging.info(f"Biscuit public Key: {public_key_str}")
    logging.info(f"Resource ID: {resourceId}")    
    logging.info(f"Biscuit: {token_string}")
    
    """
    biscuit = {
        "private_key": private_key_str,
        "public_key": public_key_str,
        "resource_id": resourceId,
        "token": token_string
    }
    return biscuit
    """

if __name__ == "__main__":
    main()
