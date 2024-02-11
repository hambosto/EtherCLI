class WalletError(Exception):
    def __init__(self, err, msg) -> None:
        """
        Initializes a new instance of the WalletError class.

        Args:
            err (str): The error message.
            msg (str): The error description.
        """
        self.error = err
        self.message = msg
