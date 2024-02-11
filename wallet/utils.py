import os
import shutil
import json
from .exception import WalletError

def is_file(path: str) -> bool:
    """
    Returns True if the path is a file.

    Args:
        path (str): The path to check.

    Returns:
        bool: True if the path is a file.
    """
    return os.path.isfile(path)


def is_directory(path: str) -> bool:
    """
    Returns True if the path is a directory.

    Args:
        path (str): The path to check.

    Returns:
        bool: True if the path is a directory.
    """
    return os.path.exists(path)


def create_directory(dirname: str) -> None:
    """
    Creates a new directory with the specified name.

    Args:
        dirname (str): The name of the directory to create.

    Raises:
        Exception: If the directory already exists.
    """
    if not is_directory(dirname):
        try:
            os.makedirs(dirname)
        except FileExistsError:
            raise WalletError("FileExistsError", f"Directory '{dirname}' already exists")
        except PermissionError:
            raise WalletError("PermissionError", f"Permission denied to create directory '{dirname}'.")

def remove_directory(dirname: str) -> None:
    """
    Removes an existing directory with the specified name.

    Args:
        dirname (str): The name of the directory to remove.

    Raises:
        Exception: If there was an error while removing the directory.
    """
    if is_directory(dirname):
        try:
            shutil.rmtree(dirname, ignore_errors=True)
        except OSError:
            raise WalletError("OSError", f"Failed to remove directory {dirname}.")

def get_json_abi() -> dict:
    """
    Returns the JSON ABI for an ERC20 token.

    Returns:
        dict: The JSON ABI for an ERC20 token.
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    abi_path = os.path.join(root_dir, "abi", "erc20.json")
    with open(abi_path) as abi:
        get_abi = json.load(abi)
    return get_abi

def append_url(base_url: str, **paths) -> str:
    """
    Appends one or more paths to a base URL and returns the result.

    Args:
        base_url (str): The base URL to append paths to.
        **paths (str): One or more paths to append to the base URL.

    Returns:
        str: The resulting URL.
    """
    return "/".join([base_url] + [str(path) for path in paths.values()])

def format_number(number):
    """
    Format a number as a string with thousands separators and two decimal places.

    Args:
        number (Union[float, str]): The number to be formatted, or 'N/A' if unavailable.

    Returns:
        str: The formatted number as a string, or 'N/A' if the input is 'N/A'.

    Example:
        >>> format_number(1234567.8901)
        '1.234.567,89'
        >>> format_number('N/A')
        'N/A'
    """
    if number == 'N/A':
        return 'N/A'
    formatted_number = "{:,.2f}".format(float(number))
    formatted_number = formatted_number.replace(",", " ").replace(".", ",").replace(" ", ".")
    return formatted_number

def clear_terminal() -> None:
     """
     Clears the terminal screen.
     """
     os.system("cls" if os.name == "nt" else "clear")
