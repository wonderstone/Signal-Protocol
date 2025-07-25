from typing import List
from .base_pre_key import PreKeyPair, PreKey, serialize_pre_key_pair, deserialize_pre_key_pair
from ..base_key import generate_key_pair


class OneTimePreKeyPair(PreKeyPair):
    """Represents a one-time pre-key pair in the Signal Protocol"""
    
    def __init__(self, key_id: int, public_key: bytes, private_key: bytes):
        """
        Initialize a one-time pre-key pair.
        
        Args:
            key_id: Unique identifier for this one-time pre-key
            public_key: 32-byte public key
            private_key: 32-byte private key
        """
        super().__init__(key_id, public_key, private_key)


class OneTimePreKey(PreKey):
    """Represents a one-time pre-key (public only) in the Signal Protocol"""
    
    def __init__(self, key_id: int, public_key: bytes):
        """
        Initialize a one-time pre-key.
        
        Args:
            key_id: Unique identifier for this one-time pre-key
            public_key: 32-byte public key
        """
        super().__init__(key_id, public_key)


def generate_one_time_pre_key_pair(key_id: int) -> OneTimePreKeyPair:
    """
    Generate a new one-time pre-key pair for use in the Signal Protocol.
    
    Args:
        key_id: Unique identifier for this one-time pre-key
        
    Returns:
        OneTimePreKeyPair: A new one-time pre-key pair
    """
    public_key, private_key = generate_key_pair()
    return OneTimePreKeyPair(key_id, public_key, private_key)


def generate_one_time_pre_keys(start_id: int, count: int) -> List[OneTimePreKeyPair]:
    """
    Generate multiple one-time pre-key pairs.
    
    Args:
        start_id: Starting key ID
        count: Number of one-time pre-key pairs to generate
        
    Returns:
        List[OneTimePreKeyPair]: List of generated one-time pre-key pairs
    """
    one_time_pre_keys = []
    for i in range(count):
        one_time_pre_key = generate_one_time_pre_key_pair(start_id + i)
        one_time_pre_keys.append(one_time_pre_key)
    
    return one_time_pre_keys


# Re-export serialization functions from base_pre_key module
serialize_one_time_pre_key_pair = serialize_pre_key_pair
deserialize_one_time_pre_key_pair = deserialize_pre_key_pair


if __name__ == "__main__":
    """
    Test the one-time pre-key functionality
    """
    print("🔑 One-Time Pre-Key 测试")
    
    # Generate single one-time pre-key
    single_key = generate_one_time_pre_key_pair(100)
    print(f"✅ 生成单个一次性预密钥 ID: {single_key.key_id}")
    print(f"   公钥: {single_key.public_key_bytes.hex()[:32]}...")
    
    # Generate multiple one-time pre-keys
    multiple_keys = generate_one_time_pre_keys(200, 5)
    print(f"✅ 生成 {len(multiple_keys)} 个一次性预密钥")
    for key in multiple_keys:
        print(f"   ID {key.key_id}: {key.public_key_bytes.hex()[:16]}...")
    
    # Test serialization
    serialized = serialize_one_time_pre_key_pair(single_key)
    print(f"✅ 序列化成功: {len(serialized)} 字段")
    
    deserialized = deserialize_one_time_pre_key_pair(serialized)
    print(f"✅ 反序列化成功: ID {deserialized.key_id}")
    
    # Create public-only version
    public_key = OneTimePreKey(single_key.key_id, single_key.public_key_bytes)
    print(f"✅ 创建公钥版本: ID {public_key.key_id}")
    
    # Test key ID continuity
    assert multiple_keys[0].key_id == 200
    assert multiple_keys[4].key_id == 204
    print("✅ 密钥ID连续性验证通过")
    
    print("🎉 所有测试通过！")
