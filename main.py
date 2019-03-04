import argparse
import sys

parser = argparse.ArgumentParser(description='Main Application')

parser.add_argument('-s','--server',action='store_true',help='Launching Server',dest='server')
parser.add_argument('-c','--client',help='Launching Client',dest='client')

args = parser.parse_args()
if args.client and args.server is True:
    print("Cannot run both Client and Server")
    sys.exit(1)

if args.server:
    from remote.server import server_init
    server_init(__name__)
elif args.client:
    from remote.client import client_init
    client_init(args.client)
