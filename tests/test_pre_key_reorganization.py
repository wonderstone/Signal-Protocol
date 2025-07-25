"""
测试重构后的预密钥模块功能
"""
import pytest
from signal_protocol.keys.identity_key import generate_identity_key_pair
from signal_protocol.keys.pre_keys import (
    # Base pre-key
    PreKey,
    PreKeyPair,
    generate_pre_key_pair,
    serialize_pre_key_pair,
    deserialize_pre_key_pair,
    
    # Signed pre-key
    SignedPreKey,
    SignedPreKeyPair,
    generate_signed_pre_key_pair,
    sign_signed_pre_key,
    verify_signed_pre_key_signature,
    
    # One-time pre-key
    OneTimePreKey,
    OneTimePreKeyPair,
    generate_one_time_pre_key_pair,
    generate_one_time_pre_keys,
    
    # Pre-key bundle
    PreKeyBundle,
    create_pre_key_bundle,
    
    # Helper
    create_complete_pre_key_set
)


class TestPreKeyReorganization:
    """测试预密钥重构功能"""
    
    def setup_method(self):
        """每个测试前的设置"""
        self.identity_key_pair = generate_identity_key_pair()
    
    def test_base_pre_key_generation(self):
        """测试基础预密钥生成"""
        pre_key_pair = generate_pre_key_pair(100)
        
        assert pre_key_pair.key_id == 100
        assert len(pre_key_pair.public_key_bytes) == 32
        assert len(pre_key_pair.private_key_bytes) == 32
        
        # 测试序列化
        serialized = serialize_pre_key_pair(pre_key_pair)
        assert 'key_id' in serialized
        assert 'public_key' in serialized
        assert 'private_key' in serialized
        
        # 测试反序列化
        deserialized = deserialize_pre_key_pair(serialized)
        assert deserialized.key_id == pre_key_pair.key_id
        assert deserialized.public_key_bytes == pre_key_pair.public_key_bytes
    
    def test_signed_pre_key_generation(self):
        """测试签名预密钥生成"""
        signed_pre_key_pair = generate_signed_pre_key_pair(self.identity_key_pair, 200)
        
        assert signed_pre_key_pair.key_id == 200
        assert hasattr(signed_pre_key_pair, 'timestamp')
        assert len(signed_pre_key_pair.public_key_bytes) == 32
        
        # 测试签名
        signature = sign_signed_pre_key(self.identity_key_pair, signed_pre_key_pair)
        assert len(signature) == 64
        
        # 测试签名验证
        is_valid = verify_signed_pre_key_signature(
            self.identity_key_pair,
            signed_pre_key_pair.public_key_bytes,
            signature
        )
        assert is_valid
    
    def test_one_time_pre_key_generation(self):
        """测试一次性预密钥生成"""
        # 生成单个一次性预密钥
        one_time_key = generate_one_time_pre_key_pair(300)
        assert one_time_key.key_id == 300
        
        # 生成多个一次性预密钥
        one_time_keys = generate_one_time_pre_keys(400, 5)
        assert len(one_time_keys) == 5
        assert one_time_keys[0].key_id == 400
        assert one_time_keys[4].key_id == 404
    
    def test_pre_key_bundle_creation(self):
        """测试预密钥包创建"""
        # 生成所有必需的密钥
        pre_key_pair = generate_pre_key_pair(500)
        signed_pre_key_pair = generate_signed_pre_key_pair(self.identity_key_pair, 600)
        signature = sign_signed_pre_key(self.identity_key_pair, signed_pre_key_pair)
        
        # 创建预密钥包
        bundle = create_pre_key_bundle(
            registration_id=12345,
            device_id=1,
            pre_key_pair=pre_key_pair,
            signed_pre_key_pair=signed_pre_key_pair,
            signed_pre_key_signature=signature,
            identity_key_pair=self.identity_key_pair
        )
        
        assert bundle.registration_id == 12345
        assert bundle.device_id == 1
        assert bundle.has_pre_key()
        assert bundle.pre_key_id == 500
        assert bundle.signed_pre_key_id == 600
        assert len(bundle.signed_pre_key_signature) == 64
    
    def test_complete_pre_key_set(self):
        """测试完整预密钥集合创建"""
        pre_key_set = create_complete_pre_key_set(
            identity_key_pair=self.identity_key_pair,
            pre_key_start_id=1000,
            signed_pre_key_id=2000,
            one_time_pre_key_start_id=3000,
            one_time_pre_key_count=10
        )
        
        assert 'pre_key_pair' in pre_key_set
        assert 'signed_pre_key_pair' in pre_key_set
        assert 'signed_pre_key_signature' in pre_key_set
        assert 'one_time_pre_keys' in pre_key_set
        
        assert pre_key_set['pre_key_pair'].key_id == 1000
        assert pre_key_set['signed_pre_key_pair'].key_id == 2000
        assert len(pre_key_set['one_time_pre_keys']) == 10
        assert pre_key_set['one_time_pre_keys'][0].key_id == 3000
    
    def test_public_key_classes(self):
        """测试公钥类"""
        # 测试基础公钥类
        pre_key_pair = generate_pre_key_pair(700)
        pre_key = PreKey(pre_key_pair.key_id, pre_key_pair.public_key_bytes)
        assert pre_key.key_id == 700
        assert pre_key.public_key_bytes == pre_key_pair.public_key_bytes
        
        # 测试签名公钥类
        signed_pre_key_pair = generate_signed_pre_key_pair(self.identity_key_pair, 800)
        signed_pre_key = SignedPreKey(
            signed_pre_key_pair.key_id,
            signed_pre_key_pair.public_key_bytes,
            signed_pre_key_pair.timestamp
        )
        assert signed_pre_key.key_id == 800
        assert hasattr(signed_pre_key, 'timestamp')
        
        # 测试一次性公钥类
        one_time_pair = generate_one_time_pre_key_pair(900)
        one_time_pre_key = OneTimePreKey(one_time_pair.key_id, one_time_pair.public_key_bytes)
        assert one_time_pre_key.key_id == 900


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v", "-s"])
