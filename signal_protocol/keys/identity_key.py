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


if __name__ == '__main__':
    # Test identity key pair generation
    print("🔑 Testing identity key pair generation...")

    # Generate a new identity key pair
    identity_key_pair = generate_identity_key_pair()
    print(f"✅ Generated identity key pair")
    print(f"   Public key: {identity_key_pair.public_key_bytes.hex()}")
    print(f"   Private key: {identity_key_pair.private_key_bytes.hex()}")
    print(
        f"   Ed25519 verify key: {identity_key_pair.ed25519_verify_key_bytes.hex()}")

    # Test key properties
    print("\n🔍 Testing key properties...")
    assert len(
        identity_key_pair.public_key_bytes) == 32, "Public key should be 32 bytes"
    assert len(
        identity_key_pair.private_key_bytes) == 32, "Private key should be 32 bytes"
    assert len(
        identity_key_pair.ed25519_verify_key_bytes) == 32, "Ed25519 verify key should be 32 bytes"
    print("✅ All key lengths are correct")

    # Test XEdDSA signing and verification
    print("\n📝 Testing XEdDSA signing and verification...")

    test_message = b"Hello, Signal Protocol!"

    # Sign the message
    signature = xeddsa_sign(identity_key_pair, test_message)
    print(f"✅ Signed message with XEdDSA")
    print(f"   Message: {test_message.decode()}")
    print(f"   Signature: {signature.hex()}")

    # Verify the signature
    is_valid = xeddsa_verify(
        identity_key_pair.ed25519_verify_key_bytes, test_message, signature)
    assert is_valid, "Signature should be valid"
    print("✅ Signature verification passed")

    # Test with invalid signature
    invalid_signature = b'\x00' * 64  # Invalid signature
    is_invalid = xeddsa_verify(
        identity_key_pair.ed25519_verify_key_bytes, test_message, invalid_signature)
    assert not is_invalid, "Invalid signature should fail verification"
    print("✅ Invalid signature correctly rejected")

    # Test with tampered message
    tampered_message = b"Hello, Tampered Protocol!"
    is_tampered = xeddsa_verify(
        identity_key_pair.ed25519_verify_key_bytes, tampered_message, signature)
    assert not is_tampered, "Signature should fail for tampered message"
    print("✅ Tampered message correctly rejected")

    # Test serialization and deserialization
    print("\n💾 Testing serialization and deserialization...")

    # Serialize the key pair
    serialized = serialize_identity_key_pair(identity_key_pair)
    print(f"✅ Serialized identity key pair")
    print(f"   Serialized data keys: {list(serialized.keys())}")

    # Deserialize the key pair
    deserialized_key_pair = deserialize_identity_key_pair(serialized)
    print("✅ Deserialized identity key pair")

    # Verify the deserialized key pair matches the original
    assert identity_key_pair.public_key_bytes == deserialized_key_pair.public_key_bytes
    assert identity_key_pair.private_key_bytes == deserialized_key_pair.private_key_bytes
    assert identity_key_pair.ed25519_verify_key_bytes == deserialized_key_pair.ed25519_verify_key_bytes
    print("✅ Deserialized key pair matches original")

    # Test signing with deserialized key pair
    deserialized_signature = xeddsa_sign(deserialized_key_pair, test_message)
    is_deserialized_valid = xeddsa_verify(
        deserialized_key_pair.ed25519_verify_key_bytes, test_message, deserialized_signature)
    assert is_deserialized_valid, "Deserialized key pair should work for signing"
    print("✅ Deserialized key pair signing works correctly")

    # Test backward compatibility (without ed25519_verify_key in serialized data)
    print("\n🔄 Testing backward compatibility...")

    # Create serialized data without ed25519_verify_key
    backward_compat_data = {
        'public_key': identity_key_pair.public_key_bytes.hex(),
        'private_key': identity_key_pair.private_key_bytes.hex()
        # Intentionally omit 'ed25519_verify_key'
    }

    # Deserialize should work and derive the ed25519_verify_key
    backward_compat_key_pair = deserialize_identity_key_pair(
        backward_compat_data)

    # The derived ed25519_verify_key should match the original
    assert backward_compat_key_pair.ed25519_verify_key_bytes == identity_key_pair.ed25519_verify_key_bytes
    print("✅ Backward compatibility works - ed25519_verify_key correctly derived")

    # Test IdentityKey (public-only) class
    print("\n🔓 Testing IdentityKey (public-only) class...")

    identity_key = IdentityKey(identity_key_pair.public_key_bytes)
    assert identity_key.public_key_bytes == identity_key_pair.public_key_bytes
    print("✅ IdentityKey class works correctly")

    # Test Ed25519 key properties
    print("\n🔐 Testing Ed25519 key properties...")

    # Test signing key property
    signing_key = identity_key_pair.ed25519_signing_key
    assert isinstance(signing_key, nacl.signing.SigningKey)
    print("✅ Ed25519 signing key property works")

    # Test verify key property
    verify_key = identity_key_pair.ed25519_verify_key
    assert isinstance(verify_key, nacl.signing.VerifyKey)
    print("✅ Ed25519 verify key property works")

    # Test cross-compatibility between properties and direct signing
    property_signature = signing_key.sign(test_message).signature
    property_verification = xeddsa_verify(
        identity_key_pair.ed25519_verify_key_bytes, test_message, property_signature)
    assert property_verification, "Property-based signing should be compatible with xeddsa_verify"
    print("✅ Property-based signing compatible with XEdDSA verification")

    print("\n🎉 All identity key tests passed!")
    print("=" * 60)
    print("Identity Key Features Tested:")
    print("  ✓ Key pair generation (Curve25519 + Ed25519)")
    print("  ✓ XEdDSA signing and verification")
    print("  ✓ Signature validation and rejection")
    print("  ✓ Serialization and deserialization")
    print("  ✓ Backward compatibility")
    print("  ✓ Public-only IdentityKey class")
    print("  ✓ Ed25519 key properties")
    print("  ✓ Cross-compatibility verification")
    print("=" * 60)
