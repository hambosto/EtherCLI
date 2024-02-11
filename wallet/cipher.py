from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from .exception import WalletError

class Cipher:
    """A class for custom AES encryption using GCM mode.

    Attributes:
        password (bytes): The password to derive the encryption key from.
    """

    def __init__(self, password: str) -> None:
        """Initializes the Cipher object with the given password.

        Args:
            password (str): The password to derive the encryption key from.
        """

        self.password = password.encode()

    def encrypt(self, plaintext: str) -> str:
        """Encrypts a given plaintext using AES-GCM and returns the ciphertext.

        Args:
            plaintext (str): The plaintext to encrypt.

        Returns:
            str: The base64-encoded ciphertext.
        """

        # generate a random salt for key derivation
        salt = get_random_bytes(16)

        # derive key from password and salt using scrypt
        private_key = self._scrypt_hash(self.password, salt)

        # generate a random nonce for encryption
        nonce = get_random_bytes(12)

        # initialize the cipher object in GCM mode with the key and nonce
        cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

        # pad the plaintext to a multiple of the block size (16 bytes for AES)
        padded_plaintext = pad(plaintext.encode(), AES.block_size)

        # encrypt the padded plaintext
        ciphertext = cipher.encrypt(padded_plaintext)

        # retrieve the authentication tag
        tag = cipher.digest()

        # concatenate the salt, nonce, ciphertext, and tag
        ciphertext_value = salt + nonce + ciphertext + tag

        # encode ciphertext value to base64 for easier storage and transmission
        encoded_ciphertext = b64encode(ciphertext_value)

        # return and decode ciphertext bytes to string
        return encoded_ciphertext.decode()

    def decrypt(self, ciphertext: str) -> str:
        """Decrypts a given ciphertext using AES-GCM and returns the plaintext.

        Args:
            ciphertext (str): The base64-encoded ciphertext to decrypt.

        Returns:
            str: The decrypted plaintext.

        Raises:
            ValueError: If the MAC verification fails or decryption error occurs.
        """

        # decode the base64-encoded ciphertext
        ciphertext_bytes = b64decode(ciphertext)

        # split the ciphertext into its components
        salt = ciphertext_bytes[:16]
        nonce = ciphertext_bytes[16:28]
        ciphertext = ciphertext_bytes[28:-16]
        tag = ciphertext_bytes[-16:]

        # derive key from password and salt using scrypt
        private_key = self._scrypt_hash(self.password, salt)

        # initialize the cipher object in GCM mode with the key and nonce
        cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

        try:
            # decrypt the ciphertext
            padded_plaintext = cipher.decrypt(ciphertext)
        except ValueError:
            raise WalletError("ValueError", "Decryption error: Unable to decrypt the ciphertext.")

        try:
            # verify the authenticity of the ciphertext
            cipher.verify(tag)
        except ValueError:
            raise WalletError("ValueError", "MAC verification failed: The ciphertext has been tampered with.")

        # unpad the decrypted plaintext value
        plaintext = unpad(padded_plaintext, AES.block_size)

        # return decoded plaintext
        return plaintext.decode()

    def _scrypt_hash(self, password: bytes, salt: bytes, key_length: int = 32, N: int = 2**18, r: int = 8, p: int = 1) -> bytes:
        """Derives a key from a password and a salt using scrypt.

        Args:
            password (bytes): The password to hash.
            salt (bytes): The salt to use for hashing.
            key_length (int, optional): The length of the derived key in bytes. Defaults to 32.
            N (int, optional): The CPU/memory cost parameter. Defaults to 2**18.
            r (int, optional): The block size parameter. Defaults to 8.
            p (int, optional): The parallelization parameter. Defaults to 1.

        Returns:
            bytes: The derived key.
        """
        return scrypt(password, salt, key_length, N=N, r=r, p=p)

