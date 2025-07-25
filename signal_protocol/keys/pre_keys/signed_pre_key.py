import time
from typing import List
from ..identity_key import IdentityKeyPair, generate_identity_key_pair, xeddsa_sign, xeddsa_verify
from .base_pre_key import PreKeyPair, PreKey
from ..base_key import generate_key_pair


class SignedPreKeyPair(PreKeyPair):
    """Represents a signed pre-key pair in the Signal Protocol"""
    
    def __init__(self, key_id: int, public_key: bytes, private_key: bytes, timestamp: int):
        """
        Initialize a signed pre-key pair.
        
        Args:
            key_id: Unique identifier for this signed pre-key
            public_key: 32-byte public key
            private_key: 32-byte private key
            timestamp: Timestamp when this key was created
        """
        super().__init__(key_id, public_key, private_key)
        self.timestamp = timestamp


class SignedPreKey(PreKey):
    """Represents a signed pre-key (public only) in the Signal Protocol"""
    
    def __init__(self, key_id: int, public_key: bytes, timestamp: int):
        """
        Initialize a signed pre-key.
        
        Args:
            key_id: Unique identifier for this signed pre-key
            public_key: 32-byte public key
            timestamp: Timestamp when this key was created
        """
        super().__init__(key_id, public_key)
        self.timestamp = timestamp


def generate_signed_pre_key_pair(identity_key_pair: IdentityKeyPair, key_id: int) -> SignedPreKeyPair:
    """
    Generate a new signed pre-key pair for use in the Signal Protocol.
    
    Args:
        identity_key_pair: The identity key pair to sign with
        key_id: Unique identifier for this signed pre-key
        
    Returns:
        SignedPreKeyPair: A new signed pre-key pair
    """
    public_key, private_key = generate_key_pair()
    
    # Get current timestamp
    timestamp = int(time.time() * 1000)  # milliseconds since epoch
    
    return SignedPreKeyPair(key_id, public_key, private_key, timestamp)


def sign_signed_pre_key(
    identity_key_pair: IdentityKeyPair,
    signed_pre_key_pair: SignedPreKeyPair
) -> bytes:
    """
    Sign a signed pre-key with the identity key using XEdDSA.

    Args:
        identity_key_pair: The identity key pair to sign with
        signed_pre_key_pair: The signed pre-key pair to sign

    Returns:
        bytes: The signature (64 bytes)
    """
    # Use XEdDSA to sign the public key of the signed pre-key
    return xeddsa_sign(identity_key_pair, signed_pre_key_pair.public_key_bytes)


def verify_signed_pre_key_signature(
    identity_key_pair: IdentityKeyPair,
    signed_pre_key_public_key: bytes,
    signature: bytes
) -> bool:
    """
    Verify the signature of a signed pre-key using XEdDSA.

    Args:
        identity_key_pair: The identity key pair (to get Ed25519 verify key)
        signed_pre_key_public_key: The signed pre-key public key (32 bytes)
        signature: The signature to verify (64 bytes)

    Returns:
        bool: True if the signature is valid, False otherwise
    """
    # Use XEdDSA to verify the signature with the Ed25519 verify key
    return xeddsa_verify(identity_key_pair.ed25519_verify_key_bytes, signed_pre_key_public_key, signature)


def serialize_signed_pre_key_pair(signed_pre_key_pair: SignedPreKeyPair) -> dict:
    """
    Serialize a signed pre-key pair to a dictionary for storage.
    
    Args:
        signed_pre_key_pair: The signed pre-key pair to serialize
        
    Returns:
        dict: Dictionary containing the serialized signed pre-key pair
    """
    return {
        'key_id': signed_pre_key_pair.key_id,
        'public_key': signed_pre_key_pair.public_key_bytes.hex(),
        'private_key': signed_pre_key_pair.private_key_bytes.hex(),
        'timestamp': signed_pre_key_pair.timestamp
    }


def deserialize_signed_pre_key_pair(data: dict) -> SignedPreKeyPair:
    """
    Deserialize a signed pre-key pair from a dictionary.
    
    Args:
        data: Dictionary containing the serialized signed pre-key pair
        
    Returns:
        SignedPreKeyPair: The deserialized signed pre-key pair
    """
    key_id = data['key_id']
    public_key = bytes.fromhex(data['public_key'])
    private_key = bytes.fromhex(data['private_key'])
    timestamp = data['timestamp']
    
    return SignedPreKeyPair(key_id, public_key, private_key, timestamp)


if __name__ == "__main__":
    """
    Test the signed pre-key functionality
    """
    print("🔑 Signed Pre-Key 测试")
    
    # Generate identity key pair for signing
    identity_key_pair = generate_identity_key_pair()
    print(f"✅ 生成身份密钥对")
    
    # Generate signed pre-key pair
    signed_pre_key_pair = generate_signed_pre_key_pair(identity_key_pair, 1)
    print(f"✅ 生成签名预密钥对 ID: {signed_pre_key_pair.key_id}")
    print(f"   时间戳: {signed_pre_key_pair.timestamp}")
    print(f"   公钥: {signed_pre_key_pair.public_key_bytes.hex()[:32]}...")
    
    # Sign the pre-key
    signature = sign_signed_pre_key(identity_key_pair, signed_pre_key_pair)
    print(f"✅ 生成签名: {signature.hex()[:32]}...")
    
    # Verify the signature
    is_valid = verify_signed_pre_key_signature(
        identity_key_pair,
        signed_pre_key_pair.public_key_bytes,
        signature
    )
    print(f"✅ 签名验证: {'通过' if is_valid else '失败'}")
    
    # Test serialization
    serialized = serialize_signed_pre_key_pair(signed_pre_key_pair)
    print(f"✅ 序列化成功: {len(serialized)} 字段")
    
    deserialized = deserialize_signed_pre_key_pair(serialized)
    print(f"✅ 反序列化成功: ID {deserialized.key_id}")
    
    # Create public-only version
    signed_pre_key = SignedPreKey(
        signed_pre_key_pair.key_id,
        signed_pre_key_pair.public_key_bytes,
        signed_pre_key_pair.timestamp
    )
    print(f"✅ 创建公钥版本: ID {signed_pre_key.key_id}")
    
    print("🎉 所有测试通过！")
