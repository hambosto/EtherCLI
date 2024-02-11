from .provider import API
from .utils import get_json_abi


class Contract:
    """
    Represents an ERC-20 contract and provides methods to interact with it.

    Attributes:
        configuration (Configuration): The configuration object to manage contract details.
        contract (Any): The web3 contract object for the ERC-20 token.

    Methods:
        get_contract() -> 'Contract':
            Returns the current Contract instance.

        get_symbol() -> str:
            Returns the symbol of the ERC-20 token.

        get_name() -> str:
            Returns the name of the ERC-20 token.

        get_decimal() -> int:
            Returns the decimal places used by the ERC-20 token.

        get_balance(address: str, to_ether: bool = True) -> float:
            Returns the token balance of the given address. If `to_ether` is True, the balance
            will be converted to ether based on the token's decimals.

        build_erc20_transfer(receiver: str, value: int) -> str:
            Builds the ABI-encoded transfer function call to transfer tokens to the given receiver.

        add_contract(token_address: str) -> None:
            Adds the token contract with its symbol to the configuration object.
    """

    def __init__(self, configuration, token_address):
        """
        Initializes a new Contract instance.

        Args:
            configuration (Configuration): The configuration object to manage contract details.
            token_address (str): The address of the ERC-20 token contract.
        """
        self.configuration = configuration
        self.contract = API.web3.eth.contract(address=API.web3.to_checksum_address(token_address), abi=get_json_abi())

    def get_contract(self) -> "Contract":
        """Returns the current Contract instance."""
        return self

    def get_symbol(self) -> str:
        """Returns the symbol of the ERC-20 token."""
        return self.contract.functions.symbol().call()

    def get_name(self) -> str:
        """Returns the name of the ERC-20 token."""
        return self.contract.functions.name().call()

    def get_contract_decimal(self) -> int:
        """Returns the decimal places used by the ERC-20 token."""
        return self.contract.functions.decimals().call()

    def get_balance(self, address: str, is_ether: bool = True) -> float:
        """
        Returns the token balance of the given address.

        Args:
            address (str): The address to get the token balance for.
            to_ether (bool): If True, the balance will be converted to ether based on the token's decimals.

        Returns:
            float: The token balance of the address.
        """
        balance_wei = self.contract.functions.balanceOf(address).call()
        contract_decimals = self.get_contract_decimal()
        if is_ether:
            balance_eth = balance_wei / float(pow(10, contract_decimals))
            return round(balance_eth, 3)
        return balance_wei

    def build_erc20_transfer(self, receiver: str, value: int) -> str:
        """
        Builds the ABI-encoded transfer function call to transfer tokens to the given receiver.

        Args:
            receiver (str): The address of the receiver.
            value (int): The amount of tokens to transfer.

        Returns:
            str: The ABI-encoded transfer function call.
        """
        return self.contract.encodeABI("transfer", [receiver, value])

    def add_contract(self, token_address: str) -> None:
        """
        Adds the token contract with its symbol to the configuration object.

        Args:
            token_address (str): The address of the token contract to add.
        """
        self.configuration.add_contract(self.get_symbol(), API.web3.to_checksum_address(token_address))
