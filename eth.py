import argparse
import json
import logging
import base64
from tabulate import tabulate
from cryptocompare import cryptocompare
from rich.console import Console
from rich.logging import RichHandler
from rich_argparse import RichHelpFormatter
from wallet.api import WalletAPI
from wallet.configuration import Configuration
from wallet.provider import API
from wallet.exception import WalletError
from wallet.utils import (
    append_url,
    clear_terminal,
    format_number,
    is_file,
    remove_directory,
)

logging.basicConfig(
    level=logging.NOTSET,  # Set the logging level
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, tracebacks_show_locals=True)],
)

logger = logging.getLogger("rich")


class EtherCLI:
    """
    Ethereum Virtual Machine Wallet Command Line Interface.

    This CLI tool allows users to interact with an Ethereum wallet, including creating,
    restoring, importing wallets, checking balances, sending transactions, and more.

    Attributes:
        provider (API): The API provider for the wallet.
        api (WalletAPI): An instance of the WalletAPI class for interacting with the wallet.
        configuration (Configuration): The wallet configuration.
        console (Console): Rich library Console for enhanced console output.

    Methods:
        check_balance(): Check the balance of the wallet and display it.
        send_transaction(symbol, amount, address, password): Send funds from the wallet to another address.
        receive(): Generate and display the wallet's address.
        add_contract(token_address): Add a new contract to the wallet.
        create_wallet(passphrase, password): Create a new wallet and display its information.
        restore_wallet(mnemonic_secret, passphrase, password): Restore a wallet from a mnemonic phrase and display its information.
        import_wallet(private_key, password): Import a wallet from a private key and display its information.
        export_wallet(password): Export the wallet's private key and display it.
        decrypt_wallet(password): Decrypt the wallet and display its information.
        erase_wallet(): Erase the wallet's configuration.

    """

    def __init__(self) -> None:
        """
        Initialize the EtherCLI.

        This constructor sets up the CLI, parses command-line arguments, and performs
        wallet actions based on the provided arguments.
        """
        self.provider = API
        self.api = WalletAPI()
        self.configuration = Configuration().load_configuration()
        self.console = Console()

        clear_terminal()
        banner = "W2JvbGQgd2hpdGVd4paI4paI4paI4paI4paI4paI4paI4pWX4paI4paI4paI4paI4paI4paI4paI4paI4pWX4paI4paI4pWXICDilojilojilZfilojilojilojilojilojilojilojilZfilojilojilojilojilojilojilZcgWy9ib2xkIHdoaXRlXVtib2xkIHJlZF0g4paI4paI4paI4paI4paI4paI4pWX4paI4paI4pWXICAgICDilojilojilZdbL2JvbGQgcmVkXQpbYm9sZCB3aGl0ZV3ilojilojilZTilZDilZDilZDilZDilZ3ilZrilZDilZDilojilojilZTilZDilZDilZ3ilojilojilZEgIOKWiOKWiOKVkeKWiOKWiOKVlOKVkOKVkOKVkOKVkOKVneKWiOKWiOKVlOKVkOKVkOKWiOKWiOKVl1svYm9sZCB3aGl0ZV1bYm9sZCByZWRd4paI4paI4pWU4pWQ4pWQ4pWQ4pWQ4pWd4paI4paI4pWRICAgICDilojilojilZFbL2JvbGQgcmVkXQpbYm9sZCB3aGl0ZV3ilojilojilojilojilojilZcgICAgIOKWiOKWiOKVkSAgIOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKVkeKWiOKWiOKWiOKWiOKWiOKVlyAg4paI4paI4paI4paI4paI4paI4pWU4pWdWy9ib2xkIHdoaXRlXVtib2xkIHJlZF3ilojilojilZEgICAgIOKWiOKWiOKVkSAgICAg4paI4paI4pWRWy9ib2xkIHJlZF0KW2JvbGQgd2hpdGVd4paI4paI4pWU4pWQ4pWQ4pWdICAgICDilojilojilZEgICDilojilojilZTilZDilZDilojilojilZHilojilojilZTilZDilZDilZ0gIOKWiOKWiOKVlOKVkOKVkOKWiOKWiOKVl1svYm9sZCB3aGl0ZV1bYm9sZCByZWRd4paI4paI4pWRICAgICDilojilojilZEgICAgIOKWiOKWiOKVkVsvYm9sZCByZWRdCltib2xkIHdoaXRlXeKWiOKWiOKWiOKWiOKWiOKWiOKWiOKVlyAgIOKWiOKWiOKVkSAgIOKWiOKWiOKVkSAg4paI4paI4pWR4paI4paI4paI4paI4paI4paI4paI4pWX4paI4paI4pWRICDilojilojilZFbL2JvbGQgd2hpdGVdW2JvbGQgcmVkXeKVmuKWiOKWiOKWiOKWiOKWiOKWiOKVl+KWiOKWiOKWiOKWiOKWiOKWiOKWiOKVl+KWiOKWiOKVkVsvYm9sZCByZWRdCltib2xkIHdoaXRlXeKVmuKVkOKVkOKVkOKVkOKVkOKVkOKVnSAgIOKVmuKVkOKVnSAgIOKVmuKVkOKVnSAg4pWa4pWQ4pWd4pWa4pWQ4pWQ4pWQ4pWQ4pWQ4pWQ4pWd4pWa4pWQ4pWdICDilZrilZDilZ1bL2JvbGQgd2hpdGVdW2JvbGQgcmVkXSDilZrilZDilZDilZDilZDilZDilZ3ilZrilZDilZDilZDilZDilZDilZDilZ3ilZrilZDilZ1bL2JvbGQgcmVkXQogICAgICBDb2RlZCBieSBbaXRhbGljXUBoYW1ib3N0b1svaXRhbGljXSAtIFtib2xkIHB1cnBsZV1odHRwczovL2dpdGh1Yi5jb20vaGFtYm9zdG9bL2JvbGQgcHVycGxlXQpbaXRhbGljIGJvbGQgeWVsbG93XUV0aGVyQ0xJWy9pdGFsaWMgYm9sZCB5ZWxsb3ddIC0gW2JvbGQgd2hpdGUgb24gZ3JlZW5dRXRoZXJldW0gVmlydHVhbCBNYWNoaW5lIFdhbGxldCBDTElbL2JvbGQgd2hpdGUgb24gZ3JlZW5dICAgCkEgY29tbWFuZC1saW5lIHRvb2wgZm9yIG1hbmFnaW5nIHlvdXIgRXRoZXJldW0gW2l0YWxpYyBib2xkIGdyZWVuXXdhbGxldHNbL2l0YWxpYyBib2xkIGdyZWVuXSwgW2l0YWxpYyBib2xkIGdyZWVuXXRyYW5zYWN0aW9uc1svaXRhbGljIGJvbGQgZ3JlZW5dLCBhbmQgW2l0YWxpYyBib2xkIGdyZWVuXW1vcmVbL2l0YWxpYyBib2xkIGdyZWVuXS4KVGFrZSBjb250cm9sIG9mIHlvdXIgZGlnaXRhbCBhc3NldHMgd2l0aCBlYXNlLgo="
        banner = base64.b64decode(banner)
        self.console.print(banner.decode())

        parser = argparse.ArgumentParser(
            description="Ethereum Virtual Machine Wallet CLI",
            formatter_class=RichHelpFormatter,
        )

        if not is_file(self.configuration.KEYSTORE_FILE_PATH):
            logger.warning("KEYSTORE_FILE_PATH is not exists!")

            subparsers = parser.add_subparsers(
                description="Wallet Setup Commands",
                dest="action",
                help="Available Actions",
            )

            # Create Wallet
            create_parser = subparsers.add_parser("create", help="Create a new wallet")
            create_parser.add_argument(
                "--passphrase",
                required=True,
                help="Passphrase for the wallet (e.g., my_passphrase)",
            )
            create_parser.add_argument(
                "--password",
                required=True,
                help="Password for the wallet (e.g., my_password)",
            )

            # Restore Wallet
            restore_parser = subparsers.add_parser(
                "restore", help="Restore your wallet from a mnemonic phrase"
            )
            restore_parser.add_argument(
                "--mnemonic",
                nargs="+",
                required=True,
                help="Mnemonic phrase (e.g., word1 word2 ...)",
            )
            restore_parser.add_argument(
                "--passphrase",
                required=True,
                help="Passphrase for the wallet (e.g., my_passphrase)",
            )
            restore_parser.add_argument(
                "--password",
                required=True,
                help="Password for the wallet (e.g., my_password)",
            )

            # Import Wallet
            import_parser = subparsers.add_parser(
                "import", help="Import a wallet from a private key"
            )
            import_parser.add_argument(
                "--private-key",
                required=True,
                help="Private key for import (e.g., 0xabcdef...)",
            )
            import_parser.add_argument(
                "--password",
                required=True,
                help="Password for the wallet (e.g., my_password)",
            )

            args = parser.parse_args()

            if args.action == "create":
                self.create_wallet(args.passphrase, args.password)
            elif args.action == "restore":
                self.restore_wallet(args.mnemonic, args.passphrase, args.password)
            elif args.action == "import":
                self.import_wallet(args.private_key, args.password)

        else:
            # Subparsers for wallet actions
            subparsers = parser.add_subparsers(
                description="Wallet Actions", dest="action", help="Available Actions"
            )

            # Check Balance
            balance_parser = subparsers.add_parser(
                "balance", help="Check the balance of your wallet"
            )

            # Send Funds
            send_parser = subparsers.add_parser(
                "send", help="Send funds to another address"
            )
            send_parser.add_argument(
                "--symbol",
                required=True,
                help="Symbol of the currency to send (e.g., ETH)",
            )
            send_parser.add_argument(
                "--amount", type=float, required=True, help="Amount to send (e.g., 1.0)"
            )
            send_parser.add_argument(
                "--address",
                required=True,
                help="Recipient's address (e.g., 0x12345...)",
            )
            send_parser.add_argument(
                "--password",
                required=True,
                help="Password for the wallet (e.g., my_password)",
            )

            # Receive Wallet Address
            receive_parser = subparsers.add_parser(
                "receive", help="Generate your wallet address"
            )

            # Interact with Contract
            contract_parser = subparsers.add_parser(
                "add-contract", help="Add a new contract to your wallet"
            )
            contract_parser.add_argument(
                "--token-address",
                required=True,
                help="Token contract address (e.g., 0x6789...)",
            )

            # Create Wallet
            create_parser = subparsers.add_parser("create", help="Create a new wallet")
            create_parser.add_argument(
                "--passphrase",
                required=True,
                help="Passphrase for the wallet (e.g., my_passphrase)",
            )
            create_parser.add_argument(
                "--password",
                required=True,
                help="Password for the wallet (e.g., my_password)",
            )

            # Restore Wallet
            restore_parser = subparsers.add_parser(
                "restore", help="Restore your wallet from a mnemonic phrase"
            )
            restore_parser.add_argument(
                "--mnemonic",
                nargs="+",
                required=True,
                help="Mnemonic phrase (e.g., word1 word2 ...)",
            )
            restore_parser.add_argument(
                "--passphrase",
                required=True,
                help="Passphrase for the wallet (e.g., my_passphrase)",
            )
            restore_parser.add_argument(
                "--password",
                required=True,
                help="Password for the wallet (e.g., my_password)",
            )

            # Import Wallet
            import_parser = subparsers.add_parser(
                "import", help="Import a wallet from a private key"
            )
            import_parser.add_argument(
                "--private-key",
                required=True,
                help="Private key for import (e.g., 0xabcdef...)",
            )
            import_parser.add_argument(
                "--password",
                required=True,
                help="Password for the wallet (e.g., my_password)",
            )

            # Export Wallet
            export_parser = subparsers.add_parser(
                "export", help="Export your wallet's private key"
            )
            export_parser.add_argument(
                "--password",
                required=True,
                help="Password to export the wallet (e.g., my_password)",
            )

            # Decrypt Wallet
            decrypt_parser = subparsers.add_parser(
                "decrypt", help="Decrypt your wallet"
            )
            decrypt_parser.add_argument(
                "--password",
                required=True,
                help="Password to decrypt the wallet (e.g., my_password)",
            )

            # Erase Wallet Configuration
            erase_parser = subparsers.add_parser(
                "erase", help="Erase the wallet configuration"
            )

            args = parser.parse_args()

            if args.action is None:
                parser.print_help()

            if args.action == "balance":
                self.get_balances()

            elif args.action == "send":
                self.send_transaction(
                    args.symbol, args.amount, args.address, args.password
                )

            elif args.action == "receive":
                self.receive()

            elif args.action == "add-contract":
                self.add_contract(args.token_address)

            elif args.action == "create":
                self.create_wallet(args.passphrase, args.password)

            elif args.action == "restore":
                self.restore_wallet(args.mnemonic, args.passphrase, args.password)

            elif args.action == "import":
                self.import_wallet(args.private_key, args.password)

            elif args.action == "export":
                self.export_wallet(args.password)

            elif args.action == "decrypt":
                self.decrypt_wallet(args.password)

            elif args.action == "erase":
                self.erase_wallet()

            # print("-" * 70)

    def get_balances(self):
        try:
            # Get wallet address
            address = self.api.get_wallet(self.configuration)

            # Retrieve token symbols and add the provider symbol
            token_symbols = list(self.api.list_token(self.configuration).keys())
            all_symbols = token_symbols + [self.provider.symbol]

            # Initialize wallet_balance dictionary with Ethereum balance
            wallet_balance = {
                self.provider.symbol: self.api.get_balance(self.configuration)
            }

            # Retrieve token balances and add them to wallet_balance
            wallet_balance.update(
                {
                    symbol: self.api.get_balance(self.configuration, symbol)
                    for symbol in token_symbols
                }
            )

            # Sort wallet_balance by keys
            sorted_balance = dict(sorted(wallet_balance.items()))

            # Show wallet address in the log
            logger.debug(f"Retrieving balance for wallet address -> {address}")

            # Retrieve prices from CryptoCompare
            cryptocompare._set_api_key_parameter(self.provider.CRYPTOCOMPARE_API_KEY)
            get_price = cryptocompare.get_price(
                all_symbols, currency=self.provider.DEFAULT_CURRENCY
            )
            price_list = {
                symbol: price[self.provider.DEFAULT_CURRENCY]
                for symbol, price in get_price.items()
            }

            # Calculate values in USD and sort by key
            calculated_value = {
                symbol: sorted_balance[symbol] * price_list[symbol]
                for symbol in all_symbols
                if symbol in price_list
            }

            calculated_value = dict(sorted(calculated_value.items()))

            # Combine balance and USD value data
            combine_data = {
                "Symbol": all_symbols,
                f"Holdings": [
                    format_number(wallet_balance.get(symbol, ""))
                    for symbol in all_symbols
                ],
                f"Market Price ({self.provider.DEFAULT_CURRENCY})": [
                    format_number(price_list.get(symbol, "N/A"))
                    for symbol in all_symbols
                ],
                f"Market Value ({self.provider.DEFAULT_CURRENCY})": [
                    format_number(calculated_value.get(symbol, "N/A"))
                    for symbol in all_symbols
                ],
            }

            # Create a single table
            table = tabulate(combine_data, headers="keys", tablefmt="pretty")

            # Log the results
            logger.info(table)

        except WalletError as err:
            logger.error(err.message)

    def send_transaction(self, symbol, amount, address, password):
        """
        Send funds from the wallet to another address.

        Args:
            symbol (str): Symbol of the currency to send (e.g., ETH).
            amount (float): Amount to send (e.g., 1.0).
            address (str): Recipient's address (e.g., 0x12345...).
            password (str): Password for the wallet.

        This method sends funds from the wallet to the specified address, supporting Ethereum
        and tokens. It also displays transaction details if the transaction is successful.
        """
        # get a list of supported symbols
        supported_symbols = list(self.api.list_token(self.configuration).keys())
        supported_symbols.append(self.provider.symbol)

        if symbol not in supported_symbols:
            logger.error(f"The symbol {symbol} was not added to the wallet.")
            logger.info(json.dumps(supported_symbols, indent=4))
            return

        try:
            if symbol == self.provider.symbol:
                token_symbol = None
            else:
                token_symbol = symbol

            transaction_hash, transaction_cost = self.api.send_tx(
                self.configuration, password, address, amount, token_symbol=token_symbol
            )

            if transaction_hash and transaction_cost:
                transaction_url = append_url(
                    base_url=self.provider.explorer_url, tx="tx", hash=transaction_hash
                )
                logger.info(
                    json.dumps(
                        {
                            "transaction_hash": str(transaction_hash),
                            "transaction_cost": str(transaction_cost),
                            "transaction_url": str(transaction_url),
                        },
                        indent=4,
                    ),
                )

        except WalletError as err:
            logger.error(err.message)

    def receive(self):
        """
        Generate and display the wallet's address.

        This method generates and displays the wallet's Ethereum address.
        """
        try:
            address = self.api.get_wallet(self.configuration)
            logger.info(
                json.dumps({"wallet_address": address}, indent=4),
            )
        except WalletError as err:
            logger.error(err.message)

    def add_contract(self, token_address):
        """
        Add a new contract to the wallet.

        Args:
            token_address (str): Token contract address (e.g., 0x6789...).

        This method adds a new contract to the wallet based on the provided token contract address.
        """
        try:
            self.api.add_contract(self.configuration, token_address)
        except WalletError as err:
            logger.error(err.message)

    def create_wallet(self, passphrase, password):
        """
        Create a new wallet and display its information.

        Args:
            passphrase (str): Passphrase for the wallet.
            password (str): Password for the wallet.

        This method creates a new wallet with the specified passphrase and password and displays
        its address, private key, and other relevant information.
        """
        try:
            wallet = self.api.new_wallet(self.configuration, passphrase, password)
            logger.info(
                json.dumps(
                    {
                        "address": wallet.get_address(),
                        "private_key": wallet.get_private_key(),
                        "mnemonic_secret": wallet.get_mnemonic(),
                        "passphrase": wallet.get_passphrase(),
                        "derivation_path": wallet.get_derivation(),
                        "password": password,
                    },
                    indent=4,
                ),
            )
        except WalletError as err:
            logger.error(err.message)

    def restore_wallet(self, mnemonic_secret, passphrase, password):
        """
        Restore a wallet from a mnemonic phrase and display its information.

        Args:
            mnemonic_secret (list): List of words forming the mnemonic phrase.
            passphrase (str): Passphrase for the wallet.
            password (str): Password for the wallet.

        This method restores a wallet using the provided mnemonic phrase, passphrase, and password,
        and then displays its address, private key, and other relevant information.
        """
        try:
            wallet = self.api.restore_wallet(
                self.configuration, " ".join(mnemonic_secret), passphrase, password
            )
            logger.info(
                json.dumps(
                    {
                        "address": wallet.get_address(),
                        "private_key": wallet.get_private_key(),
                        "mnemonic_secret": wallet.get_mnemonic(),
                        "passphrase": wallet.get_passphrase(),
                        "derivation_path": wallet.get_derivation(),
                        "password": password,
                    },
                    indent=4,
                ),
            )
        except WalletError as err:
            logger.error(err.message)

    def import_wallet(self, private_key, password):
        """
        Import a wallet from a private key and display its information.

        Args:
            private_key (str): Private key for import (e.g., 0xabcdef...).
            password (str): Password for the wallet.

        This method imports a wallet from the provided private key and displays its address
        and other relevant information.
        """
        try:
            wallet = self.api.import_key(self.configuration, private_key, password)
            logger.info(
                json.dumps(
                    {
                        "address": wallet.get_address(),
                        "private_key": wallet.get_private_key(),
                        "password": password,
                    },
                    indent=4,
                ),
            )
        except WalletError as err:
            logger.error(err.message)

    def export_wallet(self, password):
        """
        Export the wallet's private key and display it.

        Args:
            password (str): Password to export the wallet.

        This method exports the wallet's private key using the provided password and displays it.
        """
        try:
            wallet = self.api.get_private_key(self.configuration, password)
            logger.info(json.dumps({"private_key": wallet.get_private_key()}, indent=4))
        except WalletError as err:
            logger.error(err.message)

    def decrypt_wallet(self, password):
        """
        Decrypt the wallet and display its information.

        Args:
            password (str): Password to decrypt the wallet.

        This method decrypts the wallet using the provided password and displays its information.
        """
        if is_file(self.configuration.WALLET_FILE_PATH):
            try:
                wallet = self.api.decrypt_wallet(self.configuration, password)
                logger.info(json.dumps(wallet, indent=4))
            except WalletError as err:
                logger.error(err.message)

    def erase_wallet(self):
        """
        Erase the wallet's configuration.

        This method removes the wallet's configuration and associated files, effectively erasing
        the wallet's data.
        """
        key_file = self.configuration.KEYSTORE_FILE_PATH
        config_dir = self.configuration.CONFIG_DIR

        if is_file(key_file):
            try:
                remove_directory(config_dir)
                logger.info("Wallet successfulyy erased.")
                return
            except Exception as err:
                logger.error(f"Unable to erase the wallet: {str(err)}")
                return

        logger.error("Wallet configuration does not exist.")


if __name__ == "__main__":
    run = EtherCLI()
