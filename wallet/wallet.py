from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from hdwallet.utils import generate_mnemonic
from eth_account import Account
from .cipher import Cipher
from .provider import API
from .exception import WalletError
import json

class Wallet:
    """A class representing a cryptocurrency wallet."""

    def __init__(self, configuration) -> None:
        """
        Initialize the wallet.

        Args:
            configuration: An instance of the wallet's configuration.
        """
        self.configuration = configuration
        self.account = None
        self.mnemonic_secret = None
        self.passphrase = None
        self.account_path = None

    def create(self, passphrase=None, mnemonic_secret=None):
        """
        Create a new wallet or restore an existing one.

        Args:
            passphrase: Passphrase for the mnemonic (optional).
            mnemonic_secret: Mnemonic secret for wallet restoration (optional).

        Returns:
            The wallet instance.
        """
        if mnemonic_secret is None:
            self.mnemonic_secret = generate_mnemonic("english", 256)
            self.passphrase = passphrase
        else:
            self.mnemonic_secret = mnemonic_secret
            self.passphrase = passphrase

        hdwallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
        hdwallet.from_mnemonic(self.mnemonic_secret, "english", self.passphrase)
        hdwallet.clean_derivation()
        hdwallet.from_path(BIP44Derivation(cryptocurrency=EthereumMainnet, account=1, change=False, address=0))

        self.account = self.set_account(hdwallet.private_key())
        self.account_path = hdwallet.path()
        self.configuration.update_address(self.account.address)

        return self

    def restore(self, mnemonic_secret, passphrase):
        """
        Restore the wallet using a provided mnemonic secret and passphrase.

        Args:
            mnemonic_secret: Mnemonic secret for wallet restoration.
            passphrase: Passphrase for the mnemonic.

        Returns:
            The wallet instance.
        """
        return self.create(passphrase, mnemonic_secret)

    def import_key(self, private_key):
        """
        Import a private key to the wallet.

        Args:
            private_key: The private key to import.

        Returns:
            The wallet instance.
        """
        self.account = self.set_account(private_key)
        self.configuration.update_address(self.account.address)
        return self

    def get_balance(self, address, is_ether=True):
        """
        Get the balance of the wallet.

        Args:
            address: Address of the wallet.
            ether: Convert balance to Ether (default is True).

        Returns:
            The balance in Ether or Wei.
        """
        balance_wei = API.web3.eth.get_balance(address)
        if is_ether:
            balance_eth = balance_wei / float(pow(10, 18))
            return round(balance_eth, 3)
        return balance_wei

    def get_account(self):
        """
        Get the account associated with the wallet.

        Returns:
            The account instance.
        """
        return self.account

    def get_address(self):
        """
        Get the address of the wallet.

        Returns:
            The wallet address.
        """
        return self.configuration.address
    
    def get_private_key(self):
        """
        Get the private key of the wallet.

        Returns:
            The private key in hexadecimal format.
        """
        return self.account.key.hex()

    def get_mnemonic(self):
        """
        Get the mnemonic secret of the wallet.

        Returns:
            The mnemonic secret.
        """
        return self.mnemonic_secret

    def get_passphrase(self):
        """
        Get the passphrase of the wallet.

        Returns:
            The passphrase.
        """
        return self.passphrase

    def get_derivation(self):
        """
        Get the derivation path of the wallet.

        Returns:
            The account derivation path.
        """
        return self.account_path

    def set_account(self, private_key):
        """
        Set the account using a private key.

        Args:
            private_key: The private key to set the account.

        Returns:
            The account instance.
        """
        try:
            self.account = Account.from_key(private_key)
        except ValueError:
            raise WalletError(
                    "ValueError",
                    "Private key must be 32 bytes long, instead of %d bytes" % len(private_key)
            )
        return self.account

    def save_keystore(self, password):
        """
        Save the encrypted keystore.

        Args:
            password: Password to encrypt the keystore.

        Returns:
            The wallet instance.
        """
        keystore_path = self.configuration.KEYSTORE_FILE_PATH
        private_key = Account.encrypt(self.account.key, password)
        with open(keystore_path, "w+") as key_path:
            json.dump(private_key, key_path, indent=4)
        return self

    def load_keystore(self, password):
        """
        Load the encrypted keystore.

        Args:
            password: Password to decrypt the keystore.

        Returns:
            The wallet instance.
        """
        keystore_path = self.configuration.KEYSTORE_FILE_PATH
        with open(keystore_path) as key_path:
            private_key = json.load(key_path)
            try: 
                private_key = Account.decrypt(private_key, password)
            except ValueError:
                raise WalletError("ValueError", "Error while decrypting wallet, Invalid password.")
        self.account = self.set_account(private_key)
        return self

    def encrypt_wallet(self, password):
        """
        Encrypt the wallet.

        Args:
            password: Password to decrypt the wallet.

        Returns:
            The wallet instance.
        """
        wallet_details = json.dumps({
            "address": self.get_address(),
            "private_key": self.get_private_key(),
            "mnemonic_secret": self.get_mnemonic(),
            "passphrase": self.get_passphrase(),
            "derivation_path": self.get_derivation(),
        }, indent=4)
        encrypt_wallet = Cipher(password).encrypt(wallet_details)
        wallet_path = self.configuration.WALLET_FILE_PATH
        with open(wallet_path, "w+") as wallet_file:
            wallet_file.write(encrypt_wallet)
        return self

    def decrypt_wallet(self, password):
        """
        Decrypt the wallet.

        Args:
            password: Password to decrypt the wallet.

        Returns:
            Decrypted wallet data.
        """
        wallet_path = self.configuration.WALLET_FILE_PATH
        try:
            with open(wallet_path, "r") as wallet_file:
                get_wallet = Cipher(password).decrypt(wallet_file.read())
        except ValueError:
            raise WalletError("ValueError", "MAC verification failed or invalid password.")
        return json.loads(get_wallet)

