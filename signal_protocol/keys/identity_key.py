import nacl.signing
from .base_key import BaseKey, BaseKeyPair, generate_key_pair

class IdentityKeyPair(BaseKeyPair):
    """Represents an identity key pair in the Signal Protocol

    This uses Curve25519 keys for ECDH key exchange and stores the corresponding
    Ed25519 verify key for XEdDSA signature verification.
    """

    def __init__(self, public_key: bytes, private_key: bytes, ed25519_verify_key: bytes = None):
        """
        Initialize an identity key pair.

        Args:
            public_key: 32-byte Curve25519 public key
            private_key: 32-byte Curve25519 private key
            ed25519_verify_key: 32-byte Ed25519 verify key (optional, will be derived if not provided)
        """
        super().__init__(public_key, private_key)

        # Store or derive the Ed25519 verify key
        if ed25519_verify_key is not None:
            self._ed25519_verify_key_bytes = ed25519_verify_key
        else:
            # Derive Ed25519 verify key from the private key
            signing_key = nacl.signing.SigningKey(private_key)
            self._ed25519_verify_key_bytes = bytes(signing_key.verify_key)

    @property
    def ed25519_signing_key(self) -> nacl.signing.SigningKey:
        """Get the Ed25519 signing key derived from the Curve25519 private key"""
        return nacl.signing.SigningKey(self.private_key_bytes)

    @property
    def ed25519_verify_key(self) -> nacl.signing.VerifyKey:
        """Get the Ed25519 verify key"""
        return nacl.signing.VerifyKey(self._ed25519_verify_key_bytes)

    @property
    def ed25519_verify_key_bytes(self) -> bytes:
        """Get the Ed25519 verify key as bytes"""
        return self._ed25519_verify_key_bytes


class IdentityKey(BaseKey):
    """Represents an identity key (public only) in the Signal Protocol"""
    
    def __init__(self, public_key: bytes):
        """
        Initialize an identity key.
        
        Args:
            public_key: 32-byte public key
        """
        super().__init__(public_key)


def generate_identity_key_pair() -> IdentityKeyPair:
    """
    Generate a new identity key pair for use in the Signal Protocol.

    Returns:
        IdentityKeyPair: A new identity key pair
    """
    public_key, private_key = generate_key_pair()
    return IdentityKeyPair(public_key, private_key)


def xeddsa_sign(identity_key_pair: IdentityKeyPair, message: bytes) -> bytes:
    """
    Sign a message using XEdDSA (Ed25519-compatible signatures with Curve25519 keys).

    Args:
        identity_key_pair: The identity key pair to sign with
        message: The message to sign

    Returns:
        bytes: The signature (64 bytes)
    """
    # Use the Ed25519 signing key derived from the Curve25519 private key
    signing_key = identity_key_pair.ed25519_signing_key

    # Sign the message
    signed_message = signing_key.sign(message)

    # Return only the signature part (64 bytes)
    return signed_message.signature


def xeddsa_verify(ed25519_verify_key: bytes, message: bytes, signature: bytes) -> bool:
    """
    Verify an XEdDSA signature.

    Args:
        ed25519_verify_key: The Ed25519 verify key (32 bytes)
        message: The message that was signed
        signature: The signature to verify (64 bytes)

    Returns:
        bool: True if the signature is valid, False otherwise
    """
    try:
        # Create the verify key from the Ed25519 verify key bytes
        verify_key = nacl.signing.VerifyKey(ed25519_verify_key)

        # Verify the signature
        verify_key.verify(message, signature)
        return True
    except Exception:
        return False


def serialize_identity_key_pair(key_pair: IdentityKeyPair) -> dict:
    """
    Serialize an identity key pair to a dictionary for storage.

    Args:
        key_pair: The identity key pair to serialize

    Returns:
        dict: Dictionary containing the serialized key pair
    """
    return {
        'public_key': key_pair.public_key_bytes.hex(),
        'private_key': key_pair.private_key_bytes.hex(),
        'ed25519_verify_key': key_pair.ed25519_verify_key_bytes.hex()
    }


def deserialize_identity_key_pair(data: dict) -> IdentityKeyPair:
    """
    Deserialize an identity key pair from a dictionary.

    Args:
        data: Dictionary containing the serialized key pair

    Returns:
        IdentityKeyPair: The deserialized identity key pair
    """
    public_key = bytes.fromhex(data['public_key'])
    private_key = bytes.fromhex(data['private_key'])

    # Handle backward compatibility - if ed25519_verify_key is not present, derive it
    if 'ed25519_verify_key' in data:
        ed25519_verify_key = bytes.fromhex(data['ed25519_verify_key'])
    else:
        ed25519_verify_key = None

    return IdentityKeyPair(public_key, private_key, ed25519_verify_key)

