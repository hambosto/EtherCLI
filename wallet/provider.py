from os import getenv
from web3 import Web3, HTTPProvider, WebsocketProvider
from .exception import WalletError

class Provider:
    """Provider class for interacting with a blockchain node.

    Attributes:
        DEFAULT_NODE_URL (str): The default URL of the blockchain node.
        DEFAULT_SYMBOL (str): The default symbol of the blockchain (e.g., "ETH").
        DEFAULT_EXPLORER_URL (str): The default URL of the blockchain explorer.
        DEFAULT_NODE_NAME (str): The default name of the blockchain node.
        DEFAULT_GAS_LIMIT (int): The default gas limit for transactions.

    Methods:
        __init__: Initializes the Provider instance.
        provider: Property to access the Web3 provider.
        web3: Property to access the Web3 instance and check if connected.
        gas_limit: Property to access the default gas limit.
        gas_price: Property to get the current gas price.
        chain_id: Property to get the current chain ID.
        node_url: Property to access the node URL.
        symbol: Property to access the blockchain symbol.
        explorer_url: Property to access the explorer URL.
        node_name: Property to access the blockchain node name.
    """

    DEFAULT_NODE_URL     = "https://rpc.ankr.com/eth"
    DEFAULT_SYMBOL       = "ETH"
    DEFAULT_EXPLORER_URL = "http://etherscan.io"
    DEFAULT_NODE_NAME    = "Ethereum Main Network"
    DEFAULT_GAS_LIMIT    = 21000
    DEFAULT_CURRENCY     = "IDR"

    CRYPTOCOMPARE_API_KEY = "PUT YOU API KEY HERE"

    def __init__(self) -> None:
        """Initialize the BlockchainProvider instance."""
        self._provider = None

    @property
    def provider(self) -> Web3:
        """Property to access the Web3 provider."""
        if self._provider is None:
            self._provider = self._create_provider()
        return self._provider

    def _create_provider(self) -> Web3:
        """Create and return a Web3 provider based on the node URL."""
        if self.node_url.startswith("wss"):
            return Web3(WebsocketProvider(self.node_url))
        else:
            return Web3(HTTPProvider(self.node_url))
    
    @property
    def web3(self) -> Web3:
        """Property to access the Web3 instance and check if connected."""
        if not self.provider.is_connected():
            raise WalletError("Web3", f"Not connected to {self.node_name}")
        return self.provider

    @property
    def gas_limit(self) -> int:
        """Property to access the default gas limit."""
        return self.DEFAULT_GAS_LIMIT

    @property
    def gas_price(self) -> int:
        """Property to get the current gas price."""
        return self.web3.eth.gas_price

    @property
    def chain_id(self) -> int:
        """Property to get the current chain ID."""
        return self.web3.eth.chain_id

    @property
    def node_url(self) -> str:
        """Property to access the node URL."""
        return self.DEFAULT_NODE_URL

    @property
    def symbol(self) -> str:
        """Property to access the blockchain symbol."""
        return self.DEFAULT_SYMBOL

    @property
    def explorer_url(self) -> str:
        """Property to access the explorer URL."""
        return self.DEFAULT_EXPLORER_URL

    @property
    def node_name(self) -> str:
        """Property to access the blockchain node name."""
        return self.DEFAULT_NODE_NAME

API = Provider()

