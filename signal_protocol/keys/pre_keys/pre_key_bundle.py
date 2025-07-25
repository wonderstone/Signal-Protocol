from typing import Optional
from ..identity_key import IdentityKey, IdentityKeyPair, generate_identity_key_pair
from .base_pre_key import PreKey, PreKeyPair, generate_pre_key_pair
from .signed_pre_key import generate_signed_pre_key_pair, sign_signed_pre_key


class PreKeyBundle:
    """Represents a pre-key bundle in the Signal Protocol"""
    
    def __init__(
        self,
        registration_id: int,
        device_id: int,
        pre_key: Optional[PreKey],
        pre_key_id: Optional[int],
        signed_pre_key: PreKey,
        signed_pre_key_id: int,
        signed_pre_key_signature: bytes,
        identity_key: IdentityKey
    ):
        """
        Initialize a pre-key bundle.
        
        Args:
            registration_id: The registration ID of the user
            device_id: The device ID
            pre_key: The pre-key (optional)
            pre_key_id: The pre-key ID (optional)
            signed_pre_key: The signed pre-key
            signed_pre_key_id: The signed pre-key ID
            signed_pre_key_signature: The signature of the signed pre-key
            identity_key: The identity key of the user
        """
        self.registration_id = registration_id
        self.device_id = device_id
        self.pre_key = pre_key
        self.pre_key_id = pre_key_id
        self.signed_pre_key = signed_pre_key
        self.signed_pre_key_id = signed_pre_key_id
        self.signed_pre_key_signature = signed_pre_key_signature
        self.identity_key = identity_key
    
    def has_pre_key(self) -> bool:
        """Check if this bundle includes a pre-key"""
        return self.pre_key is not None and self.pre_key_id is not None


def create_pre_key_bundle(
    registration_id: int,
    device_id: int,
    pre_key_pair: Optional[PreKeyPair],
    signed_pre_key_pair: PreKeyPair,
    signed_pre_key_signature: bytes,
    identity_key_pair: IdentityKeyPair
) -> PreKeyBundle:
    """
    Create a pre-key bundle from the provided keys.
    
    Args:
        registration_id: The registration ID of the user
        device_id: The device ID
        pre_key_pair: The pre-key pair (optional)
        signed_pre_key_pair: The signed pre-key pair
        signed_pre_key_signature: The signature of the signed pre-key
        identity_key_pair: The identity key pair of the user
        
    Returns:
        PreKeyBundle: The created pre-key bundle
    """
    # Convert pre-key pair to public-only PreKey if provided
    pre_key = PreKey(pre_key_pair.key_id, pre_key_pair.public_key_bytes) if pre_key_pair else None
    pre_key_id = pre_key_pair.key_id if pre_key_pair else None
    
    # Convert signed pre-key pair to public-only PreKey
    signed_pre_key = PreKey(signed_pre_key_pair.key_id, signed_pre_key_pair.public_key_bytes)
    
    # Convert identity key pair to public-only IdentityKey
    identity_key = IdentityKey(identity_key_pair.public_key_bytes)
    
    return PreKeyBundle(
        registration_id,
        device_id,
        pre_key,
        pre_key_id,
        signed_pre_key,
        signed_pre_key_pair.key_id,
        signed_pre_key_signature,
        identity_key
    )


if __name__ == "__main__":
    """
    Test the pre-key bundle functionality
    """
    print("📦 Pre-Key Bundle 测试")
    
    # Generate identity key pair
    identity_key_pair = generate_identity_key_pair()
    print("✅ 生成身份密钥对")
    
    # Generate pre-key pair
    pre_key_pair = generate_pre_key_pair(100)
    print(f"✅ 生成预密钥对 ID: {pre_key_pair.key_id}")
    
    # Generate signed pre-key pair
    signed_pre_key_pair = generate_signed_pre_key_pair(identity_key_pair, 200)
    print(f"✅ 生成签名预密钥对 ID: {signed_pre_key_pair.key_id}")
    
    # Sign the signed pre-key
    signature = sign_signed_pre_key(identity_key_pair, signed_pre_key_pair)
    print("✅ 生成签名预密钥签名")
    
    # Create bundle with pre-key
    bundle_with_pre_key = create_pre_key_bundle(
        registration_id=12345,
        device_id=1,
        pre_key_pair=pre_key_pair,
        signed_pre_key_pair=signed_pre_key_pair,
        signed_pre_key_signature=signature,
        identity_key_pair=identity_key_pair
    )
    print(f"✅ 创建完整预密钥包 (包含预密钥)")
    print(f"   注册ID: {bundle_with_pre_key.registration_id}")
    print(f"   设备ID: {bundle_with_pre_key.device_id}")
    print(f"   预密钥ID: {bundle_with_pre_key.pre_key_id}")
    print(f"   签名预密钥ID: {bundle_with_pre_key.signed_pre_key_id}")
    print(f"   包含预密钥: {bundle_with_pre_key.has_pre_key()}")
    
    # Create bundle without pre-key
    bundle_without_pre_key = create_pre_key_bundle(
        registration_id=12345,
        device_id=1,
        pre_key_pair=None,
        signed_pre_key_pair=signed_pre_key_pair,
        signed_pre_key_signature=signature,
        identity_key_pair=identity_key_pair
    )
    print(f"✅ 创建最小预密钥包 (无预密钥)")
    print(f"   包含预密钥: {bundle_without_pre_key.has_pre_key()}")
    
    # Verify bundle contents
    assert bundle_with_pre_key.pre_key is not None
    assert bundle_with_pre_key.pre_key.key_id == 100
    assert bundle_without_pre_key.pre_key is None
    assert bundle_without_pre_key.pre_key_id is None
    print("✅ 预密钥包内容验证通过")
    
    print("🎉 所有测试通过！")
