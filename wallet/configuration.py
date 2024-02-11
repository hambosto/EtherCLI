import os
import json
from .utils import is_file, create_directory

class Configuration:
    """Handles configuration data for the application."""

    ROOT_DIR           = os.path.dirname(os.path.abspath(__file__))
    CONFIG_DIR         = os.path.join(ROOT_DIR, "config")
    CONFIG_FILE_PATH   = os.path.join(CONFIG_DIR, "config.json")
    KEYSTORE_FILE_PATH = os.path.join(CONFIG_DIR, "keystore.json")
    WALLET_FILE_PATH   = os.path.join(CONFIG_DIR, "wallet.json")
    DEFAULT_CONFIG     = {"address": "", "contracts": dict()}

    def __init__(
        self,
        config_dir=CONFIG_DIR,
        config_file_path=CONFIG_FILE_PATH,
        keystore_file_path=KEYSTORE_FILE_PATH,
        wallet_file_path=WALLET_FILE_PATH,
        default_config=DEFAULT_CONFIG,
    ):
        """
        Initialize the Configuration instance.

        Args:
            config_dir (str, optional): Directory to store configuration files. Defaults to "config".
            config_file_path (str, optional): Configuration file path. Defaults to "config/config.json".
            keystore_file_path (str, optional): Keystore file path. Defaults to "config/keystore.json".
            wallet_file_path (str, optional): Wallet file path. Defaults to "config/wallet.json".
            default_config (dict, optional): Default configuration dictionary. Defaults to {"address": "", "contracts": dict()}.
        """
        self.config_dir         = config_dir
        self.config_file_path   = config_file_path
        self.keystore_file_path = keystore_file_path
        self.wallet_file_path   = wallet_file_path
        self.default_config     = default_config
        self.address            = ""
        self.contracts          = dict()

    def load_configuration(self):
        """
        Load the configuration from the file if it exists, or set up a new one.
        """
        if not is_file(self.config_file_path):
            self.setup_configuration()
            self.load_configuration()
        else:
            with open(self.config_file_path, "r") as config_file:
                config_data = json.load(config_file)
            self.update_attributes(config_data)
        return self

    def setup_configuration(self):
        """
        Create the configuration directory and store the default configuration in a JSON file.
        """
        create_directory(self.config_dir)
        with open(self.config_file_path, "w+") as config_file:
            json.dump(self.default_config, config_file, indent=4)

    def update_attributes(self, new_attributes):
        """
        Update the configuration attributes with the provided dictionary.

        Args:
            new_attributes (dict): Dictionary containing the attributes to update.
        """
        for key, value in new_attributes.items():
            setattr(self, key, value)

    def update_address(self, new_address):
        """
        Update the address attribute and save it to the configuration file.

        Args:
            new_address (str): New address to update.
        """
        self.address = new_address
        self.__update_config_file("address", new_address)

    def add_contract(self, symbol, address):
        """
        Add a new contract to the contracts dictionary and save it to the configuration file.

        Args:
            symbol (str): Symbol of the contract.
            address (str): Address of the contract.
        """
        self.contracts[symbol] = address
        self.__update_config_file("contracts", self.contracts)

    def remove_contract(self, symbol):
        """
        Remove a contract from the contracts dictionary and save the updated dictionary to the configuration file.

        Args:
            symbol (str): Symbol of the contract to remove.
        """
        if symbol in self.contracts:
            del self.contracts[symbol]
            self.__update_config_file("contracts", self.contracts)

    def __update_config_file(self, key, value):
        """
        Update the configuration file with a new key-value pair.

        Args:
            key (str): Key to update.
            value (Any): Value to update.
        """
        with open(self.config_file_path, "r") as config_file:
            config_data = json.load(config_file)
        config_data[key] = value
        create_directory(self.config_dir)
        with open(self.config_file_path, "w+") as config_file:
            json.dump(config_data, config_file, indent=4)

