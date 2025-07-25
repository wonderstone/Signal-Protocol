from typing import List, Optional
from ..base_key import BaseKey, BaseKeyPair, generate_key_pair


class PreKeyPair(BaseKeyPair):
    """Represents a pre-key pair in the Signal Protocol"""
    
    def __init__(self, key_id: int, public_key: bytes, private_key: bytes):
        """
        Initialize a pre-key pair.
        
        Args:
            key_id: Unique identifier for this pre-key
            public_key: 32-byte public key
            private_key: 32-byte private key
        """
        super().__init__(public_key, private_key)
        self.key_id = key_id


class PreKey(BaseKey):
    """Represents a pre-key (public only) in the Signal Protocol"""
    
    def __init__(self, key_id: int, public_key: bytes):
        """
        Initialize a pre-key.
        
        Args:
            key_id: Unique identifier for this pre-key
            public_key: 32-byte public key
        """
        super().__init__(public_key)
        self.key_id = key_id


def generate_pre_key_pair(key_id: int) -> PreKeyPair:
    """
    Generate a new pre-key pair for use in the Signal Protocol.
    
    Args:
        key_id: Unique identifier for this pre-key
        
    Returns:
        PreKeyPair: A new pre-key pair
    """
    public_key, private_key = generate_key_pair()
    return PreKeyPair(key_id, public_key, private_key)


def generate_pre_keys(start_id: int, count: int) -> List[PreKeyPair]:
    """
    Generate multiple pre-key pairs.
    
    Args:
        start_id: Starting key ID
        count: Number of pre-key pairs to generate
        
    Returns:
        List[PreKeyPair]: List of generated pre-key pairs
    """
    pre_keys = []
    for i in range(count):
        pre_key = generate_pre_key_pair(start_id + i)
        pre_keys.append(pre_key)
    
    return pre_keys


def serialize_pre_key_pair(pre_key_pair: PreKeyPair) -> dict:
    """
    Serialize a pre-key pair to a dictionary for storage.
    
    Args:
        pre_key_pair: The pre-key pair to serialize
        
    Returns:
        dict: Dictionary containing the serialized pre-key pair
    """
    return {
        'key_id': pre_key_pair.key_id,
        'public_key': pre_key_pair.public_key_bytes.hex(),
        'private_key': pre_key_pair.private_key_bytes.hex()
    }


def deserialize_pre_key_pair(data: dict) -> PreKeyPair:
    """
    Deserialize a pre-key pair from a dictionary.
    
    Args:
        data: Dictionary containing the serialized pre-key pair
        
    Returns:
        PreKeyPair: The deserialized pre-key pair
    """
    key_id = data['key_id']
    public_key = bytes.fromhex(data['public_key'])
    private_key = bytes.fromhex(data['private_key'])
    
    return PreKeyPair(key_id, public_key, private_key)


if __name__ == '__main__':
    # Test generating pre-key pairs
    print("Testing pre-key generation...")
    
    # Generate a single pre-key pair
    pre_key_pair = generate_pre_key_pair(1)
    print(f"Generated pre-key pair with ID: {pre_key_pair.key_id}")
    print(f"Public key: {pre_key_pair.public_key_bytes.hex()}")
    print(f"Private key: {pre_key_pair.private_key_bytes.hex()}")
    
    # Test serialization
    print("\nTesting serialization...")
    serialized = serialize_pre_key_pair(pre_key_pair)
    print(f"Serialized: {serialized}")
    
    # Test deserialization
    print("\nTesting deserialization...")
    deserialized = deserialize_pre_key_pair(serialized)
    print(f"Deserialized key ID: {deserialized.key_id}")
    print(f"Deserialized public key: {deserialized.public_key_bytes.hex()}")
    
    # Verify they match
    assert pre_key_pair.key_id == deserialized.key_id
    assert pre_key_pair.public_key_bytes == deserialized.public_key_bytes
    assert pre_key_pair.private_key_bytes == deserialized.private_key_bytes
    
    # Generate multiple pre-keys
    print("\nTesting multiple pre-key generation...")
    pre_keys = generate_pre_keys(100, 5)
    print(f"Generated {len(pre_keys)} pre-keys with IDs: {[pk.key_id for pk in pre_keys]}")
    
    print("\nAll tests passed!")
