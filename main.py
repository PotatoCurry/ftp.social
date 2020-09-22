import textwrap

from pyftpdlib.servers import FTPServer

from custom_handler import CustomHandler
from hashed_authorizer import create_authorizer
from user import Base, engine


def main():
    Base.metadata.create_all(engine)

    handler = CustomHandler
    handler.authorizer = create_authorizer()
    handler.banner = textwrap.dedent(r"""
                        _____                      _      __
                       / _/ /____    ___ ___  ____(_)__ _/ /
                      / _/ __/ _ \_ (_-</ _ \/ __/ / _ `/ / 
                     /_/ \__/ .__(_)___/\___/\__/_/\_,_/_/  
                           /_/                              """)
    handler.certfile = 'ftpsocial.crt'
    handler.keyfile = 'ftpsocial.key'
    handler.masquerade_address = 'ftp.social'  # Resolves to external IP address
    handler.permit_foreign_addresses = False
    handler.passive_ports = range(60000, 65535)

    server = FTPServer(('0.0.0.0', 2121), handler)
    server.max_cons_per_ip = 5
    server.serve_forever()


if __name__ == '__main__':
    main()
