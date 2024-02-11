class Transaction:
    """Abstraction over ethereum virtual machine transaction"""

    def __init__(self, account, web3) -> None:
        """
        Initializes a new instance of the Transaction class.

        Args:
            account (Account): The account to use for signing transactions.
            web3 (Web3): The Web3 instance to use for sending transactions.
        """
        self.account = account
        self.web3 = web3

    def build_transaction(
        self, receiver, sender, value, gas_limit, gas_price, nonce, chain_id, data=None
    ) -> dict:
        """
        Builds a new transaction dictionary.

        Args:
            receiver (str): The address of the receiver.
            sender (str): The address of the sender.
            value (int): The value to send in wei.
            gas_limit (int): The gas limit for the transaction.
            gas_price (int): The gas price for the transaction.
            nonce (int): The nonce for the transaction.
            chain_id (int): The chain ID for the transaction.
            data (str): Optional data for the transaction.

        Returns:
            dict: A new transaction dictionary.
        """
        if data is None:  # tx dict for sending eth
            tx_dict = {
                # note that the address must be in checksum format
                "to": receiver,
                "from": sender,
                "value": value,
                "gas": gas_limit,
                "gasPrice": gas_price,
                "nonce": nonce,
                "chainId": chain_id,
            }
        else:  # tx dict for sending erc20 token
            tx_dict = {
                # note that the address must be in checksum format
                "to": receiver,
                "from": sender,
                "value": value,
                "gas": gas_limit,
                "gasPrice": gas_price,
                "nonce": nonce,
                "chainId": chain_id,
                "data": data,
            }

        return tx_dict

    def sign_transaction(self, transaction_dict):
        """
        Signs a transaction dictionary with the account's private key.

        Args:
            transaction_dict (dict): The transaction dictionary to sign.

        Returns:
            SignedTransaction: A signed transaction object.
        """
        return self.web3.eth.account.sign_transaction(transaction_dict, self.account.key)

    def send_transaction(self, raw_tx):
        """
        Sends a signed transaction to the network.

        Args:
            raw_tx (SignedTransaction): The signed transaction to send.

        Returns:
            HexBytes: The transaction hash of the sent transaction.
        """
        return self.web3.eth.send_raw_transaction(raw_tx.rawTransaction)
        
