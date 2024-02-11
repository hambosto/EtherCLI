from time import sleep
from decimal import Decimal
from .contract import Contract
from .provider import API
from .transaction import Transaction
from .wallet import Wallet
from .exception import WalletError

class WalletAPI:

    @staticmethod
    def new_wallet(configuration, passphrase, password):
        """Create a new wallet.

        Args:
            configuration (dict): Configuration settings for the wallet.
            passphrase (str): The mnemonic passphrase to create the wallet.
            password (str): Password for encrypting the wallet.

        Returns:
            Wallet: The newly created wallet instance.
        """
        wallet = Wallet(configuration).create(passphrase)
        wallet.save_keystore(password)
        wallet.encrypt_wallet(password)
        return wallet

    @staticmethod
    def restore_wallet(configuration, mnemonic_secret, passphrase, password):
        """Restore a wallet from a mnemonic secret.

        Args:
            configuration (dict): Configuration settings for the wallet.
            mnemonic_secret (str): The mnemonic secret to restore the wallet.
            passphrase (str): The passphrase for the mnemonic secret.
            password (str): Password for encrypting the wallet.

        Returns:
            Wallet: The restored wallet instance.
        """
        wallet = Wallet(configuration).restore(mnemonic_secret, passphrase)
        wallet.save_keystore(password)
        wallet.encrypt_wallet(password)
        return wallet

    @staticmethod
    def import_key(configuration, private_key, password):
        """Import a wallet using a private key.

        Args:
            configuration (dict): Configuration settings for the wallet.
            private_key (str): The private key to import.
            password (str): Password for encrypting the wallet.

        Returns:
            Wallet: The imported wallet instance.
        """
        wallet = Wallet(configuration).import_key(private_key)
        wallet.save_keystore(password)
        return wallet

    @staticmethod
    def get_private_key(configuration, password):
        """Get the private key from the encrypted keystore.

        Args:
            configuration (dict): Configuration settings for the wallet.
            password (str): Password for decrypting the keystore.

        Returns:
            str: The decrypted private key.
        """
        wallet = Wallet(configuration).load_keystore(password)
        return wallet

    @staticmethod
    def decrypt_wallet(configuration, password):
        """Decrypt a wallet using the provided password.

        Args:
            configuration (dict): Configuration settings for the wallet.
            password (str): Password for decrypting the wallet.

        Returns:
            Wallet: The decrypted wallet instance.
        """
        wallet = Wallet(configuration).decrypt_wallet(password)
        return wallet

    @staticmethod
    def get_wallet(configuration):
        """Get the wallet's address.

        Args:
            configuration (dict): Configuration settings for the wallet.

        Returns:
            str: The address of the wallet.
        """
        address = Wallet(configuration).get_address()
        return address

    @staticmethod
    def get_balance(configuration, token_symbol=None, to_ether=True):
        """Get the wallet's balance.

        Args:
            configuration (dict): Configuration settings for the wallet.
            token_symbol (str, optional): Symbol of the token to check balance for. Defaults to None.
            to_ether (bool, optional): Whether to format the balance in ether. Defaults to True.

        Returns:
            float: The wallet's balance.
        """
        address = Wallet(configuration).get_address()
        if token_symbol:
            try:
                token_address = configuration.contracts[token_symbol]
            except KeyError:
                raise WalletError("KeyError", f"The token contract for {token_symbol} does not exist.")
            contract = Contract(configuration, token_address)
            return contract.get_balance(address, to_ether)
        return Wallet(configuration).get_balance(address, to_ether)

    @classmethod
    def send_tx(cls, configuration, password, receiver, value, token_symbol=None):
        """Send a transaction from the wallet.

        Args:
            configuration (dict): Configuration settings for the wallet.
            password (str): Password for decrypting the keystore.
            receiver (str): Receiver's address.
            value (float): Value to send in the transaction.
            token_symbol (str, optional): Symbol of the token to send. Defaults to None.

        Returns:
            Tuple[str, Decimal]: Tuple containing the transaction hash and transaction cost in ether.
        """
        # load wallet and create a transaction object
        wallet = Wallet(configuration).load_keystore(password)
        transaction = Transaction(wallet.get_account(), API.web3)

        # validate the value
        try:
            float(value)
        except ValueError:
            raise WalletError("ValueError", "The provided value could not be converted to a float.")

        # validate the receiver's object
        if not API.web3.is_address(receiver):
            raise WalletError("ValueError", "Invalid receiver address.")

        # validate the token symbol
        if token_symbol is not None and not isinstance(token_symbol, str):
            raise WalletError("TypeError", "Token symbol must be a string or None.")

        if token_symbol is None:
            # if no token symbol is provided, handle ether transaction
            eth_balance = cls.get_balance(configuration)
            if Decimal(value) == eth_balance:
                wei_balance = cls.get_balance(configuration, None, False)
                amount = wei_balance - (API.gas_price * API.gas_limit)
            else:
                amount = API.web3.to_wei(value, "ether")
            
            # build the transaction dictionary
            transaction_dict = transaction.build_transaction(
                receiver  = receiver,
                sender    = wallet.get_address(),
                value     = amount,
                gas_limit = API.gas_limit,
                gas_price = API.gas_price,
                nonce     = API.web3.eth.get_transaction_count(wallet.get_address()),
                chain_id  = API.chain_id,
            )

            # calculate the transaction cost in wei and ether
            tx_cost_wei = transaction_dict["gas"] * transaction_dict["gasPrice"]
            tx_cost_eth = API.web3.from_wei(tx_cost_wei, "ether")

            # check if there's enough balance for the transaction
            if value != eth_balance and (tx_cost_eth + Decimal(value)) > eth_balance:
                raise WalletError("ValueError", f"Insufficient balance for the transaction. Available balance: {eth_balance} {API.symbol}")

        else:
            # handle token transaction
            eth_balance = WalletAPI.get_balance(configuration)

            # validate token symbol
            try:
                token_address = configuration.contracts[token_symbol]
            except KeyError:
                raise WalletError("KeyError", f"The token contract for {token_symbol} does not exist.")

            contract_instance = Contract(configuration, token_address)
            token_value = int(float(value) * (10 ** contract_instance.get_contract_decimal()))
            token_balance = cls.get_balance(configuration, token_symbol)
            if float(value) > token_balance:
                raise WalletError("ValueError", f"Insufficient {token_symbol} balance for the transaction.")

            # check if there's enough balance for the token transaction
            transaction_dict = transaction.build_transaction(
                receiver  = token_address,
                sender    = wallet.get_address(),
                value     = 0,
                gas_limit = 0,
                gas_price = API.gas_price,
                nonce     = API.web3.eth.get_transaction_count(wallet.get_address()),
                chain_id  = API.chain_id,
                data      = contract_instance.build_erc20_transfer(receiver, token_value)
            )

            try:
                transaction_dict["gas"] = API.web3.eth.estimate_gas(transaction_dict)
            except ValueError:
                raise WalletError("ValueError", f"Insufficient {API.symbol} balance for {token_symbol} transaction.")

            # calculate the transaction cost in Wei and Ether
            tx_cost_wei = transaction_dict["gas"] * transaction_dict["gasPrice"]
            tx_cost_eth = API.web3.from_wei(tx_cost_wei, "ether")
            if tx_cost_eth > eth_balance:
                raise WalletError("ValueError", f"Insufficient balance to cover the network fee. Required: {tx_cost_eth} {API.symbol}")

        # sign and send the transaction
        sign_transaction = transaction.sign_transaction(transaction_dict)
        try:
            transaction_hash = transaction.send_transaction(sign_transaction)
        except ValueError as e:
            raise WalletError("ValueError", f"Error while sending transaction: {e}")
        except Exception as e:
            raise WalletError("Error", f"An error occurred while sending the transaction: {e}")

        #transaction_hash = transaction.send_transaction(sign_transaction)

        # wait for confirmation of the transaction
            #with Halo(text="Waiting for confirmation...", color="green", text_color="white", spinner="dots"):
        while True:
            try:
                transaction_receipt = API.web3.eth.get_transaction_receipt(transaction_hash)
            except:
                transaction_receipt = None
            if transaction_receipt is None:
                sleep(1)
            else:
                break

        return transaction_hash.hex(), tx_cost_eth

    @staticmethod
    def add_contract(configuration, token_address):
        """Add a new token contract address to the configuration.

        Args:
            configuration (dict): Configuration settings for the wallet.
            token_address (str): Address of the token contract to add.
        """
        contract = Contract(configuration, token_address)
        contract.add_contract(token_address)

    @staticmethod
    def list_token(configuration):
        """Get the list of token contracts from the configuration.

        Args:
            configuration (dict): Configuration settings for the wallet.

        Returns:
            Dict[str, str]: Dictionary containing token symbols and their corresponding contract addresses.
        """
        return configuration.contracts
